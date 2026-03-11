#!/usr/bin/env python3
"""
X / Reddit 自动涨粉系统
结合 Skill 内容 + 自动互动
"""

import json
import random
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import time


class GrowthAutomation:
    """涨粉自动化系统"""
    
    def __init__(self):
        self.log_file = Path("growth_automation.log")
        self.config_file = Path("growth_config.json")
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """加载配置"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)
        return {
            'daily_posts': 1,
            'daily_comments': 10,
            'target_keywords': ['AI', 'OpenClaw', 'Skill', 'Automation'],
            'engagement_topics': [
                'AI tools', 'productivity', 'automation', 
                'OpenClaw', 'AI agents', 'workflow'
            ]
        }
    
    def _log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
        
        print(log_line, end='')
    
    def generate_engagement_content(self, topic: str) -> dict:
        """生成互动内容（英文，适合涨粉）"""
        
        # 钩子模板（吸引点击）
        hooks = [
            f"Just discovered a game-changer for {topic} 🧵",
            f"I've been using this {topic} workflow for 30 days. Here's what happened:",
            f"Stop doing {topic} manually. Here's the automation stack:",
            f"This {topic} setup saves me 2 hours every day:",
            f"The {topic} tool nobody is talking about yet 👇",
        ]
        
        # 价值模板（提供干货）
        value_props = [
            "✅ Zero manual work\n✅ OpenClaw native integration\n✅ 5-min setup\n✅ Fully customizable",
            "📊 Results after 7 days:\n• 1.5h saved daily\n• 300% efficiency boost\n• Zero missed tasks\n• Stress reduced",
            "⚡ Core features:\n• Auto-processing\n• Multi-platform sync\n• Smart triggers\n• Custom workflows",
            "🎯 Perfect for:\n• Content creators\n• Automation enthusiasts\n• Busy professionals\n• AI early adopters",
        ]
        
        # CTA 模板（引导互动）
        ctas = [
            "Want the full setup guide?\nComment 'SKILL' and I'll DM you 🎯",
            "What's your biggest {topic} challenge?\nLet me know below 👇",
            "Follow for daily AI automation tips 🚀",
            "Save this for later 📌\nRT if you found it helpful",
        ]
        
        hook = random.choice(hooks)
        value = random.choice(value_props)
        cta = random.choice(ctas).format(topic=topic)
        
        return {
            'hook': hook,
            'value': value,
            'cta': cta,
            'full_thread': [
                f"{hook}\n\n{value}\n\n👇 Thread",
                f"Why this matters:\n\nMost people waste 2+ hours daily on repetitive {topic} tasks.\n\nThis automation stack eliminates that completely.",
                f"The ROI:\n\n• Time saved: 1.5h/day\n• Annual impact: 547 hours\n• Equivalent: 68 work days\n• Cost: $0 (open source)",
                f"How to start:\n\n1. Read docs (10 min)\n2. Test locally (30 min)\n3. Small pilot (1 week)\n4. Full deployment\n\nDon't go all-in at once.",
                f"{cta}\n\n#OpenClaw #AI #Automation #{topic.replace(' ', '')} #Productivity"
            ]
        }
    
    def generate_comment_templates(self) -> list:
        """生成评论模板（用于自动互动）"""
        return [
            "This is exactly what I needed! Thanks for sharing 🙌",
            "Been looking for something like this. How long did it take you to set up?",
            "The ROI calculation is eye-opening. 68 work days saved is massive!",
            "Just tried this workflow. Game changer for real 💯",
            "What other tools do you recommend for AI automation?",
            "This thread is pure gold. Following for more 🎯",
            "How does this compare to other automation tools you've tried?",
            "The step-by-step approach is smart. Most people skip testing phase.",
            "Bookmarked! Will implement this weekend 📌",
            "Your content consistently delivers value. Appreciate it!",
        ]
    
    def post_content(self, content: dict) -> bool:
        """发布内容到 Twitter"""
        tweets = content['full_thread']
        
        self._log(f"🐦 发布 {len(tweets)} 条推文")
        
        prev_id = None
        for i, tweet in enumerate(tweets, 1):
            self._log(f"  推文 {i}/{len(tweets)}")
            
            cmd = ['twitter', 'post', tweet]
            if prev_id:
                cmd.extend(['--reply-to', prev_id])
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    self._log(f"    ✅ 成功")
                    try:
                        data = json.loads(result.stdout)
                        if data.get('ok'):
                            prev_id = data['data'].get('id')
                    except:
                        pass
                else:
                    self._log(f"    ❌ 失败")
                    return False
                
                if i < len(tweets):
                    time.sleep(random.randint(180, 300))
                    
            except Exception as e:
                self._log(f"    ❌ 错误: {e}")
                return False
        
        return True
    
    def search_and_engage(self, keyword: str, count: int = 5):
        """搜索并互动（需要 Rube MCP）"""
        self._log(f"🔍 搜索关键词: {keyword}")
        
        # 使用 twitter-cli 搜索
        cmd = ['twitter', 'search', keyword, '--max', str(count * 2)]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                tweets = data.get('data', [])
                
                comments = self.generate_comment_templates()
                engaged = 0
                
                for tweet in tweets[:count]:
                    tweet_id = tweet.get('id')
                    author = tweet.get('author', {}).get('screenName', '')
                    
                    # 跳过自己的推文
                    if author == 'your_username':  # 需要替换
                        continue
                    
                    # 随机选择评论
                    comment = random.choice(comments)
                    
                    self._log(f"  💬 评论 @{author}: {comment[:50]}...")
                    
                    # 发布评论
                    cmd = ['twitter', 'post', comment, '--reply-to', tweet_id]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        self._log(f"    ✅ 评论成功")
                        engaged += 1
                    else:
                        self._log(f"    ❌ 评论失败")
                    
                    time.sleep(random.randint(60, 120))
                
                self._log(f"✅ 互动完成: {engaged}/{count}")
                
        except Exception as e:
            self._log(f"❌ 搜索失败: {e}")
    
    def run_daily_growth(self):
        """运行每日涨粉任务"""
        self._log("="*60)
        self._log("🚀 涨粉自动化系统启动")
        self._log(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self._log("="*60)
        
        # 1. 发布内容（1条主帖）
        topic = random.choice(self.config['engagement_topics'])
        self._log(f"\n📝 生成内容: {topic}")
        content = self.generate_engagement_content(topic)
        
        if self.post_content(content):
            self._log("✅ 内容发布成功")
        else:
            self._log("❌ 内容发布失败")
        
        # 2. 自动互动（评论他人帖子）
        self._log("\n🤝 开始自动互动...")
        keyword = random.choice(self.config['target_keywords'])
        self.search_and_engage(keyword, count=5)
        
        self._log("\n✅ 今日涨粉任务完成")
        self._log("="*60)
    
    def generate_rube_commands(self):
        """生成 Rube MCP 命令（用于 Reddit 养号）"""
        commands = [
            "Rube, help me post 10 comments on Reddit about AI automation tools",
            "Rube, find 5 posts about OpenClaw and add valuable comments",
            "Rube, engage with 10 posts in r/artificialintelligence with helpful replies",
            "Rube, comment on trending productivity tool posts on Reddit",
        ]
        
        print("\n" + "="*60)
        print("🛠️ Rube MCP 命令示例（用于 Reddit 养号）:")
        print("="*60 + "\n")
        
        for i, cmd in enumerate(commands, 1):
            print(f"{i}. {cmd}\n")
        
        print("使用步骤:")
        print("1. 安装 Rube: https://rube.app")
        print("2. 在 Claude Code CLI 中输入上述命令")
        print("3. 授权 Reddit 账号")
        print("4. 自动开始养号涨 Karma")
        print("="*60)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自动涨粉系统')
    parser.add_argument('--run', action='store_true', help='运行每日任务')
    parser.add_argument('--rube', action='store_true', help='显示 Rube 命令')
    parser.add_argument('--content-only', action='store_true', help='只发布内容')
    
    args = parser.parse_args()
    
    growth = GrowthAutomation()
    
    if args.rube:
        growth.generate_rube_commands()
    elif args.content_only:
        topic = random.choice(growth.config['engagement_topics'])
        content = growth.generate_engagement_content(topic)
        growth.post_content(content)
    else:
        growth.run_daily_growth()


if __name__ == "__main__":
    main()
