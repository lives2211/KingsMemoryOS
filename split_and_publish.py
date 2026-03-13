#!/usr/bin/env python3
"""
分割长推文并发布
"""

import json
import subprocess
import time
from datetime import datetime


def split_tweet(long_tweet, max_length=280):
    """分割长推文"""
    # 按段落分割
    sections = long_tweet.split('\n\n')
    tweets = []
    current = ""
    
    for section in sections:
        if len(current) + len(section) + 2 > max_length - 20:
            if current:
                tweets.append(current.strip())
            current = section
        else:
            current = current + '\n\n' + section if current else section
    
    if current:
        tweets.append(current.strip())
    
    return tweets


def main():
    """主函数"""
    print("="*60)
    print("🚀 分割并发布")
    print("="*60)
    
    # 加载
    with open('single_premium_20260312_204136.json', 'r') as f:
        data = json.load(f)
    
    long_tweet = data['tweet']
    
    print(f"\n📊 原始推文:")
    print(f"   字符数: {len(long_tweet)}")
    
    # 分割
    tweets = split_tweet(long_tweet, max_length=280)
    print(f"   分割为: {len(tweets)} 条")
    
    # 预览
    print(f"\n预览:")
    for i, t in enumerate(tweets[:3], 1):
        print(f"\nTweet {i} ({len(t)} chars):")
        print(t[:100] + "...")
    
    print(f"\n⏳ 5秒后开始发布...")
    time.sleep(5)
    
    # 发布
    print(f"\n{'='*60}")
    print("📤 发布中...")
    print(f"{'='*60}\n")
    
    prev_id = None
    success = 0
    
    for i, tweet in enumerate(tweets, 1):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Tweet {i}/{len(tweets)} ({len(tweet)} chars)")
        
        cmd = ['twitter', 'post', tweet]
        if prev_id:
            cmd.extend(['--reply-to', prev_id])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("   ✅ 成功")
            success += 1
            try:
                d = json.loads(result.stdout)
                if d.get('ok'):
                    prev_id = d['data'].get('id')
                    if d['data'].get('url'):
                        print(f"   🔗 {d['data']['url']}")
            except:
                pass
        else:
            print(f"   ❌ 失败")
        
        if i < len(tweets):
            time.sleep(3)
    
    print(f"\n{'='*60}")
    print(f"✅ 完成: {success}/{len(tweets)} 条成功")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
