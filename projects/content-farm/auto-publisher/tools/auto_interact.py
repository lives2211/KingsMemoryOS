#!/usr/bin/env python3
"""
自动互动工具
基于 xiaohongshu-cli 的自动化互动
- 自动浏览推荐流
- 智能点赞/收藏
- 自动评论
"""

import sys
import random
import time
from pathlib import Path
from typing import List, Dict
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from api_publisher import XHSAPIPublisher
from loguru import logger


class AutoInteractor:
    """自动互动器"""
    
    def __init__(self):
        self.publisher = XHSAPIPublisher()
        self.interacted_today = set()  # 今日已互动笔记ID
        self.daily_limit = 50  # 每日互动上限
        self.interact_count = 0
    
    def _should_interact(self, note: Dict) -> bool:
        """决定是否互动"""
        # 已互动过
        note_id = note.get('id')
        if note_id in self.interacted_today:
            return False
        
        # 达到上限
        if self.interact_count >= self.daily_limit:
            return False
        
        # 智能筛选：根据互动率
        likes = note.get('likes', 0)
        collects = note.get('collects', 0)
        comments = note.get('comments', 0)
        
        # 高互动内容更可能互动
        total_interactions = likes + collects + comments
        if total_interactions > 100:
            return random.random() < 0.7  # 70%概率
        elif total_interactions > 50:
            return random.random() < 0.5  # 50%概率
        else:
            return random.random() < 0.3  # 30%概率
    
    def _select_action(self, note: Dict) -> str:
        """选择互动动作"""
        actions = ['like', 'favorite', 'skip']
        weights = [0.5, 0.3, 0.2]  # 点赞50%，收藏30%，跳过20%
        
        return random.choices(actions, weights=weights)[0]
    
    def _random_delay(self, min_sec: float = 2, max_sec: float = 8):
        """随机延迟"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def browse_and_interact(
        self,
        category: str = "food",
        limit: int = 20,
        interact_ratio: float = 0.3
    ):
        """
        浏览并互动
        
        Args:
            category: 分类
            limit: 浏览数量
            interact_ratio: 互动比例
        """
        logger.info(f"开始浏览 {category} 分类，计划浏览 {limit} 条")
        
        # 获取热门内容
        notes = self.publisher.get_hot(category, limit=limit)
        
        if not notes:
            logger.warning("没有获取到内容")
            return
        
        logger.info(f"获取到 {len(notes)} 条内容")
        
        for i, note in enumerate(notes, 1):
            if self.interact_count >= self.daily_limit:
                logger.info("达到每日互动上限")
                break
            
            title = note.get('title', '无标题')
            note_id = note.get('id')
            
            logger.info(f"[{i}/{len(notes)}] {title}")
            
            # 模拟浏览时间
            self._random_delay(3, 10)
            
            # 决定是否互动
            if self._should_interact(note):
                action = self._select_action(note)
                
                if action == 'like':
                    if self.publisher.like_note(i):
                        self.interacted_today.add(note_id)
                        self.interact_count += 1
                        logger.info(f"  👍 点赞成功")
                
                elif action == 'favorite':
                    if self.publisher.favorite_note(i):
                        self.interacted_today.add(note_id)
                        self.interact_count += 1
                        logger.info(f"  ⭐ 收藏成功")
                
                # 互动后延迟
                self._random_delay(5, 15)
            else:
                logger.info(f"  ⏭️ 跳过")
        
        logger.info(f"浏览完成，今日互动: {self.interact_count}/{self.daily_limit}")
    
    def auto_comment(
        self,
        keywords: List[str],
        comments: List[str],
        limit: int = 10
    ):
        """
        自动评论
        
        Args:
            keywords: 搜索关键词
            comments: 评论内容库
            limit: 评论数量上限
        """
        logger.info(f"开始自动评论，关键词: {keywords}")
        
        for keyword in keywords:
            if self.interact_count >= self.daily_limit:
                break
            
            # 搜索相关内容
            notes = self.publisher.search_notes(keyword, limit=10)
            
            for i, note in enumerate(notes, 1):
                if self.interact_count >= self.daily_limit:
                    break
                
                note_id = note.get('id')
                if note_id in self.interacted_today:
                    continue
                
                # 随机选择评论
                comment = random.choice(comments)
                
                logger.info(f"评论 [{i}]: {comment[:30]}...")
                
                if self.publisher.comment_on_note(i, comment):
                    self.interacted_today.add(note_id)
                    self.interact_count += 1
                    logger.info("  💬 评论成功")
                
                self._random_delay(10, 30)
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "interacted_today": len(self.interacted_today),
            "daily_limit": self.daily_limit,
            "remaining": self.daily_limit - self.interact_count,
            "progress": f"{self.interact_count}/{self.daily_limit}"
        }


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书自动互动工具")
    parser.add_argument(
        "action",
        choices=["browse", "comment", "status"],
        help="操作类型"
    )
    parser.add_argument("--category", default="food", help="内容分类")
    parser.add_argument("--limit", type=int, default=20, help="数量限制")
    
    args = parser.parse_args()
    
    interactor = AutoInteractor()
    
    if args.action == "browse":
        interactor.browse_and_interact(
            category=args.category,
            limit=args.limit
        )
    
    elif args.action == "comment":
        # 示例评论库
        comments = [
            "很有用，收藏了！",
            "感谢分享，学到了",
            "mark一下",
            "这个真的好用",
            "已关注，期待更多",
        ]
        keywords = ["AI工具", "效率神器"]
        
        interactor.auto_comment(keywords, comments, limit=args.limit)
    
    elif args.action == "status":
        status = interactor.get_status()
        print(f"今日互动: {status['progress']}")
        print(f"剩余额度: {status['remaining']}")


if __name__ == "__main__":
    main()
