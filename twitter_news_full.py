#!/usr/bin/env python3
"""
Twitter 新闻聚合推送系统 - 完整版
整合：Twitter + RSS + 其他平台
每小时自动推送 10-20 条最新内容
"""

import subprocess
import json
import sys
import os
import time
import asyncio
import aiohttp
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, asdict, field
from pathlib import Path
import hashlib
import logging
from urllib.parse import urlparse


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_news.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class NewsItem:
    """统一的新闻条目数据结构"""
    id: str
    title: str
    content: str
    url: str
    author: str
    source: str  # twitter, rss, etc.
    source_name: str
    created_at: datetime
    published_at: str
    likes: int = 0
    retweets: int = 0
    replies: int = 0
    views: int = 0
    bookmarks: int = 0
    media: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    engagement_score: int = 0
    
    def __post_init__(self):
        """计算互动分数"""
        self.engagement_score = self.likes + self.retweets * 2 + self.replies * 3 + self.bookmarks


class TwitterFetcher:
    """Twitter 数据获取器"""
    
    def __init__(self):
        self.name = "Twitter"
    
    def _run_command(self, cmd: List[str]) -> Optional[Dict]:
        """运行 twitter-cli 命令"""
        try:
            full_cmd = ["twitter"] + cmd + ["--json"]
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                logger.error(f"Twitter 命令失败: {result.stderr}")
                return None
        except Exception as e:
            logger.error(f"Twitter 执行错误: {e}")
            return None
    
    def _parse_tweet(self, data: Dict) -> NewsItem:
        """解析推文为统一格式"""
        author = data.get("author", {})
        metrics = data.get("metrics", {})
        
        screen_name = author.get("screenName", "")
        tweet_id = data.get("id", "")
        url = f"https://x.com/{screen_name}/status/{tweet_id}" if screen_name and tweet_id else ""
        
        # 解析时间
        created_at = datetime.now()
        try:
            created_at = datetime.strptime(
                data.get("createdAt", ""), 
                "%a %b %d %H:%M:%S +0000 %Y"
            )
        except:
            pass
        
        # 处理媒体
        media_list = []
        for media in data.get("media", []):
            if media.get("type") == "photo":
                media_list.append(media.get("url", ""))
            elif media.get("type") == "video":
                media_list.append(media.get("url", ""))
        
        return NewsItem(
            id=tweet_id,
            title=data.get("text", "")[:100] + "..." if len(data.get("text", "")) > 100 else data.get("text", ""),
            content=data.get("text", ""),
            url=url,
            author=f"{author.get('name', '')} (@{screen_name})",
            source="twitter",
            source_name="Twitter",
            created_at=created_at,
            published_at=data.get("createdAt", ""),
            likes=metrics.get("likes", 0),
            retweets=metrics.get("retweets", 0),
            replies=metrics.get("replies", 0),
            views=metrics.get("views", 0),
            bookmarks=metrics.get("bookmarks", 0),
            media=media_list,
            tags=["twitter"]
        )
    
    def fetch(self, max_results: int = 10, feed_type: str = "for-you") -> List[NewsItem]:
        """获取推文"""
        cmd = ["feed", "--max", str(max_results)]
        if feed_type == "following":
            cmd.extend(["-t", "following"])
        
        result = self._run_command(cmd)
        if result and result.get("ok"):
            return [self._parse_tweet(t) for t in result.get("data", [])]
        return []
    
    def search(self, query: str, max_results: int = 10) -> List[NewsItem]:
        """搜索推文"""
        cmd = ["search", query, "--max", str(max_results)]
        result = self._run_command(cmd)
        if result and result.get("ok"):
            return [self._parse_tweet(t) for t in result.get("data", [])]
        return []


class RSSFetcher:
    """RSS 数据获取器"""
    
    def __init__(self):
        self.name = "RSS"
        self.feeds = []
    
    def add_feed(self, name: str, url: str, tags: List[str] = None):
        """添加 RSS 源"""
        self.feeds.append({
            "name": name,
            "url": url,
            "tags": tags or ["rss"]
        })
    
    def _parse_entry(self, entry, feed_info: Dict) -> Optional[NewsItem]:
        """解析 RSS 条目"""
        try:
            # 获取发布时间
            published = entry.get('published', entry.get('updated', ''))
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                created_at = datetime(*entry.published_parsed[:6])
            else:
                created_at = datetime.now()
            
            # 生成唯一 ID
            url = entry.get('link', '')
            item_id = hashlib.md5(f"{url}{published}".encode()).hexdigest()
            
            return NewsItem(
                id=item_id,
                title=entry.get('title', ''),
                content=entry.get('summary', entry.get('description', '')),
                url=url,
                author=entry.get('author', feed_info['name']),
                source="rss",
                source_name=feed_info['name'],
                created_at=created_at,
                published_at=published,
                tags=feed_info['tags']
            )
        except Exception as e:
            logger.error(f"解析 RSS 条目失败: {e}")
            return None
    
    def fetch(self, max_per_feed: int = 5) -> List[NewsItem]:
        """获取 RSS 内容"""
        all_items = []
        
        for feed_info in self.feeds:
            try:
                logger.info(f"📡 正在获取 RSS: {feed_info['name']}...")
                feed = feedparser.parse(feed_info['url'])
                
                for entry in feed.entries[:max_per_feed]:
                    item = self._parse_entry(entry, feed_info)
                    if item:
                        all_items.append(item)
                
                logger.info(f"   ✅ 获取到 {len(feed.entries[:max_per_feed])} 条")
            except Exception as e:
                logger.error(f"   ❌ RSS 获取失败 {feed_info['name']}: {e}")
        
        return all_items


