#!/usr/bin/env python3
"""
最终自动发布
- 无确认
- 直接发布
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
    print("🚀 自动发布系统")
    print("="*60)
    print(f"\n来源: @{source['author']}")
    print(f"主题: {source.get('topic', 'AI Skill')}")
    print(f"推文数: {len(tweets)}")
    print(f"\n⏳ 5秒后开始...")
    time.sleep(5)
    
    # 开始发布
    print("\n" + "="*60)
    print("📤 发布中...")
    print("="*60)
    
    prev_id = None
    success = 0
    
    for i, tweet in enumerate(tweets, 1):
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {i}/{len(tweets)} ({len(tweet)}字符)")
        
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
                error = result.stderr[:80] if result.stderr else "失败"
                print(f"❌ {error}")
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
