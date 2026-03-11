#!/usr/bin/env python3
"""
浏览器自动化发布模块
- 使用Playwright模拟真人操作
- 自动登录、上传图片、填写内容、发布
"""

import os
import sys
import time
import random
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ 需要安装Playwright: pip3 install playwright")
    print("然后运行: python3 -m playwright install chromium")
    sys.exit(1)

class BrowserPublisher:
    """浏览器自动化发布器"""
    
    def __init__(self, cookie_str=None):
        self.cookie_str = cookie_str
        self.browser = None
        self.context = None
        self.page = None
        
    def init_browser(self):
        """初始化浏览器"""
        print("🌐 启动浏览器...")
        
        playwright = sync_playwright().start()
        
        # 启动浏览器（模拟真实用户）
        self.browser = playwright.chromium.launch(
            headless=False,  # 显示浏览器窗口，方便调试
            args=['--disable-blink-features=AutomationControlled']
        )
        
        # 创建上下文（模拟真实设备）
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        self.page = self.context.new_page()
        
        # 注入Cookie
        if self.cookie_str:
            self._inject_cookies()
        
        print("✅ 浏览器启动成功")
        return True
    
    def _inject_cookies(self):
        """注入Cookie实现自动登录"""
        print("🍪 注入Cookie...")
        
        # 先访问小红书域名
        self.page.goto("https://www.xiaohongshu.com")
        time.sleep(2)
        
        # 解析Cookie字符串
        cookies = []
        for item in self.cookie_str.split(';'):
            item = item.strip()
            if '=' in item:
                name, value = item.split('=', 1)
                cookies.append({
                    'name': name.strip(),
                    'value': value.strip(),
                    'domain': '.xiaohongshu.com',
                    'path': '/'
                })
        
        # 添加Cookie
        for cookie in cookies:
            try:
                self.context.add_cookies([cookie])
            except Exception as e:
                print(f"⚠️  Cookie添加失败: {cookie['name']}")
        
        print(f"✅ 注入 {len(cookies)} 个Cookie")
    
    def publish_note(self, title, content, images, is_public=True):
        """
        发布笔记
        
        Args:
            title: 标题
            content: 正文内容
            images: 图片路径列表
            is_public: 是否公开
        """
        print(f"📝 开始发布: {title[:20]}...")
        
        try:
            # 1. 访问发布页面
            print("1️⃣ 打开发布页面...")
            self.page.goto("https://creator.xiaohongshu.com/publish/publish")
            time.sleep(3)
            
            # 2. 上传图片
            print("2️⃣ 上传图片...")
            self._upload_images(images)
            
            # 3. 填写标题
            print("3️⃣ 填写标题...")
            self._fill_title(title)
            
            # 4. 填写正文
            print("4️⃣ 填写正文...")
            self._fill_content(content)
            
            # 5. 设置公开/私密
            if not is_public:
                print("5️⃣ 设置为私密...")
                self._set_private()
            
            # 6. 发布
            print("6️⃣ 点击发布...")
            self._click_publish()
            
            print("✅ 发布成功！")
            return True
            
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return False
    
    def _upload_images(self, images):
        """上传图片"""
        # 等待上传按钮
        self.page.wait_for_selector('input[type="file"]', timeout=10000)
        
        # 上传图片
        for img_path in images:
            if Path(img_path).exists():
                self.page.set_input_files('input[type="file"]', img_path)
                print(f"  📷 上传: {img_path}")
                time.sleep(random.uniform(1, 2))  # 随机延迟
            else:
                print(f"  ❌ 图片不存在: {img_path}")
        
        # 等待上传完成
        time.sleep(3)
    
    def _fill_title(self, title):
        """填写标题"""
        # 找到标题输入框
        title_input = self.page.locator('input[placeholder*="标题"], textarea[placeholder*="标题"]').first
        title_input.fill(title)
        print(f"  📝 标题: {title[:30]}...")
        time.sleep(random.uniform(0.5, 1))
    
    def _fill_content(self, content):
        """填写正文"""
        # 检查内容长度，小红书限制约 260KB (260096 bytes)
        MAX_CONTENT_LENGTH = 250000  # 留一些余量
        if len(content.encode('utf-8')) > MAX_CONTENT_LENGTH:
            print(f"  ⚠️  内容过长 ({len(content.encode('utf-8'))} bytes)，截断到 {MAX_CONTENT_LENGTH} bytes")
            # 截断内容，保留前 250KB
            content = content.encode('utf-8')[:MAX_CONTENT_LENGTH].decode('utf-8', errors='ignore')
        
        # 找到正文输入框
        content_input = self.page.locator('div[contenteditable="true"], textarea[placeholder*="内容"]').first
        content_input.fill(content)
        print(f"  📝 正文: {content[:50]}... (共 {len(content.encode('utf-8'))} bytes)")
        time.sleep(random.uniform(1, 2))
    
    def _set_private(self):
        """设置为私密"""
        try:
            # 找到可见性设置
            visibility_btn = self.page.locator('text=公开 或 text=私密').first
            visibility_btn.click()
            time.sleep(1)
            
            # 选择私密
            private_option = self.page.locator('text=私密').first
            private_option.click()
            print("  🔒 设置为私密")
        except:
            print("  ⚠️  设置私密失败，使用默认")
    
    def _click_publish(self):
        """点击发布按钮"""
        # 找到发布按钮
        publish_btn = self.page.locator('button:has-text("发布"), button:has-text("立即发布")').first
        
        # 随机延迟（模拟真人思考）
        time.sleep(random.uniform(2, 5))
        
        publish_btn.click()
        print("  🚀 点击发布")
        
        # 等待发布完成
        time.sleep(5)
    
    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
            print("🌐 浏览器已关闭")

def publish_with_browser(account, title, content, images, cookie):
    """使用浏览器发布"""
    publisher = BrowserPublisher(cookie)
    
    try:
        # 初始化浏览器
        publisher.init_browser()
        
        # 发布笔记
        success = publisher.publish_note(title, content, images)
        
        # 关闭浏览器
        publisher.close()
        
        return success
    except Exception as e:
        print(f"❌ 发布异常: {e}")
        publisher.close()
        return False

if __name__ == "__main__":
    # 测试
    cookie = os.getenv('XHS_COOKIE', '')
    
    if not cookie:
        print("❌ 需要设置XHS_COOKIE环境变量")
        sys.exit(1)
    
    # 发布测试
    success = publish_with_browser(
        account="tech-geek",
        title="测试发布",
        content="这是测试内容",
        images=[],
        cookie=cookie
    )
    
    if success:
        print("✅ 发布成功")
    else:
        print("❌ 发布失败")
