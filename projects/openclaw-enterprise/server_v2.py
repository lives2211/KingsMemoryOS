"""
OpenClaw 多 Agent 派发服务器 V2
基于 Paperclip 架构优化
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from core.agent import BaseAgent, AgentConfig
from core.task import Task, TaskStatus, TaskPriority, TaskBudget
from core.heartbeat import HeartbeatScheduler, init_heartbeat_system
from true_dispatcher import dispatch_to_true_agent, TRUE_AGENTS

app = Flask(__name__)
CORS(app)

# 数据目录
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "tasks.db"

# 初始化数据库
def init_db():
    """初始化 SQLite 数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'backlog',
            priority TEXT DEFAULT 'normal',
            agent_id TEXT,
            agent_name TEXT,
            budget_total REAL DEFAULT 0,
            budget_spent REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            assigned_at TIMESTAMP,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            requester TEXT DEFAULT 'unknown',
            tags TEXT,
            result TEXT,
            deliverables TEXT,
            audit_log TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT,
            skills TEXT,
            model TEXT,
            status TEXT DEFAULT 'idle',
            current_task TEXT,
            total_cost REAL DEFAULT 0,
            tokens_used INTEGER DEFAULT 0,
            last_heartbeat TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event TEXT NOT NULL,
            task_id TEXT,
            actor TEXT,
            details TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"[DB] 数据库初始化完成: {DB_PATH}")

# Agent 配置 (9 Agents - 基于 agency-agents 优化)
AGENTS_CONFIG = {
    # === Engineering Division (工程部) ===
    "yitai": AgentConfig(
        id="yitai",
        name="yitai",
        role="技术官",
        skills=["编程", "代码", "脚本", "开发", "调试", "爬取", "修复", "实现", "功能开发"],
        model="claude-3-5-sonnet"
    ),
    "architect": AgentConfig(
        id="architect",
        name="architect",
        role="软件架构师",
        skills=["架构", "设计", "方案", "技术选型", "重构", "微服务", "ddd", "系统", "模块", 
                "接口设计", "数据库设计", "api设计", "架构图", "技术栈", "性能优化", "扩展性", "高并发", "分布式"],
        model="claude-3-5-sonnet"
    ),
    "devops": AgentConfig(
        id="devops",
        name="devops",
        role="DevOps工程师",
        skills=["部署", "ci/cd", "docker", "kubernetes", "k8s", "自动化", "pipeline", 
                "github actions", "jenkins", "监控", "日志", "nginx", "服务器", "运维",
                "ssl", "域名", "cdn", "负载均衡", "容器", "配置"],
        model="claude-3-5-sonnet"
    ),
    
    # === Design Division (设计部) ===
    "bingbing": AgentConfig(
        id="bingbing",
        name="bingbing",
        role="创意官",
        skills=["设计", "创意", "封面", "内容", "文案", "写作", "图像", "视频", "视觉", "品牌"],
        model="claude-3-5-sonnet"
    ),
    
    # === Data Division (数据部) ===
    "daping": AgentConfig(
        id="daping",
        name="daping",
        role="检测官",
        skills=["分析", "数据", "检测", "监控", "竞品", "报表", "可视化", "统计"],
        model="claude-3-5-sonnet"
    ),
    
    # === Quality Division (质量部) ===
    "spikey": AgentConfig(
        id="spikey",
        name="spikey",
        role="审计官",
        skills=["审计", "复盘", "质量", "审查", "检查", "代码审查", "代码质量"],
        model="claude-3-5-sonnet"
    ),
    "security": AgentConfig(
        id="security",
        name="security",
        role="安全工程师",
        skills=["安全", "审计", "漏洞", "渗透", "防护", "xss", "sql注入", "csrf", 
                "加密", "https", "代码审计", "安全扫描", "owasp", "鉴权", "认证", "授权", "token", "jwt", "oauth"],
        model="claude-3-5-sonnet"
    ),
    
    # === Growth Division (增长部) ===
    "xiaohongcai": AgentConfig(
        id="xiaohongcai",
        name="xiaohongcai",
        role="运营官",
        skills=["社媒", "运营", "发布", "小红书", "公众号", "内容运营"],
        model="claude-3-5-sonnet"
    ),
    
    # === Product Division (产品部) ===
    "pm": AgentConfig(
        id="pm",
        name="pm",
        role="产品经理",
        skills=["产品", "需求", "prd", "用户故事", "功能设计", "原型", "流程图", 
                "竞品分析", "用户调研", "优先级", "路线图", "mvp", "迭代", "版本规划",
                "商业模式", "用户体验", "交互设计", "文档"],
        model="claude-3-5-sonnet"
    )
}

