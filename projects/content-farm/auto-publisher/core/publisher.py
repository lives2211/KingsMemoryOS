"""
小红书安全自动发布核心模块
基于CDP浏览器自动化，模拟真人操作
"""

import asyncio
import json
import random
import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from loguru import logger

from playwright.async_api import async_playwright, Page, Browser, BrowserContext


@dataclass
class PublishConfig:
    """发布配置"""
    title: str
    content: str
    images: List[str]  # 图片路径列表
    hashtags: Optional[List[str]] = None
    

@dataclass
class SafetyConfig:
    """风控配置"""
    delays: Dict[str, Dict[str, float]]
    fingerprint: Dict[str, Any]
    random_behavior: Dict[str, Any]


class XHSPublisher:
    """小红书发布器"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    def _load_config(self, path: str) -> Dict:
        """加载配置"""
        import yaml
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    async def _random_delay(self, action: str):
        """随机延迟，模拟真人操作"""
        delay_config = self.config['safety']['delays'].get(action, {'min': 1, 'max': 3})
        delay = random.uniform(delay_config['min'], delay_config['max'])
        logger.debug(f"延迟 {action}: {delay:.2f}s")
        await asyncio.sleep(delay)
    
    async def _simulate_mouse_move(self, page: Page):
        """模拟鼠标移动"""
        if not self.config['safety']['random_behavior']['simulate_mouse']:
            return
            
        # 随机移动鼠标到页面某个位置
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        await page.mouse.move(x, y)
        await self._random_delay('between_actions')
    
    async def _simulate_scroll(self, page: Page):
        """模拟页面滚动"""
        if not self.config['safety']['random_behavior']['simulate_scroll']:
            return
            
        # 随机滚动一小段
        scroll_amount = random.randint(100, 500)
        await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        await self._random_delay('between_actions')
    
    async def _simulate_typing(self, page: Page, selector: str, text: str):
        """模拟真人打字"""
        typing_config = self.config['safety']['delays']['typing']
        
        # 点击输入框
        await page.click(selector)
        await self._random_delay('click')
        
        # 逐个字符输入，带随机延迟
        for char in text:
            await page.type(selector, char, delay=random.uniform(typing_config['min'], typing_config['max']) * 1000)
        
        await self._random_delay('between_actions')
    
    async def launch_browser(self, headless: bool = False):
        """启动浏览器"""
        logger.info("启动浏览器...")
        
        playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-site-isolation-trials',
        ]
        
        if headless:
            browser_args.append('--headless=new')
        
        self.browser = await playwright.chromium.launch(
            headless=headless,
            args=browser_args
        )
        
        # 创建上下文，设置指纹
        fingerprint = self.config['safety']['fingerprint']
        self.context = await self.browser.new_context(
            viewport=fingerprint['viewport'],
            locale=fingerprint['locale'],
            timezone_id=fingerprint['timezone'],
            user_agent=fingerprint['user_agent']
        )
        
        # 注入脚本隐藏自动化特征
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        """)
        
        self.page = await self.context.new_page()
        logger.info("浏览器启动成功")
    
    async def check_login(self) -> bool:
        """检查登录状态"""
        if not self.page:
            raise RuntimeError("浏览器未启动")
        
        logger.info("检查登录状态...")
        try:
            await self.page.goto("https://www.xiaohongshu.com", timeout=30000, wait_until="domcontentloaded")
        except Exception as e:
            logger.warning(f"页面加载部分超时: {e}")
        await self._random_delay('page_load')
        
        # 检查是否有登录按钮
        login_btn = await self.page.query_selector('.login-btn, .login-button')
        if login_btn:
            logger.warning("未登录状态")
            return False
        
        # 检查是否有用户头像
        avatar = await self.page.query_selector('.avatar, .user-avatar')
        if avatar:
            logger.info("已登录")
            return True
        
        return False
    
    async def login(self):
        """扫码登录"""
        if not self.page:
            raise RuntimeError("浏览器未启动")
        
        logger.info("启动登录流程，请扫码...")
        try:
            await self.page.goto("https://www.xiaohongshu.com", timeout=60000)
        except Exception as e:
            logger.warning(f"页面加载超时，继续尝试: {e}")
        
        await self._random_delay('page_load')
        
        # 关闭可能的弹窗
        try:
            close_btn = await self.page.query_selector('.reds-mask, .close-btn, .close')
            if close_btn:
                await close_btn.click()
                await self._random_delay('click')
                logger.info("关闭弹窗")
        except:
            pass
        
        # 尝试点击登录按钮
        try:
            login_btn = await self.page.query_selector('.login-btn, .login-button, [class*="login"]')
            if login_btn:
                await login_btn.click()
                await self._random_delay('click')
                logger.info("点击登录按钮")
        except Exception as e:
            logger.warning(f"点击登录按钮失败: {e}")
        
        # 等待扫码完成（手动）
        logger.info("=" * 50)
        logger.info("请在浏览器中完成扫码登录")
        logger.info("等待90秒，请尽快扫码...")
        logger.info("=" * 50)
        await asyncio.sleep(90)  # 给用户90秒扫码时间
        
        # 保存登录状态
        await self._save_cookies()
    
    async def _save_cookies(self):
        """保存Cookie"""
        if not self.context:
            return
        
        cookies = await self.context.cookies()
        cookie_dir = Path("cookies")
        cookie_dir.mkdir(exist_ok=True)
        
        with open(cookie_dir / "account_1.json", 'w', encoding='utf-8') as f:
            json.dump(cookies, f)
        
        logger.info("Cookie已保存")
    
    async def load_cookies(self):
        """加载Cookie"""
        cookie_file = Path("cookies/account_1.json")
        if not cookie_file.exists():
            logger.warning("Cookie文件不存在")
            return False
        
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        if self.context:
            await self.context.add_cookies(cookies)
            logger.info("Cookie已加载")
            return True
        
        return False
    
    async def publish(self, config: PublishConfig) -> bool:
        """
        发布笔记
        
        Args:
            config: 发布配置
            
        Returns:
            是否发布成功
        """
        if not self.page:
            raise RuntimeError("浏览器未启动")
        
        try:
            logger.info(f"开始发布: {config.title}")
            
            # 1. 进入创作者中心
            await self.page.goto("https://creator.xiaohongshu.com/publish/publish")
            await self._random_delay('page_load')
            await self._simulate_scroll(self.page)
            
            # 2. 上传图片
            await self._upload_images(config.images)
            
            # 3. 填写标题
            await self._fill_title(config.title)
            
            # 4. 填写正文
            await self._fill_content(config.content)
            
            # 5. 添加话题标签
            if config.hashtags:
                await self._add_hashtags(config.hashtags)
            
            # 6. 模拟阅读停顿
            if self.config['safety']['random_behavior']['simulate_reading']:
                reading_pause = self.config['safety']['random_behavior']['reading_pause']
                pause_time = random.uniform(reading_pause['min'], reading_pause['max'])
                logger.info(f"模拟阅读停顿: {pause_time:.1f}s")
                await asyncio.sleep(pause_time)
            
            # 7. 点击发布
            await self._click_publish()
            
            logger.info("发布成功!")
            return True
            
        except Exception as e:
            logger.error(f"发布失败: {e}")
            return False
    
    async def _upload_images(self, image_paths: List[str]):
        """上传图片"""
        logger.info(f"上传 {len(image_paths)} 张图片...")
        
        # 找到上传按钮
        upload_btn = await self.page.wait_for_selector('input[type="file"]', timeout=10000)
        
        # 逐个上传图片
        for img_path in image_paths:
            await upload_btn.set_input_files(img_path)
            await self._random_delay('upload')
            await self._simulate_mouse_move(self.page)
        
        logger.info("图片上传完成")
    
    async def _fill_title(self, title: str):
        """填写标题"""
        logger.info("填写标题...")
        
        # 找到标题输入框
        title_input = await self.page.wait_for_selector(
            'input[placeholder*="标题"], textarea[placeholder*="标题"], .title-input',
            timeout=10000
        )
        
        await self._simulate_typing(self.page, 'input[placeholder*="标题"]', title)
        logger.info("标题填写完成")
    
    async def _fill_content(self, content: str):
        """填写正文"""
        logger.info("填写正文...")
        
        # 找到正文输入框
        content_input = await self.page.wait_for_selector(
            'textarea[placeholder*="正文"], .content-input, .editor-content',
            timeout=10000
        )
        
        await self._simulate_typing(self.page, 'textarea[placeholder*="正文"]', content)
        logger.info("正文填写完成")
    
    async def _add_hashtags(self, hashtags: List[str]):
        """添加话题标签"""
        logger.info(f"添加 {len(hashtags)} 个话题标签...")
        
        # 在正文末尾添加标签
        for tag in hashtags:
            # 点击添加话题按钮
            tag_btn = await self.page.query_selector('.add-topic, .topic-btn')
            if tag_btn:
                await tag_btn.click()
                await self._random_delay('click')
            
            # 输入标签
            tag_input = await self.page.wait_for_selector(
                'input[placeholder*="话题"], .topic-input',
                timeout=5000
            )
            await self._simulate_typing(self.page, 'input[placeholder*="话题"]', tag)
            
            # 选择下拉选项
            await self.page.keyboard.press('Enter')
            await self._random_delay('between_actions')
        
        logger.info("话题标签添加完成")
    
    async def _click_publish(self):
        """点击发布按钮"""
        logger.info("点击发布按钮...")
        
        # 找到发布按钮
        publish_btn = await self.page.wait_for_selector(
            'button:has-text("发布"), .publish-btn, [data-testid="publish"]',
            timeout=10000
        )
        
        await self._simulate_mouse_move(self.page)
        await publish_btn.click()
        await self._random_delay('click')
        
        # 等待发布完成
        await self.page.wait_for_load_state('networkidle')
        await self._random_delay('page_load')
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            logger.info("浏览器已关闭")


async def main():
    """测试代码"""
    publisher = XHSPublisher()
    
    try:
        # 启动浏览器
        await publisher.launch_browser(headless=False)
        
        # 检查登录
        if not await publisher.check_login():
            await publisher.login()
        
        # 发布测试
        config = PublishConfig(
            title="测试标题",
            content="这是测试内容\n#测试 #自动化",
            images=["test.jpg"],
            hashtags=["测试", "自动化"]
        )
        
        success = await publisher.publish(config)
        print(f"发布结果: {'成功' if success else '失败'}")
        
    finally:
        await publisher.close()


if __name__ == "__main__":
    asyncio.run(main())
