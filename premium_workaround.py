#!/usr/bin/env python3
"""
Premium 发布解决方案
- 检测 Twitter 限制
- 自动调整推文长度
- 分段发布长内容
"""

import json
import subprocess
from datetime import datetime


def check_twitter_limit():
    """检查 Twitter 限制"""
    # 测试不同长度
    test_lengths = [280, 500, 1000, 2000, 4000]
    
    print("🔍 检测 Twitter 字符限制...")
    
    for length in test_lengths:
        test_text = "A" * length
        try:
            result = subprocess.run(
                ['twitter', 'post', test_text],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ {length} 字符: 成功")
                return length
            else:
                error = result.stderr
                if "shorter" in error.lower() or "186" in error:
                    print(f"❌ {length} 字符: 超出限制")
                    break
                else:
                    print(f"⚠️ {length} 字符: 其他错误")
                    
        except Exception as e:
            print(f"❌ 错误: {e}")
            break
    
    return 280  # 默认限制


def split_for_standard(tweets, max_length=280):
    """为标准账户分割推文"""
    split_tweets = []
    
    for tweet in tweets:
        if len(tweet) <= max_length - 20:
            split_tweets.append(tweet)
        else:
            # 智能分割
            paragraphs = tweet.split('\n\n')
            current = ""
            
            for para in paragraphs:
                if len(current) + len(para) + 2 > max_length - 20:
                    if current:
                        split_tweets.append(current.strip())
                    current = para
                else:
                    current = current + '\n\n' + para if current else para
            
            if current:
                split_tweets.append(current.strip())
    
    return split_tweets


def main():
    """主函数"""
    print("="*60)
    print("🛠️ Premium 发布解决方案")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # 检测限制
    limit = check_twitter_limit()
    print(f"\n📊 检测到的限制: {limit} 字符")
    
    if limit < 4000:
        print("⚠️ 检测到标准账户限制 (280字符)")
        print("   将自动分割内容为多条推文")
        
        # 加载内容
        with open('deep_analysis_20260312_142625.json', 'r') as f:
            data = json.load(f)
        
        original_count = len(data['tweets'])
        split_tweets = split_for_standard(data['tweets'], limit)
        
        print(f"\n📋 分割结果:")
        print(f"   原始: {original_count} 条长推文")
        print(f"   分割后: {len(split_tweets)} 条标准推文")
        
        # 保存
        data['tweets_standard'] = split_tweets
        data['limit_detected'] = limit
        
        with open('deep_analysis_20260312_142625.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存分割后的内容")
        print(f"   使用 tweets_standard 进行发布")
    else:
        print("✅ Premium 账户 detected (4000字符)")
        print("   可以使用原始长推文")


if __name__ == "__main__":
    main()
