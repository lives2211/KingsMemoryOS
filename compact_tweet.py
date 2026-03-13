#!/usr/bin/env python3
"""
精简版推文生成器
- 280字符以内
- 包含核心信息
- 高质量内容
"""

import subprocess
from datetime import datetime


def generate_compact_tweet():
    """生成精简版推文"""
    
    tweet = """🔥 OpenClaw深度分析

中文KOL @AlchainHust分享的框架(2482👍614🔄)，实测有效。

核心：不是工具，是Agent操作系统

GitHub: github.com/openclaw/openclaw
⭐8900 stars | 4天Trending

✅150+预置Skills
✅可视化工作流
✅多Agent协作
✅企业级安全

Before: 开发2-6月，$10K-50K
After: 70分钟，$0

技术栈: Python/TS + Docker + REST API

使用:
pip install openclaw
openclaw config init
openclaw run ai-content-pipeline

3步搞定。

ROI: 立即回本

#OpenClaw #AI #OpenSource #GitHubTrending"""
    
    return tweet


def main():
    """主函数"""
    print("="*60)
    print("🚀 精简版推文生成并发布")
    print("="*60)
    
    tweet = generate_compact_tweet()
    
    print(f"\n📊 推文信息:")
    print(f"   字符数: {len(tweet)}")
    print(f"\n内容:")
    print(tweet)
    
    if len(tweet) > 280:
        print(f"\n⚠️ 警告: 超出280字符限制 ({len(tweet)} chars)")
        return
    
    print(f"\n⏳ 5秒后开始发布...")
    import time
    time.sleep(5)
    
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
            import json
            d = json.loads(result.stdout)
            if d.get('ok') and d.get('data', {}).get('url'):
                print(f"🔗 {d['data']['url']}")
        except:
            pass
    else:
        print(f"❌ 失败: {result.stderr[:100]}")
    
    print(f"\n{'='*60}")
    print("✅ 完成")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
