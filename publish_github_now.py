#!/usr/bin/env python3
"""
立即发布 - 带 GitHub 链接的中文区 Skill
"""

import sys
sys.path.insert(0, '/home/fengxueda/.openclaw/workspace')

from china_skill_github import ChinaSkillGitHub
import subprocess
import json
import time
import random


class GitHubPublisher:
    """GitHub 发布器"""
    
    def __init__(self):
        self.exporter = ChinaSkillGitHub()
    
    def post_thread(self, tweets):
        """发布 Thread"""
        print(f"\n🐦 发布 {len(tweets)} 条推文\n")
        
        prev_id = None
        for i, tweet in enumerate(tweets, 1):
            print(f"推文 {i}/{len(tweets)}:")
            print(tweet[:100] + "..." if len(tweet) > 100 else tweet)
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
        
        print(f"\n🎉 发布完成！")
        return True
    
    def run(self):
        """运行"""
        print("="*60)
        print("🇨🇳 China Skill → GitHub → Twitter")
        print("="*60)
        
        # 选择并生成
        skill = self.exporter.select_skill()
        data = self.exporter.skills_data[skill]
        
        print(f"\n🎯 选择: {skill}")
        print(f"   ⭐ Stars: {data['stars']}")
        print(f"   👥 Users: {data['users']}")
        print(f"   🔗 GitHub: {data['github']}")
        
        tweets = self.exporter.generate_github_thread(skill)
        print(f"\n✅ 生成 {len(tweets)} 条推文")
        
        # 确认
        response = input("\n确认发布? (y/n): ")
        if response.lower() != 'y':
            print("⏸️ 已取消")
            return
        
        # 发布
        if self.post_thread(tweets):
            print(f"\n✅ {skill} 发布成功！")
        else:
            print(f"\n❌ 发布失败")


if __name__ == "__main__":
    publisher = GitHubPublisher()
    publisher.run()
