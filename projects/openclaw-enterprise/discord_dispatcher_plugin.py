#!/usr/bin/env python3
"""
OpenClaw Discord 自动派发插件
监听总指挥频道消息，自动识别任务并派发
"""

import os
import sys
import json
import re
from pathlib import Path

# 添加项目路径
sys.path.insert(0, '/home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise')

from auto_dispatcher import AutoDispatcher


class DiscordDispatcherPlugin:
    """
    Discord 自动派发插件
    
    功能：
    - 监听总指挥频道 (1480388799589515446)
    - 自动识别任务请求
    - 调用 Paperclip 派发任务
    - 回复派发结果
    """
    
    def __init__(self):
        self.dispatcher = AutoDispatcher()
        self.command_channel = "1480388799589515446"
        self.bot_id = "1480390276500557824"  # 龙虾总管 Bot ID
    
    def process_incoming_message(self, message_data: dict) -> dict:
        """
        处理收到的 Discord 消息
        
        Args:
            message_data: {
                "content": "消息内容",
                "author": {"id": "用户ID", "name": "用户名"},
                "channel_id": "频道ID",
                "guild_id": "服务器ID"
            }
        
        Returns:
            回复消息（如果有）
        """
        content = message_data.get("content", "")
        author_id = message_data.get("author", {}).get("id", "")
        channel_id = message_data.get("channel_id", "")
        author_name = message_data.get("author", {}).get("name", "")
        
        # 忽略自己的消息
        if author_id == self.bot_id:
            return {}
        
        # 只处理总指挥频道
        if channel_id != self.command_channel:
            return {}
        
        # 使用自动派发器处理
        response = self.dispatcher.process_message(
            content,
            author_name,
            channel_id
        )
        
        if response:
            return {
                "action": "reply",
                "content": response
            }
        
        return {}


# OpenClaw 插件接口
plugin = DiscordDispatcherPlugin()

def on_message(message_data):
    """OpenClaw 消息回调"""
    return plugin.process_incoming_message(message_data)


if __name__ == "__main__":
    # 测试模式
    test_messages = [
        {
            "content": "帮我爬取twitter数据，预算10美元",
            "author": {"id": "1245303958352691221", "name": "candycion"},
            "channel_id": "1480388799589515446",
            "guild_id": "1480388798729814189"
        },
        {
            "content": "设计一个小红书封面",
            "author": {"id": "1245303958352691221", "name": "candycion"},
            "channel_id": "1480388799589515446",
            "guild_id": "1480388798729814189"
        }
    ]
    
    for msg in test_messages:
        print(f"\n💬 收到消息: {msg['content']}")
        result = on_message(msg)
        if result:
            print(f"🤖 回复:\n{result['content']}")
        else:
            print("🤖 无回复（未识别为任务）")
