#!/usr/bin/env python3
"""
发布单条优质长推文
"""

import json
import subprocess
from datetime import datetime


def load_tweet():
    """加载推文"""
    with open('single_premium_20260312_204136.json', 'r') as f:
        return json.load(f)


def main():
    """主函数"""
    print("="*60)
    print("🚀 发布单条优质长推文")
    print("="*60)
    
    # 加载
    data = load_tweet()
    tweet = data['tweet']
    
    print(f"\n📊 推文信息:")
    print(f"   字符数: {data['char_count']}")
    print(f"   单词数: {data['word_count']}")
    print(f"\n预览:")
    print(tweet[:200] + "...")
    
    print(f"\n⏳ 5秒后开始发布...")
    import time
    time.sleep(5)
    
    # 发布
    print(f"\n📤 发布中...")
    result = subprocess.run(
        ['twitter', 'post', tweet],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        print("✅ 发布成功！")
        try:
            d = json.loads(result.stdout)
            if d.get('ok') and d.get('data', {}).get('url'):
                print(f"🔗 {d['data']['url']}")
        except:
            pass
    else:
        print(f"❌ 发布失败: {result.stderr[:100]}")
    
    print(f"\n{'='*60}")
    print("✅ 完成")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
