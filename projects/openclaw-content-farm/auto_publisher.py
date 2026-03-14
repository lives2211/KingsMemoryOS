#!/usr/bin/env python3
"""
OpenClaw Content Farm - 自动发布系统
自动发布生成的推文到 X/Twitter
"""

import os
import json
import time
import random
import subprocess
from datetime import datetime
from pathlib import Path

class AutoPublisher:
    """自动发布器"""
    
    def __init__(self, config_path="config.yaml"):
        self.config = self._load_config(config_path)
        self.cookies = os.getenv('TWITTER_COOKIES', '')
        
    def _load_config(self, config_path):
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def publish_tweet(self, tweet_content):
        """发布单条推文"""
        # 保存推文到临时文件
        temp_file = f"/tmp/tweet_{int(time.time())}.txt"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(tweet_content)
        
        # 使用 twitter CLI 发布
        cmd = f'export TWITTER_COOKIES="{self.cookies}" && twitter post "$(cat {temp_file})"'
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # 清理临时文件
            os.remove(temp_file)
            
            if result.returncode == 0:
                # 解析结果获取推文链接
                output = result.stdout
                if 'url:' in output:
                    url_line = [l for l in output.split('\n') if 'url:' in l]
                    if url_line:
                        return True, url_line[0].split('url:')[-1].strip()
                return True, None
            else:
                error = result.stderr
                # 检查是否是字符限制错误
                if 'needs to be a bit shorter' in error:
                    return False, "CHARACTER_LIMIT"
                return False, error
                
        except subprocess.TimeoutExpired:
            return False, "TIMEOUT"
        except Exception as e:
            return False, str(e)
    
    def publish_daily_tweets(self, date_str=None):
        """发布一天的推文"""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 加载生成的推文
        tweets_file = Path(self.config['output']['save_path']) / f"tweets_{date_str}.json"
        
        if not tweets_file.exists():
            print(f"❌ No tweets found for {date_str}")
            return []
        
        with open(tweets_file, 'r', encoding='utf-8') as f:
            tweets = json.load(f)
        
        print(f"📤 Publishing {len(tweets)} tweets...")
        
        published = []
        for i, tweet in enumerate(tweets):
            print(f"\n[{i+1}/{len(tweets)}] Publishing: {tweet['skill']} ({tweet['theme']})")
            
            # 尝试发布
            success, result = self.publish_tweet(tweet['content'])
            
            if success:
                print(f"✅ Published: {result}")
                tweet['published_url'] = result
                tweet['published_at'] = datetime.now().isoformat()
                published.append(tweet)
            else:
                if result == "CHARACTER_LIMIT":
                    print("⚠️ Character limit exceeded, generating shorter version...")
                    # 生成精简版
                    short_tweet = self._generate_short_version(tweet)
                    success, result = self.publish_tweet(short_tweet)
                    if success:
                        print(f"✅ Published (short): {result}")
                        tweet['published_url'] = result
                        tweet['published_at'] = datetime.now().isoformat()
                        tweet['is_short_version'] = True
                        published.append(tweet)
                    else:
                        print(f"❌ Failed: {result}")
                else:
                    print(f"❌ Failed: {result}")
            
            # 等待间隔（避免 rate limit）
            if i < len(tweets) - 1:
                interval = self.config['content_generation']['publish_interval']
                print(f"⏳ Waiting {interval} minutes before next tweet...")
                time.sleep(interval * 60)
        
        # 保存发布记录
        self._save_publish_log(published, date_str)
        
        return published
    
    def _generate_short_version(self, tweet):
        """生成精简版推文"""
        skill_name = tweet['skill']
        emoji = '📦'
        
        # 从内容中提取关键信息
        short_tweet = f"""OpenClaw {skill_name.title()} Skill

After 24 hours using this skill:

🎯 Key benefits
⚡ Quick setup
🔧 Easy automation

Transform your workflow

github.com/openclaw/openclaw

#OpenClaw #{skill_name.replace('-', '')}"""
        
        return short_tweet
    
    def _save_publish_log(self, published, date_str):
        """保存发布日志"""
        log_dir = Path(self.config['output']['log_path'])
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"published_{date_str}.json"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                'date': date_str,
                'total': len(published),
                'published': published
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 Published {len(published)} tweets")
        print(f"📁 Log saved to: {log_file}")


def main():
    """主函数"""
    print("🚀 OpenClaw Auto Publisher")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    publisher = AutoPublisher()
    published = publisher.publish_daily_tweets()
    
    print(f"\n✅ Done! Published {len(published)} tweets today.")


if __name__ == "__main__":
    main()
