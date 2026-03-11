#!/usr/bin/env python3
"""
Twitter Discord 推送器 - 中文版
自动翻译英文内容为中文
"""

import json
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
import os
from pathlib import Path
import re


@dataclass
class Tweet:
    """推文数据结构"""
    id: str
    url: str
    title: str
    content: str
    author_name: str
    author_screen_name: str
    author_verified: bool
    created_at: str
    content_zh: str = ""  # 中文翻译
    likes: int = 0
    retweets: int = 0
    replies: int = 0
    views: int = 0
    bookmarks: int = 0
    media: List[str] = field(default_factory=list)
    urls: List[str] = field(default_factory=list)
    is_retweet: bool = False
    quoted_text: Optional[str] = None
    quoted_text_zh: Optional[str] = None
    quoted_author: Optional[str] = None
    source: str = "twitter"
    source_name: str = "Twitter"


class Translator:
    """简单翻译器（使用规则翻译常用词）"""
    
    COMMON_WORDS = {
        # 常见 Twitter/科技词汇
        'AI': '人工智能',
        'agent': '智能体',
        'launch': '发布',
        'launched': '发布了',
        'new': '新的',
        'toolkit': '工具包',
        'connect': '连接',
        'exchange': '交易所',
        'trading': '交易',
        'open-source': '开源',
        'build': '构建',
        'today': '今天',
        'announced': '宣布',
        'update': '更新',
        'feature': '功能',
        'beta': '测试版',
        'official': '官方',
        'support': '支持',
        'available': '可用',
        'now': '现在',
        'free': '免费',
        'access': '访问',
        'public': '公开',
        'release': '发布',
        'version': '版本',
        'improved': '改进',
        'enhanced': '增强',
        'powered by': '由...驱动',
        'directly': '直接',
        'natural language': '自然语言',
        'execution': '执行',
        'done': '完成',
        'ready': '准备好',
        'check out': '查看',
        'learn more': '了解更多',
        'join': '加入',
        'community': '社区',
        'developers': '开发者',
        'building': '构建',
        'create': '创建',
        'integrate': '集成',
        'platform': '平台',
        'service': '服务',
        'app': '应用',
        'application': '应用程序',
    }
    
    @classmethod
    def translate_simple(cls, text: str) -> str:
        """简单翻译 - 替换常见词汇"""
        if not text:
            return text
        
        translated = text
        for en, zh in cls.COMMON_WORDS.items():
            # 大小写不敏感替换
            pattern = re.compile(re.escape(en), re.IGNORECASE)
            translated = pattern.sub(zh, translated)
        
        return translated
    
    @classmethod
    def translate_with_formatting(cls, text: str) -> str:
        """翻译并保留格式"""
        if not text:
            return text
        
        # 先进行简单翻译
        translated = cls.translate_simple(text)
        
        # 添加原文提示
        if text != translated:
            return f"{translated}\n\n[原文]: {text[:200]}{'...' if len(text) > 200 else ''}"
        
        return text


class TwitterDiscordPusherZH:
    """Twitter Discord 推送器 - 中文版"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.session = None
        self.translator = Translator()
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def translate_tweet(self, tweet: Tweet) -> Tweet:
        """翻译推文内容"""
        # 翻译标题
        tweet.title = self.translator.translate_simple(tweet.title)
        
        # 翻译内容
        tweet.content_zh = self.translator.translate_with_formatting(tweet.content)
        
        # 翻译引用推文
        if tweet.quoted_text:
            tweet.quoted_text_zh = self.translator.translate_simple(tweet.quoted_text)
        
        return tweet
    
    def format_tweet_embed(self, tweet: Tweet, index: int) -> dict:
        """格式化推文为 Discord Embed（中文版）"""
        
        # 翻译内容
        tweet = self.translate_tweet(tweet)
        
        # 作者信息
        verified_emoji = "✅" if tweet.author_verified else ""
        author_text = f"{tweet.author_name} {verified_emoji} (@{tweet.author_screen_name})"
        
        # 构建描述（优先使用中文）
        description = tweet.content_zh if tweet.content_zh else tweet.content
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
            quoted_content = tweet.quoted_text_zh if tweet.quoted_text_zh else tweet.quoted_text
            quoted_content = quoted_content[:500]
            if len(tweet.quoted_text) > 500:
                quoted_content += "..."
            
            quoted_value = f"**{tweet.quoted_author}**\n{quoted_content}"
            
            fields.append({
                "name": "📎 引用推文",
                "value": quoted_value,
                "inline": False
            })
        
        # 构建 embed
        embed = {
            "title": f"🐦 {tweet.title}",
            "description": description,
            "url": tweet.url,
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
        await asyncio.sleep(1)
    
    async def send_summary(self, count: int):
        """发送摘要"""
        payload = {
            "content": f"""## 🔔 Twitter 新闻推送（中文版）

