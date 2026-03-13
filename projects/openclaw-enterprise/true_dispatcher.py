"""
真正的独立 Agent 派发器
将任务发送到 OpenClaw 子会话，Agent 独立执行
"""

import subprocess
import json
import time
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


def ensure_agent_running(agent_id: str) -> bool:
    """确保 Agent 子会话正在运行"""
    try:
        # 检查是否已有会话
        result = subprocess.run(
            ["openclaw", "sessions", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if agent_id in result.stdout:
            return True
        
        # 启动新会话
        agent = TRUE_AGENTS.get(agent_id)
        if not agent:
            return False
        
        subprocess.Popen(
            ["openclaw", "sessions", "spawn",
             "--label", agent_id,
             "--mode", "session",
             "--cwd", agent["workspace"]],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        time.sleep(3)  # 等待启动
        return True
        
    except Exception as e:
        print(f"[TrueDispatcher] 启动失败: {e}")
        return False


def dispatch_to_true_agent(agent_id: str, task: Dict) -> bool:
    """
    派发任务到真正的独立 Agent
    
    Agent 会:
    1. 接收任务
    2. 自主分析
    3. 独立执行
    4. 生成真实结果
    5. 汇报完成
    """
    if agent_id not in TRUE_AGENTS:
        return False
    
    agent = TRUE_AGENTS[agent_id]
    
    # 1. 确保 Agent 运行
    if not ensure_agent_running(agent_id):
        return False
    
    # 2. 构建任务指令
    task_instruction = f"""🎯 【任务委派】

来自总指挥 Monica 的任务委派：

📋 任务: {task['title']}
📝 描述: {task['description']}
💰 预算: ${task.get('budget', {}).get('total', 0)}
🆔 任务ID: {task['id']}

【你的角色】
你是 {agent['role']}，专长: {', '.join(agent['skills'][:3])}

【执行要求】
1. 确认收到任务
2. 自主分析需求
3. 独立完成执行
4. 生成真实交付物
5. 完成后向 Monica 汇报

请立即开始执行！
"""
    
    # 3. 发送到 Agent 子会话
    try:
        result = subprocess.run(
            ["openclaw", "sessions", "send",
             "--label", agent_id,
             "--message", task_instruction],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=agent["workspace"]
        )
        
        if result.returncode == 0:
            print(f"[TrueDispatcher] ✅ 任务已发送到 @{agent_id}")
            return True
        else:
            print(f"[TrueDispatcher] ❌ 发送失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[TrueDispatcher] ❌ 异常: {e}")
        return False


if __name__ == "__main__":
    # 测试
    test_task = {
        "id": "TEST-001",
        "title": "测试任务",
        "description": "这是一个测试任务，请确认收到",
        "budget": {"total": 10},
        "priority": "normal"
    }
    
    for agent_id in TRUE_AGENTS.keys():
        print(f"\n测试派发到 @{agent_id}:")
        success = dispatch_to_true_agent(agent_id, test_task)
        print(f"结果: {'✅ 成功' if success else '❌ 失败'}")
