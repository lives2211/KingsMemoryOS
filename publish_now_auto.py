#!/usr/bin/env python3
"""
自动发布今日内容（无需确认）
"""

import json
import subprocess
import time
import random
from datetime import datetime


def load_today_content():
    """加载今日内容"""
    with open('today_content_20260312.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def post_thread(tweets, thread_name):
    """发布 Thread"""
    print(f"\n{'='*60}")
    print(f"🐦 发布: {thread_name} ({len(tweets)} 条推文)")
    print(f"{'='*60}\n")
    
    prev_id = None
    success_count = 0
    
    for i, tweet in enumerate(tweets, 1):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 推文 {i}/{len(tweets)}")
        print(f"内容: {tweet[:80]}...")
        
        cmd = ['twitter', 'post', tweet]
        if prev_id:
            cmd.extend(['--reply-to', prev_id])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✅ 成功")
                success_count += 1
                try:
                    data = json.loads(result.stdout)
                    if data.get('ok'):
                        prev_id = data['data'].get('id')
                        url = data['data'].get('url', '')
                        if url:
                            print(f"🔗 {url}")
                except:
                    pass
            else:
                print(f"❌ 失败: {result.stderr[:100]}")
                continue
            
            if i < len(tweets):
                delay = random.randint(180, 360)
                print(f"⏳ 等待 {delay//60} 分钟...\n")
                time.sleep(delay)
                
        except Exception as e:
            print(f"❌ 错误: {e}")
            continue
    
    print(f"\n🎉 {thread_name} 完成: {success_count}/{len(tweets)} 条成功")
    return success_count == len(tweets)


def main():
    """主函数"""
    print("="*60)
    print("🚀 自动发布系统")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # 加载内容
    content = load_today_content()
    
    print(f"\n📋 今日内容:")
    print(f"   主 Thread: Agency Agents ({len(content['primary_thread'])} 条)")
    print(f"   Skill Thread: App Store Screenshots ({len(content['skill_thread'])} 条)")
    print(f"\n⏳ 10秒后开始自动发布...")
    time.sleep(10)
    
    # 发布主 Thread
    print("\n" + "="*60)
    print("📌 阶段 1: Agency Agents (GitHub Trending)")
    print("="*60)
    
    if post_thread(content['primary_thread'], "Agency Agents"):
        print("\n✅ 主 Thread 完成")
    else:
        print("\n⚠️ 主 Thread 部分失败")
    
    # 等待后发布 Skill Thread
    wait_minutes = 5  # 测试用5分钟，实际用120-180
    print(f"\n⏳ 等待 {wait_minutes} 分钟后发布 Skill Thread...")
    time.sleep(wait_minutes * 60)
    
    print("\n" + "="*60)
    print("📌 阶段 2: App Store Screenshots (OpenClaw Skill)")
    print("="*60)
    
    if post_thread(content['skill_thread'], "App Store Screenshots"):
        print("\n✅ Skill Thread 完成")
    else:
        print("\n⚠️ Skill Thread 部分失败")
    
    print("\n" + "="*60)
    print("✅ 今日发布任务全部完成")
    print(f"⏰ {datetime.now().strftime('%H:%M')}")
    print("="*60)


if __name__ == "__main__":
    main()
