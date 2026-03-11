#!/usr/bin/env python3
"""
英文版 Skill 发布系统 V2
内容更详细、更有价值、更像真实分享
"""

import json
import random
import subprocess
from datetime import datetime
from pathlib import Path
import time


class EnglishPublisherV2:
    """英文发布器 V2"""
    
    def __init__(self):
        self.skills_dir = Path.home() / ".openclaw" / "skills"
        self.history_file = Path("english_v2_published.json")
        self.published = self._load_history()
        self.log_file = Path("english_v2.log")
    
    def _load_history(self):
        if self.history_file.exists():
            with open(self.history_file) as f:
                return json.load(f).get('skills', [])
        return []
    
    def _save_history(self):
        data = {
            'skills': self.published,
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
        
        available = [s for s in all_skills if s not in self.published]
        if not available:
            self.published = []
            available = all_skills
        
        priority = ['ai-image-generation', 'ai-video-generation', 'ai-content-pipeline',
                   'ai-automation-workflows', 'ai-voice-cloning', 'agentic-browser']
        priority_available = [s for s in priority if s in available]
        
        return random.choice(priority_available) if priority_available else random.choice(available)
    
    def generate_detailed_thread(self, skill_name: str) -> list:
        """生成详细 Thread"""
        
        display_name = skill_name.replace('-', ' ').title()
        
        return [
            # Tweet 1: 强钩子 + 具体成果
            f"I built an automated {display_name} workflow that saves me 2 hours daily.\n\n"
            f"Cost: $0\n"
            f"Setup time: 30 minutes\n"
            f"ROI: 547 hours/year\n\n"
            f"Here's exactly how I did it 🧵",
            
            # Tweet 2: 详细痛点
            f"The problem I was facing:\n\n"
            f"• Spending 2+ hours daily on manual {display_name}\n"
            f"• Inconsistent output quality\n"
            f"• Couldn't scale beyond 10 items/day\n"
            f"• Constant context switching\n\n"
            f"Sound familiar?",
            
            # Tweet 3: 解决方案介绍
            f"The solution: {display_name} + OpenClaw automation\n\n"
            f"What this stack does:\n"
            f"✅ Processes 100+ items automatically\n"
            f"✅ Maintains consistent quality\n"
            f"✅ Runs 24/7 without supervision\n"
            f"✅ Integrates with existing tools\n\n"
            f"All open source.",
            
            # Tweet 4: 详细实施步骤
            f"Step-by-step setup (takes 30 min):\n\n"
            f"1️⃣ Install OpenClaw CLI\n"
            f"2️⃣ Configure {display_name} Skill\n"
            f"3️⃣ Set up automation triggers\n"
            f"4️⃣ Test with 5 sample items\n"
            f"5️⃣ Deploy to production\n\n"
            f"I'll share the exact config below 👇",
            
            # Tweet 5: 技术细节
            f"Technical details:\n\n"
            f"• Built on OpenClaw framework\n"
            f"• Uses {display_name} API\n"
            f"• Triggers: Webhook + Schedule\n"
            f"• Error handling: Auto-retry + Alert\n"
            f"• Monitoring: Built-in logs\n\n"
            f"Zero maintenance required.",
            
            # Tweet 6: 实际数据
            f"Real results after 30 days:\n\n"
            f"📊 Before:\n"
            f"• Manual: 2 hours/day\n"
            f"• Output: 10 items/day\n"
            f"• Error rate: 15%\n\n"
            f"📈 After:\n"
            f"• Automated: 0 hours/day\n"
            f"• Output: 100+ items/day\n"
            f"• Error rate: 2%",
            
            # Tweet 7: 成本分析
            f"Cost breakdown:\n\n"
            f"Traditional tools: $500-2000/month\n"
            f"Freelancer: $3000+/month\n"
            f"Enterprise solution: $10k+/month\n\n"
            f"This setup: $0\n\n"
            f"Time investment: 30 minutes setup\n"
            f"Annual savings: $6,000-36,000",
            
            # Tweet 8: 适用人群
            f"Who is this for?\n\n"
            f"✅ Content creators scaling output\n"
            f"✅ Agencies handling bulk work\n"
            f"✅ Developers building products\n"
            f"✅ Anyone valuing their time\n\n"
            f"Not for: People who enjoy manual work",
            
            # Tweet 9: 优缺点
            f"Honest review after 30 days:\n\n"
            f"👍 Pros:\n"
            f"• Works out of the box\n"
            f"• Active community support\n"
            f"• Regular updates\n"
            f"• Extensive documentation\n\n"
            f"👎 Cons:\n"
            f"• Initial learning curve\n"
            f"• Requires technical setup\n\n"
            f"Rating: ⭐⭐⭐⭐⭐ (90/100)",
            
            # Tweet 10: 资源分享
            f"Want to implement this?\n\n"
            f"I documented everything:\n"
            f"• Full setup guide\n"
            f"• Configuration templates\n"
            f"• Troubleshooting tips\n"
            f"• Advanced customization\n\n"
            f"Comment 'SETUP' and I'll DM you the link 📩\n\n"
            f"RT to help someone save time 🔄",
            
            # Tweet 11: 总结
            f"Key takeaways:\n\n"
            f"1. Automation isn't just about saving time\n"
            f"2. It's about scaling what works\n"
            f"3. Open source tools are production-ready\n"
            f"4. 30 min setup → 547 hours saved/year\n\n"
            f"Start small. Test. Scale.\n\n"
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
                    self._log(f"    ❌ Failed: {result.stderr[:100]}")
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
        self._log("🚀 English Publisher V2 (Detailed)")
        self._log(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self._log("="*60)
        
        skill = self.select_skill()
        self._log(f"🎯 Today's Skill: {skill}")
        
        tweets = self.generate_detailed_thread(skill)
        self._log(f"✅ Generated {len(tweets)} detailed tweets")
        
        if dry_run:
            self._log("🔍 Preview mode")
            for i, tweet in enumerate(tweets, 1):
                print(f"\nTweet {i}:\n{tweet[:200]}...")
            return
        
        self._log("📤 Posting...")
        if self.post_thread(tweets):
            self.published.append(skill)
            self._save_history()
            self._log(f"✅ {skill} posted and saved")
        
        self._log("="*60)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    
    publisher = EnglishPublisherV2()
    publisher.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
