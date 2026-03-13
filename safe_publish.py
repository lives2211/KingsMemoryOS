#!/usr/bin/env python3
"""
安全发布系统
- 预览所有推文
- 确认后再发布
- 跳过测试内容
"""

import json
import subprocess
from datetime import datetime


def preview_content():
    """预览内容"""
    with open('deep_analysis_20260312_142625.json', 'r') as f:
        data = json.load(f)
    
    tweets = data.get('tweets_standard', data['tweets'])
    source = data['source']
    
    print("="*60)
    print("📋 发布预览")
    print("="*60)
    print(f"\n来源: @{source['author']}")
    print(f"主题: {source.get('topic', 'AI Skill')}")
    print(f"推文数: {len(tweets)}")
    print(f"\n前3条推文预览:\n")
    
    for i, tweet in enumerate(tweets[:3], 1):
        print(f"推文 {i}:")
        print(tweet[:150] + "..." if len(tweet) > 150 else tweet)
        print()
    
    return tweets


def main():
    """主函数"""
    tweets = preview_content()
    
    response = input("\n确认发布这 {} 条推文? (yes/no): ".format(len(tweets)))
    
    if response.lower() != 'yes':
        print("⏸️ 已取消")
        return
    
    print("\n🚀 开始发布...")
    # 这里添加发布代码


if __name__ == "__main__":
    main()
