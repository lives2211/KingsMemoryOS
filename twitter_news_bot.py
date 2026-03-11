#!/usr/bin/env python3
"""
Twitter 新闻聚合推送机器人
每小时自动获取 10-20 条最新推文，包含详细内容和链接
支持：首页推荐、关注时间线、关键词搜索、特定用户
推送渠道：Discord、Telegram、控制台
"""

import subprocess
import json
import sys
import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib


@dataclass
class Tweet:
    """推文数据结构"""
    id: str
    url: str
    text: str
    author_name: str
    author_screen_name: str
    author_verified: bool
    created_at: str
    likes: int
    retweets: int
    replies: int
    views: int
    bookmarks: int
    media: List[str]
    urls: List[str]
    is_retweet: bool
    quoted_text: Optional[str] = None
    quoted_author: Optional[str] = None
    lang: str = ""
    
    @property
    def short_text(self) -> str:
        """获取短文本（前200字符）"""
        if len(self.text) > 200:
            return self.text[:200] + "..."
        return self.text
    
    @property
    def engagement_score(self) -> int:
        """计算互动分数"""
        return self.likes + self.retweets * 2 + self.replies * 3 + self.bookmarks


class TwitterFetcher:
    """Twitter 数据获取器"""
    
    def __init__(self):
        self.cache_dir = Path.home() / ".twitter_news_cache"
        self.cache_dir.mkdir(exist_ok=True)
    
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
                print(f"命令失败: {result.stderr}", file=sys.stderr)
                return None
        except Exception as e:
            print(f"执行错误: {e}", file=sys.stderr)
            return None
    
    def _parse_tweet(self, data: Dict) -> Tweet:
        """解析推文数据"""
        author = data.get("author", {})
        metrics = data.get("metrics", {})
        
        # 构建推文链接
        screen_name = author.get("screenName", "")
        tweet_id = data.get("id", "")
        url = f"https://x.com/{screen_name}/status/{tweet_id}" if screen_name and tweet_id else ""
        
        # 处理引用推文
        quoted = data.get("quotedTweet")
        quoted_text = None
        quoted_author = None
        if quoted:
            quoted_author_info = quoted.get("author", {})
            quoted_text = quoted.get("text", "")
            quoted_author = f"{quoted_author_info.get('name', '')} (@{quoted_author_info.get('screenName', '')})"
        
        # 处理媒体
        media_list = []
        for media in data.get("media", []):
            if media.get("type") == "photo":
                media_list.append(f"[图片] {media.get('url', '')}")
            elif media.get("type") == "video":
                media_list.append(f"[视频] {media.get('url', '')}")
        
        return Tweet(
            id=tweet_id,
            url=url,
            text=data.get("text", ""),
            author_name=author.get("name", ""),
            author_screen_name=screen_name,
            author_verified=author.get("verified", False),
            created_at=data.get("createdAt", ""),
            likes=metrics.get("likes", 0),
            retweets=metrics.get("retweets", 0),
            replies=metrics.get("replies", 0),
            views=metrics.get("views", 0),
            bookmarks=metrics.get("bookmarks", 0),
            media=media_list,
            urls=data.get("urls", []),
            is_retweet=data.get("isRetweet", False),
            quoted_text=quoted_text,
            quoted_author=quoted_author,
            lang=data.get("lang", "")
        )
    
    def fetch_feed(self, max_results: int = 10, feed_type: str = "for-you") -> List[Tweet]:
        """获取首页时间线"""
        cmd = ["feed", "--max", str(max_results)]
        if feed_type == "following":
            cmd.extend(["-t", "following"])
        
        result = self._run_command(cmd)
        if result and result.get("ok"):
            return [self._parse_tweet(t) for t in result.get("data", [])]
        return []
    
    def search(self, query: str, max_results: int = 10) -> List[Tweet]:
        """搜索推文"""
        cmd = ["search", query, "--max", str(max_results)]
        result = self._run_command(cmd)
        if result and result.get("ok"):
            return [self._parse_tweet(t) for t in result.get("data", [])]
        return []
    
    def fetch_user(self, screen_name: str, max_results: int = 10) -> List[Tweet]:
        """获取用户推文"""
        cmd = ["user-posts", screen_name, "--max", str(max_results)]
        result = self._run_command(cmd)
        if result and result.get("ok"):
            return [self._parse_tweet(t) for t in result.get("data", [])]
        return []
    
    def deduplicate(self, tweets: List[Tweet]) -> List[Tweet]:
        """去重（基于推文ID）"""
        seen = set()
        unique = []
        for tweet in tweets:
            if tweet.id not in seen:
                seen.add(tweet.id)
                unique.append(tweet)
        return unique
    
    def filter_by_time(self, tweets: List[Tweet], hours: int = 1) -> List[Tweet]:
        """过滤最近 N 小时的推文"""
        cutoff = datetime.now() - timedelta(hours=hours)
        filtered = []
        for tweet in tweets:
            try:
                # 解析时间字符串
                tweet_time = datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y")
                if tweet_time >= cutoff:
                    filtered.append(tweet)
            except:
                # 如果解析失败，保留推文
                filtered.append(tweet)
        return filtered
    
    def sort_by_engagement(self, tweets: List[Tweet]) -> List[Tweet]:
        """按互动分数排序"""
        return sorted(tweets, key=lambda x: x.engagement_score, reverse=True)


