#!/usr/bin/env python3
"""
Discord 通知发送器
发送任务通知到指定频道
"""

import os
import json
import requests
from datetime import datetime


def send_task_notification(channel_id: str, task_info: dict, agent_info: dict):
    """
    发送任务通知到 Discord
    
    Args:
        channel_id: Discord 频道 ID
        task_info: 任务信息
        agent_info: Agent 信息
    """
    
    # 构建消息
    embed = {
        "title": "📋 新任务派发",
        "color": 3447003,  # 蓝色
        "fields": [
            {
                "name": "任务标题",
                "value": task_info.get('title', 'N/A'),
                "inline": False
            },
            {
                "name": "指派给",
                "value": f"{agent_info.get('agent_name', 'Unknown')} (@{agent_info.get('assigned_to', 'N/A')})",
                "inline": True
            },
            {
                "name": "任务ID",
                "value": task_info.get('id', 'N/A'),
                "inline": True
            },
            {
                "name": "预算",
                "value": f"${task_info.get('budget', 0)}",
                "inline": True
            },
            {
                "name": "匹配度",
                "value": f"{agent_info.get('match_score', 0)}/4",
                "inline": True
            },
            {
                "name": "剩余预算",
                "value": f"${agent_info.get('budget_remaining', 0)}",
                "inline": True
            }
        ],
        "footer": {
            "text": f"派发时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
    }
    
    # 添加描述（如果不太长）
    description = task_info.get('description', '')
    if len(description) > 100:
        description = description[:100] + "..."
    if description:
        embed["fields"].append({
            "name": "任务描述",
            "value": description,
            "inline": False
        })
    
    # 构建 payload
    payload = {
        "content": f"🚀 新任务已派发! <@{agent_info.get('assigned_to', '')}>",
        "embeds": [embed]
    }
    
    # 获取 Discord webhook URL
    # 注意：需要配置 DISCORD_WEBHOOK_URL 环境变量
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("⚠️ 未配置 DISCORD_WEBHOOK_URL，跳过通知")
        return False
    
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 204:
            print(f"✅ 通知已发送到 Discord")
            return True
        else:
            print(f"⚠️ 通知发送失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ 通知发送失败: {e}")
        return False


# 简单的消息发送（不使用 embed）
def send_simple_message(channel_id: str, message: str):
    """发送简单文本消息"""
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("⚠️ 未配置 DISCORD_WEBHOOK_URL")
        return False
    
    try:
        response = requests.post(
            webhook_url,
            json={"content": message},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        return response.status_code == 204
    except Exception as e:
        print(f"⚠️ 发送失败: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 notify_discord.py '消息内容'")
        sys.exit(1)
    
    message = sys.argv[1]
    send_simple_message("1480388799589515446", message)
