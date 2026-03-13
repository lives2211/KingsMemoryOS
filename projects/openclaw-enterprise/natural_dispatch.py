#!/usr/bin/env python3
"""
自然语言任务派发系统
用自然语言描述任务，自动解析并派发
"""

import re
import json
from typing import Dict, List, Optional
from paperclip_client import PaperclipClient


class NaturalLanguageDispatch:
    """自然语言任务派发器"""
    
    def __init__(self):
        self.client = PaperclipClient()
        
        # 能力关键词映射
        self.capability_patterns = {
            "编程|代码|脚本|开发|爬虫|程序": ["编程", "脚本"],
            "设计|创意|封面|图片|UI|美工": ["设计", "创意"],
            "内容|文案|写作|文章|推文": ["内容", "文案"],
            "检测|测试|分析|数据|质检": ["检测", "分析"],
            "审计|复盘|质量|文档|检查": ["审计", "质量"],
            "社媒|运营|小红书|公众号|twitter|发布": ["社媒", "运营"],
            "统筹|管理|协调|决策": ["统筹", "决策"]
        }
        
        # 预算模式
        self.budget_patterns = {
            r'(\d+)\s*美元?': lambda m: float(m.group(1)),
            r'(\d+)\s*刀': lambda m: float(m.group(1)),
            r'(\d+)\s*usd': lambda m: float(m.group(1)),
            r'(\d+)\s*元': lambda m: float(m.group(1)),
        }
    
    def parse_task(self, natural_text: str) -> Dict:
        """
        解析自然语言任务描述
        
        示例输入：
        "帮我爬取twitter上的openclaw教程，预算10美元，需要编程能力"
        "设计一个小红书封面，5刀"
        "写一篇文案"
        
        返回：
        {
            "title": "任务标题",
            "description": "任务描述",
            "capabilities": ["能力1", "能力2"],
            "budget": 10.0
        }
        """
        result = {
            "title": "",
            "description": natural_text,
            "capabilities": [],
            "budget": 5.0  # 默认预算
        }
        
        # 1. 提取标题（第一句号或逗号前的内容，或前20个字）
        # 查找第一个标点符号
        match = re.search(r'^([^，。！？,\.\n]{10,50})[，。！？,\.\n]', natural_text)
        if match:
            result["title"] = match.group(1).strip()
        else:
            # 取前30个字作为标题
            result["title"] = natural_text[:30] + "..." if len(natural_text) > 30 else natural_text
        
        # 2. 提取能力关键词
        for pattern, caps in self.capability_patterns.items():
            if re.search(pattern, natural_text, re.IGNORECASE):
                result["capabilities"].extend(caps)
        
        # 去重
        result["capabilities"] = list(set(result["capabilities"]))
        
        # 如果没有匹配到能力，根据关键词猜测
        if not result["capabilities"]:
            result["capabilities"] = self._guess_capabilities(natural_text)
        
        # 3. 提取预算
        for pattern, extractor in self.budget_patterns.items():
            match = re.search(pattern, natural_text, re.IGNORECASE)
            if match:
                result["budget"] = extractor(match)
                break
        
        return result
    
    def _guess_capabilities(self, text: str) -> List[str]:
        """根据文本内容猜测能力需求"""
        text_lower = text.lower()
        
        # 技术类关键词
        tech_keywords = ["爬", "脚本", "程序", "代码", "数据", "api", "自动化", "教程", "分析"]
        if any(kw in text_lower for kw in tech_keywords):
            return ["编程", "脚本"]
        
        # 设计类关键词
        design_keywords = ["设计", "封面", "图", "ui", "美工", "视觉"]
        if any(kw in text_lower for kw in design_keywords):
            return ["设计", "创意"]
        
        # 内容类关键词
        content_keywords = ["写", "文案", "文章", "内容", "推文", "twitter"]
        if any(kw in text_lower for kw in content_keywords):
            return ["内容", "文案"]
        
        # 默认
        return ["统筹", "协调"]
    
    def dispatch(self, natural_text: str, notify_channel: Optional[str] = None) -> Dict:
        """
        自然语言派发任务
        
        Args:
            natural_text: 自然语言描述的任务
            notify_channel: 通知频道ID（Discord channel ID）
        
        Returns:
            派发结果
        """
        # 1. 解析任务
        parsed = self.parse_task(natural_text)
        
        print(f"📝 解析任务:")
        print(f"   标题: {parsed['title']}")
        print(f"   能力: {', '.join(parsed['capabilities'])}")
        print(f"   预算: ${parsed['budget']}")
        
        # 2. 智能派发
        result = self.client.smart_dispatch(
            title=parsed['title'],
            description=parsed['description'],
            required_caps=parsed['capabilities'],
            estimated_cost=parsed['budget']
        )
        
        # 3. 发送通知
        if notify_channel and result.get('success'):
            self._send_notification(notify_channel, parsed, result)
        
        return result
    
    def _send_notification(self, channel_id: str, parsed: Dict, result: Dict):
        """发送任务通知到 Discord"""
        try:
            from message import message as msg_tool
            
            task = result.get('task', {})
            agent_name = result.get('agent_name', 'Unknown')
            
            notification = f"""
📋 **新任务派发**

**标题:** {parsed['title']}
**指派给:** {agent_name}
**任务ID:** {task.get('id', 'N/A')}
**预算:** ${parsed['budget']}
**能力匹配:** {', '.join(parsed['capabilities'])}

**原始描述:**
{parsed['description'][:100]}...

💡 查看详情: http://localhost:3100/api/tasks/{task.get('id', '')}
            """
            
            # 发送消息
            msg_tool({
                "action": "send",
                "channel": "discord",
                "target": channel_id,
                "message": notification
            })
            
            print(f"✅ 通知已发送到频道: {channel_id}")
            
        except Exception as e:
            print(f"⚠️ 通知发送失败: {e}")
    
    def interactive_mode(self):
        """交互模式"""
        print("🚀 自然语言任务派发系统")
        print("=" * 60)
        print("直接输入任务描述，例如：")
        print('  - "帮我爬取twitter数据，预算10美元"')
        print('  - "设计一个小红书封面"')
        print('  - "写一篇产品介绍文案，5刀"')
        print("=" * 60)
        print()
        
        while True:
            try:
                user_input = input("📝 请输入任务 (或输入 'quit' 退出): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见!")
                    break
                
                if not user_input:
                    continue
                
                # 派发任务
                result = self.dispatch(user_input, notify_channel="1480388799589515446")
                
                if result.get('success'):
                    print(f"\n✅ 任务派发成功!")
                    print(f"   分配给: {result['agent_name']}")
                    print(f"   任务ID: {result['task']['id']}")
                    print(f"   剩余预算: ${result['budget_remaining']}")
                else:
                    print(f"\n❌ 派发失败: {result.get('error', 'Unknown error')}")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
                print()


# CLI 接口
if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="自然语言任务派发")
    parser.add_argument("task", nargs="?", help="任务描述（自然语言）")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--channel", "-c", default="1480388799589515446", 
                       help="通知频道ID")
    
    args = parser.parse_args()
    
    dispatcher = NaturalLanguageDispatch()
    
    if args.interactive:
        # 交互模式
        dispatcher.interactive_mode()
    elif args.task:
        # 单任务模式
        result = dispatcher.dispatch(args.task, notify_channel=args.channel)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 从标准输入读取
        if not sys.stdin.isatty():
            task_desc = sys.stdin.read().strip()
            if task_desc:
                result = dispatcher.dispatch(task_desc, notify_channel=args.channel)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("请输入任务描述")
        else:
            # 默认进入交互模式
            dispatcher.interactive_mode()
