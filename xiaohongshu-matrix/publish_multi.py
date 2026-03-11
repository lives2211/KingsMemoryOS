#!/usr/bin/env python3
"""
多账号发布脚本
- 为每个账号创建独立的Chrome配置
- 支持多账号切换
"""

import os
import sys
import subprocess
from pathlib import Path

# 账号配置
ACCOUNTS = {
    "tech-geek": {
        "name": "数码虾",
        "cookie_file": ".env.tech-geek",
    },
    "career-growth": {
        "name": "职场虾",
        "cookie_file": ".env.career-growth",
    },
}

def get_cookie(account):
    """获取账号Cookie"""
    base_dir = Path("/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix")
    cookie_file = base_dir / ACCOUNTS[account]["cookie_file"]
    
    if not cookie_file.exists():
        print(f"❌ Cookie文件不存在: {cookie_file}")
        return None
    
    with open(cookie_file, 'r') as f:
        for line in f:
            if line.startswith("XHS_COOKIE="):
                return line.replace("XHS_COOKIE=", "").strip()
    
    return None

def publish_with_account(account, content_file):
    """使用指定账号发布"""
    
    base_dir = Path("/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix")
    skills_dir = base_dir / "xiaohongshu-skills"
    
    # 获取Cookie
    cookie = get_cookie(account)
    if not cookie:
        print(f"❌ 无法获取 {account} 的Cookie")
        return False
    
    # 设置环境变量
    env = os.environ.copy()
    env["XHS_COOKIE"] = cookie
    
    # 为每个账号创建独立的Chrome配置
    profile_dir = f"/home/fengxueda/Google/Chrome/XiaohongshuProfiles/{account}"
    
    # 构建命令
    cmd = [
        "python3", str(skills_dir / "scripts" / "publish_pipeline.py"),
        "--content-file", str(content_file),
        "--headless",
    ]
    
    print(f"🚀 使用账号 {ACCOUNTS[account]['name']} ({account}) 发布...")
    print(f"📄 内容文件: {content_file}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=skills_dir,
            env=env
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print(f"✅ {account} 发布成功！")
            return True
        else:
            print(f"❌ {account} 发布失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ {account} 发布异常: {e}")
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="多账号发布")
    parser.add_argument("account", help="账号名称")
    parser.add_argument("--file", required=True, help="内容文件路径")
    
    args = parser.parse_args()
    
    if args.account not in ACCOUNTS:
        print(f"❌ 未知账号: {args.account}")
        print(f"可用账号: {', '.join(ACCOUNTS.keys())}")
        return 1
    
    success = publish_with_account(args.account, args.file)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
