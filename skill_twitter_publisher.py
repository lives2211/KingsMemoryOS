#!/usr/bin/env python3
"""
Skill Twitter 发布器 - 简化版
直接使用专家分析生成推文并发布
"""

import json
import random
import subprocess
from datetime import datetime
from pathlib import Path
import time
import sys

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from skill_expert_analysis import SkillExpertAnalyzer


class SkillTwitterPublisher:
    """Skill Twitter 发布器"""
    
    def __init__(self):
        self.analyzer = SkillExpertAnalyzer()
        self.history_file = Path("published_skills.json")
        self.published_skills = self._load_history()
    
    def _load_history(self) -> list:
        """加载历史"""
        if self.history_file.exists():
            with open(self.history_file) as f:
                data = json.load(f)
                return data.get('skills', [])
        return []
    
    def _save_history(self):
        """保存历史"""
        data = {
            'skills': self.published_skills,
            'last_update': datetime.now().isoformat()
        }
        with open(self.history_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def select_skill(self) -> str:
        """选择 Skill"""
        all_skills = []
        skills_dir = Path.home() / ".openclaw" / "skills"
        
        if skills_dir.exists():
            for item in skills_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    all_skills.append(item.name)
        
        # 排除已发布的
        available = [s for s in all_skills if s not in self.published_skills]
        
        if not available:
            print("🔄 重置历史记录")
            self.published_skills = []
            available = all_skills
        
        # 优先列表
        priority = [
            'ai-image-generation', 'ai-video-generation', 'ai-content-pipeline',
            'ai-rag-pipeline', 'ai-automation-workflows', 'ai-voice-cloning',
            'agentic-browser', 'autonomous-agents', 'ai-news-aggregator',
            'ai-podcast-creation', 'ai-avatar-video', 'ai-marketing-videos'
        ]
        
        priority_available = [s for s in priority if s in available]
        
        if priority_available:
            return random.choice(priority_available)
        
        return random.choice(available)
    
    def generate_tweets(self, skill_name: str) -> list:
        """生成推文"""
        analysis = self.analyzer.analyze_skill_deep(skill_name)
        
        if not analysis:
            return []
        
        return analysis.get('twitter_thread_expert', [])
    
    def post_thread(self, tweets: list) -> bool:
        """发布推文串"""
        if not tweets:
            print("❌ 没有推文")
            return False
        
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
                            prev_id = data.get('data', {}).get('id')
                    except:
                        pass
                else:
                    print(f"❌ 失败: {result.stderr}")
                    return False
                
                if i < len(tweets):
                    time.sleep(5)
                    
            except Exception as e:
                print(f"❌ 错误: {e}")
                return False
        
        print(f"✅ 发布完成！")
        return True
    
    def run(self, dry_run: bool = False):
        """运行"""
        print("🚀 Skill Twitter 发布系统")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*60)
        
        # 选择 Skill
        skill = self.select_skill()
        print(f"\n🎯 今日 Skill: {skill}")
        
        # 生成推文
        print("\n📝 生成推文...")
        tweets = self.generate_tweets(skill)
        
        if not tweets:
            print("❌ 生成失败")
            return
        
        print(f"✅ 生成 {len(tweets)} 条推文")
        
        # 显示预览
        print(f"\n{'='*60}")
        print("预览:")
        print(f"{'='*60}\n")
        
        for i, tweet in enumerate(tweets, 1):
            print(f"推文 {i}:")
            print(tweet[:150] + "..." if len(tweet) > 150 else tweet)
            print()
        
        # 保存草稿
        draft_file = f"skill_tweets_{skill}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(draft_file, 'w', encoding='utf-8') as f:
            for i, tweet in enumerate(tweets, 1):
                f.write(f"推文 {i}:\n{tweet}\n\n")
        print(f"💾 草稿: {draft_file}")
        
        # 发布
        if dry_run:
            print("\n🔍 预览模式，未发布")
            return
        
        print("\n📤 准备发布...")
        response = input("确认发布? (y/n): ")
        
        if response.lower() == 'y':
            if self.post_thread(tweets):
                self.published_skills.append(skill)
                self._save_history()
                print(f"\n✅ {skill} 已记录")
            else:
                print("\n❌ 发布失败")
        else:
            print("\n⏸️ 已取消")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    
    publisher = SkillTwitterPublisher()
    publisher.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
