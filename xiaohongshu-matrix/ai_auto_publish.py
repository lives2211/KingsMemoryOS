#!/usr/bin/env python3
"""
AI自动发布 - 无需人工干预
使用API直接发布
"""

import os
import sys
import json
import requests
import time
from pathlib import Path
from datetime import datetime

class AIAutoPublisher:
    """AI自动发布器"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"):
        self.base_path = Path(base_path)
    
    def load_cookie(self, account):
        """加载Cookie"""
        env_file = self.base_path / f".env.{account}"
        
        if not env_file.exists():
            print(f"❌ 配置文件不存在: {env_file}")
            return None
        
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith("XHS_COOKIE="):
                    return line.replace("XHS_COOKIE=", "").strip()
        
        return None
    
    def parse_cookie(self, cookie_str):
        """解析Cookie"""
        cookies = {}
        for item in cookie_str.split(';'):
            item = item.strip()
            if '=' in item:
                name, value = item.split('=', 1)
                cookies[name] = value
        return cookies
    
    def publish_by_api(self, account, title, content, images):
        """
        通过API直接发布
        注意：需要逆向小红书的发布API
        """
        print(f"🚀 AI自动发布: {account}")
        print(f"📝 标题: {title}")
        
        # 加载Cookie
        cookie_str = self.load_cookie(account)
        if not cookie_str:
            print("❌ Cookie未配置")
            return False
        
        cookies = self.parse_cookie(cookie_str)
        
        # 小红书API端点（需要逆向获取）
        # PUBLISH_API = "https://creator.xiaohongshu.com/api/xxx/publish"
        
        # 构造请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://creator.xiaohongshu.com/',
            'Origin': 'https://creator.xiaohongshu.com',
            'Content-Type': 'application/json',
        }
        
        # 构造发布数据
        publish_data = {
            'title': title,
            'content': content,
            'images': images,
            'topics': ['AI', '效率工具', '2026趋势'],
        }
        
        print("⚠️  API直接发布需要逆向小红书的发布接口")
        print("   当前使用浏览器自动化更稳定")
        print("")
        print("💡 建议方案:")
        print("   1. 使用 xiaohongshu-cli 工具")
        print("   2. 或使用 xiaohongshu-skills 的CDP方案")
        print("   3. 或手动复制发布")
        
        return False
    
    def auto_publish(self, account):
        """自动发布"""
        print(f"\n{'='*50}")
        print(f"🤖 AI自动发布: {account}")
        print(f"{'='*50}\n")
        
        # 查找内容文件
        content_dir = self.base_path / "generated" / account
        md_files = list(content_dir.glob("**/ai_*.md"))
        
        if not md_files:
            print(f"❌ 未找到内容文件: {content_dir}")
            return False
        
        # 选择最新的
        latest_md = max(md_files, key=lambda x: x.stat().st_mtime)
        
        # 读取内容
        with open(latest_md, 'r') as f:
            lines = f.readlines()
            title = lines[0].replace('# ', '').strip()
            content = ''.join(lines[2:])
        
        print(f"📄 文件: {latest_md.name}")
        print(f"📝 标题: {title}")
        print(f"📊 字数: {len(content)}")
        print()
        
        # 尝试发布
        success = self.publish_by_api(account, title, content, [])
        
        return success
    
    def run(self):
        """运行自动发布"""
        print("🚀 AI自动发布系统")
        print("=" * 50)
        print()
        
        accounts = ["tech-geek", "career-growth"]
        
        for account in accounts:
            self.auto_publish(account)
            time.sleep(2)
        
        print()
        print("=" * 50)
        print("✅ AI执行完成")
        print()
        print("💡 由于小红书API限制，建议:")
        print("   1. 使用 xiaohongshu-cli 工具")
        print("   2. 或使用浏览器自动化")
        print("   3. 或手动复制发布")

def main():
    """主函数"""
    publisher = AIAutoPublisher()
    publisher.run()

if __name__ == "__main__":
    main()
