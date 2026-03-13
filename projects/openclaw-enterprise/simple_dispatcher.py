"""
简化的真正独立 Agent 派发器

通过文件系统实现 Agent 通信:
1. 派发任务到共享目录
2. Agent 独立工作空间读取并执行
3. Agent 汇报结果
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Agent 配置
TRUE_AGENTS = {
    "yitai": {
        "name": "yitai",
        "role": "技术官",
        "workspace": "/home/fengxueda/.openclaw/workspace-yitai",
        "skills": ["编程", "代码", "脚本", "开发", "调试", "爬取", "修复"],
        "can_execute": True
    },
    "bingbing": {
        "name": "bingbing",
        "role": "创意官",
        "workspace": "/home/fengxueda/.openclaw/workspace-bingbing",
        "skills": ["设计", "创意", "封面", "内容", "文案", "写作", "图像", "视频"],
        "can_execute": True
    },
    "daping": {
        "name": "daping",
        "role": "检测官",
        "workspace": "/home/fengxueda/.openclaw/workspace-daping",
        "skills": ["分析", "数据", "检测", "监控", "竞品"],
        "can_execute": True
    },
    "spikey": {
        "name": "spikey",
        "role": "审计官",
        "workspace": "/home/fengxueda/.openclaw/workspace-spikey",
        "skills": ["审计", "复盘", "质量", "审查", "检查"],
        "can_execute": True
    }
}

# 共享任务目录
SHARED_TASKS_DIR = Path("/home/fengxueda/.openclaw/workspace/memory/shared/tasks")


def ensure_shared_dir():
    """确保共享目录存在"""
    SHARED_TASKS_DIR.mkdir(parents=True, exist_ok=True)


def dispatch_to_agent(agent_id: str, task: Dict) -> bool:
    """
    派发任务到真正的独立 Agent
    
    通过文件系统通信:
    1. 创建任务文件到共享目录
    2. Agent 工作空间读取
    3. Agent 独立执行
    4. Agent 写入结果
    """
    if agent_id not in TRUE_AGENTS:
        return False
    
    agent = TRUE_AGENTS[agent_id]
    
    # 1. 确保共享目录
    ensure_shared_dir()
    
    # 2. 创建任务文件
    task_file = SHARED_TASKS_DIR / f"{task['id']}.json"
    
    task_data = {
        "id": task['id'],
        "title": task['title'],
        "description": task['description'],
        "budget": task.get('budget', {}).get('total', 0),
        "priority": task.get('priority', 'normal'),
        "assigned_to": agent_id,
        "assigned_at": datetime.now().isoformat(),
        "status": "assigned",
        "agent_role": agent['role'],
        "agent_skills": agent['skills'],
        "workspace": agent['workspace']
    }
    
    # 3. 写入任务文件
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(task_data, f, ensure_ascii=False, indent=2)
    
    print(f"[SimpleDispatcher] ✅ 任务已派发到 @{agent_id}")
    print(f"  任务文件: {task_file}")
    print(f"  Agent 工作空间: {agent['workspace']}")
    print(f"  Agent 角色: {agent['role']}")
    
    return True


def check_agent_result(task_id: str) -> Optional[Dict]:
    """检查 Agent 是否已完成任务"""
    result_file = SHARED_TASKS_DIR / f"{task_id}_result.json"
    
    if result_file.exists():
        with open(result_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return None


# 测试
if __name__ == "__main__":
    test_task = {
        "id": "TEST-001",
        "title": "测试真正独立 Agent",
        "description": "验证 Agent 是否真正独立执行",
        "budget": {"total": 10},
        "priority": "normal"
    }
    
    print("🧪 测试简化的真正独立 Agent:")
    print('=' * 60)
    
    for agent_id in TRUE_AGENTS.keys():
        print(f"\n测试 @{agent_id}:")
        success = dispatch_to_agent(agent_id, test_task)
        print(f"结果: {'✅ 成功' if success else '❌ 失败'}")
    
    print('\n' + '=' * 60)
    print(f"任务文件位置: {SHARED_TASKS_DIR}")
