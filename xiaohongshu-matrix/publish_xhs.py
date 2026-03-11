#!/usr/bin/env python3
"""
小红书全自动发布 - 修复版
使用XiaohongshuSkills工具
"""

import os
import sys
import subprocess
from pathlib import Path

def publish_note(account, title_file, content_file, images, headless=True):
    """
    发布笔记
    
    Args:
        account: 账号名称
        title_file: 标题文件路径
        content_file: 正文文件路径
        images: 图片路径列表
        headless: 是否无头模式
    """
    
    base_dir = Path("/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix")
    skills_dir = base_dir / "xiaohongshu-skills"
    
    # 构建命令
    cmd = [
        "python3", str(skills_dir / "scripts" / "publish_pipeline.py"),
        "--title-file", str(title_file),
        "--content-file", str(content_file),
    ]
    
    # 添加图片
    if images:
        cmd.append("--images")
        for img in images:
            cmd.append(str(img))
    
    # 添加其他参数
    if headless:
        cmd.append("--headless")
    
    cmd.append("--auto-publish")
    
    print(f"🚀 执行命令: {' '.join(cmd[:5])}...")
    
    try:
        # 设置环境变量
        env = os.environ.copy()
        
        # 执行发布
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=skills_dir,
            env=env
        )
        
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

def publish_from_generated(account):
    """从生成的内容发布"""
    
    base_dir = Path("/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix")
    content_dir = base_dir / "generated" / account / "high_quality"
    
    if not content_dir.exists():
        print(f"❌ 内容目录不存在: {content_dir}")
        return False
    
    # 查找最新的markdown文件
    md_files = sorted(content_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not md_files:
        print("❌ 未找到内容文件")
        return False
    
    latest_md = md_files[0]
    
    # 提取标题（第一行）
    with open(latest_md, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        title = lines[0].replace('# ', '').strip()
    
    # 创建标题文件
    title_file = content_dir / "title.txt"
    with open(title_file, 'w', encoding='utf-8') as f:
        f.write(title)
    
    # 查找图片
    images = sorted(content_dir.glob("card_*.png"))
    
    print(f"📄 发布文件: {latest_md.name}")
    print(f"📝 标题: {title}")
    print(f"🖼️  图片: {len(images)} 张")
    
    # 发布
    return publish_note(account, title_file, latest_md, images)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书全自动发布")
    parser.add_argument("account", help="账号名称 (tech-geek, career-growth)")
    parser.add_argument("--no-headless", action="store_true", help="显示浏览器窗口")
    
    args = parser.parse_args()
    
    # 发布
    success = publish_from_generated(args.account)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
