#!/usr/bin/env python3
"""
Twitter 推文收集工具
支持：首页时间线、搜索、用户推文、关注时间线
自动添加推文链接
"""

import subprocess
import json
import sys
from datetime import datetime
from typing import List, Dict, Optional


def run_twitter_command(cmd: List[str]) -> Optional[Dict]:
    """运行 twitter-cli 命令并返回 JSON 结果"""
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


def build_tweet_url(screen_name: str, tweet_id: str) -> str:
    """构建推文链接"""
    return f"https://x.com/{screen_name}/status/{tweet_id}"


def process_tweet(tweet: Dict) -> Dict:
    """处理推文数据，添加链接和格式化"""
    author = tweet.get("author", {})
    screen_name = author.get("screenName", "")
    tweet_id = tweet.get("id", "")
    
    # 构建推文链接
    tweet_url = build_tweet_url(screen_name, tweet_id) if screen_name and tweet_id else ""
    
    # 处理媒体
    media_list = []
    for media in tweet.get("media", []):
        if media.get("type") == "photo":
            media_list.append(f"[图片] {media.get('url', '')}")
        elif media.get("type") == "video":
            media_list.append(f"[视频] {media.get('url', '')}")
    
    # 处理引用推文
    quoted = tweet.get("quotedTweet")
    quoted_info = None
    if quoted:
        quoted_author = quoted.get("author", {})
        quoted_info = {
            "text": quoted.get("text", ""),
            "author": quoted_author.get("name", ""),
            "screen_name": quoted_author.get("screenName", "")
        }
    
    return {
        "id": tweet_id,
        "url": tweet_url,
        "text": tweet.get("text", ""),
        "author": {
            "name": author.get("name", ""),
            "screen_name": screen_name,
            "verified": author.get("verified", False)
        },
        "created_at": tweet.get("createdAt", ""),
        "metrics": {
            "likes": tweet.get("metrics", {}).get("likes", 0),
            "retweets": tweet.get("metrics", {}).get("retweets", 0),
            "replies": tweet.get("metrics", {}).get("replies", 0),
            "views": tweet.get("metrics", {}).get("views", 0),
            "bookmarks": tweet.get("metrics", {}).get("bookmarks", 0)
        },
        "media": media_list,
        "urls": tweet.get("urls", []),
        "is_retweet": tweet.get("isRetweet", False),
        "quoted_tweet": quoted_info,
        "lang": tweet.get("lang", "")
    }


def fetch_feed(max_results: int = 20, feed_type: str = "for-you") -> List[Dict]:
    """获取首页时间线"""
    cmd = ["feed", "--max", str(max_results)]
    if feed_type == "following":
        cmd.extend(["-t", "following"])
    
    result = run_twitter_command(cmd)
    if result and result.get("ok"):
        return [process_tweet(t) for t in result.get("data", [])]
    return []


def search_tweets(query: str, max_results: int = 20, search_type: str = "Top") -> List[Dict]:
    """搜索推文"""
    cmd = ["search", query, "--max", str(max_results)]
    if search_type in ["Latest", "Photos", "Videos"]:
        cmd.extend(["-t", search_type.lower()])
    
    result = run_twitter_command(cmd)
    if result and result.get("ok"):
        return [process_tweet(t) for t in result.get("data", [])]
    return []


def fetch_user_tweets(screen_name: str, max_results: int = 20) -> List[Dict]:
    """获取用户推文"""
    cmd = ["user-posts", screen_name, "--max", str(max_results)]
    
    result = run_twitter_command(cmd)
    if result and result.get("ok"):
        return [process_tweet(t) for t in result.get("data", [])]
    return []


