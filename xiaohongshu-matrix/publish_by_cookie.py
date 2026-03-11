#!/usr/bin/env python3
"""
使用Cookie直接发布
- 无需Chrome浏览器
- 无需扫码
- 直接发送HTTP请求
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

class CookiePublisher:
    """Cookie发布器"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"):
        self.base_path = Path(base_path)
        self.session = requests.Session()
    
    def load_cookie(self, account):
        """加载账号Cookie"""
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
        """解析Cookie字符串"""
        cookies = {}
        for item in cookie_str.split(';'):
            item = item.strip()
            if '=' in item:
                name, value = item.split('=', 1)
                cookies[name.strip()] = value.strip()
        return cookies
    
    def publish_note(self, account, title, content, images):
        """
        发布笔记
        注意：这是简化版，实际小红书发布需要更多步骤
        """
        print(f"🚀 使用Cookie发布: {account}")
        
        # 加载Cookie
        cookie_str = self.load_cookie(account)
        if not cookie_str:
            return False
        
        cookies = self.parse_cookie(cookie_str)
        
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://creator.xiaohongshu.com/',
            'Origin': 'https://creator.xiaohongshu.com',
        }
        
        # 设置Cookie
        self.session.cookies.update(cookies)
        
        print(f"✅ Cookie已加载: {len(cookies)} 个字段")
        print(f"📝 标题: {title[:30]}...")
        print(f"🖼️  图片: {len(images)} 张")
        
        # 注意：实际发布需要调用小红书的API
        # 这里只是演示Cookie的使用
        # 完整实现需要逆向小红书的发布接口
        
        print("⚠️  Cookie直接发布需要完整的API实现")
        print("   当前版本使用浏览器自动化更稳定")
        
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cookie直接发布")
    parser.add_argument("account", help="账号名称")
    parser.add_argument("--file", help="内容文件")
    
    args = parser.parse_args()
    
    publisher = CookiePublisher()
    
    # 加载内容
    if args.file:
        content_file = Path(args.file)
        if content_file.exists():
            with open(content_file, 'r') as f:
                lines = f.readlines()
                title = lines[0].replace('# ', '').strip()
                content = ''.join(lines[2:])
            
            # 查找图片
            images = sorted(content_file.parent.glob("card_*.png"))
            
            publisher.publish_note(args.account, title, content, images)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
