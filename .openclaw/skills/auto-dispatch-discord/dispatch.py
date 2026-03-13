#!/usr/bin/env python3
"""
OpenClaw Skill: Discord 自动派发
在总指挥频道自动识别任务并派发
"""

import sys
import json
import re
from pathlib import Path

# 添加项目路径
sys.path.insert(0, '/home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise')

def main():
    """主函数 - 处理 Discord 消息"""
    
    # 读取输入（Discord 消息）
    try:
        input_data = json.loads(sys.stdin.read())
    except:
        print("❌ 无法解析输入")
        return
    
    message = input_data.get('message', '')
    channel = input_data.get('channel', '')
    sender = input_data.get('sender', '')
    
    # 只处理总指挥频道
    if channel != '1480388799589515446':
        return
    
    # 忽略自己的消息
    if sender == '龙虾总管':
        return
    
    # 检查是否是任务请求
    task_keywords = [
        '帮我', '我要', '我想', '需要', '请',
        '做一个', '写个', '设计个', '分析', '爬取',
        '生成', '创建', '制作', '开发'
    ]
    
    is_task = any(kw in message for kw in task_keywords)
    
    if not is_task:
        return
    
    # 导入派发客户端
    try:
        from paperclip_client import PaperclipClient
        client = PaperclipClient()
        
        # 解析预算
        budget_match = re.search(r'(\d+)\s*(美元|刀|usd|\$|元)', message.lower())
        budget = float(budget_match.group(1)) if budget_match else 5.0
        
        # 解析能力
        caps = []
        if any(kw in message for kw in ['爬', '脚本', '程序', '代码']):
            caps = ['编程', '脚本']
        elif any(kw in message for kw in ['设计', '封面', '图']):
            caps = ['设计', '创意']
        elif any(kw in message for kw in ['写', '文案', '文章']):
            caps = ['内容', '文案']
        elif any(kw in message for kw in ['分析', '数据']):
            caps = ['检测', '分析']
        else:
            caps = ['统筹', '协调']
        
        # 检查是否指定Agent
        agent_match = re.search(r'@(yitai|bingbing|daping|spikey|xiaohongcai)', message)
        
        if agent_match:
            # 指定派发
            agent_id = agent_match.group(1)
            result = client.create_task(
                title=message[:50],
                description=message,
                assignee=agent_id,
                priority='P2',
                budget=budget
            )
            
            if result.get('success'):
                print(f"""📍 **指定派发**

**任务:** {message[:50]}...
**指派给:** @{agent_id}
**任务ID:** `{result['task']['id']}`
**预算:** ${budget}
""")
        else:
            # 智能派发
            result = client.smart_dispatch(
                title=message[:50],
                description=message,
                required_caps=caps,
                estimated_cost=budget
            )
            
            if result.get('success'):
                print(f"""🤖 **智能派发**

**任务:** {message[:50]}...
**指派给:** @{result['agent_name']}
**任务ID:** `{result['task']['id']}`
**匹配度:** {result['match_score']}/4
**预算:** ${budget}
""")
            else:
                print(f"❌ 派发失败: {result.get('error', 'Unknown')}")
    
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == '__main__':
    main()