# 内存中的 Agent 实例
agents: Dict[str, BaseAgent] = {}
scheduler: Optional[HeartbeatScheduler] = None

def init_agents():
    """初始化 Agent"""
    global agents, scheduler
    
    for agent_id, config in AGENTS_CONFIG.items():
        agents[agent_id] = BaseAgent(config)
    
    # 启动心跳调度器
    scheduler = HeartbeatScheduler(check_interval=60)
    for agent in agents.values():
        scheduler.register_agent(agent)
    scheduler.start()
    
    print(f"[Agents] {len(agents)} 个 Agent 已初始化")

def match_agent(description: str) -> str:
    """匹配最佳 Agent"""
    desc_lower = description.lower()
    scores = {}
    
    for agent_id, config in AGENTS_CONFIG.items():
        score = 0
        for skill in config.skills:
            if skill.lower() in desc_lower:
                score += 1
        scores[agent_id] = score
    
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "yitai"

def save_task(task: Task):
    """保存任务到数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO tasks (
            id, title, description, status, priority,
            agent_id, agent_name, budget_total, budget_spent,
            created_at, assigned_at, started_at, completed_at,
            requester, tags, result, deliverables, audit_log
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        task.id, task.title, task.description,
        task.status.value, task.priority.value,
        task.agent_id, task.agent_name,
        task.budget.total, task.budget.spent,
        task.created_at.isoformat(),
        task.assigned_at.isoformat() if task.assigned_at else None,
        task.started_at.isoformat() if task.started_at else None,
        task.completed_at.isoformat() if task.completed_at else None,
        task.requester,
        json.dumps(task.tags),
        json.dumps(task.result) if task.result else None,
        json.dumps(task.deliverables),
        json.dumps([{"timestamp": a.timestamp.isoformat(), "event": a.event, "actor": a.actor, "details": a.details} for a in task.audit_log])
    ))
    
    conn.commit()
    conn.close()

def load_task(task_id: str) -> Optional[Task]:
    """从数据库加载任务"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    # 转换为 Task 对象
    task = Task(
        id=row[0],
        title=row[1],
        description=row[2],
        status=TaskStatus(row[3]),
        priority=TaskPriority(row[4]),
        agent_id=row[5],
        agent_name=row[6],
        budget=TaskBudget(total=row[7], spent=row[8]),
        requester=row[13],
        tags=json.loads(row[14]) if row[14] else [],
        result=json.loads(row[15]) if row[15] else None,
        deliverables=json.loads(row[16]) if row[16] else []
    )
    
    return task