⏰ **时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
📊 **数量**: {count} 条推文
🌐 **翻译**: 英文内容已自动翻译为中文
{'─' * 40}""",
            "allowed_mentions": {"parse": []}
        }
        
        await self._send_request(payload)
    
    async def _send_request(self, payload: dict):
        """发送请求"""
        try:
            async with self.session.post(self.webhook_url, json=payload) as resp:
                if resp.status == 429:
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
            print("⚠️ Discord Webhook 未配置")
            return
        
        print(f"\n📤 正在推送到 Discord（中文版）...")
        
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
    
    def fetch_from_json(self, json_file: str) -> List[Tweet]:
        """从 JSON 文件加载推文"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tweets = []
        for item in data.get('items', []):
            if item.get('source') == 'twitter':
                author_str = item.get('author', '')
                author_name = author_str.split(' (@')[0] if ' (@' in author_str else author_str
                author_screen = author_str.split('(@')[1].rstrip(')') if '(@' in author_str else ''
                
                tweet = Tweet(
                    id=item.get('id', ''),
                    url=item.get('url', ''),
                    title=item.get('title', ''),
                    content=item.get('content', ''),
                    author_name=author_name,
                    author_screen_name=author_screen,
                    author_verified=item.get('author_verified', False),
                    created_at=item.get('published_at', ''),
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
                    source=item.get('source', 'twitter'),
                    source_name=item.get('source_name', 'Twitter')
                )
                tweets.append(tweet)
        
        return tweets


def load_webhook_url() -> Optional[str]:
    """加载 Webhook URL"""
    if 'DISCORD_WEBHOOK_URL' in os.environ:
        return os.environ['DISCORD_WEBHOOK_URL']
    
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
    
    parser = argparse.ArgumentParser(description='Discord 推文推送（中文版）')
    parser.add_argument('--webhook', help='Discord Webhook URL')
    parser.add_argument('--file', '-f', help='JSON 文件路径')
    
    args = parser.parse_args()
    
    webhook_url = args.webhook or load_webhook_url()
    
    if not webhook_url:
        print("❌ 未配置 Discord Webhook URL")
        return
    
    # 获取 JSON 文件
    json_file = args.file
    if not json_file:
        import glob
        files = sorted(glob.glob('news_*.json'), reverse=True)
        if files:
            json_file = files[0]
            print(f"📁 使用最新文件: {json_file}")
    
    if not json_file or not Path(json_file).exists():
        print("❌ 未找到 JSON 文件")
        return
    
    # 加载推文
    fetcher = TweetFetcher()
    tweets = fetcher.fetch_from_json(json_file)
    
    if not tweets:
        print("⚠️ 未找到 Twitter 推文")
        return
    
    print(f"📊 找到 {len(tweets)} 条推文，将翻译为中文推送")
    
    # 推送到 Discord
    async with TwitterDiscordPusherZH(webhook_url) as pusher:
        await pusher.push_tweets(tweets)


if __name__ == "__main__":
    asyncio.run(main())
