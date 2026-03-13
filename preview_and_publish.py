#!/usr/bin/env python3
"""
预览并发布
- 显示完整预览
- 10秒确认时间
- 自动发布
"""

import json
import subprocess
import time
import random
from datetime import datetime


def main():
    """主函数"""
    # 加载内容
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
    print(f"\n推文列表:\n")
    
    for i, tweet in enumerate(tweets[:5], 1):
        preview = tweet[:100] + "..." if len(tweet) > 100 else tweet
        print(f"{i}. {preview}")
    
    if len(tweets) > 5:
        print(f"... 还有 {len(tweets)-5} 条")
    
    print(f"\n⏳ 10秒后开始自动发布...")
    print("按 Ctrl+C 取消")
    
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print("\n⏸️ 已取消")
        return
    
    # 开始发布
    print("\n" + "="*60)
    print("🚀 开始发布")
    print("="*60)
    
    prev_id = None
    success = 0
    
    for i, tweet in enumerate(tweets, 1):
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {i}/{len(tweets)}")
        
        cmd = ['twitter', 'post', tweet]
        if prev_id:
            cmd.extend(['--reply-to', prev_id])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ 成功")
                success += 1
                try:
                    d = json.loads(result.stdout)
                    if d.get('ok'):
                        prev_id = d['data'].get('id')
                        if d['data'].get('url'):
                            print(f"🔗 {d['data']['url']}")
                except:
                    pass
            else:
                print(f"❌ 失败")
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        if i < len(tweets):
            delay = random.randint(180, 300)
            print(f"⏳ 等待 {delay//60} 分钟...")
            time.sleep(delay)
    
    print(f"\n{'='*60}")
    print(f"✅ 完成: {success}/{len(tweets)} 条成功")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
