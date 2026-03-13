"""
Agent Bridge - 连接 Dispatch Server 与真正的独立 Agent

将任务派发到之前创建的 OpenClaw 子会话
"""

import subprocess
import json
from typing import Optional, Dict

# Agent 配置映射
AGENT_SESSIONS = {
    "yitai": {
        "workspace": "/home/fengxueda/.openclaw/workspace-yitai",
        "description": "技术官 - 编程/开发/调试",
        "session_label": "yitai"
    },
    "bingbing": {
        "workspace": "/home/fengxueda/.openclaw/workspace-bingbing",
        "description": "创意官 - 设计/文案/内容",
        "session_label": "bingbing"
    },
    "daping": {
        "workspace": "/home/fengxueda/.openclaw/workspace-daping",
        "description": "检测官 - 分析/数据/监控",
        "session_label": "daping"
    },
    "spikey": {
        "workspace": "/home/fengxueda/.openclaw/workspace-spikey",
        "description": "审计官 - 审计/质量/检查",
        "session_label": "spikey"
    },
    "xiaohongcai": {
        "workspace": "/home/fengxueda/.openclaw/workspace-xiaohongcai",
        "description": "运营官 - 社媒/运营/发布",
        "session_label": "xiaohongcai"
    }
}


def dispatch_to_agent(agent_id: str, task: Dict) -> bool:
    """
    派发任务到真正的独立 Agent
    
    使用 sessions_send 发送到 Agent 的子会话
    """
    if agent_id not in AGENT_SESSIONS:
        print(f"[Bridge] 未知 Agent: {agent_id}")
        return False
    
    agent = AGENT_SESSIONS[agent_id]
    
    # 构建任务消息
    message = f"""🎯 【新任务】{task['title']}

📋 描述: {task['description']}
🆔 任务ID: {task['id']}
💰 预算: ${task.get('budget', {}).get('total', 0)}
⏰ 优先级: {task.get('priority', 'normal')}

请确认收到任务并开始执行。
完成后请汇报结果。
"""
    
    try:
        # 使用 openclaw sessions send 发送到 Agent 会话
        result = subprocess.run(
            [
                "openclaw", "sessions", "send",
                "--label", agent["session_label"],
                "--message", message
            ],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=agent["workspace"]
        )
        
        if result.returncode == 0:
            print(f"[Bridge] ✅ 任务已发送到 @{agent_id}")
            return True
        else:
            print(f"[Bridge] ❌ 发送失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[Bridge] ❌ 异常: {e}")
        return False


def spawn_agent_session(agent_id: str) -> bool:
    """
    启动 Agent 子会话 (如果未运行)
    
    使用 sessions_spawn 创建新的 Agent 会话
    """
    if agent_id not in AGENT_SESSIONS:
        return False
    
    agent = AGENT_SESSIONS[agent_id]
    
    try:
        # 检查是否已有活跃会话
        result = subprocess.run(
            ["openclaw", "sessions", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if agent["session_label"] in result.stdout:
            print(f"[Bridge] @{agent_id} 会话已存在")
            return True
        
        # 启动新会话
        print(f"[Bridge] 启动 @{agent_id} 会话...")
        subprocess.Popen(
            [
                "openclaw", "sessions", "spawn",
                "--label", agent["session_label"],
                "--mode", "session",
                "--cwd", agent["workspace"]
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        return True
        
    except Exception as e:
        print(f"[Bridge] 启动失败: {e}")
        return False


# 测试
if __name__ == "__main__":
    test_task = {
        "id": "TEST-001",
        "title": "测试任务",
        "description": "这是一个测试任务",
        "budget": {"total": 10},
        "priority": "normal"
    }
    
    for agent_id in AGENT_SESSIONS.keys():
        print(f"\n测试派发到 @{agent_id}:")
        success = dispatch_to_agent(agent_id, test_task)
        print(f"结果: {'✅ 成功' if success else '❌ 失败'}")
