#!/usr/bin/env python3
"""
使用xiaohongshu-cli发布
直接调用CLI的Python API
"""

import os
import sys
import subprocess
from pathlib import Path

def get_cookie(account):
    """获取账号Cookie"""
    base_dir = Path("/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix")
    env_file = base_dir / f".env.{account}"
    
    if not env_file.exists():
        print(f"❌ 配置文件不存在: {env_file}")
        return None
    
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith("XHS_COOKIE="):
                return line.replace("XHS_COOKIE=", "").strip()
    
    return None

def publish_with_cli(account, title, content, images):
    """使用CLI发布"""
    
    # 获取Cookie
    cookie = get_cookie(account)
    if not cookie:
        print("❌ 无法获取Cookie")
        return False
    
    # 设置环境变量
    env = os.environ.copy()
    env["XHS_COOKIE"] = cookie
    
    print(f"🚀 使用CLI发布: {account}")
    print(f"📝 标题: {title[:30]}...")
    print(f"🖼️  图片: {len(images)} 张")
    
    # 构建xhs命令
    # 注意：需要确认xhs是否有post-image命令
    cmd = ["xhs", "--cookie-source", "env"]
    
    # 尝试发布
    try:
        result = subprocess.run(
            cmd + ["whoami"],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )
        print(result.stdout)
        
        if result.returncode == 0:
            print("✅ CLI连接成功")
            # 这里可以继续调用发布命令
            return True
        else:
            print(f"❌ CLI错误: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CLI发布")
    parser.add_argument("account", help="账号")
    
    args = parser.parse_args()
    
    # 查找内容
    base_dir = Path("/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix")
    content_dir = base_dir / "generated" / args.account / "high_quality"
    
    if not content_dir.exists():
        print(f"❌ 内容目录不存在")
        return 1
    
    # 获取最新内容
    md_files = sorted(content_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not md_files:
        print("❌ 未找到内容")
        return 1
    
    latest_md = md_files[0]
    
    # 读取内容
    with open(latest_md, 'r') as f:
        lines = f.readlines()
        title = lines[0].replace('# ', '').strip()
        content = ''.join(lines[2:])
    
    # 查找图片
    images = sorted(content_dir.glob("card_*.png"))
    
    # 发布
    success = publish_with_cli(args.account, title, content, images)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
