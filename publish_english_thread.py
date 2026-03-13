#!/usr/bin/env python3
"""
发布优质英文推文
- 16条完整Thread
- 包含GitHub链接
- 深度Skill分析
"""

import json
import subprocess
import time
import random
from datetime import datetime


def load_english_thread():
    """加载英文推文"""
    with open('deep_english_ai-content-pipeline_20260312.json', 'r') as f:
        return json.load(f)


def post_thread(tweets, analysis):
    """发布Thread"""
    print(f"\n{'='*60}")
    print(f"🚀 发布优质英文推文")
    print(f"   Skill: {analysis['display_name']}")
    print(f"   GitHub: {analysis['github_url']}")
    print(f"   推文数: {len(tweets)}")
    print(f"{'='*60}\n")
    
    prev_id = None
    success = 0
    
    for i, tweet in enumerate(tweets, 1):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Tweet {i}/{len(tweets)} ({len(tweet)} chars)")
        
        cmd = ['twitter', 'post', tweet]
        if prev_id:
            cmd.extend(['--reply-to', prev_id])
        
        try:
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
                error = result.stderr[:80] if result.stderr else "失败"
                print(f"   ❌ {error}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
        
        if i < len(tweets):
            delay = random.randint(180, 300)
            print(f"   ⏳ 等待 {delay//60} 分钟...\n")
            time.sleep(delay)
    
    print(f"\n{'='*60}")
    print(f"✅ 完成: {success}/{len(tweets)} 条成功")
    print(f"{'='*60}")


def main():
    """主函数"""
    print("="*60)
    print("🚀 优质英文推文自动发布")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # 加载内容
    data = load_english_thread()
    tweets = data['tweets']
    analysis = data['analysis']
    
    print(f"\n📋 内容:")
    print(f"   Skill: {analysis['display_name']}")
    print(f"   分类: {analysis['category']}")
    print(f"   ⭐: {analysis['stars']}")
    print(f"   👥: {analysis['users']}")
    print(f"   质量: {analysis['quality_score']}/100")
    print(f"   推文: {len(tweets)} 条")
    
    print(f"\n⏳ 10秒后开始...")
    time.sleep(10)
    
    # 发布
    post_thread(tweets, analysis)


if __name__ == "__main__":
    main()
