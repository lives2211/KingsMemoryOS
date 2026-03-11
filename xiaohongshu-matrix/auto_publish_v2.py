#!/usr/bin/env python3
"""
全自动发布脚本 V2
- 集成 XiaohongshuSkills 工具
- 使用 CDP 浏览器自动化
- 支持多账号、无头模式
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

class AutoPublisherV2:
    """全自动发布器 V2"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"):
        self.base_path = Path(base_path)
        self.skills_path = self.base_path / "xiaohongshu-skills"
        self.config_path = self.skills_path / "config"
        
    def setup_config(self, account, cookie):
        """配置账号"""
        # 创建配置文件
        config_file = self.config_path / f"{account}.json"
        
        config = {
            "cookie": cookie,
            "created_at": datetime.now().isoformat()
        }
        
        config_file.parent.mkdir(exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ 账号配置已保存: {config_file}")
        return config_file
    
    def launch_browser(self, headless=True):
        """启动浏览器"""
        print("🌐 启动 Chrome 浏览器...")
        
        cmd = [
            "python3", str(self.skills_path / "scripts" / "chrome_launcher.py")
        ]
        
        if headless:
            cmd.append("--headless")
        
        try:
            subprocess.Popen(cmd, cwd=self.skills_path)
            print("✅ 浏览器已启动")
            return True
        except Exception as e:
            print(f"❌ 浏览器启动失败: {e}")
            return False
    
    def check_login(self, account):
        """检查登录状态"""
        print(f"🔐 检查账号 {account} 登录状态...")
        
        cmd = [
            "python3", str(self.skills_path / "scripts" / "cdp_publish.py"),
            "--config", str(self.config_path / f"{account}.json"),
            "check-login"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.skills_path)
            if "已登录" in result.stdout or "login" in result.stdout.lower():
                print("✅ 登录状态正常")
                return True
            else:
                print("⚠️  需要重新登录")
                return False
        except Exception as e:
            print(f"❌ 检查失败: {e}")
            return False
    
    def publish(self, account, title, content, images, headless=True):
        """发布笔记"""
        print(f"🚀 发布笔记: {title[:30]}...")
        
        # 准备图片路径（转换为URL格式或本地路径）
        image_urls = []
        for img in images:
            img_path = Path(img)
            if img_path.exists():
                # 使用本地文件路径
                image_urls.append(str(img_path.absolute()))
        
        # 构建发布命令
        cmd = [
            "python3", str(self.skills_path / "scripts" / "publish_pipeline.py"),
            "--config", str(self.config_path / f"{account}.json"),
            "--title", title,
            "--content", content,
        ]
        
        if headless:
            cmd.append("--headless")
        
        # 添加图片
        if image_urls:
            cmd.extend(["--image-urls", ",".join(image_urls)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.skills_path)
            print(result.stdout)
            
            if result.returncode == 0:
                print("✅ 发布成功！")
                return True
            else:
                print(f"❌ 发布失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 发布异常: {e}")
            return False
    
    def publish_from_file(self, account, md_file):
        """从markdown文件发布"""
        md_path = Path(md_file)
        if not md_path.exists():
            print(f"❌ 文件不存在: {md_file}")
            return False
        
        # 读取内容
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        lines = content.split('\n')
        title = lines[0].replace('# ', '').strip()
        body = '\n'.join(lines[2:]).strip()
        
        # 查找图片
        images = sorted(md_path.parent.glob("card_*.png"))
        
        # 发布
        return self.publish(account, title, body, images)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书全自动发布 V2")
    parser.add_argument("account", help="账号名称")
    parser.add_argument("--setup", action="store_true", help="配置账号")
    parser.add_argument("--file", help="从markdown文件发布")
    parser.add_argument("--title", help="标题")
    parser.add_argument("--content", help="正文")
    parser.add_argument("--images", nargs='+', help="图片路径")
    parser.add_argument("--no-headless", action="store_true", help="显示浏览器窗口")
    
    args = parser.parse_args()
    
    publisher = AutoPublisherV2()
    
    # 配置账号
    if args.setup:
        cookie = os.getenv('XHS_COOKIE')
        if not cookie:
            print("❌ 需要设置XHS_COOKIE环境变量")
            return 1
        
        publisher.setup_config(args.account, cookie)
        return 0
    
    # 从文件发布
    if args.file:
        success = publisher.publish_from_file(args.account, args.file)
        return 0 if success else 1
    
    # 直接发布
    if args.title and args.content:
        headless = not args.no_headless
        success = publisher.publish(args.account, args.title, args.content, args.images or [], headless)
        return 0 if success else 1
    
    # 默认：显示帮助
    parser.print_help()
    return 1

if __name__ == "__main__":
    sys.exit(main())
