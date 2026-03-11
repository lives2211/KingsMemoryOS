#!/usr/bin/env python3
"""
Twitter Discord 推送器 - 完整版
包含完整推文链接、标题、详细内容
"""

import json
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
import os
from pathlib import Path


@dataclass
class Tweet:
    """推文数据结构"""
    id: str
    url: str  # 完整推文链接
    title: str  # 推文题目（前100字符）
    content: str  # 完整内容
    author_name: str
    author_screen_name: str
    author_verified: bool
    created_at: str
    likes: int = 0
    retweets: int = 0
    replies: int = 0
    views: int = 0
    bookmarks: int = 0
    media: List[str] = field(default_factory=list)
    urls: List[str] = field(default_factory=list)
    is_retweet: bool = False
    quoted_text: Optional[str] = None
    quoted_author: Optional[str] = None
    quoted_url: Optional[str] = None


class TwitterDiscordPusher:
    """Twitter Discord 推送器"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def format_tweet_embed(self, tweet: Tweet, index: int) -> dict:
        """格式化推文为 Discord Embed"""
        
        # 作者信息
        verified_emoji = "✅" if tweet.author_verified else ""
        author_text = f"{tweet.author_name} {verified_emoji} (@{tweet.author_screen_name})"
        
        # 构建描述
        description = tweet.content
        if len(description) > 2000:
            description = description[:1997] + "..."
        
        # 构建字段
        fields = []
        
        # 互动数据
        fields.append({
            "name": "📊 互动数据",
            "value": f"❤️ {tweet.likes} | 🔁 {tweet.retweets} | 💬 {tweet.replies} | 👁️ {tweet.views} | 🔖 {tweet.bookmarks}",
            "inline": True
        })
        
        # 媒体
        if tweet.media:
            media_text = "\n".join([f"[媒体 {i+1}]({url})" for i, url in enumerate(tweet.media[:3])])
            fields.append({
                "name": f"🖼️ 媒体 ({len(tweet.media)} 个)",
                "value": media_text,
                "inline": False
            })
        
        # 外部链接
        if tweet.urls:
            links_text = "\n".join([f"[链接 {i+1}]({url})" for i, url in enumerate(tweet.urls[:3])])
            fields.append({
                "name": f"🔗 外部链接 ({len(tweet.urls)} 个)",
                "value": links_text,
                "inline": False
            })
        
        # 引用推文
        if tweet.quoted_text:
            quoted_content = tweet.quoted_text[:500]
            if len(tweet.quoted_text) > 500:
                quoted_content += "..."
            
            quoted_value = f"**{tweet.quoted_author}**\n{quoted_content}"
            if tweet.quoted_url:
                quoted_value += f"\n[查看引用推文]({tweet.quoted_url})"
            
            fields.append({
                "name": "📎 引用推文",
                "value": quoted_value,
                "inline": False
            })
        
        # 构建 embed
        embed = {
            "title": f"🐦 {tweet.title}",
            "description": description,
            "url": tweet.url,  # 点击标题跳转的链接
            "color": 1942002,  # Twitter 蓝色
            "author": {
                "name": author_text,
                "url": f"https://x.com/{tweet.author_screen_name}",
                "icon_url": f"https://unavatar.io/twitter/{tweet.author_screen_name}"
            },
            "fields": fields,
            "footer": {
                "text": f"推文 ID: {tweet.id} | {tweet.created_at}"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # 如果有媒体，使用第一张作为缩略图
        if tweet.media:
            embed["image"] = {"url": tweet.media[0]}
        
        return embed
    
    async def send_tweet(self, tweet: Tweet, index: int):
        """发送单条推文"""
        embed = self.format_tweet_embed(tweet, index)
        
        payload = {
            "content": f"**[{index}]** 🔗 [查看原文]({tweet.url})",
            "embeds": [embed],
            "allowed_mentions": {"parse": []}
        }
        
        await self._send_request(payload)
        await asyncio.sleep(1)  # 避免频率限制
    
    async def send_summary(self, count: int):
        """发送摘要"""
        payload = {
            "content": f"""## 🔔 Twitter 新闻推送

