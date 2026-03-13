#!/usr/bin/env python3
"""
Mock Paperclip Server
模拟 Paperclip API，用于演示 OpenClaw 集成
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Mock Paperclip Server", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据存储
DATA_DIR = Path("/home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise/data/paperclip")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 模型定义
class Agent(BaseModel):
    id: str
    name: str
    title: str
    department: str
    role: str
    capabilities: List[str]
    budget_monthly: float
    budget_used: float = 0.0
    status: str = "active"
    reports_to: Optional[str] = None
    created_at: Optional[str] = None

class Task(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    assignee: str
    status: str = "backlog"
    priority: str = "P2"
    budget: float = 0.0
    cost: float = 0.0
    parent_id: Optional[str] = None
    sub_tasks: List[str] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

# 内存存储
agents_db: Dict[str, Agent] = {}
tasks_db: Dict[str, Task] = {}

# 初始化数据
def init_data():
    """初始化示例数据"""
    # 创建 Agent
    agents_data = [
        {
            "id": "main",
            "name": "Monica",
            "title": "龙虾总管",
            "department": "管理层",
            "role": "CEO",
            "capabilities": ["统筹", "决策", "协调", "审核"],
            "budget_monthly": 100.0,
            "reports_to": None
        },
        {
            "id": "yitai",
            "name": "yitai",
            "title": "技术官",
            "department": "技术部",
            "role": "CTO",
            "capabilities": ["编程", "开发", "架构", "脚本"],
            "budget_monthly": 80.0,
            "reports_to": "main"
        },
        {
            "id": "bingbing",
            "name": "bingbing",
            "title": "创意官",
            "department": "创作部",
            "role": "CCO",
            "capabilities": ["内容", "设计", "文案", "创意"],
            "budget_monthly": 70.0,
            "reports_to": "main"
        },
        {
            "id": "daping",
            "name": "daping",
            "title": "检测官",
            "department": "质检部",
            "role": "QA Lead",
            "capabilities": ["检测", "分析", "测试", "数据"],
            "budget_monthly": 60.0,
            "reports_to": "main"
        },
        {
            "id": "spikey",
            "name": "spikey",
            "title": "审计官",
            "department": "审计部",
            "role": "Auditor",
            "capabilities": ["审计", "复盘", "质量", "文档"],
            "budget_monthly": 60.0,
            "reports_to": "main"
        },
        {
            "id": "xiaohongcai",
            "name": "xiaohongcai",
            "title": "运营官",
            "department": "运营部",
            "role": "COO",
            "capabilities": ["社媒", "运营", "小红书", "公众号"],
            "budget_monthly": 70.0,
            "reports_to": "main"
        }
    ]
    
    for agent_data in agents_data:
        agent_data["created_at"] = datetime.now().isoformat()
        agent = Agent(**agent_data)
        agents_db[agent.id] = agent
    
    print(f"✅ 已初始化 {len(agents_db)} 个 Agent")

# API 路由

@app.get("/")
def root():
    return {"message": "Mock Paperclip Server", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok", "agents": len(agents_db), "tasks": len(tasks_db)}

# Agent API
@app.get("/api/agents")
def list_agents():
    """列出所有 Agent"""
    return {"agents": [a.dict() for a in agents_db.values()]}

@app.get("/api/agents/{agent_id}")
def get_agent(agent_id: str):
    """获取 Agent 详情"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents_db[agent_id].dict()

