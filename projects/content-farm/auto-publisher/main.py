#!/usr/bin/env python3
"""
小红书自动发布系统 - 主入口
整合内容生成、卡片渲染、浏览器自动化发布
"""

import asyncio
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from loguru import logger
import yaml

# 添加core目录到路径
sys.path.insert(0, str(Path(__file__).parent / "core"))

from content_loader import ContentLoader, XHSNote
from card_generator import CardGenerator, CardConfig
from publisher import XHSPublisher, PublishConfig
from scheduler import PublishScheduler


class XHSAutoPublisher:
    """小红书自动发布系统"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.content_loader = ContentLoader(self.config['content']['source_dir'])
        self.card_generator = CardGenerator("./card-renderer")
        self.scheduler: Optional[PublishScheduler] = None
        self.publisher: Optional[XHSPublisher] = None
        
        # 初始化调度器
        account_config = self.config['accounts']['account_1']
        self.scheduler = PublishScheduler(account_config)
        
        # 设置日志
        self._setup_logging()
    
    def _load_config(self, path: str) -> dict:
        """加载配置"""
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _setup_logging(self):
        """设置日志"""
        log_config = self.config.get('logging', {})
        log_level = log_config.get('level', 'INFO')
        log_file = log_config.get('file', 'logs/auto-publisher.log')
        
        # 创建日志目录
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # 配置日志
        logger.remove()
        logger.add(sys.stderr, level=log_level)
        logger.add(
            log_file,
            level=log_level,
            rotation=log_config.get('max_size', '10MB'),
            retention=log_config.get('backup_count', 7)
        )
    
    async def publish_single(
        self,
        note: XHSNote,
        headless: bool = False,
        skip_publish: bool = False
    ) -> bool:
        """
        发布单篇笔记
        
        Args:
            note: 笔记内容
            headless: 是否无头模式
            skip_publish: 跳过实际发布（仅生成卡片）
            
        Returns:
            是否成功
        """
        try:
            logger.info(f"处理笔记: {note.title}")
            
            # 1. 生成卡片
            logger.info("生成卡片...")
            img_config = self.config['content']['image_generation']
            card_config = CardConfig(
                theme=img_config['theme'],
                mode=img_config['mode'],
                width=img_config['width'],
                height=img_config['height'],
                dpr=img_config['dpr']
            )
            
            output_dir = f"./output/{datetime.now().strftime('%Y%m%d')}"
            cards = self.card_generator.generate_from_content(
                title=note.title,
                content=note.content,
                output_dir=output_dir,
                config=card_config
            )
            
            logger.info(f"生成 {len(cards)} 张卡片")
            
            if skip_publish:
                logger.info("跳过发布（仅生成卡片）")
                return True
            
            # 2. 启动浏览器并发布
            logger.info("启动浏览器...")
            self.publisher = XHSPublisher()
            await self.publisher.launch_browser(headless=headless)
            
            # 检查/登录
            if not await self.publisher.check_login():
                logger.info("需要登录，请扫码...")
                await self.publisher.login()
            
            # 3. 发布
            publish_config = PublishConfig(
                title=note.title,
                content=note.content,
                images=cards,
                hashtags=note.hashtags
            )
            
            success = await self.publisher.publish(publish_config)
            
            if success:
                self.scheduler.record_publish()
                logger.info("✅ 发布成功!")
            else:
                logger.error("❌ 发布失败")
            
            return success
            
        except Exception as e:
            logger.error(f"发布异常: {e}")
            return False
        finally:
            if self.publisher:
                await self.publisher.close()
    
    async def publish_batch(
        self,
        date: Optional[str] = None,
        limit: int = 3,
        headless: bool = False
    ):
        """
        批量发布
        
        Args:
            date: 指定日期，默认为今天
            limit: 最大发布数量
            headless: 是否无头模式
        """
        # 加载笔记
        notes = self.content_loader.load_notes_by_date(date, limit)
        
        if not notes:
            logger.warning("没有可发布的笔记")
            return
        
        logger.info(f"计划发布 {len(notes)} 篇笔记")
        
        # 依次发布
        success_count = 0
        for i, note in enumerate(notes, 1):
            logger.info(f"\n[{i}/{len(notes)}] 发布: {note.title}")
            
            # 检查是否应该发布
            if not self.scheduler.should_publish_now():
                next_time = self.scheduler.get_next_publish_time()
                if next_time:
                    logger.info(f"等待下次发布时间: {next_time.strftime('%Y-%m-%d %H:%M')}")
                    wait_seconds = (next_time - datetime.now()).total_seconds()
                    await asyncio.sleep(wait_seconds)
            
            success = await self.publish_single(note, headless=headless)
            if success:
                success_count += 1
            
            # 发布间隔
            if i < len(notes):
                delay = self.scheduler.get_random_delay()
                logger.info(f"等待 {delay/60:.1f} 分钟后发布下一篇...")
                await asyncio.sleep(delay)
        
        logger.info(f"\n批量发布完成: {success_count}/{len(notes)} 成功")
    
    def preview_schedule(self, notes_count: int = 5):
        """预览发布计划"""
        tasks = self.scheduler.calculate_publish_schedule(notes_count)
        
        print("\n📅 发布计划预览:")
        print("-" * 50)
        
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        
        print("-" * 50)
    
    def status(self):
        """显示系统状态"""
        print("\n📊 小红书自动发布系统状态:")
        print("-" * 50)
        
        # 内容状态
        dates = self.content_loader.list_available_dates()
        print(f"📁 内容日期: {len(dates)} 天")
        if dates:
            latest = dates[0]
            count = self.content_loader.get_notes_count_by_date(latest)
            print(f"   最新 ({latest}): {count} 篇笔记")
        
        # 调度器状态
        if self.scheduler:
            status = self.scheduler.get_status()
            print(f"\n⏰ 发布状态:")
            print(f"   今日已发布: {status['published_today']}/{status['max_daily_posts']}")
            if status['last_publish_time']:
                print(f"   上次发布: {status['last_publish_time']}")
            if status['next_publish_time']:
                print(f"   下次发布: {status['next_publish_time']}")
        
        print("-" * 50)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="小红书自动发布系统")
    parser.add_argument(
        "action",
        choices=["status", "preview", "publish", "batch", "login"],
        help="操作类型"
    )
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--limit", type=int, default=3, help="最大发布数量")
    parser.add_argument("--headless", action="store_true", help="无头模式")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不实际发布")
    
    args = parser.parse_args()
    
    # 创建系统实例
    app = XHSAutoPublisher()
    
    if args.action == "status":
        app.status()
    
    elif args.action == "preview":
        app.preview_schedule(args.limit)
    
    elif args.action == "publish":
        # 发布单篇（第一篇）
        notes = app.content_loader.load_notes_by_date(args.date, 1)
        if notes:
            asyncio.run(app.publish_single(
                notes[0],
                headless=args.headless,
                skip_publish=args.dry_run
            ))
        else:
            print("没有可发布的笔记")
    
    elif args.action == "batch":
        # 批量发布
        asyncio.run(app.publish_batch(
            date=args.date,
            limit=args.limit,
            headless=args.headless
        ))
    
    elif args.action == "login":
        # 仅登录
        async def do_login():
            publisher = XHSPublisher()
            await publisher.launch_browser(headless=False)
            await publisher.login()
            await publisher.close()
        
        asyncio.run(do_login())


if __name__ == "__main__":
    main()
