#!/usr/bin/env python3
"""
手动登录脚本
打开浏览器，显示二维码，等待扫码
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def manual_login():
    """手动登录"""
    print("🚀 启动浏览器...")
    print("=" * 50)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            locale='zh-CN'
        )
        
        # 注入脚本隐藏自动化特征
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        page = await context.new_page()
        
        print("🔐 访问小红书...")
        await page.goto("https://www.xiaohongshu.com", timeout=60000)
        
        print("✅ 页面已加载")
        print("\n" + "=" * 50)
        print("📱 请扫码登录")
        print("=" * 50)
        print("\n步骤:")
        print("1. 在浏览器中点击'登录'按钮")
        print("2. 使用小红书App扫码")
        print("3. 完成登录后，按回车键继续")
        print("\n等待登录...")
        
        # 等待用户扫码登录（90秒）
        print("\n⏳ 等待90秒完成扫码登录...")
        await asyncio.sleep(90)
        
        # 保存Cookie
        cookies = await context.cookies()
        cookie_file = Path("cookies/account_1.json")
        
        import json
        with open(cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Cookie已保存: {cookie_file}")
        print(f"   共 {len(cookies)} 个Cookie")
        
        # 截图确认
        await page.screenshot(path="login_success.png")
        print("📸 已截图: login_success.png")
        
        await browser.close()
        print("\n👋 浏览器已关闭")
        print("✅ 登录完成！")

if __name__ == "__main__":
    asyncio.run(manual_login())
