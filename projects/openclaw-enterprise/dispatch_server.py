#!/usr/bin/env python3
"""
OpenClaw 任务派发服务器
轻量级替代方案，直接集成到 OpenClaw
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import subprocess
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 内存存储（可用 SQLite 替代）
tasks = []
task_counter = 1

# Agent 配置
AGENTS = {
    "yitai": {"name": "yitai", "role": "技术官", "skills": ["编程", "代码", "脚本", "开发", "调试", "爬取", "修复"]},
    "bingbing": {"name": "bingbing", "role": "创意官", "skills": ["设计", "创意", "封面", "内容", "文案", "写作", "图像", "视频"]},
    "daping": {"name": "daping", "role": "检测官", "skills": ["分析", "数据", "检测", "监控", "竞品"]},
    "spikey": {"name": "spikey", "role": "审计官", "skills": ["审计", "复盘", "质量", "审查", "检查"]},
    "xiaohongcai": {"name": "xiaohongcai", "role": "运营官", "skills": ["社媒", "运营", "发布", "小红书", "公众号"]}
}

def match_agent(description: str) -> str:
    """匹配最佳 Agent"""
    desc_lower = description.lower()
    scores = {}
    
    for agent_id, config in AGENTS.items():
        score = 0
        for skill in config["skills"]:
            if skill.lower() in desc_lower:
                score += 1
        scores[agent_id] = score
    
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "yitai"

def send_to_agent(agent_id: str, task: dict):
    """发送任务到 OpenClaw Agent"""
    agent = AGENTS.get(agent_id)
    if not agent:
        return False
    
    message = f"""【新任务】{task['title']}
【描述】{task['description']}
【任务ID】{task['id']}
【预算】${task.get('budget', 0)}
【优先级】{task.get('priority', 'normal')}

请回复"收到"确认，并开始执行。"""
    
    try:
        subprocess.run(
            ["openclaw", "sessions", "send", 
             "--label", agent_id,
             "--message", message],
            capture_output=True,
            timeout=10
        )
        return True
    except:
        return False

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    global task_counter
    
    data = request.json
    description = data.get('description', '')
    
    # 自动匹配 Agent
    agent_id = match_agent(description)
    
    task = {
        "id": f"TASK-{task_counter:04d}",
        "title": data.get('title', description[:50]),
        "description": description,
        "agent_id": agent_id,
        "agent_name": AGENTS[agent_id]['name'],
        "agent_role": AGENTS[agent_id]['role'],
        "budget": data.get('budget', 0),
        "priority": data.get('priority', 'normal'),
        "status": "backlog",
        "created_at": datetime.now().isoformat(),
        "requester": data.get('requester', 'unknown')
    }
    
    tasks.append(task)
    task_counter += 1
    
    # 通知 Agent
    send_to_agent(agent_id, task)
    
    return jsonify(task), 201

@app.route('/api/agents', methods=['GET'])
def list_agents():
    return jsonify(AGENTS)

@app.route('/api/match', methods=['POST'])
def match_agent_api():
    description = request.json.get('description', '')
    agent_id = match_agent(description)
    return jsonify({
        "agent_id": agent_id,
        "agent": AGENTS[agent_id]
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "tasks_count": len(tasks)})

if __name__ == '__main__':
    print("🚀 OpenClaw 任务派发服务器启动中...")
    print("📡 API: http://localhost:3100")
    app.run(host='0.0.0.0', port=3100, debug=False)