class NewsAggregator:
    """新闻聚合器 - 整合多个数据源"""
    
    def __init__(self, fetcher: TwitterFetcher):
        self.fetcher = fetcher
        self.sources = []
    
    def add_source(self, name: str, fetch_func: Callable[[], List[Tweet]], priority: int = 1):
        """添加数据源"""
        self.sources.append({
            "name": name,
            "fetch": fetch_func,
            "priority": priority
        })
    
    def fetch_all(self, max_total: int = 20, hours: int = 1) -> List[Tweet]:
        """从所有数据源获取并聚合"""
        all_tweets = []
        
        # 按优先级排序
        sorted_sources = sorted(self.sources, key=lambda x: x["priority"])
        
        for source in sorted_sources:
            try:
                print(f"📡 正在获取: {source['name']}...")
                tweets = source["fetch"]()
                print(f"   ✅ 获取到 {len(tweets)} 条")
                all_tweets.extend(tweets)
            except Exception as e:
                print(f"   ❌ 失败: {e}")
        
        # 去重
        all_tweets = self.fetcher.deduplicate(all_tweets)
        
        # 过滤时间
        all_tweets = self.fetcher.filter_by_time(all_tweets, hours)
        
        # 按互动排序
        all_tweets = self.fetcher.sort_by_engagement(all_tweets)
        
        # 限制数量
        return all_tweets[:max_total]


class DiscordPusher:
    """Discord 推送器"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
    
    def format_tweet(self, tweet: Tweet, index: int = 0) -> str:
        """格式化推文为 Discord 消息"""
        verified = "✅" if tweet.author_verified else ""
        
        content = f"""**[{index}] {tweet.author_name} {verified}** (@{tweet.author_screen_name})
🔗 {tweet.url}
🕐 {tweet.created_at}

{tweet.text}

