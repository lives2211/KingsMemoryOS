#!/usr/bin/env python3
"""
安全发布策略
避免触发 Twitter 风控
"""

import random
import time
from datetime import datetime


class SafePostingStrategy:
    """安全发布策略"""
    
    def __init__(self):
        self.daily_limits = {
            'tweets': 15,      # 每天最多15条推文
            'threads': 2,      # 每天最多2个Thread
            'replies': 20,     # 每天最多20条回复
            'likes': 50,       # 每天最多50个点赞
        }
        
        self.hourly_limits = {
            'tweets': 5,       # 每小时最多5条
            'replies': 8,      # 每小时最多8条回复
        }
        
        self.timing_rules = {
            'min_interval': 180,      # 推文间隔最少3分钟
            'max_interval': 480,      # 推文间隔最多8分钟
            'thread_interval': 240,   # Thread内间隔4分钟
            'reply_interval': 60,     # 回复间隔1分钟
        }
    
    def get_random_interval(self, action_type='tweet'):
        """获取随机间隔"""
        if action_type == 'tweet':
            return random.randint(180, 480)  # 3-8分钟
        elif action_type == 'reply':
            return random.randint(60, 180)   # 1-3分钟
        elif action_type == 'thread':
            return random.randint(240, 360)  # 4-6分钟
        return 300
    
    def get_daily_schedule(self):
        """生成每日发布计划"""
        schedule = []
        
        # 主 Thread 1: 上午随机时间 (8:00-12:00)
        hour1 = random.randint(8, 11)
        minute1 = random.randint(0, 59)
        schedule.append({
            'time': f"{hour1:02d}:{minute1:02d}",
            'type': 'main_thread',
            'count': 12,
            'description': '中文区 Skill 推广 (带GitHub)'
        })
        
        # 互动批次 1: 下午 (13:00-15:00)
        hour2 = random.randint(13, 14)
        minute2 = random.randint(0, 59)
        schedule.append({
            'time': f"{hour2:02d}:{minute2:02d}",
            'type': 'engagement_batch_1',
            'count': 5,
            'description': '互动最近24小时帖子'
        })
        
        # 互动批次 2: 下午 (15:30-17:30)
        hour3 = random.randint(15, 17)
        minute3 = random.randint(30, 59)
        schedule.append({
            'time': f"{hour3:02d}:{minute3:02d}",
            'type': 'engagement_batch_2',
            'count': 5,
            'description': '第二批互动'
        })
        
        # 互动批次 3: 晚上 (19:00-21:00)
        hour4 = random.randint(19, 20)
        minute4 = random.randint(0, 59)
        schedule.append({
            'time': f"{hour4:02d}:{minute4:02d}",
            'type': 'engagement_batch_3',
            'count': 5,
            'description': '第三批互动'
        })
        
        # 晚间 Thread (20% 概率)
        if random.random() < 0.2:
            hour5 = random.randint(21, 23)
            minute5 = random.randint(0, 59)
            schedule.append({
                'time': f"{hour5:02d}:{minute5:02d}",
                'type': 'night_thread',
                'count': 8,
                'description': '晚间 Thread (随机)'
            })
        
        return sorted(schedule, key=lambda x: x['time'])
    
    def calculate_total_actions(self, schedule):
        """计算总操作数"""
        total = {'tweets': 0, 'replies': 0}
        
        for item in schedule:
            if 'thread' in item['type']:
                total['tweets'] += item['count']
            elif 'engagement' in item['type']:
                total['replies'] += item['count']
        
        return total
    
    def check_safety(self, schedule):
        """检查是否安全"""
        total = self.calculate_total_actions(schedule)
        
        checks = []
        
        # 检查每日限制
        if total['tweets'] <= self.daily_limits['tweets']:
            checks.append(f"✅ 推文: {total['tweets']}/{self.daily_limits['tweets']}")
        else:
            checks.append(f"❌ 推文超限: {total['tweets']}/{self.daily_limits['tweets']}")
        
        if total['replies'] <= self.daily_limits['replies']:
            checks.append(f"✅ 回复: {total['replies']}/{self.daily_limits['replies']}")
        else:
            checks.append(f"❌ 回复超限: {total['replies']}/{self.daily_limits['replies']}")
        
        # 检查时间分布
        times = [item['time'] for item in schedule]
        if len(times) >= 2:
            checks.append(f"✅ 时间分布: {len(times)} 个时段")
        
        return checks
    
    def generate_report(self):
        """生成每日策略报告"""
        schedule = self.get_daily_schedule()
        total = self.calculate_total_actions(schedule)
        checks = self.check_safety(schedule)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║           每日安全发布策略                                       ║
╚══════════════════════════════════════════════════════════════════╝

📅 日期: {datetime.now().strftime('%Y-%m-%d')}

⏰ 发布计划:
"""
        
        for i, item in enumerate(schedule, 1):
            report += f"\n  {i}. {item['time']} - {item['description']}\n"
            report += f"     类型: {item['type']} | 数量: {item['count']}\n"
        
        report += f"""
📊 总计:
   • 推文: {total['tweets']} 条
   • 回复: {total['replies']} 条

✅ 安全检查:
"""
        for check in checks:
            report += f"   {check}\n"
        
        report += f"""
⏱️ 时间间隔:
   • 推文间隔: 3-8 分钟
   • 回复间隔: 1-3 分钟
   • Thread内间隔: 4-6 分钟

🛡️ 安全措施:
   • 随机时间发布
   • 分批次操作
   • 模拟真人行为
   • 自动限速保护

═══════════════════════════════════════════════════════════════════
"""
        return report


def main():
    strategy = SafePostingStrategy()
    print(strategy.generate_report())


if __name__ == "__main__":
    main()
