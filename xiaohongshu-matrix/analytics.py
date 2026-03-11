#!/usr/bin/env python3
"""
小红书矩阵数据分析
- 发布数据统计
- 账号表现分析
- 内容效果追踪
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import statistics

class MatrixAnalytics:
    """矩阵数据分析器"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"):
        self.base_path = Path(base_path)
        self.schedule_file = self.base_path / "schedule.json"
        self.logs_dir = self.base_path / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
    def load_schedule(self):
        """加载调度数据"""
        if self.schedule_file.exists():
            with open(self.schedule_file, 'r') as f:
                return json.load(f)
        return {}
    
    def get_daily_stats(self, date=None):
        """获取每日统计"""
        if date is None:
            date = datetime.now().date().isoformat()
        
        schedule = self.load_schedule()
        day_data = schedule.get(date, [])
        
        if not day_data:
            return None
        
        # 统计各账号
        account_stats = defaultdict(lambda: {"total": 0, "posted": 0, "pending": 0})
        
        for post in day_data:
            account = post["account"]
            account_stats[account]["total"] += 1
            if post["status"] == "posted":
                account_stats[account]["posted"] += 1
            else:
                account_stats[account]["pending"] += 1
        
        total = len(day_data)
        posted = sum(1 for p in day_data if p["status"] == "posted")
        pending = total - posted
        
        return {
            "date": date,
            "total_posts": total,
            "posted": posted,
            "pending": pending,
            "completion_rate": round(posted / total * 100, 1) if total > 0 else 0,
            "account_breakdown": dict(account_stats)
        }
    
    def get_weekly_stats(self):
        """获取本周统计"""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        daily_stats = []
        for i in range(7):
            date = (week_start + timedelta(days=i)).isoformat()
            stats = self.get_daily_stats(date)
            if stats:
                daily_stats.append(stats)
        
        if not daily_stats:
            return None
        
        total_posts = sum(d["total_posts"] for d in daily_stats)
        total_posted = sum(d["posted"] for d in daily_stats)
        
        return {
            "week_start": week_start.isoformat(),
            "week_end": (week_start + timedelta(days=6)).isoformat(),
            "daily_stats": daily_stats,
            "total_posts": total_posts,
            "total_posted": total_posted,
            "completion_rate": round(total_posted / total_posts * 100, 1) if total_posts > 0 else 0,
            "avg_daily": round(total_posts / len(daily_stats), 1) if daily_stats else 0
        }
    
    def get_account_performance(self, account_type, days=7):
        """获取账号表现"""
        schedule = self.load_schedule()
        
        posts = []
        today = datetime.now().date()
        
        for i in range(days):
            date = (today - timedelta(days=i)).isoformat()
            if date in schedule:
                for post in schedule[date]:
                    if post["account"] == account_type:
                        posts.append(post)
        
        if not posts:
            return None
        
        total = len(posts)
        posted = sum(1 for p in posts if p["status"] == "posted")
        
        # 计算发布时间分布
        hours = []
        for post in posts:
            try:
                dt = datetime.fromisoformat(post["time"])
                hours.append(dt.hour)
            except:
                pass
        
        avg_hour = statistics.mean(hours) if hours else 0
        
        return {
            "account": account_type,
            "period_days": days,
            "total_scheduled": total,
            "total_posted": posted,
            "completion_rate": round(posted / total * 100, 1) if total > 0 else 0,
            "avg_posting_hour": round(avg_hour, 1),
            "posting_hours": hours
        }
    
    def generate_report(self):
        """生成数据报告"""
        print("=" * 60)
        print("🦞 小红书矩阵运营数据报告")
        print("=" * 60)
        print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 今日统计
        print("📊 今日概况")
        print("-" * 60)
        today_stats = self.get_daily_stats()
        if today_stats:
            print(f"计划发布: {today_stats['total_posts']} 篇")
            print(f"已完成: {today_stats['posted']} 篇")
            print(f"待发布: {today_stats['pending']} 篇")
            print(f"完成率: {today_stats['completion_rate']}%")
            print()
            print("各账号分布:")
            for account, stats in today_stats['account_breakdown'].items():
                status = "✅" if stats['pending'] == 0 else "⏳"
                print(f"  {status} {account}: {stats['posted']}/{stats['total']}")
        else:
            print("暂无今日数据")
        print()
        
        # 本周统计
        print("📈 本周概况")
        print("-" * 60)
        weekly_stats = self.get_weekly_stats()
        if weekly_stats:
            print(f"统计周期: {weekly_stats['week_start']} ~ {weekly_stats['week_end']}")
            print(f"总计划: {weekly_stats['total_posts']} 篇")
            print(f"已完成: {weekly_stats['total_posted']} 篇")
            print(f"完成率: {weekly_stats['completion_rate']}%")
            print(f"日均发布: {weekly_stats['avg_daily']} 篇")
            print()
            print("每日详情:")
            for day in weekly_stats['daily_stats']:
                print(f"  {day['date']}: {day['posted']}/{day['total_posts']} ({day['completion_rate']}%)")
        else:
            print("暂无本周数据")
        print()
        
        # 各账号表现
        print("👤 账号表现 (近7天)")
        print("-" * 60)
        accounts = ["tech-geek", "life-aesthetics", "career-growth", "foodie", "fashion"]
        account_names = {
            "tech-geek": "数码虾",
            "life-aesthetics": "美学虾",
            "career-growth": "职场虾",
            "foodie": "吃货虾",
            "fashion": "潮虾"
        }
        
        for account in accounts:
            perf = self.get_account_performance(account)
            if perf:
                name = account_names.get(account, account)
                print(f"\n{name} ({account}):")
                print(f"  计划: {perf['total_scheduled']} 篇")
                print(f"  完成: {perf['total_posted']} 篇")
                print(f"  完成率: {perf['completion_rate']}%")
                print(f"  平均发布时间: {perf['avg_posting_hour']:.1f}:00")
        print()
        
        # 建议
        print("💡 运营建议")
        print("-" * 60)
        self._generate_suggestions(today_stats, weekly_stats)
        print()
        
        print("=" * 60)
    
    def _generate_suggestions(self, today_stats, weekly_stats):
        """生成运营建议"""
        suggestions = []
        
        if today_stats:
            if today_stats['completion_rate'] < 50:
                suggestions.append("⚠️ 今日完成率较低，建议检查发布流程")
            elif today_stats['completion_rate'] == 100:
                suggestions.append("✅ 今日任务全部完成，表现优秀！")
            
            pending = today_stats['pending']
            if pending > 0:
                suggestions.append(f"⏳ 还有 {pending} 篇待发布，注意时间安排")
        
        if weekly_stats:
            if weekly_stats['avg_daily'] < 15:
                suggestions.append("📉 日均发布量偏低，可适当增加内容")
            elif weekly_stats['avg_daily'] > 25:
                suggestions.append("⚠️ 日均发布量较高，注意账号风控")
            
            if weekly_stats['completion_rate'] < 80:
                suggestions.append("📊 本周完成率偏低，建议优化发布流程")
        
        if not suggestions:
            suggestions.append("✅ 运营状况良好，继续保持！")
        
        for s in suggestions:
            print(f"  {s}")
    
    def export_data(self, days=30):
        """导出数据"""
        schedule = self.load_schedule()
        
        # 筛选最近N天
        today = datetime.now().date()
        filtered_data = {}
        
        for i in range(days):
            date = (today - timedelta(days=i)).isoformat()
            if date in schedule:
                filtered_data[date] = schedule[date]
        
        # 保存到文件
        export_file = self.logs_dir / f"export_{datetime.now().strftime('%Y%m%d')}.json"
        with open(export_file, 'w') as f:
            json.dump(filtered_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 数据已导出: {export_file}")
        return export_file

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书矩阵数据分析")
    parser.add_argument("--report", action="store_true", help="生成数据报告")
    parser.add_argument("--export", action="store_true", help="导出数据")
    parser.add_argument("--days", type=int, default=30, help="导出天数")
    parser.add_argument("--account", type=str, help="查看特定账号表现")
    
    args = parser.parse_args()
    
    analytics = MatrixAnalytics()
    
    if args.report:
        analytics.generate_report()
    elif args.export:
        analytics.export_data(args.days)
    elif args.account:
        perf = analytics.get_account_performance(args.account)
        if perf:
            print(f"\n账号: {args.account}")
            print(f"计划: {perf['total_scheduled']}")
            print(f"完成: {perf['total_posted']}")
            print(f"完成率: {perf['completion_rate']}%")
        else:
            print(f"暂无账号 {args.account} 的数据")
    else:
        # 默认生成报告
        analytics.generate_report()

if __name__ == "__main__":
    main()
