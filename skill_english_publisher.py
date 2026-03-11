#!/usr/bin/env python3
"""
英文版 Skill 发布系统 - 专为涨粉优化
"""

import json
import random
import subprocess
from datetime import datetime
from pathlib import Path
import time


class EnglishSkillPublisher:
    """英文 Skill 发布器"""
    
    def __init__(self):
        self.skills_dir = Path.home() / ".openclaw" / "skills"
        self.history_file = Path("english_published_skills.json")
        self.published_skills = self._load_history()
        self.log_file = Path("english_publish.log")
    
    def _load_history(self):
        if self.history_file.exists():
            with open(self.history_file) as f:
                return json.load(f).get('skills', [])
        return []
    
    def _save_history(self):
        data = {
            'skills': self.published_skills,
            'last_update': datetime.now().isoformat()
        }
        with open(self.history_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] {message}\n"
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
        print(log_line, end='')
    
    def select_skill(self):
        """选择 Skill"""
        all_skills = [d.name for d in self.skills_dir.iterdir() 
                     if d.is_dir() and not d.name.startswith('.')]
        
        available = [s for s in all_skills if s not in self.published_skills]
        
        if not available:
            self.published_skills = []
            available = all_skills
        
        # 优先 AI 相关
        priority = ['ai-image-generation', 'ai-video-generation', 'ai-content-pipeline',
                   'ai-automation-workflows', 'ai-voice-cloning', 'ai-marketing-videos']
        priority_available = [s for s in priority if s in available]
        
        return random.choice(priority_available) if priority_available else random.choice(available)
    
    def generate_thread(self, skill_name: str) -> list:
        """生成英文 Thread（涨粉优化版）"""
        
        display_name = skill_name.replace('-', ' ').title()
        
        # 高吸引力钩子
        hooks = [
            f"I spent 30 days testing {display_name}.\n\nHere are the results (they're wild): 🧵",
            f"Stop doing {display_name} manually.\n\nThis automation stack saves me 2 hours daily:",
            f"Nobody is talking about this {display_name} workflow yet.\n\nBut it changed everything for me:",
            f"The {display_name} setup that 10x'd my productivity:\n\n(Thread) 👇",
        ]
        
        hook = random.choice(hooks)
        
        return [
            # 推文 1: 强钩子
            hook,
            
            # 推文 2: 痛点共鸣
            f"Here's the problem:\n\n"
            f"Most people waste 2+ hours daily on repetitive {display_name} tasks.\n\n"
            f"They're either:\n"
            f"• Doing it manually (slow)\n"
            f"• Using wrong tools (frustrating)\n"
            f"• Not automating at all (expensive)",
            
            # 推文 3: 解决方案
            f"The solution:\n\n"
            f"{display_name} + OpenClaw integration\n\n"
            f"What it does:\n"
            f"✅ Zero manual work\n"
            f"✅ 5-minute setup\n"
            f"✅ Fully customizable\n"
            f"✅ Open source (free)",
            
            # 推文 4: 数据证明
            f"My results after 7 days:\n\n"
            f"⏱️ Time saved: 1.5 hours/day\n"
            f"📈 Efficiency: +300%\n"
            f"💰 Cost: $0 (vs $500+/mo tools)\n"
            f"😌 Stress level: Way down\n\n"
            f"That's 547 hours/year = 68 work days!",
            
            # 推文 5: 适用人群
            f"Who is this for?\n\n"
            f"✅ Content creators\n"
            f"✅ AI automation enthusiasts\n"
            f"✅ Busy professionals\n"
            f"✅ Anyone who values time\n\n"
            f"Not for: People who enjoy manual work",
            
            # 推文 6: 实施步骤
            f"How to implement (4-step process):\n\n"
            f"1️⃣ Read docs (10 min)\n"
            f"2️⃣ Test locally (30 min)\n"
            f"3️⃣ Small pilot (1 week)\n"
            f"4️⃣ Full deployment\n\n"
            f"Don't skip the testing phase. Most people do.",
            
            # 推文 7: 优缺点
            f"Honest review:\n\n"
            f"👍 Pros:\n"
            f"• Works out of the box\n"
            f"• Active community\n"
            f"• Great documentation\n\n"
            f"👎 Cons:\n"
            f"• Initial setup takes patience\n"
            f"• Some features need customization\n\n"
            f"Rating: ⭐⭐⭐⭐ (85/100)",
            
            # 推文 8: CTA
            f"Want the full setup guide?\n\n"
            f"I've documented everything:\n"
            f"• Step-by-step setup\n"
            f"• Common pitfalls\n"
            f"• Advanced tips\n\n"
            f"Comment 'SKILL' and I'll DM you the link 🎯\n\n"
            f"RT to save a friend time\n\n"
            f"#OpenClaw #AI #Automation #{skill_name.replace('-', '')} #Productivity"
        ]
    
    def post_thread(self, tweets):
        """发布 Thread"""
        self._log(f"🐦 Posting {len(tweets)} tweets")
        
        prev_id = None
        for i, tweet in enumerate(tweets, 1):
            self._log(f"  Tweet {i}/{len(tweets)}")
            
            cmd = ['twitter', 'post', tweet]
            if prev_id:
                cmd.extend(['--reply-to', prev_id])
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    self._log(f"    ✅ Success")
                    try:
                        data = json.loads(result.stdout)
                        if data.get('ok'):
                            prev_id = data['data'].get('id')
                    except:
                        pass
                else:
                    self._log(f"    ❌ Failed")
                    return False
                
                if i < len(tweets):
                    time.sleep(random.randint(180, 300))
                    
            except Exception as e:
                self._log(f"    ❌ Error: {e}")
                return False
        
        return True
    
    def run(self, dry_run=False):
        """运行"""
        self._log("="*60)
        self._log("🚀 English Skill Publisher")
        self._log(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self._log("="*60)
        
        skill = self.select_skill()
        self._log(f"🎯 Today's Skill: {skill}")
        
        tweets = self.generate_thread(skill)
        self._log(f"✅ Generated {len(tweets)} tweets")
        
        if dry_run:
            self._log("🔍 Preview mode")
            for i, tweet in enumerate(tweets, 1):
                print(f"\nTweet {i}:\n{tweet[:150]}...")
            return
        
        self._log("📤 Posting...")
        if self.post_thread(tweets):
            self.published_skills.append(skill)
            self._save_history()
            self._log(f"✅ {skill} posted and saved")
        
        self._log("="*60)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    
    publisher = EnglishSkillPublisher()
    publisher.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
