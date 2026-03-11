#!/usr/bin/env python3
"""
简化版发布脚本
- 生成发布命令
- 指导手动操作
- 或调用浏览器自动化
"""

import os
import sys
import argparse
from pathlib import Path

def get_latest_content(account):
    """获取最新内容"""
    base_dir = Path("/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix")
    content_dir = base_dir / "generated" / account / "high_quality"
    
    if not content_dir.exists():
        return None
    
    # 获取最新的markdown文件
    md_files = sorted(content_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not md_files:
        return None
    
    latest_md = md_files[0]
    
    # 读取内容
    with open(latest_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题（第一行）
    lines = content.split('\n')
    title = lines[0].replace('# ', '').strip()
    
    # 提取正文
    body = '\n'.join(lines[2:]).strip()
    
    # 查找图片
    images = sorted(content_dir.glob("card_*.png"))
    
    return {
        'title': title,
        'body': body,
        'images': [str(img) for img in images],
        'md_file': str(latest_md)
    }

def print_publish_guide(account, content):
    """打印发布指南"""
    print("=" * 60)
    print("🚀 小红书发布指南")
    print("=" * 60)
    print()
    print(f"账号: {account}")
    print()
    print("📋 发布步骤:")
    print()
    print("1️⃣ 打开小红书网页版")
    print("   https://creator.xiaohongshu.com/publish/publish")
    print()
    print("2️⃣ 上传图片")
    for i, img in enumerate(content['images'], 1):
        print(f"   图片{i}: {img}")
    print()
    print("3️⃣ 填写标题")
    print(f"   {content['title']}")
    print()
    print("4️⃣ 填写正文")
    print("   (以下内容已复制到剪贴板)")
    print()
    print("5️⃣ 点击发布")
    print()
    print("=" * 60)
    print()
    
    # 打印正文
    print("📝 正文内容:")
    print("-" * 60)
    print(content['body'])
    print("-" * 60)
    print()

def main():
    parser = argparse.ArgumentParser(description="小红书发布助手")
    parser.add_argument("account", help="账号名称 (tech-geek, career-growth)")
    parser.add_argument("--copy", action="store_true", help="复制内容到剪贴板")
    parser.add_argument("--browser", action="store_true", help="使用浏览器自动化")
    
    args = parser.parse_args()
    
    # 获取内容
    content = get_latest_content(args.account)
    if not content:
        print(f"❌ 未找到账号 {args.account} 的内容")
        return 1
    
    # 打印发布指南
    print_publish_guide(args.account, content)
    
    # 复制到剪贴板
    if args.copy:
        try:
            import pyperclip
            pyperclip.copy(content['body'])
            print("✅ 正文已复制到剪贴板")
        except:
            print("⚠️  复制失败，请手动复制")
    
    # 浏览器自动化
    if args.browser:
        print("🌐 启动浏览器自动化...")
        # 这里可以调用browser_publisher
        print("(功能开发中)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
