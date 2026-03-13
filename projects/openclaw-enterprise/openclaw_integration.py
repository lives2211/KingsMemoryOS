"""
OpenClaw 集成模块
让 Monica 在总指挥频道自动识别任务并派发
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from discord_dispatcher import handle_discord_message
from typing import Optional

# 总指挥频道 ID
COMMAND_CHANNEL_ID = "1480388799589515446"

# 任务触发关键词
TASK_KEYWORDS = [
    "帮我", "我要", "我想", "需要", "请",
    "做一个", "写个", "设计个", "分析", "爬取",
    "生成", "创建", "制作", "开发", "修复",
    "预算", "刀", "美元", "元"
]

def should_handle_message(message: str, channel_id: str, sender_id: str) -> bool:
    """
    判断是否应该处理这条消息
    
    Args:
        message: 消息内容
        channel_id: 频道ID
        sender_id: 发送者ID
        
    Returns:
        是否应该处理
    """
    # 只在总指挥频道处理
    if channel_id != COMMAND_CHANNEL_ID:
        return False
    
    # 不处理 Bot 消息
    if sender_id == "bot":
        return False
    
    # 检查是否包含任务关键词
    msg_lower = message.lower()
    return any(kw in msg_lower for kw in TASK_KEYWORDS)

def process_message(message: str, user: str, channel_id: str) -> Optional[str]:
    """
    处理消息，自动派发任务
    
    这是主入口，在 Monica 收到消息时调用
    """
    # 调用派发器
    reply = handle_discord_message(message, user)
    
    return reply


# 测试函数
def test_integration():
    """测试集成"""
    test_cases = [
        {
            "message": "帮我爬取 Twitter 数据，预算10美元",
            "user": "candycion",
            "channel": COMMAND_CHANNEL_ID,
            "expected": True
        },
        {
            "message": "设计一个小红书封面",
            "user": "candycion",
            "channel": COMMAND_CHANNEL_ID,
            "expected": True
        },
        {
            "message": "大家好",
            "user": "candycion",
            "channel": COMMAND_CHANNEL_ID,
            "expected": False
        },
        {
            "message": "帮我写代码",
            "user": "candycion",
            "channel": "123456",  # 其他频道
            "expected": False
        }
    ]
    
    print("🦞 OpenClaw 集成测试\n")
    
    for case in test_cases:
        should = should_handle_message(case["message"], case["channel"], "user")
        result = "✅" if should == case["expected"] else "❌"
        
        print(f"{result} 消息: {case['message'][:30]}...")
        print(f"   频道: {case['channel']}")
        print(f"   应该处理: {case['expected']}, 实际: {should}\n")
        
        if should and case["expected"]:
            reply = process_message(case["message"], case["user"], case["channel"])
            if reply:
                print(f"   回复:\n{reply[:200]}...\n")

if __name__ == "__main__":
    test_integration()
