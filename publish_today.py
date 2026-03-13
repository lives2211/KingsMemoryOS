#!/usr/bin/env python3
"""
立即发布今日内容
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
    print(f"🐦 发布: {thread_name}")
    print(f"{'='*60}\n")
    
    prev_id = None
    for i, tweet in enumerate(tweets, 1):
        print(f"推文 {i}/{len(tweets)}:")
        print(tweet[:120] + "..." if len(tweet) > 120 else tweet)
        print()
        
        cmd = ['twitter', 'post', tweet]
        if prev_id:
            cmd.extend(['--reply-to', prev_id])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✅ 成功")
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
                return False
            
            if i < len(tweets):
                delay = random.randint(180, 360)
                print(f"⏳ 等待 {delay//60} 分钟...")
                time.sleep(delay)
                
        except Exception as e:
            print(f"❌ 错误: {e}")
            return False
    
    print(f"\n🎉 {thread_name} 发布完成！")
    return True


def main():
    """主函数"""
    print("="*60)
    print("🚀 今日内容发布系统")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # 加载内容
    content = load_today_content()
    
    print(f"\n📋 今日内容:")
    print(f"   主 Thread: Agency Agents ({len(content['primary_thread'])} 条)")
    print(f"   Skill Thread: App Store Screenshots ({len(content['skill_thread'])} 条)")
    
    # 确认
    response = input("\n确认发布? (y/n): ")
    if response.lower() != 'y':
        print("⏸️ 已取消")
        return
    
    # 发布主 Thread
    print("\n" + "="*60)
    print("📌 阶段 1: 发布主 Thread (Agency Agents)")
    print("="*60)
    
    if post_thread(content['primary_thread'], "Agency Agents"):
        print("\n✅ 主 Thread 发布成功")
    else:
        print("\n❌ 主 Thread 发布失败")
        return
    
    # 等待 2-3 小时后发布 Skill Thread
    wait_minutes = 120 + random.randint(0, 60)
    print(f"\n⏳ 等待 {wait_minutes} 分钟后发布 Skill Thread...")
    print(f"   预计时间: {datetime.now().strftime('%H:%M')} + {wait_minutes//60}小时{wait_minutes%60}分钟")
    
    # 实际等待或后台继续
    print(f"\n💡 提示: 实际运行时会等待 {wait_minutes} 分钟")
    print("   现在立即继续发布 Skill Thread?")
    
    response2 = input("\n立即发布 Skill Thread? (y/n): ")
    if response2.lower() == 'y':
        print("\n" + "="*60)
        print("📌 阶段 2: 发布 Skill Thread (App Store Screenshots)")
        print("="*60)
        
        if post_thread(content['skill_thread'], "App Store Screenshots"):
            print("\n✅ Skill Thread 发布成功")
        else:
            print("\n❌ Skill Thread 发布失败")
    else:
        print("\n⏸️ Skill Thread 稍后手动发布")
        print("   命令: python3 publish_today.py (修改后)")
    
    print("\n" + "="*60)
    print("✅ 今日发布任务完成")
    print("="*60)


if __name__ == "__main__":
    main()