@app.post("/api/agents/{agent_id}/tasks")
def create_task_for_agent(agent_id: str, task: Task):
    """为 Agent 创建任务"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = agents_db[agent_id]
    
    # 检查预算
    if agent.budget_used + task.budget > agent.budget_monthly:
        raise HTTPException(status_code=400, detail="Budget exceeded")
    
    # 创建任务
    task.id = str(uuid.uuid4())[:8]
    task.assignee = agent_id
    task.created_at = datetime.now().isoformat()
    task.updated_at = task.created_at
    
    tasks_db[task.id] = task
    
    # 更新预算
    agent.budget_used += task.budget
    
    return {"success": True, "task": task.dict()}

# Task API
@app.get("/api/tasks")
def list_tasks(status: Optional[str] = None, assignee: Optional[str] = None):
    """列出任务"""
    tasks = list(tasks_db.values())
    
    if status:
        tasks = [t for t in tasks if t.status == status]
    if assignee:
        tasks = [t for t in tasks if t.assignee == assignee]
    
    return {"tasks": [t.dict() for t in tasks], "total": len(tasks)}

@app.get("/api/tasks/{task_id}")
def get_task(task_id: str):
    """获取任务详情"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id].dict()

@app.post("/api/tasks/{task_id}/delegate")
def delegate_task(task_id: str, sub_task: Task, sub_assignee: str):
    """委派子任务"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Parent task not found")
    
    parent = tasks_db[task_id]
    
    # 创建子任务
    sub_task.id = str(uuid.uuid4())[:8]
    sub_task.assignee = sub_assignee
    sub_task.parent_id = task_id
    sub_task.created_at = datetime.now().isoformat()
    sub_task.updated_at = sub_task.created_at
    
    tasks_db[sub_task.id] = sub_task
    parent.sub_tasks.append(sub_task.id)
    
    return {
        "success": True,
        "parent_task": asdict(parent),
        "sub_task": asdict(sub_task)
    }

@app.post("/api/tasks/{task_id}/complete")
def complete_task(task_id: str, cost: float = 0.0):
    """完成任务"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[task_id]
    task.status = "done"
    task.cost = cost
    task.updated_at = datetime.now().isoformat()
    
    return {"success": True, "task": asdict(task)}

# Org Chart API
@app.get("/api/org/chart")
def get_org_chart():
    """获取组织架构"""
    chart = {
        "id": "main",
        "name": "Monica",
        "title": "龙虾总管",
        "children": []
    }
    
    for agent in agents_db.values():
        if agent.id == "main":
            continue
        if agent.reports_to == "main":
            chart["children"].append({
                "id": agent.id,
                "name": agent.name,
                "title": agent.title,
                "department": agent.department
            })
    
    return chart

# Dashboard API
@app.get("/api/dashboard")
def get_dashboard():
    """获取仪表盘数据"""
    total_budget = sum(a.budget_monthly for a in agents_db.values())
    total_used = sum(a.budget_used for a in agents_db.values())
    
    return {
        "agents": {
            "total": len(agents_db),
            "active": sum(1 for a in agents_db.values() if a.status == "active")
        },
        "tasks": {
            "total": len(tasks_db),
            "backlog": sum(1 for t in tasks_db.values() if t.status == "backlog"),
            "in_progress": sum(1 for t in tasks_db.values() if t.status == "in_progress"),
            "done": sum(1 for t in tasks_db.values() if t.status == "done")
        },
        "budget": {
            "total": total_budget,
            "used": total_used,
            "remaining": total_budget - total_used,
            "usage_pct": (total_used / total_budget * 100) if total_budget > 0 else 0
        }
    }

# OpenClaw Integration API
@app.post("/api/openclaw/dispatch")
def dispatch_to_openclaw(agent_id: str, task_title: str, task_desc: str):
    """派发任务到 OpenClaw"""
    import requests
    
    try:
        # 调用 OpenClaw API
        response = requests.post("http://localhost:18788/v1/sessions/spawn", json={
            "agentId": agent_id,
            "task": f"{task_title}: {task_desc}",
            "runtime": "subagent",
            "mode": "run"
        }, timeout=30)
        
        return {
            "success": True,
            "openclaw_response": response.json() if response.status_code == 200 else None,
            "dispatched_to": agent_id
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "note": "OpenClaw may not be running"
        }

if __name__ == "__main__":
    init_data()
    uvicorn.run(app, host="0.0.0.0", port=3100, log_level="info")
