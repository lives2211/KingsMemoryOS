#!/usr/bin/env python3
"""
总指挥自动任务派发系统
监听总指挥频道消息，自动解析并派发任务
"""

import re
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from natural_dispatch import NaturalLanguageDispatch
from paperclip_client import PaperclipClient


class AutoDispatcher:
    """
    自动任务派发器
    
    功能：
    1. 监听总指挥频道消息
    2. 识别任务意图
    3. 自动解析并派发
    4. 通知相关Agent
    """
    
    def __init__(self):
        self.dispatcher = NaturalLanguageDispatch()
        self.client = PaperclipClient()
        self.command_channel = "1480388799589515446"  # 总指挥频道
        
        # 任务触发词
        self.task_triggers = [
            "帮我", "我要", "我想", "需要", "请",
            "做一个", "写个", "设计个", "分析", "爬取",
            "生成", "创建", "制作", "开发"
        ]
        
        # 预算提取模式
        self.budget_pattern = r'(\d+)\s*(美元|刀|usd|元|\$)'
    
    def is_task_request(self, text: str) -> bool:
        """判断是否是任务请求"""
        text_lower = text.lower()
        
        # 检查是否包含触发词
        for trigger in self.task_triggers:
            if trigger in text_lower:
                return True
        
        # 检查是否包含预算信息
        if re.search(self.budget_pattern, text):
            return True
        
        # 检查是否包含能力关键词
        capability_keywords = [
            "编程", "代码", "脚本", "爬虫", "程序",
            "设计", "创意", "封面", "图片", "UI",
            "文案", "写作", "文章", "内容",
            "分析", "数据", "检测", "测试",
            "审计", "复盘", "质量",
            "社媒", "运营", "小红书", "twitter", "发布"
        ]
        
        for kw in capability_keywords:
            if kw in text:
                return True
        
        return False
    
    def parse_task_from_message(self, message: str, sender: str) -> Optional[Dict]:
        """
        从消息中解析任务
        
        示例消息：
        "帮我爬取twitter数据，预算10美元"
        "设计一个小红书封面"
        "@yitai 写个爬虫脚本"
        """
        
        # 检查是否是任务请求
        if not self.is_task_request(message):
            return None
        
        # 解析任务
        parsed = self.dispatcher.parse_task(message)
        
        # 检查是否指定了特定Agent（通过@）
        agent_mention = re.search(r'@(yitai|bingbing|daping|spikey|xiaohongcai|main)', message)
        if agent_mention:
            parsed['specified_agent'] = agent_mention.group(1)
        
        parsed['original_message'] = message
        parsed['sender'] = sender
        parsed['parsed_at'] = datetime.now().isoformat()
        
        return parsed
    
    def dispatch_task(self, task_info: Dict) -> Dict:
        """派发任务"""
        
        # 如果指定了Agent，直接分配给该Agent
        if task_info.get('specified_agent'):
            agent_id = task_info['specified_agent']
            
            # 检查预算
            budget_check = self.client.check_budget(agent_id, task_info['budget'])
            if not budget_check['allowed']:
                return {
                    "success": False,
                    "error": f"@{agent_id} 预算不足",
                    "budget_status": budget_check
                }
            
            # 直接创建任务
            result = self.client.create_task(
                title=task_info['title'],
                description=task_info['description'],
                assignee=agent_id,
                priority="P2",
                budget=task_info['budget']
            )
            
            # 添加指定标记
            result['specified'] = True
            result['specified_agent'] = agent_id
            
            return result
        
        # 否则使用智能派发
        return self.dispatcher.dispatch(
            task_info['description'],
            notify_channel=None  # 我们在外部处理通知
        )
    
    def generate_dispatch_report(self, task_info: Dict, result: Dict) -> str:
        """生成派发报告"""
        
        if not result.get('success'):
            return f"""
❌ **任务派发失败**

**原因:** {result.get('error', 'Unknown error')}

**原始任务:**
{task_info['original_message'][:100]}

请检查预算或重新描述任务。
            """
        
        task = result.get('task', {})
        agent_name = result.get('agent_name', result.get('specified_agent', 'Unknown'))
        
        # 判断是否是指定派发
        if result.get('specified'):
            dispatch_type = "📍 指定派发"
        else:
            dispatch_type = "🤖 智能匹配"
        
        report = f"""
{dispatch_type}

📋 **任务已派发**

**任务标题:** {task.get('title', 'N/A')}
**任务ID:** `{task.get('id', 'N/A')}`

**指派给:** @{agent_name}
**匹配度:** {result.get('match_score', 'N/A')}/4
**优先级:** {task.get('priority', 'P2')}

**预算:**
- 任务预算: ${task.get('budget', 0)}
- Agent剩余预算: ${result.get('budget_remaining', 'N/A')}

**能力需求:** {', '.join(task_info.get('capabilities', []))}

**任务描述:**
{task_info['description'][:200]}...

💡 查看任务: http://localhost:3100/api/tasks/{task.get('id', '')}
        """
        
        return report
    
    def process_message(self, message: str, sender: str, channel: str) -> Optional[str]:
        """
        处理频道消息
        
        Args:
            message: 消息内容
            sender: 发送者
            channel: 频道ID
        
        Returns:
            回复消息（如果有）
        """
        # 只处理总指挥频道的消息
        if channel != self.command_channel:
            return None
        
        # 解析任务
        task_info = self.parse_task_from_message(message, sender)
        if not task_info:
            return None
        
        print(f"📝 检测到任务请求: {task_info['title']}")
        
        # 派发任务
        result = self.dispatch_task(task_info)
        
        # 生成报告
        report = self.generate_dispatch_report(task_info, result)
        
        return report
    
    def simulate_dispatch(self, message: str, sender: str = "user") -> str:
        """
        模拟派发（用于测试）
        
        用法:
        python3 auto_dispatcher.py "帮我爬取twitter数据，预算10美元"
        """
        result = self.process_message(message, sender, self.command_channel)
        return result if result else "未识别为任务请求"


