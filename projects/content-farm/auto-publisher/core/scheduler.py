"""
发布调度器
管理发布时间和频率，模拟真人作息
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from loguru import logger


@dataclass
class PublishWindow:
    """发布时间段"""
    start: str  # "HH:MM"格式
    end: str    # "HH:MM"格式
    weight: float  # 权重 (0-1)


@dataclass
class PublishTask:
    """发布任务"""
    note_file: str
    scheduled_time: datetime
    priority: int = 0


class PublishScheduler:
    """发布调度器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.publish_windows = self._parse_windows(config.get('publish_windows', []))
        self.max_daily_posts = config.get('max_daily_posts', 3)
        self.min_interval = config.get('min_interval', 1800)  # 最小间隔30分钟
        self.max_interval = config.get('max_interval', 7200)  # 最大间隔2小时
        self.published_today = 0
        self.last_publish_time: Optional[datetime] = None
    
    def _parse_windows(self, windows: List[Dict]) -> List[PublishWindow]:
        """解析发布时间段"""
        parsed = []
        for w in windows:
            parsed.append(PublishWindow(
                start=w['start'],
                end=w['end'],
                weight=w.get('weight', 1.0)
            ))
        return parsed
    
    def should_publish_now(self) -> bool:
        """检查当前是否应该发布"""
        now = datetime.now()
        
        # 检查是否超过每日限制
        if self.published_today >= self.max_daily_posts:
            logger.info(f"今日已发布 {self.published_today} 篇，达到上限")
            return False
        
        # 检查是否在发布时间段内
        current_time = now.strftime("%H:%M")
        in_window = False
        
        for window in self.publish_windows:
            if window.start <= current_time <= window.end:
                in_window = True
                break
        
        if not in_window:
            logger.debug(f"当前时间 {current_time} 不在发布时间段内")
            return False
        
        # 检查发布间隔
        if self.last_publish_time:
            elapsed = (now - self.last_publish_time).total_seconds()
            if elapsed < self.min_interval:
                logger.debug(f"距离上次发布仅 {elapsed:.0f} 秒，需等待 {self.min_interval} 秒")
                return False
        
        return True
    
    def get_next_publish_time(self) -> Optional[datetime]:
        """获取下次发布时间"""
        now = datetime.now()
        
        # 如果今天还能发布
        if self.published_today < self.max_daily_posts:
            # 在当前时间段内找下一个时间点
            for window in self.publish_windows:
                window_start = datetime.strptime(window.start, "%H:%M").time()
                window_end = datetime.strptime(window.end, "%H:%M").time()
                current_time = now.time()
                
                if window_start <= current_time <= window_end:
                    # 在当前窗口内，计算随机发布时间
                    remaining_minutes = (
                        datetime.combine(now.date(), window_end) - now
                    ).total_seconds() / 60
                    
                    if remaining_minutes > 10:  # 至少剩余10分钟
                        delay = random.randint(5, int(remaining_minutes) - 5)
                        return now + timedelta(minutes=delay)
        
        # 找下一个发布窗口
        tomorrow = now.date() + timedelta(days=1)
        
        for window in self.publish_windows:
            window_start = datetime.strptime(window.start, "%H:%M").time()
            next_time = datetime.combine(tomorrow, window_start)
            
            # 添加随机偏移
            offset = random.randint(0, 30)
            return next_time + timedelta(minutes=offset)
        
        return None
    
    def calculate_publish_schedule(
        self,
        notes_count: int,
        start_date: Optional[datetime] = None
    ) -> List[PublishTask]:
        """
        计算发布计划
        
        Args:
            notes_count: 要发布的笔记数量
            start_date: 开始日期，默认为明天
            
        Returns:
            发布任务列表
        """
        if start_date is None:
            start_date = datetime.now() + timedelta(days=1)
        
        tasks = []
        current_date = start_date
        remaining = notes_count
        
        while remaining > 0:
            # 为每一天分配发布任务
            daily_count = min(self.max_daily_posts, remaining)
            
            # 根据权重选择发布窗口
            windows = self._select_windows_for_day(daily_count)
            
            for i, window in enumerate(windows):
                # 在窗口内选择随机时间
                window_start = datetime.strptime(window['start'], "%H:%M").time()
                window_end = datetime.strptime(window['end'], "%H:%M").time()
                
                # 计算窗口持续时间
                start_dt = datetime.combine(current_date.date(), window_start)
                end_dt = datetime.combine(current_date.date(), window_end)
                duration = (end_dt - start_dt).total_seconds()
                
                # 在窗口内随机选择时间
                random_offset = random.randint(300, int(duration) - 300)  # 前后留5分钟
                publish_time = start_dt + timedelta(seconds=random_offset)
                
                tasks.append(PublishTask(
                    note_file=f"",  # 稍后填充
                    scheduled_time=publish_time,
                    priority=remaining
                ))
                
                remaining -= 1
                if remaining <= 0:
                    break
            
            current_date += timedelta(days=1)
        
        # 排序并添加间隔
        tasks.sort(key=lambda x: x.scheduled_time)
        tasks = self._add_intervals(tasks)
        
        return tasks
    
    def _select_windows_for_day(self, count: int) -> List[Dict]:
        """为一天选择发布窗口"""
        if not self.publish_windows:
            return []
        
        # 按权重选择
        weights = [w.weight for w in self.publish_windows]
        total_weight = sum(weights)
        
        selected = []
        for _ in range(count):
            r = random.uniform(0, total_weight)
            current = 0
            for window in self.publish_windows:
                current += window.weight
                if r <= current:
                    selected.append({
                        'start': window.start,
                        'end': window.end
                    })
                    break
        
        return selected
    
    def _add_intervals(self, tasks: List[PublishTask]) -> List[PublishTask]:
        """在任务之间添加随机间隔"""
        if len(tasks) <= 1:
            return tasks
        
        adjusted = [tasks[0]]
        
        for i in range(1, len(tasks)):
            prev_time = adjusted[-1].scheduled_time
            min_next = prev_time + timedelta(seconds=self.min_interval)
            
            if tasks[i].scheduled_time < min_next:
                # 添加随机间隔
                extra_delay = random.randint(0, self.max_interval - self.min_interval)
                new_time = min_next + timedelta(seconds=extra_delay)
                tasks[i].scheduled_time = new_time
            
            adjusted.append(tasks[i])
        
        return adjusted
    
    def record_publish(self):
        """记录一次发布"""
        self.published_today += 1
        self.last_publish_time = datetime.now()
        logger.info(f"记录发布，今日已发布: {self.published_today}/{self.max_daily_posts}")
    
    def reset_daily_count(self):
        """重置每日计数（每天0点调用）"""
        self.published_today = 0
        logger.info("重置每日发布计数")
    
    def get_random_delay(self) -> float:
        """获取随机延迟（秒）"""
        return random.uniform(self.min_interval, self.max_interval)
    
    def get_status(self) -> Dict:
        """获取调度器状态"""
        return {
            'published_today': self.published_today,
            'max_daily_posts': self.max_daily_posts,
            'last_publish_time': self.last_publish_time.isoformat() if self.last_publish_time else None,
            'next_publish_time': self.get_next_publish_time().isoformat() if self.get_next_publish_time() else None,
            'can_publish_now': self.should_publish_now()
        }


def main():
    """测试代码"""
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
    
    scheduler = PublishScheduler(config)
    
    # 测试发布计划
    tasks = scheduler.calculate_publish_schedule(5)
    
    print("发布计划:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    
    print(f"\n当前状态: {scheduler.get_status()}")


if __name__ == "__main__":
    main()