⏰ **时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
📊 **数量**: {count} 条推文
{'─' * 40}""",
            "allowed_mentions": {"parse": []}
        }
        
        await self._send_request(payload)
    
    async def _send_request(self, payload: dict):
        """发送请求"""
        try:
            async with self.session.post(self.webhook_url, json=payload) as resp:
                if resp.status == 429:  # 频率限制
                    retry_after = int(resp.headers.get('Retry-After', 5))
                    print(f"⚠️ Discord 频率限制，等待 {retry_after} 秒")
                    await asyncio.sleep(retry_after)
                    return await self._send_request(payload)
                
                if resp.status not in [200, 204]:
                    text = await resp.text()
                    print(f"❌ Discord 发送失败: {resp.status} - {text}")
                else:
                    print(f"✅ 消息发送成功")
                    
        except Exception as e:
            print(f"❌ Discord 请求失败: {e}")
    
    async def push_tweets(self, tweets: List[Tweet], title: str = "Twitter 新闻推送"):
        """推送多条推文"""
        if not self.webhook_url or "YOUR_WEBHOOK" in self.webhook_url:
            print("⚠️ Discord Webhook 未配置，跳过推送")
            return
        
        print(f"\n📤 正在推送到 Discord...")
        
        # 发送摘要
        await self.send_summary(len(tweets))
        await asyncio.sleep(1)
        
        # 发送每条推文
        for i, tweet in enumerate(tweets, 1):
            print(f"  正在发送 [{i}/{len(tweets)}]: {tweet.title[:50]}...")
            await self.send_tweet(tweet, i)
        
        print(f"✅ Discord 推送完成！共 {len(tweets)} 条")


class TweetFetcher:
    """推文获取器"""
    
    def __init__(self):
        pass
    
    def fetch_from_json(self, json_file: str) -> List[Tweet]:
        """从 JSON 文件加载推文"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tweets = []
        for item in data.get('items', []):
            if item.get('source') == 'twitter':
                tweet = Tweet(
                    id=item['id'],
                    url=item['url'],
                    title=item['title'],
                    content=item['content'],
                    author_name=item['author'].split(' (@')[0] if ' (@' in item['author'] else item['author'],
                    author_screen_name=item['author'].split('(@')[1].rstrip(')') if '(@' in item['author'] else '',
                    author_verified=item.get('author_verified', False),
                    created_at=item['published_at'],
                    likes=item.get('likes', 0),
                    retweets=item.get('retweets', 0),
                    replies=item.get('replies', 0),
                    views=item.get('views', 0),
                    bookmarks=item.get('bookmarks', 0),
                    media=item.get('media', []),
                    urls=item.get('urls', []),
                    is_retweet=item.get('is_retweet', False),
                    quoted_text=item.get('quoted_text'),
                    quoted_author=item.get('quoted_author'),
                    quoted_url=item.get('quoted_url')
                )
                tweets.append(tweet)
        
        return tweets


def load_webhook_url() -> Optional[str]:
    """加载 Webhook URL"""
    # 从环境变量
    if 'DISCORD_WEBHOOK_URL' in os.environ:
        return os.environ['DISCORD_WEBHOOK_URL']
    
    # 从配置文件
    env_file = Path(__file__).parent / '.env.discord'
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith('DISCORD_WEBHOOK_URL='):
                    return line.split('=', 1)[1].strip()
    
    return None


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Discord 推文推送')
    parser.add_argument('--webhook', help='Discord Webhook URL')
    parser.add_argument('--file', '-f', help='JSON 文件路径')
    
    args = parser.parse_args()
    
    # 获取 Webhook URL
    webhook_url = args.webhook or load_webhook_url()
    
    if not webhook_url:
        print("❌ 错误: 未配置 Discord Webhook URL")
        print("\n配置方式:")
        print("1. 运行: python3 discord_webhook_setup.py")
        print("2. 或设置环境变量: export DISCORD_WEBHOOK_URL=...")
        print("3. 或使用 --webhook 参数")
        return
    
    # 获取 JSON 文件
    json_file = args.file
    if not json_file:
        # 查找最新的 news_*.json 文件
        import glob
        files = sorted(glob.glob('news_*.json'), reverse=True)
        if files:
            json_file = files[0]
            print(f"📁 使用最新文件: {json_file}")
    
    if not json_file or not Path(json_file).exists():
        print("❌ 错误: 未找到 JSON 文件")
        print("请先运行: python3 twitter_news_full.py --once --max 10")
        return
    
    # 加载推文
    fetcher = TweetFetcher()
    tweets = fetcher.fetch_from_json(json_file)
    
    if not tweets:
        print("⚠️ 未找到 Twitter 推文")
        return
    
    print(f"📊 找到 {len(tweets)} 条推文")
    
    # 推送到 Discord
    async with TwitterDiscordPusher(webhook_url) as pusher:
        await pusher.push_tweets(tweets)


if __name__ == "__main__":
    asyncio.run(main())
