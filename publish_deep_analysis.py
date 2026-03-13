#!/usr/bin/env python3
"""
深度分析自动发布系统
- 20 条长推文
- Premium 会员特性
- 自动发布
"""

import json
import subprocess
import time
import random
from datetime import datetime
import glob


def load_deep_analysis():
    """加载深度分析内容"""
    files = sorted(glob.glob('deep_analysis_*.json'), reverse=True)
    if not files:
        print("❌ 未找到深度分析文件")
        return None
    
    with open(files[0], 'r', encoding='utf-8') as f:
        return json.load(f)


def post_long_thread(tweets, source_info):
    """发布长 Thread"""
    print(f"\n{'='*60}")
    print(f"🐦 Premium 深度分析发布")
    print(f"   来源: @{source_info.get('author', 'KOL')}")
    print(f"   主题: {source_info.get('topic', 'AI Skill')}")
    print(f"   推文: {len(tweets)} 条长推文")
    print(f"   单词: {source_info.get('word_count', 1956)}")
    print(f"{'='*60}\n")
    
    prev_id = None
    success_count = 0
    failed_tweets = []
    
    for i, tweet in enumerate(tweets, 1):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] 推文 {i}/{len(tweets)} ({len(tweet)} 字符)")
        
        # 显示预览
        preview = tweet[:120] + "..." if len(tweet) > 120 else tweet
        print(f"   {preview}")
        
        cmd = ['twitter', 'post', tweet]
        if prev_id:
            cmd.extend(['--reply-to', prev_id])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"   ✅ 成功")
                success_count += 1
                try:
                    data = json.loads(result.stdout)
                    if data.get('ok'):
                        prev_id = data['data'].get('id')
                        url = data['data'].get('url', '')
                        if url:
                            print(f"   🔗 {url}")
                except:
                    pass
            else:
                error = result.stderr[:80] if result.stderr else "未知错误"
                print(f"   ❌ 失败: {error}")
                failed_tweets.append({'index': i, 'content': tweet})
                # 继续下一条
                
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            failed_tweets.append({'index': i, 'content': tweet})
        
        # 间隔 (Premium 可以更长)
        if i < len(tweets):
            delay = random.randint(300, 600)  # 5-10分钟
            print(f"   ⏳ 等待 {delay//60} 分钟...\n")
            time.sleep(delay)
    
    # 总结
    print(f"\n{'='*60}")
    print(f"✅ 发布完成: {success_count}/{len(tweets)} 条成功")
    if failed_tweets:
        print(f"⚠️ 失败: {len(failed_tweets)} 条")
    print(f"{'='*60}")
    
    return success_count, failed_tweets


def main():
    """主函数"""
    print("="*60)
    print("🚀 Premium 深度分析自动发布")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # 加载内容
    content = load_deep_analysis()
    if not content:
        return
    
    tweets = content['tweets']
    source = content['source']
    stats = content['stats']
    
    print(f"\n📋 内容信息:")
    print(f"   来源: @{source['author']}")
    print(f"   主题: {source.get('topic', 'AI Skill')}")
    print(f"   推文: {stats['tweet_count']} 条")
    print(f"   单词: {stats['word_count']}")
    print(f"   字符: {stats['char_count']}")
    print(f"   阅读: {stats['read_time']} 分钟")
    
    print(f"\n⏳ 10秒后开始自动发布...")
    time.sleep(10)
    
    # 发布
    success, failed = post_long_thread(tweets, {**source, **stats})
    
    # 重试失败的
    if failed:
        print(f"\n🔄 重试失败的 {len(failed)} 条推文...")
        for item in failed:
            print(f"\n重试推文 {item['index']}:")
            cmd = ['twitter', 'post', item['content']]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print("✅ 重试成功")
                else:
                    print(f"❌ 重试失败")
            except Exception as e:
                print(f"❌ 错误: {e}")
            time.sleep(60)
    
    print(f"\n{'='*60}")
    print("✅ Premium 深度分析发布完成")
    print(f"⏰ {datetime.now().strftime('%H:%M')}")
    print(f"📊 总计: {success}/{len(tweets)} 条成功")
    print("="*60)


if __name__ == "__main__":
    main()
