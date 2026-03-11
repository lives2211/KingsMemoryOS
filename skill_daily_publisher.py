#!/usr/bin/env python3
"""
AI Skill 每日自动发布系统
每天自动选择优质 Skill，生成专家级分析，发布到 Twitter
"""

import json
import random
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import time


class SkillDailyPublisher:
    """Skill 每日发布器"""
    
    def __init__(self):
        self.skills_dir = Path.home() / ".openclaw" / "skills"
        self.history_file = Path("published_skills.json")
        self.published_skills = self._load_history()
    
    def _load_history(self) -> List[str]:
        """加载已发布的 Skill 历史"""
        if self.history_file.exists():
            with open(self.history_file) as f:
                data = json.load(f)
                return data.get('skills', [])
        return []
    
    def _save_history(self):
        """保存发布历史"""
        data = {
            'skills': self.published_skills,
            'last_update': datetime.now().isoformat()
        }
        with open(self.history_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_all_skills(self) -> List[str]:
        """获取所有 Skill 名称"""
        skills = []
        if self.skills_dir.exists():
            for item in self.skills_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    skills.append(item.name)
        return skills
    
    def select_today_skill(self) -> str:
        """选择今日的 Skill"""
        all_skills = self.get_all_skills()
        
        # 排除已发布的
        available = [s for s in all_skills if s not in self.published_skills]
        
        # 如果都发布过了，重置历史
        if not available:
            print("🔄 所有 Skill 都已发布过，重置历史记录")
            self.published_skills = []
            available = all_skills
        
        # 优先选择高质量的 Skill
        priority_skills = [
            'ai-image-generation', 'ai-video-generation', 'ai-content-pipeline',
            'ai-rag-pipeline', 'ai-automation-workflows', 'ai-voice-cloning',
            'agentic-browser', 'autonomous-agents', 'ai-news-aggregator',
            'ai-podcast-creation', 'ai-avatar-video', 'ai-marketing-videos',
            'ai-music-generation', 'ai-product-photography', 'ai-social-media-content'
        ]
        
        # 从优先列表中选择未发布的
        priority_available = [s for s in priority_skills if s in available]
        
        if priority_available:
            selected = random.choice(priority_available)
        else:
            selected = random.choice(available)
        
        return selected
    
    def analyze_skill(self, skill_name: str) -> Dict:
        """分析 Skill"""
        # 运行专家分析
        cmd = ['python3', 'skill_expert_analysis.py', skill_name]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # 解析输出
            if result.returncode == 0:
                # 从输出中提取 Twitter Thread
                lines = result.stdout.split('\n')
                tweets = []
                current_tweet = []
                in_tweet = False
                
                for line in lines:
                    if line.startswith('推文 '):
                        if current_tweet:
                            tweets.append('\n'.join(current_tweet))
                            current_tweet = []
                        in_tweet = True
                    elif line.startswith('---') or line.startswith('==='):
                        if current_tweet:
                            tweets.append('\n'.join(current_tweet))
                            current_tweet = []
                        in_tweet = False
                    elif in_tweet and line.strip():
                        current_tweet.append(line)
                
                if current_tweet:
                    tweets.append('\n'.join(current_tweet))
                
                return {
                    'name': skill_name,
                    'tweets': tweets,
                    'success': True
                }
            else:
                return {
                    'name': skill_name,
                    'tweets': [],
                    'success': False,
                    'error': result.stderr
                }
                
        except Exception as e:
            return {
                'name': skill_name,
                'tweets': [],
                'success': False,
                'error': str(e)
            }
    
    def post_to_twitter(self, tweets: List[str]) -> bool:
        """发布到 Twitter"""
        if not tweets:
            print("❌ 没有推文可发布")
            return False
        
        print(f"\n🐦 准备发布 Twitter Thread ({len(tweets)} 条推文)\n")
        
        prev_id = None
        for i, tweet in enumerate(tweets, 1):
            print(f"\n{'='*60}")
            print(f"推文 {i}/{len(tweets)}:")
            print(f"{'-'*60}")
            print(tweet)
            print(f"{'='*60}")
            
            # 构建命令
            cmd = ['twitter', 'post', tweet]
            if prev_id:
                cmd.extend(['--reply-to', prev_id])
            
            # 执行发布
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print(f"✅ 推文 {i} 发布成功")
                    # 解析返回的推文 ID
                    try:
                        data = json.loads(result.stdout)
                        if data.get('ok'):
                            prev_id = data.get('data', {}).get('id')
                    except:
                        pass
                else:
                    print(f"❌ 推文 {i} 发布失败: {result.stderr}")
                    return False
                
                # 等待避免频率限制
                if i < len(tweets):
                    print("⏳ 等待 5 秒...")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"❌ 发布错误: {e}")
                return False
        
        print(f"\n🎉 Twitter Thread 发布完成！共 {len(tweets)} 条")
        return True
    
    def run_daily(self, dry_run: bool = False):
        """运行每日发布"""
        print("🚀 AI Skill 每日发布系统")
        print("="*60)
        print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"📚 已发布: {len(self.published_skills)} 个 Skill")
        print("="*60)
        
        # 选择今日 Skill
        print("\n🎯 选择今日 Skill...")
        skill_name = self.select_today_skill()
        print(f"✅ 今日精选: {skill_name}")
        
        # 分析 Skill
        print(f"\n🔍 深度分析 {skill_name}...")
        analysis = self.analyze_skill(skill_name)
        
        if not analysis['success']:
            print(f"❌ 分析失败: {analysis.get('error', '未知错误')}")
            return
        
        tweets = analysis['tweets']
        if not tweets:
            print("❌ 未生成推文")
            return
        
        print(f"✅ 生成 {len(tweets)} 条推文")
        
        # 显示预览
        print(f"\n{'='*60}")
        print("📱 Twitter Thread 预览:")
        print(f"{'='*60}\n")
        
        for i, tweet in enumerate(tweets, 1):
            print(f"推文 {i}:")
            print("-"*40)
            print(tweet[:200] + "..." if len(tweet) > 200 else tweet)
            print()
        
        # 保存草稿
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        draft_file = f"skill_thread_{skill_name}_{timestamp}.txt"
        
        with open(draft_file, 'w', encoding='utf-8') as f:
            f.write(f"Skill: {skill_name}\n")
            f.write(f"时间: {datetime.now().isoformat()}\n")
            f.write(f"推文数: {len(tweets)}\n")
            f.write("="*60 + "\n\n")
            for i, tweet in enumerate(tweets, 1):
                f.write(f"推文 {i}:\n")
                f.write("-"*60 + "\n")
                f.write(tweet + "\n\n")
        
        print(f"💾 草稿已保存: {draft_file}")
        
        # 发布或预览
        if dry_run:
            print("\n🔍 预览模式，未实际发布")
            print("运行时不加 --dry-run 参数将实际发布")
        else:
            print("\n📤 准备发布到 Twitter...")
            response = input("确认发布? (y/n): ")
            
            if response.lower() == 'y':
                if self.post_to_twitter(tweets):
                    # 记录已发布
                    self.published_skills.append(skill_name)
                    self._save_history()
                    print(f"\n✅ {skill_name} 已添加到发布历史")
                else:
                    print("\n❌ 发布失败，未记录到历史")
            else:
                print("\n⏸️ 已取消发布")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Skill 每日自动发布')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际发布')
    parser.add_argument('--list', action='store_true', help='列出所有 Skill')
    parser.add_argument('--history', action='store_true', help='查看发布历史')
    
    args = parser.parse_args()
    
    publisher = SkillDailyPublisher()
    
    if args.list:
        skills = publisher.get_all_skills()
        print(f"📚 发现 {len(skills)} 个 Skill:\n")
        for i, skill in enumerate(sorted(skills), 1):
            status = "✅" if skill in publisher.published_skills else "⬜"
            print(f"{i}. {status} {skill}")
    
    elif args.history:
        print(f"📜 发布历史 ({len(publisher.published_skills)} 个):\n")
        for i, skill in enumerate(publisher.published_skills, 1):
            print(f"{i}. {skill}")
    
    else:
        publisher.run_daily(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
