#!/usr/bin/env python3
"""
Discord Bot - 总指挥频道监听
监听 1480388799589515446 频道消息，自动派发任务
"""

import json
import asyncio
from auto_dispatcher import AutoDispatcher


class DiscordCommandBot:
    """
    Discord 命令 Bot
    
    监听总指挥频道，自动识别任务并派发
    """
    
    def __init__(self):
        self.dispatcher = AutoDispatcher()
        self.command_channel = "1480388799589515446"
        self.bot_name = "Monica"
    
    def handle_message(self, message: str, sender: str, channel: str) -> str:
        """
        处理收到的消息
        
        返回回复内容（如果有）
        """
        # 忽略自己的消息
        if sender == self.bot_name:
            return ""
        
        # 使用自动派发器处理
        response = self.dispatcher.process_message(message, sender, channel)
        
        return response if response else ""
    
    def simulate_conversation(self):
        """模拟对话（测试用）"""
        print("🚀 Discord Bot 模拟器")
        print(f"监听频道: {self.command_channel}")
        print("=" * 60)
        print()
        
        test_messages = [
            ("user1", "帮我爬取twitter上的openclaw教程，预算10美元"),
            ("user2", "@yitai 写个自动化脚本"),
            ("user3", "设计一个小红书封面，5刀"),
            ("user4", "分析一下竞品数据"),
            ("user5", "大家好，今天天气不错"),  # 非任务，应该忽略
        ]
        
        for sender, message in test_messages:
            print(f"💬 [{sender}]: {message}")
            
            response = self.handle_message(message, sender, self.command_channel)
            
            if response:
                print(f"🤖 [{self.bot_name}]:")
                print(response)
            else:
                print("🤖 [Monica]: (未识别为任务)")
            
            print()
    
    def run_interactive(self):
        """交互模式"""
        print("🚀 Discord Bot - 总指挥频道监听")
        print(f"频道ID: {self.command_channel}")
        print("=" * 60)
        print("输入消息测试，或输入 'demo' 查看示例")
        print("=" * 60)
        print()
        
        while True:
            try:
                user_input = input("💬 输入消息: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if user_input.lower() == 'demo':
                    self.simulate_conversation()
                    continue
                
                if not user_input:
                    continue
                
                # 模拟发送者
                sender = "user"
                
                response = self.handle_message(user_input, sender, self.command_channel)
                
                if response:
                    print(f"\n🤖 [{self.bot_name}]:")
                    print(response)
                else:
                    print("\n🤖 [Monica]: 未识别为任务请求")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")


# 快捷命令脚本
def create_shortcut_scripts():
    """创建快捷命令脚本"""
    
    # 1. 监听脚本
    with open('listen', 'w') as f:
        f.write('''#!/bin/bash
# 启动 Discord Bot 监听
cd "$(dirname "$0")"
python3 discord_bot.py
''')
    
    # 2. 快速派发脚本
    with open('ask', 'w') as f:
        f.write('''#!/bin/bash
# 向总指挥提问/派任务
# 用法: ./ask "任务描述"

if [ -z "$1" ]; then
    echo "用法: ./ask \"任务描述\""
    echo "示例: ./ask \"帮我爬取数据，预算10美元\""
    exit 1
fi

cd "$(dirname "$0")"
echo "$1" | python3 auto_dispatcher.py
''')
    
    import os
    os.chmod('listen', 0o755)
    os.chmod('ask', 0o755)
    
    print("✅ 快捷命令已创建:")
    print("  ./listen  - 启动监听模式")
    print("  ./ask     - 快速派任务")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Discord Bot")
    parser.add_argument("--demo", action="store_true", help="运行示例")
    parser.add_argument("--create-scripts", action="store_true", help="创建快捷脚本")
    
    args = parser.parse_args()
    
    bot = DiscordCommandBot()
    
    if args.create_scripts:
        create_shortcut_scripts()
    elif args.demo:
        bot.simulate_conversation()
    else:
        bot.run_interactive()
