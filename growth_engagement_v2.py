#!/usr/bin/env python3
"""
智能互动系统 V2
只互动最近24小时的帖子，获取最大流量
"""

import json
import subprocess
import random
from datetime import datetime, timedelta
from pathlib import Path
import time


class SmartEngagement:
    """智能互动系统"""
    
    def __init__(self):
        self.log_file = Path("smart_engagement.log")
        self.engaged_file = Path("engaged_posts.json")
        self.engaged = self._load_engaged()
    
    def _load_engaged(self):
        """加载已互动列表"""
        if self.engaged_file.exists():
            with open(self.engaged_file) as f:
                return json.load(f).get('posts', [])
        return []
    
    def _save_engaged(self):
        """保存已互动列表"""
        data = {
            'posts': self.engaged[-500:],  # 只保留最近500条
            'last_update': datetime.now().isoformat()
        }
        with open(self.engaged_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] {message}\n"
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
        print(log_line, end='')
    
    def search_recent_posts(self, keyword: str, hours: int = 24, max_results: int = 20) -> list:
        """搜索最近24小时的帖子"""
        self._log(f"🔍 搜索最近{hours}小时的帖子: {keyword}")
        
        cmd = ['twitter', 'search', keyword, '--max', str(max_results * 2)]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                self._log(f"❌ 搜索失败: {result.stderr[:100]}")
                return []
            
            data = json.loads(result.stdout)
            posts = data.get('data', [])
            
            # 过滤最近24小时
            cutoff = datetime.now() - timedelta(hours=hours)
            recent_posts = []
            
            for post in posts:
                created_at = post.get('createdAt', '')
                try:
                    post_time = datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
                    if post_time >= cutoff:
                        recent_posts.append(post)
                except:
                    continue
            
            self._log(f"✅ 找到 {len(recent_posts)} 条最近{hours}小时的帖子")
            return recent_posts
            
        except Exception as e:
            self._log(f"❌ 搜索错误: {e}")
            return []
    
    def filter_high_engagement(self, posts: list, min_likes: int = 10) -> list:
        """过滤高互动帖子"""
        filtered = []
        for post in posts:
            metrics = post.get('metrics', {})
            likes = metrics.get('likes', 0)
            retweets = metrics.get('retweets', 0)
            
            # 只互动有一定热度的帖子
            if likes >= min_likes or retweets >= 5:
                filtered.append(post)
        
        self._log(f"📊 高互动帖子: {len(filtered)}/{len(posts)}")
        return filtered
    
    def generate_comment(self, post_text: str, author: str) -> str:
        """生成智能评论"""
        # 根据帖子内容生成相关评论
        comments = [
            "This is exactly what I needed! Thanks for sharing 🙌",
            "Been looking for something like this. How long did setup take?",
            "The ROI calculation is eye-opening. 68 work days saved!",
            "Just tried this workflow. Game changer 💯",
            "What other tools do you recommend for AI automation?",
            "This thread is pure gold. Following for more 🎯",
            "How does this compare to other tools you've tried?",
            "Bookmarked! Will implement this weekend 📌",
            "Your content consistently delivers value. Appreciate it!",
            "The step-by-step approach is smart. Most people skip testing.",
        ]
        
        # 根据帖子内容选择更相关的评论
        text_lower = post_text.lower()
        
        if 'roi' in text_lower or 'save' in text_lower:
            return "The ROI numbers are impressive. How long until you saw results?"
        
        if 'automation' in text_lower or 'workflow' in text_lower:
            return "This automation approach is smart. What was the biggest challenge?"
        
        if 'ai' in text_lower or 'openclaw' in text_lower:
            return "Love seeing practical AI applications like this. What's next on your list?"
        
        return random.choice(comments)
    
    def engage_post(self, post: dict) -> bool:
        """互动单条帖子"""
        post_id = post.get('id')
        author = post.get('author', {}).get('screenName', '')
        text = post.get('text', '')
        
        # 跳过已互动的
        if post_id in self.engaged:
            return False
        
        # 生成评论
        comment = self.generate_comment(text, author)
        
        self._log(f"💬 @{author}: {comment[:50]}...")
        
        # 发布评论
        cmd = ['twitter', 'post', comment, '--reply-to', post_id]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self._log(f"  ✅ 成功")
                self.engaged.append(post_id)
                return True
            else:
                self._log(f"  ❌ 失败")
                return False
                
        except Exception as e:
            self._log(f"  ❌ 错误: {e}")
            return False
    
    def run_engagement(self, keywords: list = None, target_count: int = 10):
        """运行互动"""
        if keywords is None:
            keywords = ['AI automation', 'OpenClaw', 'productivity tools', 
                     'workflow automation', 'AI agents']
        
        self._log("="*60)
        self._log("🚀 智能互动系统启动")
        self._log(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self._log("="*60)
        
        all_posts = []
        
        # 搜索多个关键词
        for keyword in keywords:
            posts = self.search_recent_posts(keyword, hours=24, max_results=15)
            all_posts.extend(posts)
            time.sleep(2)
        
        if not all_posts:
            self._log("❌ 未找到帖子")
            return
        
        # 去重
        seen_ids = set()
        unique_posts = []
        for post in all_posts:
            pid = post.get('id')
            if pid not in seen_ids:
                seen_ids.add(pid)
                unique_posts.append(post)
        
        self._log(f"📊 去重后: {len(unique_posts)} 条")
        
        # 过滤高互动
        high_engagement = self.filter_high_engagement(unique_posts, min_likes=5)
        
        # 排除已互动
        to_engage = [p for p in high_engagement 
                     if p.get('id') not in self.engaged]
        
        self._log(f"🎯 准备互动: {len(to_engage)} 条")
        
        # 随机选择
        random.shuffle(to_engage)
        selected = to_engage[:target_count]
        
        # 开始互动
        success = 0
        for post in selected:
            if self.engage_post(post):
                success += 1
            
            # 间隔随机 60-120 秒
            if success < len(selected):
                delay = random.randint(60, 120)
                self._log(f"⏳ 等待 {delay} 秒...")
                time.sleep(delay)
        
        self._save_engaged()
        
        self._log(f"✅ 完成: {success}/{len(selected)} 成功")
        self._log("="*60)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='智能互动系统')
    parser.add_argument('--keywords', nargs='+', default=['AI automation', 'OpenClaw', 'productivity tools'])
    parser.add_argument('--count', type=int, default=10, help='互动数量')
    
    args = parser.parse_args()
    
    engagement = SmartEngagement()
    engagement.run_engagement(args.keywords, args.count)


if __name__ == "__main__":
    main()
