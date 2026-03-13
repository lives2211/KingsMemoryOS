#!/usr/bin/env python3
"""
Paperclip ↔ OpenClaw Bridge
连接 Paperclip 的任务系统与 OpenClaw 的多 Agent 执行
"""

import os
import sys
import json
import requests
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any

# OpenClaw Gateway 配置
OPENCLAW_GATEWAY = os.getenv("OPENCLAW_GATEWAY", "http://localhost:18788")

# Agent 映射配置 - 匹配你的团队
AGENT_MAP = {
    "yitai": {
        "name": "yitai",
        "role": "技术官",
        "skills": ["编程", "代码", "脚本", "开发", "调试", "爬取"],
        "session_label": "yitai",
        "model": "claude-3-5-sonnet"
    },
    "bingbing": {
        "name": "bingbing",
        "role": "创意官",
        "skills": ["设计", "创意", "封面", "内容", "文案", "写作", "图像", "视频"],
        "session_label": "bingbing",
        "model": "claude-3-5-sonnet"
    },
    "daping": {
        "name": "daping",
        "role": "检测官",
        "skills": ["分析", "数据", "检测", "监控", "竞品"],
        "session_label": "daping",
        "model": "claude-3-5-sonnet"
    },
    "spikey": {
        "name": "spikey",
        "role": "审计官",
        "skills": ["审计", "复盘", "质量", "审查", "检查"],
        "session_label": "spikey",
        "model": "claude-3-5-sonnet"
    },
    "xiaohongcai": {
        "name": "xiaohongcai",
        "role": "运营官",
        "skills": ["社媒", "运营", "发布", "小红书", "公众号"],
        "session_label": "xiaohongcai",
        "model": "claude-3-5-sonnet"
    }
}

# 任务关键词匹配
def match_agent(task_description: str) -> Optional[str]:
    """根据任务描述匹配最佳 Agent"""
    task_lower = task_description.lower()
    scores = {}
    
    for agent_id, config in AGENT_MAP.items():
        score = 0
        for skill in config["skills"]:
            if skill.lower() in task_lower:
                score += 1
        scores[agent_id] = score
    
    # 返回得分最高的 Agent
    if scores:
        best_match = max(scores, key=scores.get)
        if scores[best_match] > 0:
            return best_match
    
    return None

def dispatch_to_openclaw(agent_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
    """派发任务到 OpenClaw Agent"""
    agent_config = AGENT_MAP.get(agent_id)
    if not agent_config:
        return {"error": f"Unknown agent: {agent_id}"}
    
    # 构建任务消息
    task_message = f"""【任务】{task.get('title', '未命名任务')}
【背景】{task.get('description', '无描述')}
【来自】Paperclip 任务系统
【任务ID】{task.get('id', 'unknown')}
【预算】${task.get('budget', 0)}
【优先级】{task.get('priority', 'normal')}

请确认收到任务并开始执行。完成后请汇报结果。
"""
    
    # 使用 sessions_send 发送给 Agent
    try:
        result = subprocess.run(
            ["openclaw", "sessions", "send", 
             "--label", agent_config["session_label"],
             "--message", task_message],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "success": result.returncode == 0,
            "agent": agent_id,
            "agent_name": agent_config["name"],
            "role": agent_config["role"],
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        return {
            "success": False,
            "agent": agent_id,
            "error": str(e)
        }

def notify_discord(task: Dict[str, Any], agent_info: Dict[str, Any]) -> bool:
    """在 Discord 总指挥频道通知任务派发"""
    # 这里可以通过 OpenClaw 的 message 工具发送
    # 或者通过 webhook
    return True

def main():
    """CLI 入口"""
    if len(sys.argv) < 2:
        print("Usage: python paperclip_bridge.py <command> [args]")
        print("Commands:")
        print("  dispatch <task_json>  - 派发任务到 Agent")
        print("  match <description>   - 匹配最佳 Agent")
        print("  agents               - 列出所有 Agent")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "agents":
        print(json.dumps(AGENT_MAP, indent=2, ensure_ascii=False))
    
    elif command == "match" and len(sys.argv) >= 3:
        description = sys.argv[2]
        agent_id = match_agent(description)
        if agent_id:
            agent = AGENT_MAP[agent_id]
            print(f"✅ 匹配成功: @{agent_id} ({agent['role']})")
            print(f"   技能: {', '.join(agent['skills'][:5])}")
        else:
            print("❌ 未匹配到合适的 Agent")
    
    elif command == "dispatch" and len(sys.argv) >= 3:
        task_json = sys.argv[2]
        try:
            task = json.loads(task_json)
            agent_id = match_agent(task.get('description', ''))
            if not agent_id:
                # 默认派发给 yitai
                agent_id = 'yitai'
            
            result = dispatch_to_openclaw(agent_id, task)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析错误: {e}")
            sys.exit(1)
    
    else:
        print(f"❌ 未知命令: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