def format_tweet(tweet: Dict, index: int = 0) -> str:
    """格式化单条推文为可读文本"""
    author = tweet["author"]
    metrics = tweet["metrics"]
    verified_badge = "✓" if author["verified"] else ""
    
    lines = [
        f"\n{'='*60}",
        f"[{index}] {author['name']} {verified_badge} (@{author['screen_name']})",
        f"🔗 {tweet['url']}",
        f"🕐 {tweet['created_at']}",
        f"{'-'*60}",
        f"{tweet['text']}",
    ]
    
    # 添加引用推文
    if tweet["quoted_tweet"]:
        qt = tweet["quoted_tweet"]
        lines.extend([
            f"\n📎 引用推文: {qt['author']} (@{qt['screen_name']}):",
            f"   {qt['text'][:100]}{'...' if len(qt['text']) > 100 else ''}"
        ])
    
    # 添加媒体
    if tweet["media"]:
        lines.append(f"\n🖼️ 媒体:")
        for m in tweet["media"]:
            lines.append(f"   {m}")
    
    # 添加外部链接
    if tweet["urls"]:
        lines.append(f"\n🔗 链接:")
        for url in tweet["urls"]:
            lines.append(f"   {url}")
    
    # 添加互动数据
    lines.extend([
        f"\n📊 互动: ❤️{metrics['likes']} 🔁{metrics['retweets']} 💬{metrics['replies']} 👁️{metrics['views']} 🔖{metrics['bookmarks']}",
        f"{'='*60}"
    ])
    
    return "\n".join(lines)


def save_tweets(tweets: List[Dict], filename: str = None):
    """保存推文到文件"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tweets_{timestamp}.json"
    
    output = {
        "fetch_time": datetime.now().isoformat(),
        "count": len(tweets),
        "tweets": tweets
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 已保存到: {filename}")
    return filename


def print_summary(tweets: List[Dict], title: str = "推文列表"):
    """打印推文摘要"""
    print(f"\n{'#'*60}")
    print(f"# {title}")
    print(f"# 共获取 {len(tweets)} 条推文")
    print(f"{'#'*60}")
    
    for i, tweet in enumerate(tweets, 1):
        print(format_tweet(tweet, i))


def main():
    """主函数 - 示例用法"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Twitter 推文收集工具')
    parser.add_argument('command', choices=['feed', 'following', 'search', 'user'], 
                        help='命令类型')
    parser.add_argument('--query', '-q', help='搜索关键词或用户名')
    parser.add_argument('--max', '-n', type=int, default=10, help='获取数量')
    parser.add_argument('--save', '-s', action='store_true', help='保存到文件')
    parser.add_argument('--output', '-o', help='输出文件名')
    
    args = parser.parse_args()
    
    tweets = []
    title = ""
    
    if args.command == 'feed':
        print("📱 正在获取首页推荐...")
        tweets = fetch_feed(args.max, "for-you")
        title = "首页推荐"
    
    elif args.command == 'following':
        print("📱 正在获取关注时间线...")
        tweets = fetch_feed(args.max, "following")
        title = "关注时间线"
    
    elif args.command == 'search':
        if not args.query:
            print("❌ 搜索需要提供 --query 参数")
            return
        print(f"🔍 正在搜索: {args.query}...")
        tweets = search_tweets(args.query, args.max)
        title = f"搜索: {args.query}"
    
    elif args.command == 'user':
        if not args.query:
            print("❌ 获取用户推文需要提供 --query 参数（用户名）")
            return
        print(f"👤 正在获取用户 @{args.query} 的推文...")
        tweets = fetch_user_tweets(args.query, args.max)
        title = f"用户 @{args.query} 的推文"
    
    if tweets:
        print_summary(tweets, title)
        
        if args.save:
            save_tweets(tweets, args.output)
        
        # 打印所有链接（方便复制）
        print(f"\n{'='*60}")
        print("📋 所有推文链接:")
        print(f"{'='*60}")
        for i, tweet in enumerate(tweets, 1):
            print(f"{i}. {tweet['url']}")
    else:
        print("❌ 未获取到推文")


if __name__ == "__main__":
    main()