def load_all_tasks() -> List[Task]:
    """加载所有任务"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    tasks = []
    for row in rows:
        task = Task(
            id=row[0],
            title=row[1],
            description=row[2],
            status=TaskStatus(row[3]),
            priority=TaskPriority(row[4]),
            agent_id=row[5],
            agent_name=row[6],
            budget=TaskBudget(total=row[7], spent=row[8]),
            requester=row[13],
            tags=json.loads(row[14]) if row[14] else [],
            result=json.loads(row[15]) if row[15] else None,
            deliverables=json.loads(row[16]) if row[16] else []
        )
        tasks.append(task)
    
    return tasks

# API 路由
@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "version": "2.0",
        "agents_count": len(agents),
        "scheduler_running": scheduler.running if scheduler else False
    })

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """获取任务列表"""
    tasks = load_all_tasks()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """创建新任务"""
    data = request.json
    
    # 生成任务ID
    task_id = f"TASK-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{os.urandom(2).hex()}"
    
    # 自动匹配 Agent
    agent_id = match_agent(data.get('description', ''))
    agent_config = AGENTS_CONFIG[agent_id]
    
    # 创建任务
    task = Task(
        id=task_id,
        title=data.get('title', data.get('description', '未命名任务')[:50]),
        description=data.get('description', ''),
        priority=TaskPriority(data.get('priority', 'normal')),
        agent_id=agent_id,
        agent_name=agent_config.name,
        budget=TaskBudget(total=data.get('budget', 0)),
        requester=data.get('requester', 'unknown'),
        tags=data.get('tags', [])
    )
    
    # 指派任务
    task.assign(agent_id, agent_config.name)
    
    # 保存到数据库
    save_task(task)
    
    # 通知 Agent - 真正的独立 Agent
    if agent_id in TRUE_AGENTS:
        # 发送到真正的独立 Agent 子会话
        dispatch_to_true_agent(agent_id, task.to_dict())
    elif agent_id in agents:
        # 回退到模拟 Agent
        agents[agent_id].state.status = "busy"
        agents[agent_id].state.current_task = task_id
    
    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id: str):
    """获取单个任务"""
    task = load_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict())

@app.route('/api/tasks/<task_id>/start', methods=['POST'])
def start_task(task_id: str):
    """开始任务"""
    task = load_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    task.start()
    save_task(task)
    
    return jsonify(task.to_dict())

@app.route('/api/tasks/<task_id>/complete', methods=['POST'])
def complete_task(task_id: str):
    """完成任务"""
    task = load_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.json or {}
    task.complete(
        result=data.get('result', {}),
        deliverables=data.get('deliverables', [])
    )
    save_task(task)
    
    # 更新 Agent 状态
    if task.agent_id in agents:
        agents[task.agent_id].state.status = "idle"
        agents[task.agent_id].state.current_task = None
    
    return jsonify(task.to_dict())

@app.route('/api/agents', methods=['GET'])
def list_agents():
    """获取所有 Agent"""
    return jsonify({
        agent_id: {
            "config": {
                "id": config.id,
                "name": config.name,
                "role": config.role,
                "skills": config.skills,
                "model": config.model
            },
            "state": agents[agent_id].to_dict()["state"] if agent_id in agents else None
        }
        for agent_id, config in AGENTS_CONFIG.items()
    })

@app.route('/api/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id: str):
    """获取单个 Agent"""
    if agent_id not in AGENTS_CONFIG:
        return jsonify({"error": "Agent not found"}), 404
    
    config = AGENTS_CONFIG[agent_id]
    agent = agents.get(agent_id)
    
    return jsonify({
        "config": {
            "id": config.id,
            "name": config.name,
            "role": config.role,
            "skills": config.skills,
            "model": config.model
        },
        "state": agent.to_dict()["state"] if agent else None
    })

@app.route('/api/match', methods=['POST'])
def match_agent_api():
    """匹配最佳 Agent"""
    description = request.json.get('description', '')
    agent_id = match_agent(description)
    config = AGENTS_CONFIG[agent_id]
    
    return jsonify({
        "agent_id": agent_id,
        "agent": {
            "id": config.id,
            "name": config.name,
            "role": config.role,
            "skills": config.skills
        },
        "confidence": "high" if any(s.lower() in description.lower() for s in config.skills) else "low"
    })

@app.route('/api/scheduler/status', methods=['GET'])
def scheduler_status():
    """获取调度器状态"""
    if not scheduler:
        return jsonify({"error": "Scheduler not initialized"}), 500
    
    return jsonify(scheduler.get_status())

# Dashboard
@app.route('/dashboard.html')
def dashboard():
    """Dashboard"""
    return send_from_directory('.', 'dashboard_v2.html')

@app.route('/')
def index():
    """首页"""
    return jsonify({
        "name": "OpenClaw Multi-Agent System",
        "version": "2.0",
        "paperclip_inspired": True,
        "endpoints": {
            "tasks": "/api/tasks",
            "agents": "/api/agents",
            "dashboard": "/dashboard.html"
        }
    })

if __name__ == '__main__':
    print("🚀 OpenClaw 多 Agent 系统 V2 启动中...")
    print("📐 架构: Paperclip-inspired")
    
    # 初始化
    init_db()
    init_agents()
    
    print("📡 API: http://localhost:3100")
    print("🌐 Dashboard: http://localhost:3100/dashboard.html")
    
    app.run(host='0.0.0.0', port=3100, debug=False)
