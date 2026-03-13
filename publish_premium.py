#!/usr/bin/env python3
"""
Premium 内容自动发布系统
- 长推文（4000字符）
- 深度分析
- 自动发布
"""

import json
import subprocess
import time
import random
from datetime import datetime


def load_premium_content():
    """加载 Premium 内容"""
    # 找到最新的 premium 内容文件
    import glob
    files = sorted(glob.glob('premium_content_*.json'), reverse=True)
    if not files:
        print("❌ 未找到 Premium 内容文件")
        return None
    
    with open(files[0], 'r', encoding='utf-8') as f:
        return json.load(f)


def post_premium_thread(tweets, source_info):
    """发布 Premium Thread"""
    print(f"\n{'='*60}")
    print(f"🐦 Premium Thread 发布")
    print(f"   来源: {source_info['author']}")
    print(f"   主题: {source_info['topic']}")
    print(f"   推文数: {len(tweets)} 条")
    print(f"{'='*60}\n")
    
    prev_id = None
    success_count = 0
    
    for i, tweet in enumerate(tweets, 1):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 推文 {i}/{len(tweets)}")
        print(f"   长度: {len(tweet)} 字符")
        print(f"   预览: {tweet[:100]}...")
        
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
                error = result.stderr[:100] if result.stderr else "未知错误"
                print(f"   ❌ 失败: {error}")
                # 继续下一条
                continue
            
            if i < len(tweets):
                # Premium 用户间隔可以更长
                delay = random.randint(300, 600)  # 5-10分钟
                print(f"   ⏳ 等待 {delay//60} 分钟...\n")
                time.sleep(delay)
                
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            continue
    
    print(f"\n{'='*60}")
    print(f"✅ 发布完成: {success_count}/{len(tweets)} 条成功")
    print(f"{'='*60}")
    return success_count == len(tweets)


def main():
    """主函数"""
    print("="*60)
    print("🚀 Premium 内容自动发布系统")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # 加载内容
    content = load_premium_content()
    if not content:
        return
    
    tweets = content['tweets']
    source = content['source']
    
    print(f"\n📋 内容信息:")
    print(f"   来源: {source['author']}")
    print(f"   主题: {source['topic']}")
    print(f"   推文数: {len(tweets)} 条")
    print(f"   总字符: {content['total_chars']}")
    print(f"   生成时间: {content['generated_at']}")
    
    print(f"\n⏳ 10秒后开始自动发布...")
    time.sleep(10)
    
    # 发布
    if post_premium_thread(tweets, source):
        print("\n🎉 Premium Thread 发布成功！")
    else:
        print("\n⚠️ 部分推文发布失败")
    
    print(f"\n{'='*60}")
    print("✅ 任务完成")
    print(f"⏰ {datetime.now().strftime('%H:%M')}")
    print("="*60)


if __name__ == "__main__":
    main()