# 模拟消息监听
class MockDiscordListener:
    """模拟 Discord 消息监听"""
    
    def __init__(self, dispatcher: AutoDispatcher):
        self.dispatcher = dispatcher
    
    def on_message(self, message: str, sender: str, channel: str):
        """收到消息时调用"""
        response = self.dispatcher.process_message(message, sender, channel)
        if response:
            print("\n" + "=" * 60)
            print(response)
            print("=" * 60 + "\n")


# CLI 接口
if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="总指挥自动任务派发")
    parser.add_argument("message", nargs="?", help="测试消息")
    parser.add_argument("--test", "-t", action="store_true", help="测试模式")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    dispatcher = AutoDispatcher()
    
    if args.test and args.message:
        # 测试单条消息
        print(f"🧪 测试消息: {args.message}")
        print()
        result = dispatcher.simulate_dispatch(args.message)
        print(result)
    
    elif args.interactive:
        # 交互模式
        print("🚀 总指挥自动任务派发系统")
        print("=" * 60)
        print("输入自然语言任务，例如：")
        print('  - "帮我爬取twitter数据，预算10美元"')
        print('  - "@yitai 写个爬虫脚本"')
        print('  - "设计一个小红书封面"')
        print("=" * 60)
        print()
        
        while True:
            try:
                user_input = input("📝 输入任务: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                result = dispatcher.simulate_dispatch(user_input)
                print(result)
                print()
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
    
    elif args.message:
        # 直接处理消息
        result = dispatcher.simulate_dispatch(args.message)
        print(result)
    
    else:
        print("用法:")
        print("  python3 auto_dispatcher.py \"任务描述\"")
        print("  python3 auto_dispatcher.py -t \"任务描述\"")
        print("  python3 auto_dispatcher.py -i")