class NewsAggregator:
    """新闻聚合器"""
    
    def __init__(self):
        self.fetchers = []
    
    def add_fetcher(self, fetcher):
        """添加数据获取器"""
        self.fetchers.append(fetcher)
    
    def fetch_all(self, hours: int = 1) -> List[NewsItem]:
        """从所有源获取并聚合"""
        all_items = []
        
        for fetcher in self.fetchers:
            try:
                items = fetcher.fetch()
                all_items.extend(items)
            except Exception as e:
                logger.error(f"获取器 {fetcher.name} 失败: {e}")
        
        # 去重
        seen_ids = set()
        unique_items = []
        for item in all_items:
            if item.id not in seen_ids:
                seen_ids.add(item.id)
                unique_items.append(item)
        
        # 过滤时间
        cutoff = datetime.now() - timedelta(hours=hours)
        filtered = [item for item in unique_items if item.created_at >= cutoff]
        
        # 按时间和互动排序
        filtered.sort(key=lambda x: (x.engagement_score, x.created_at), reverse=True)
        
        return filtered


class DiscordPusher:
    """Discord 推送器"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def format_item(self, item: NewsItem, index: int) -> str:
        """格式化新闻条目"""
        emoji_map = {
            "twitter": "🐦",
            "rss": "📰",
        }
        emoji = emoji_map.get(item.source, "📄")
        
        content = f"""**{emoji} [{index}] {item.source_name}**
**{item.title}**
🔗 {item.url}
👤 {item.author}
🕐 {item.published_at}

