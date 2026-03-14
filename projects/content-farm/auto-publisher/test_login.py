#!/usr/bin/env python3
"""
测试登录状态
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def test_login():
    """测试登录"""
    print("🚀 启动浏览器...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        # 加载Cookie
        cookie_file = Path("cookies/account_1.json")
        if cookie_file.exists():
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
            print(f"✅ 加载了 {len(cookies)} 个Cookie")
        
        page = await context.new_page()
        
        print("🔐 访问小红书...")
        try:
            await page.goto("https://www.xiaohongshu.com", timeout=30000)
            print("✅ 页面加载成功")
        except Exception as e:
            print(f"⚠️ 页面加载超时: {e}")
        
        # 等待一下页面渲染
        await asyncio.sleep(3)
        
        # 检查登录状态
        print("🔍 检查登录状态...")
        
        # 截图查看
        await page.screenshot(path="test_screenshot.png")
        print("📸 已截图: test_screenshot.png")
        
        # 查找用户头像
        avatar = await page.query_selector('.avatar, .user-avatar, img[class*="avatar"]')
        if avatar:
            print("✅ 检测到用户头像，已登录！")
        else:
            print("⚠️ 未检测到用户头像，可能未登录")
        
        # 保持浏览器打开一段时间供查看
        print("\n⏳ 保持浏览器打开30秒，请查看...")
        await asyncio.sleep(30)
        
        await browser.close()
        print("👋 浏览器已关闭")

if __name__ == "__main__":
    asyncio.run(test_login())
