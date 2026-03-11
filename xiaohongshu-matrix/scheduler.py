#!/usr/bin/env python3
"""
小红书矩阵发布调度器
- 管理5个账号
- 随机时间发布
- 错峰策略
"""

import random
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# 账号配置
ACCOUNTS = {
    "tech-geek": {
        "name": "数码虾",
        "theme": "terminal",
        "mode": "auto-split",
        "persona": "personas/tech-geek.md",
        "posting_window": [(7, 30, 9, 0), (12, 0, 13, 30), (18, 30, 20, 0), (21, 0, 22, 30)],
        "daily_posts": (3, 5)
    },
    "life-aesthetics": {
        "name": "美学虾", 
        "theme": "botanical",
        "mode": "auto-split",
        "persona": "personas/life-aesthetics.md",
        "posting_window": [(8, 0, 9, 30), (12, 30, 14, 0), (15, 0, 16, 30), (20, 0, 21, 30)],
        "daily_posts": (3, 5)
    },
    "career-growth": {
        "name": "职场虾",
        "theme": "professional", 
        "mode": "auto-split",
        "persona": "personas/career-growth.md",
        "posting_window": [(7, 30, 9, 0), (12, 0, 13, 30), (18, 0, 19, 30), (21, 30, 23, 0)],
        "daily_posts": (3, 5)
    },
    "foodie": {
        "name": "吃货虾",
        "theme": "retro",
        "mode": "auto-split", 
        "persona": "personas/foodie.md",
        "posting_window": [(11, 30, 13, 0), (17, 30, 19, 0), (20, 0, 21, 30), (22, 0, 23, 30)],
        "daily_posts": (3, 5)
    },
    "fashion": {
        "name": "潮虾",
        "theme": "neo-brutalism",
        "mode": "auto-split",
        "persona": "personas/fashion.md", 
        "posting_window": [(8, 30, 10, 0), (13, 0, 14, 30), (16, 0, 17, 30), (19, 30, 21, 0)],
        "daily_posts": (3, 5)
    }
}

class PostingScheduler:
    def __init__(self, schedule_file="schedule.json"):
        self.schedule_file = schedule_file
        self.schedule = self.load_schedule()
        
    def load_schedule(self):
        """加载现有调度计划"""
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_schedule(self):
        """保存调度计划"""
        with open(self.schedule_file, 'w') as f:
            json.dump(self.schedule, f, indent=2, ensure_ascii=False)
    
    def generate_daily_schedule(self, date=None):
        """生成一天的发布计划"""
        if date is None:
            date = datetime.now().date()
        
        date_str = date.isoformat()
        daily_plan = {}
        all_posts = []
        
        for account_id, config in ACCOUNTS.items():
            # 随机决定今天发几篇
            num_posts = random.randint(*config["daily_posts"])
            posts = []
            
            for i in range(num_posts):
                # 随机选择一个时间窗口
                window = random.choice(config["posting_window"])
                start_h, start_m, end_h, end_m = window
                
                # 在窗口内随机选择时间
                start_time = datetime.combine(date, datetime.min.time().replace(hour=start_h, minute=start_m))
                end_time = datetime.combine(date, datetime.min.time().replace(hour=end_h, minute=end_m))
                
                # 随机时间点（人工化：避免整点）
                random_minutes = random.randint(0, int((end_time - start_time).total_seconds() / 60))
                post_time = start_time + timedelta(minutes=random_minutes)
                
                # 避免整点和半点（太规律）
                if post_time.minute in [0, 30]:
                    post_time = post_time + timedelta(minutes=random.choice([-1, 1]) * random.randint(1, 10))
                
                posts.append({
                    "time": post_time.isoformat(),
                    "account": account_id,
                    "account_name": config["name"],
                    "theme": config["theme"],
                    "status": "pending"
                })
            
            daily_plan[account_id] = posts
            all_posts.extend(posts)
        
        # 全局排序，检查冲突
        all_posts.sort(key=lambda x: x["time"])
        
        # 确保同一账号的帖子间隔至少30分钟
        for account_id in ACCOUNTS:
            account_posts = [p for p in all_posts if p["account"] == account_id]
            for i in range(1, len(account_posts)):
                prev_time = datetime.fromisoformat(account_posts[i-1]["time"])
                curr_time = datetime.fromisoformat(account_posts[i]["time"])
                if (curr_time - prev_time).total_seconds() < 1800:  # 30分钟
                    # 推迟当前帖子
                    new_time = prev_time + timedelta(minutes=30)
                    account_posts[i]["time"] = new_time.isoformat()
        
        # 重新排序
        all_posts.sort(key=lambda x: x["time"])
        
        # 保存
        self.schedule[date_str] = all_posts
        self.save_schedule()
        
        return all_posts
    
    def get_next_post(self):
        """获取下一个待发布的帖子"""
        now = datetime.now()
        
        for date_str, posts in self.schedule.items():
            for post in posts:
                if post["status"] == "pending":
                    post_time = datetime.fromisoformat(post["time"])
                    if post_time <= now + timedelta(minutes=5):  # 5分钟内要发的
                        return post
        return None
    
    def mark_posted(self, post_time, account):
        """标记帖子为已发布"""
        date_str = datetime.fromisoformat(post_time).date().isoformat()
        if date_str in self.schedule:
            for post in self.schedule[date_str]:
                if post["time"] == post_time and post["account"] == account:
                    post["status"] = "posted"
                    self.save_schedule()
                    return True
        return False
    
    def get_today_schedule(self):
        """获取今天的发布计划"""
        today = datetime.now().date().isoformat()
        return self.schedule.get(today, [])

if __name__ == "__main__":
    scheduler = PostingScheduler()
    
    # 生成今天的计划
    print("🦞 生成今日发布计划...")
    schedule = scheduler.generate_daily_schedule()
    
    print(f"\n今日共计划发布 {len(schedule)} 篇笔记:\n")
    
    for post in schedule:
        time_str = datetime.fromisoformat(post["time"]).strftime("%H:%M")
        print(f"[{time_str}] {post['account_name']} ({post['account']}) - 主题: {post['theme']}")