{item.content[:300]}{'...' if len(item.content) > 300 else ''}
"""
        
        # 添加媒体
        if item.media:
            content += f"\n🖼️ 媒体: {len(item.media)} 个\n"
            for media_url in item.media[:3]:
                content += f"• {media_url}\n"
        
        # 添加互动数据
        if item.source == "twitter":
            content += f"\n📊 ❤️{item.likes} 🔁{item.retweets} 💬{item.replies} 👁️{item.views} 🔖{item.bookmarks}"
        
        return content
    
    async def push(self, items: List[NewsItem], title: str = "新闻推送"):
        """推送到 Discord"""
        if not self.webhook_url or self.webhook_url == "YOUR_WEBHOOK_URL":
            logger.warning("⚠️ Discord Webhook 未配置")
            return
        
        # 发送标题
        await self._send_message(
            f"## 🔔 {title}\n"
            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"📊 共 {len(items)} 条新闻\n"
            f"{'─' * 40}"
        )
        
        # 发送每条新闻
        for i, item in enumerate(items, 1):
            message = self.format_item(item, i)
            await self._send_message(message)
            await asyncio.sleep(1)  # 避免频率限制
    
    async def _send_message(self, content: str):
        """发送消息"""
        payload = {
            "content": content[:2000],  # Discord 限制 2000 字符
            "allowed_mentions": {"parse": []}
        }
        
        try:
            async with self.session.post(self.webhook_url, json=payload) as resp:
                if resp.status == 429:  # 频率限制
                    retry_after = int(resp.headers.get('Retry-After', 5))
                    logger.warning(f"Discord 频率限制，等待 {retry_after} 秒")
                    await asyncio.sleep(retry_after)
                    return await self._send_message(content)
                resp.raise_for_status()
        except Exception as e:
            logger.error(f"Discord 发送失败: {e}")


class ConsolePusher:
    """控制台推送器"""
    
    def format_item(self, item: NewsItem, index: int) -> str:
        """格式化新闻条目"""
        lines = [
            f"\n{'='*70}",
            f"[{index}] {item.source_name} | {item.title[:60]}{'...' if len(item.title) > 60 else ''}",
            f"🔗 {item.url}",
            f"👤 {item.author}",
            f"🕐 {item.published_at}",
            f"{'-'*70}",
            f"{item.content[:400]}{'...' if len(item.content) > 400 else ''}",
        ]
        
        if item.media:
            lines.append(f"\n🖼️ 媒体:")
            for url in item.media[:3]:
                lines.append(f"   {url}")
        
        if item.source == "twitter":
            lines.append(f"\n📊 ❤️{item.likes} 🔁{item.retweets} 💬{item.replies} 👁️{item.views} 🔖{item.bookmarks}")
        
        lines.append(f"{'='*70}")
        
        return "\n".join(lines)
    
    def push(self, items: List[NewsItem], title: str = "新闻推送"):
        """输出到控制台"""
        print(f"\n{'#'*70}")
        print(f"# 🔔 {title}")
        print(f"# ⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"# 📊 共 {len(items)} 条新闻")
        print(f"{'#'*70}")
        
        for i, item in enumerate(items, 1):
            print(self.format_item(item, i))


class NewsBot:
    """新闻机器人主类"""
    
    def __init__(self, discord_webhook: Optional[str] = None):
        self.aggregator = NewsAggregator()
        self.console_pusher = ConsolePusher()
        self.discord_webhook = discord_webhook
        
        # 配置数据源
        self._setup_sources()
    
    def _setup_sources(self):
        """配置数据源"""
        # Twitter
        twitter = TwitterFetcher()
        self.aggregator.add_fetcher(twitter)
        
        # RSS 源
        rss = RSSFetcher()
        # 添加一些 AI/科技相关的 RSS 源
        rss.add_feed("Hacker News", "https://news.ycombinator.com/rss", ["tech", "hn"])
        rss.add_feed("AI News", "https://www.artificialintelligence-news.com/feed/", ["ai"])
        rss.add_feed("MIT Tech Review", "https://www.technologyreview.com/feed/", ["tech"])
        rss.add_feed("VentureBeat AI", "https://venturebeat.com/category/ai/feed/", ["ai"])
        self.aggregator.add_fetcher(rss)
    
    async def run_once(self, max_items: int = 20, hours: int = 1) -> List[NewsItem]:
        """运行一次抓取"""
        logger.info(f"🚀 开始抓取新闻... 目标: {max_items} 条, 时间范围: {hours} 小时")
        
        items = self.aggregator.fetch_all(hours)
        items = items[:max_items]
        
        if items:
            # 控制台推送
            self.console_pusher.push(items)
            
            # Discord 推送
            if self.discord_webhook:
                async with DiscordPusher(self.discord_webhook) as discord:
                    await discord.push(items)
            
            # 保存到文件
            self._save_items(items)
        else:
            logger.warning("⚠️ 未获取到新闻")
        
        return items
    
    def _save_items(self, items: List[NewsItem]):
        """保存到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"news_{timestamp}.json"
        
        data = {
            "fetch_time": datetime.now().isoformat(),
            "count": len(items),
            "items": [asdict(item) for item in items]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"💾 已保存到: {filename}")
    
    async def run_scheduler(self, interval_minutes: int = 60, max_items: int = 20):
        """定时运行"""
        logger.info(f"🤖 新闻机器人已启动")
        logger.info(f"   每 {interval_minutes} 分钟抓取一次")
        logger.info(f"   每次获取 {max_items} 条新闻")
        
        try:
            while True:
                await self.run_once(max_items)
                
                next_run = datetime.now() + timedelta(minutes=interval_minutes)
                logger.info(f"⏳ 下次运行: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                
                await asyncio.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            logger.info("👋 机器人已停止")


def load_config():
    """加载配置"""
    config = {
        'discord_webhook': None,
        'max_items': 15,
        'hours': 1,
        'interval': 60
    }
    
    # 从环境变量加载
    if 'DISCORD_WEBHOOK_URL' in os.environ:
        config['discord_webhook'] = os.environ['DISCORD_WEBHOOK_URL']
    
    # 从 .env 文件加载
    env_file = Path(__file__).parent / '.env.discord'
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if key == 'DISCORD_WEBHOOK_URL':
                        config['discord_webhook'] = value
    
    return config


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='新闻聚合推送系统')
    parser.add_argument('--max', '-n', type=int, default=15, help='每次获取数量 (默认15)')
    parser.add_argument('--hours', type=int, default=1, help='时间范围小时数 (默认1)')
    parser.add_argument('--interval', '-i', type=int, default=60, help='定时间隔分钟 (默认60)')
    parser.add_argument('--once', action='store_true', help='只运行一次')
    parser.add_argument('--daemon', '-d', action='store_true', help='后台运行')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    
    # 创建机器人
    bot = NewsBot(discord_webhook=config['discord_webhook'])
    
    # 运行
    if args.once:
        await bot.run_once(max_items=args.max, hours=args.hours)
    elif args.daemon:
        await bot.run_scheduler(interval_minutes=args.interval, max_items=args.max)
    else:
        await bot.run_once(max_items=args.max, hours=args.hours)


if __name__ == "__main__":
    asyncio.run(main())
