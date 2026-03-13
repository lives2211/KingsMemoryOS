#!/usr/bin/env python3
"""
中文区 KOL 推文爬取器
- 爬取最新一个月优质推文
- 筛选 OpenClaw/AI Skill 相关内容
- 深度分析内容结构
"""

import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path


class ChineseKOLCrawler:
    """中文 KOL 推文爬取器"""
    
    def __init__(self):
        self.target_keywords = [
            'OpenClaw', 'Skill', 'AI Agent', '自动化', 'workflow',
            'GitHub', '开源', '教程', '工具', '效率'
        ]
        
        # 已知优质中文 KOL
        self.target_kols = [
            'AlchainHust',      # AI进化论-花生
            'wangray',          # Ray Wang
            'Jimmy_JingLv',     # 吕立青
            'servasyy_ai',      # huangserva
            'dashen_wang',      # AI最严厉的父亲
            'AYi_AInotes',      # 阿绎 AYi
            'jakevin7',         # 卡比卡比
            'cnyzgkc',          # 木马人
            'Graceruansu',      # 软苏 Grace
            'hunterweb303'      # 0x 哆啦A梦
        ]
    
    def fetch_kol_tweets(self, screen_name, max_results=50):
        """获取特定 KOL 的推文"""
        try:
            result = subprocess.run(
                ['twitter', 'user-posts', screen_name, '--max', str(max_results), '--json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get('data', [])
            else:
                print(f"❌ 获取 {screen_name} 失败: {result.stderr[:100]}")
                return []
                
        except Exception as e:
            print(f"❌ 错误: {e}")
            return []
    
    def filter_quality_tweets(self, tweets, min_likes=50):
        """筛选高质量推文"""
        quality_tweets = []
        
        for tweet in tweets:
            # 检查互动数据
            metrics = tweet.get('metrics', {})
            likes = metrics.get('likes', 0)
            retweets = metrics.get('retweets', 0)
            
            if likes < min_likes:
                continue
            
            text = tweet.get('text', '')
            
            # 检查是否包含关键词
            has_keyword = any(kw.lower() in text.lower() for kw in self.target_keywords)
            
            # 检查是否包含中文
            has_chinese = any('\u4e00' <= c <= '\u9fff' for c in text)
            
            if has_keyword and has_chinese and len(text) > 50:
                quality_tweets.append({
                    'id': tweet.get('id'),
                    'text': text,
                    'author': tweet.get('author', {}).get('screenName', ''),
                    'likes': likes,
                    'retweets': retweets,
                    'created_at': tweet.get('createdAt', ''),
                    'urls': tweet.get('urls', []),
                    'has_chinese': True
                })
        
        # 按互动排序
        quality_tweets.sort(key=lambda x: x['likes'] + x['retweets'], reverse=True)
        return quality_tweets[:20]
    
    def analyze_tweet_structure(self, tweet):
        """分析推文结构"""
        text = tweet['text']
        
        analysis = {
            'has_hook': any(word in text for word in ['🔥', '💡', '⚡', '🎯', '刚发现', '分享']),
            'has_problem': any(word in text for word in ['问题', '痛点', '困难', '挑战', '以前']),
            'has_solution': any(word in text for word in ['解决', '方案', '工具', '方法', '神器']),
            'has_data': any(word in text for word in ['小时', '分钟', '天', '%', '倍']),
            'has_github': 'github.com' in text.lower(),
            'has_steps': any(word in text for word in ['步骤', '步', '1️⃣', '2️⃣', '3️⃣']),
            'has_cta': any(word in text for word in ['回复', '评论', '私信', '获取', '链接']),
            'thread_marker': '🧵' in text or '👇' in text,
            'structure_score': 0
        }
        
        # 计算结构分
        score = 0
        if analysis['has_hook']: score += 2
        if analysis['has_problem']: score += 2
        if analysis['has_solution']: score += 2
        if analysis['has_data']: score += 1
        if analysis['has_github']: score += 2
        if analysis['has_steps']: score += 1
        if analysis['has_cta']: score += 1
        if analysis['thread_marker']: score += 1
        
        analysis['structure_score'] = score
        return analysis
    
    def crawl_all_kols(self):
        """爬取所有 KOL"""
        print("="*60)
        print("🔍 中文区 KOL 推文爬取器")
        print("="*60)
        print(f"\n目标 KOL: {len(self.target_kols)} 个")
        print(f"关键词: {', '.join(self.target_keywords[:5])}...")
        print()
        
        all_quality_tweets = []
        
        for i, kol in enumerate(self.target_kols, 1):
            print(f"[{i}/{len(self.target_kols)}] 爬取 @{kol}...")
            
            tweets = self.fetch_kol_tweets(kol, max_results=30)
            quality = self.filter_quality_tweets(tweets, min_likes=30)
            
            # 分析结构
            for tweet in quality:
                tweet['structure'] = self.analyze_tweet_structure(tweet)
            
            all_quality_tweets.extend(quality)
            print(f"   ✅ 获取 {len(quality)} 条高质量推文")
        
        # 全局排序
        all_quality_tweets.sort(key=lambda x: x['likes'] + x['retweets'], reverse=True)
        
        print(f"\n{'='*60}")
        print(f"📊 爬取完成:")
        print(f"   总计: {len(all_quality_tweets)} 条高质量推文")
        print(f"{'='*60}")
        
        # 保存
        filename = f"kol_crawled_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'crawled_at': datetime.now().isoformat(),
                'total': len(all_quality_tweets),
                'tweets': all_quality_tweets
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存: {filename}")
        
        return all_quality_tweets
    
    def show_top_tweets(self, tweets, n=5):
        """展示热门推文"""
        print(f"\n🔥 Top {n} 热门推文:\n")
        
        for i, tweet in enumerate(tweets[:n], 1):
            print(f"{i}. @{tweet['author']}")
            print(f"   ❤️ {tweet['likes']}  🔁 {tweet['retweets']}")
            print(f"   结构分: {tweet['structure']['structure_score']}/12")
            print(f"   内容: {tweet['text'][:100]}...")
            print()


def main():
    """主函数"""
    crawler = ChineseKOLCrawler()
    
    # 爬取
    tweets = crawler.crawl_all_kols()
    
    # 展示热门
    crawler.show_top_tweets(tweets, n=5)


if __name__ == "__main__":
    main()
