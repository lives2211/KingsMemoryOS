#!/usr/bin/env python3
"""
Auto Dispatch Tool for OpenClaw
自动派发任务到 Paperclip
"""

import sys
import json
import re
import subprocess

def main():
    # 读取输入
    try:
        input_data = json.loads(sys.stdin.read())
    except:
        print(json.dumps({"error": "Invalid input"}))
        return
    
    message = input_data.get('message', '')
    channel = input_data.get('channel_id', '')
    sender = input_data.get('sender', '')
    
    # 只处理总指挥频道
    if channel != '1480388799589515446':
        print(json.dumps({"skip": True}))
        return
    
    # 检查是否是任务
    keywords = ['帮我', '我要', '我想', '需要', '做一个', '写个', '设计个', '分析', '爬取']
    is_task = any(kw in message for kw in keywords)
    
    if not is_task:
        print(json.dumps({"skip": True}))
        return
    
    # 执行派发
    try:
        result = subprocess.run(
            ['/home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise/quick_dispatch.sh', message, sender],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout.strip()
        
        print(json.dumps({
            "action": "reply",
            "content": output
        }))
        
    except Exception as e:
        print(json.dumps({
            "action": "reply", 
            "content": f"❌ 派发失败: {str(e)}"
        }))

if __name__ == '__main__':
    main()
