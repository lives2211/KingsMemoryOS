#!/usr/bin/env python3
"""
自动切换账号脚本
- 退出当前账号
- 登录新账号
- 自动扫码
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class AccountSwitcher:
    """账号切换器"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"):
        self.base_path = Path(base_path)
        self.skills_path = self.base_path / "xiaohongshu-skills"
    
    def close_chrome(self):
        """关闭Chrome"""
        print("🔄 关闭Chrome...")
        subprocess.run(["pkill", "-f", "Google Chrome"], capture_output=True)
        time.sleep(2)
        print("✅ Chrome已关闭")
    
    def clear_login_cache(self):
        """清除登录缓存"""
        print("🧹 清除登录缓存...")
        cache_dir = Path.home() / "Google" / "Chrome" / "XiaohongshuProfiles" / "default"
        if cache_dir.exists():
            # 删除缓存文件但保留配置
            for item in cache_dir.glob("*"):
                if item.is_file() and "cookie" in item.name.lower():
                    item.unlink()
        print("✅ 缓存已清除")
    
    def launch_chrome(self):
        """启动Chrome"""
        print("🌐 启动Chrome...")
        cmd = [
            "python3", str(self.skills_path / "scripts" / "chrome_launcher.py")
        ]
        subprocess.Popen(cmd, cwd=self.skills_path)
        time.sleep(5)
        print("✅ Chrome已启动")
    
    def switch_to_account(self, account_name):
        """切换到指定账号"""
        print(f"\n🎯 切换到账号: {account_name}")
        print("=" * 50)
        
        # 1. 关闭Chrome
        self.close_chrome()
        
        # 2. 清除登录缓存
        self.clear_login_cache()
        
        # 3. 启动Chrome
        self.launch_chrome()
        
        # 4. 等待扫码登录
        print(f"\n📱 请扫码登录 {account_name} 账号")
        print("   1. 在Chrome窗口中找到二维码")
        print("   2. 用手机小红书APP扫码")
        print("   3. 登录成功后按回车继续")
        print("")
        input("登录完成后按回车继续...")
        
        # 5. 验证登录
        print("\n🔐 验证登录...")
        result = subprocess.run(
            ["python3", str(self.skills_path / "scripts" / "cdp_publish.py"), "check-login"],
            capture_output=True,
            text=True,
            cwd=self.skills_path
        )
        
        if "Login confirmed" in result.stdout or "已登录" in result.stdout:
            print(f"✅ {account_name} 登录成功！")
            return True
        else:
            print(f"❌ {account_name} 登录失败")
            return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="切换小红书账号")
    parser.add_argument("account", help="账号名称 (如: 数码虾, 职场虾)")
    
    args = parser.parse_args()
    
    switcher = AccountSwitcher()
    success = switcher.switch_to_account(args.account)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
