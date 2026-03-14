#!/usr/bin/env python3
"""
快速发布脚本 - 一键发布最新笔记
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "core"))

from content_loader import ContentLoader
from card_generator import CardGenerator, CardConfig
from api_publisher import XHSAPIPublisher, APIPublishConfig
from loguru import logger


async def quick_publish():
    """快速发布最新笔记"""
    print("🚀 小红书快速发布")
    print("=" * 50)
    
    # 1. 加载最新笔记
    print("\n📚 加载最新笔记...")
    loader = ContentLoader("../xiaohongshu")
    notes = loader.load_all_pending_notes(limit=1)
    
    if not notes:
        print("❌ 没有可发布的笔记")
        return False
    
    note = notes[0]
    print(f"✅ 找到笔记: {note.title}")
    print(f"   标签: {', '.join(note.hashtags[:5])}...")
    
    # 2. 生成卡片
    print("\n🎨 生成卡片...")
    generator = CardGenerator("./card-renderer")
    
    config = CardConfig(
        theme="playful-geometric",
        mode="auto-split",
        width=1080,
        height=1440,
        dpr=2
    )
    
    try:
        cards = generator.generate_from_content(
            title=note.title,
            content=note.content,
            output_dir=f"./output/{datetime.now().strftime('%Y%m%d')}",
            config=config
        )
        print(f"✅ 生成 {len(cards)} 张卡片")
        for card in cards:
            print(f"   - {card}")
    except Exception as e:
        print(f"❌ 卡片生成失败: {e}")
        return False
    
    # 3. 检查登录状态
    print("\n🔐 检查登录状态...")
    publisher = XHSAPIPublisher()
    
    if not publisher.check_auth():
        print("⚠️ 未登录，请先运行: xhs auth")
        print("   或使用: python3 main.py login")
        return False
    
    print("✅ 已登录")
    
    # 4. 准备发布
    print("\n📤 准备发布...")
    print(f"   标题: {note.title}")
    print(f"   图片: {len(cards)} 张")
    print(f"   标签: {len(note.hashtags)} 个")
    
    # 注意：xiaohongshu-cli 的发布功能需要确认
    print("\n⚠️ 注意: 图片发布功能需要 xiaohongshu-cli 支持")
    print("   当前版本主要支持文字内容发布")
    
    # 显示发布预览
    print("\n" + "=" * 50)
    print("📋 发布预览:")
    print("=" * 50)
    print(f"标题: {note.title}")
    print(f"\n正文预览:")
    print(note.content[:200] + "...")
    print(f"\n标签: {' '.join(['#' + t for t in note.hashtags[:10]])}")
    print("=" * 50)
    
    print("\n✅ 准备完成！")
    print("\n下一步:")
    print("  1. 使用 CDP 浏览器发布: python3 main.py publish")
    print("  2. 或手动使用 xiaohongshu-cli 发布")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(quick_publish())
    sys.exit(0 if success else 1)
