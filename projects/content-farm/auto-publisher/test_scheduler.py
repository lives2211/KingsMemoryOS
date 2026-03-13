#!/usr/bin/env python3
"""
测试发布调度器
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "core"))

from scheduler import PublishScheduler


def test_scheduler():
    """测试调度器"""
    print("⏰ 测试发布调度器...")
    
    config = {
        'publish_windows': [
            {'start': '08:00', 'end': '10:00', 'weight': 0.3},
            {'start': '12:00', 'end': '14:00', 'weight': 0.3},
            {'start': '19:00', 'end': '22:00', 'weight': 0.4}
        ],
        'max_daily_posts': 3,
        'min_interval': 1800,
        'max_interval': 7200
    }
    
    try:
        scheduler = PublishScheduler(config)
        
        # 生成发布计划
        print("\n📅 生成5篇笔记的发布计划:")
        tasks = scheduler.calculate_publish_schedule(5)
        
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        
        # 查看状态
        print(f"\n📊 当前状态:")
        status = scheduler.get_status()
        print(f"   今日已发布: {status['published_today']}/{status['max_daily_posts']}")
        print(f"   下次可发布: {status['next_publish_time']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_scheduler()
    sys.exit(0 if success else 1)