"""
        
        # 引用推文
        if tweet.quoted_text:
            content += f"📎 **引用**: {tweet.quoted_author}\n> {tweet.quoted_text[:150]}{'...' if len(tweet.quoted_text) > 150 else ''}\n\n"
        
        # 媒体
        if tweet.media:
            content += "🖼️ **媒体**:\n"
            for m in tweet.media[:3]:  # 最多显示3个媒体
                content += f"• {m}\n"
            content += "\n"
        
        # 外部链接
        if tweet.urls:
            content += "🔗 **链接**:\n"
            for url in tweet.urls[:3]:
                content += f"• {url}\n"
            content += "\n"
        
        # 互动数据
        content += f"📊 ❤️{tweet.likes} 🔁{tweet.retweets} 💬{tweet.replies} 👁️{tweet.views} 🔖{tweet.bookmarks}"
        
        return content
    
    def push(self, tweets: List[Tweet], title: str = "Twitter 新闻推送"):
        """推送到 Discord"""
        if not self.webhook_url:
            print("⚠️ 未配置 Discord Webhook")
            return
        
        # 发送标题
        self._send_to_discord(f"## 🐦 {title}\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}\n共 {len(tweets)} 条推文")
        
        # 发送每条推文
        for i, tweet in enumerate(tweets, 1):
            message = self.format_tweet(tweet, i)
            self._send_to_discord(message)
            time.sleep(0.5)  # 避免频率限制
    
    def _send_to_discord(self, content: str):
        """发送消息到 Discord"""
        import requests
        
        payload = {
            "content": content[:2000]  # Discord 限制 2000 字符
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"Discord 发送失败: {e}")


class ConsolePusher:
    """控制台推送器（用于测试）"""
    
    def format_tweet(self, tweet: Tweet, index: int = 0) -> str:
        """格式化推文"""
        verified = "✓" if tweet.author_verified else ""
        
        lines = [
            f"\n{'='*70}",
            f"[{index}] {tweet.author_name} {verified} (@{tweet.author_screen_name})",
            f"🔗 {tweet.url}",
            f"🕐 {tweet.created_at}",
            f"{'-'*70}",
            f"{tweet.text}",
        ]
        
        if tweet.quoted_text:
            lines.extend([
                f"\n📎 引用: {tweet.quoted_author}",
                f"   {tweet.quoted_text[:100]}{'...' if len(tweet.quoted_text) > 100 else ''}"
            ])
        
        if tweet.media:
            lines.append(f"\n🖼️ 媒体:")
            for m in tweet.media:
                lines.append(f"   {m}")
        
        if tweet.urls:
            lines.append(f"\n🔗 外部链接:")
            for url in tweet.urls:
                lines.append(f"   {url}")
        
        lines.extend([
            f"\n📊 互动: ❤️{tweet.likes} 🔁{tweet.retweets} 💬{tweet.replies} 👁️{tweet.views} 🔖{tweet.bookmarks}",
            f"{'='*70}"
        ])
        
        return "\n".join(lines)
    
    def push(self, tweets: List[Tweet], title: str = "Twitter 新闻推送"):
        """输出到控制台"""
        print(f"\n{'#'*70}")
        print(f"# 🐦 {title}")
        print(f"# ⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"# 📊 共 {len(tweets)} 条推文")
        print(f"{'#'*70}")
        
        for i, tweet in enumerate(tweets, 1):
            print(self.format_tweet(tweet, i))


class TwitterNewsBot:
    """Twitter 新闻机器人主类"""
    
    def __init__(self, discord_webhook: Optional[str] = None):
        self.fetcher = TwitterFetcher()
        self.aggregator = NewsAggregator(self.fetcher)
        self.console_pusher = ConsolePusher()
        self.discord_pusher = DiscordPusher(discord_webhook) if discord_webhook else None
        
        # 配置数据源
        self._setup_sources()
    
    def _setup_sources(self):
        """配置数据源"""
        # 首页推荐（优先级 1）
        self.aggregator.add_source(
            "首页推荐",
            lambda: self.fetcher.fetch_feed(max_results=10, feed_type="for-you"),
            priority=1
        )
        
        # 关注时间线（优先级 2）
        self.aggregator.add_source(
            "关注时间线",
            lambda: self.fetcher.fetch_feed(max_results=10, feed_type="following"),
            priority=2
        )
    
    def add_search_source(self, query: str, max_results: int = 10):
        """添加搜索数据源"""
        self.aggregator.add_source(
            f"搜索: {query}",
            lambda: self.fetcher.search(query, max_results),
            priority=3
        )
    
    def add_user_source(self, screen_name: str, max_results: int = 10):
        """添加用户数据源"""
        self.aggregator.add_source(
            f"用户: @{screen_name}",
            lambda: self.fetcher.fetch_user(screen_name, max_results),
            priority=3
        )
    
    def run_once(self, max_tweets: int = 20, hours: int = 1) -> List[Tweet]:
        """运行一次抓取"""
        print(f"\n🚀 开始抓取 Twitter 新闻...")
        print(f"   目标: {max_tweets} 条")
        print(f"   时间范围: 最近 {hours} 小时\n")
        
        tweets = self.aggregator.fetch_all(max_tweets, hours)
        
        if tweets:
            # 推送到控制台
            self.console_pusher.push(tweets)
            
            # 推送到 Discord
            if self.discord_pusher:
                self.discord_pusher.push(tweets)
            
            # 保存到文件
            self._save_tweets(tweets)
        else:
            print("⚠️ 未获取到推文")
        
        return tweets
    
    def _save_tweets(self, tweets: List[Tweet]):
        """保存推文到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"twitter_news_{timestamp}.json"
        
        data = {
            "fetch_time": datetime.now().isoformat(),
            "count": len(tweets),
            "tweets": [asdict(t) for t in tweets]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {filename}")
    
    def run_scheduler(self, interval_minutes: int = 60, max_tweets: int = 20):
        """定时运行"""
        print(f"🤖 Twitter 新闻机器人已启动")
        print(f"   每 {interval_minutes} 分钟抓取一次")
        print(f"   每次获取 {max_tweets} 条推文")
        print(f"   按 Ctrl+C 停止\n")
        
        try:
            while True:
                self.run_once(max_tweets)
                
                next_run = datetime.now() + timedelta(minutes=interval_minutes)
                print(f"\n⏳ 下次运行: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   等待 {interval_minutes} 分钟...\n")
                
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("\n\n👋 机器人已停止")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Twitter 新闻聚合推送机器人')
    parser.add_argument('--discord-webhook', help='Discord Webhook URL')
    parser.add_argument('--max', '-n', type=int, default=15, help='每次获取推文数量 (默认15)')
    parser.add_argument('--hours', type=int, default=1, help='时间范围小时数 (默认1)')
    parser.add_argument('--interval', '-i', type=int, default=60, help='定时运行间隔分钟数 (默认60)')
    parser.add_argument('--search', '-s', action='append', help='添加搜索关键词')
    parser.add_argument('--user', '-u', action='append', help='添加关注用户')
    parser.add_argument('--once', action='store_true', help='只运行一次')
    parser.add_argument('--daemon', '-d', action='store_true', help='后台定时运行')
    
    args = parser.parse_args()
    
    # 创建机器人
    bot = TwitterNewsBot(discord_webhook=args.discord_webhook)
    
    # 添加搜索源
    if args.search:
        for query in args.search:
            bot.add_search_source(query, max_results=10)
    
    # 添加用户源
    if args.user:
        for user in args.user:
            bot.add_user_source(user, max_results=10)
    
    # 运行模式
    if args.once:
        bot.run_once(max_tweets=args.max, hours=args.hours)
    elif args.daemon:
        bot.run_scheduler(interval_minutes=args.interval, max_tweets=args.max)
    else:
        # 默认运行一次
        bot.run_once(max_tweets=args.max, hours=args.hours)


if __name__ == "__main__":
    main()
