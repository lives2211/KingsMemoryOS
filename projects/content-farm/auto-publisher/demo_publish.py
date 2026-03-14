#!/usr/bin/env python3
"""
发布流程演示
展示完整的发布流程（不实际发布）
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path('.') / "core"))

from content_loader import ContentLoader
from card_generator import CardGenerator, CardConfig
from scheduler import PublishScheduler
from loguru import logger


async def demo_publish():
    """演示发布流程"""
    print("🚀 小红书自动发布系统 - 流程演示")
    print("=" * 60)
    
    # 1. 加载内容
    print("\n📚 步骤1: 加载内容")
    print("-" * 60)
    loader = ContentLoader("../xiaohongshu")
    notes = loader.load_all_pending_notes(limit=1)
    
    if not notes:
        print("❌ 没有可发布的笔记")
        return False
    
    note = notes[0]
    print(f"✅ 找到笔记: {note.title}")
    print(f"   创建日期: {note.created_date}")
    print(f"   标签数量: {len(note.hashtags)}")
    print(f"   内容长度: {len(note.content)} 字符")
    
    # 2. 生成卡片
    print("\n🎨 步骤2: 生成小红书卡片")
    print("-" * 60)
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
        print(f"✅ 成功生成 {len(cards)} 张卡片")
        for i, card in enumerate(cards, 1):
            size = Path(card).stat().st_size / 1024
            print(f"   卡片{i}: {size:.1f} KB")
    except Exception as e:
        print(f"❌ 卡片生成失败: {e}")
        return False
    
    # 3. 检查发布计划
    print("\n⏰ 步骤3: 检查发布计划")
    print("-" * 60)
    
    scheduler_config = {
        'publish_windows': [
            {'start': '08:00', 'end': '10:00', 'weight': 0.3},
            {'start': '12:00', 'end': '14:00', 'weight': 0.3},
            {'start': '19:00', 'end': '22:00', 'weight': 0.4}
        ],
        'max_daily_posts': 3,
        'min_interval': 1800,
        'max_interval': 7200
    }
    
    scheduler = PublishScheduler(scheduler_config)
    
    if scheduler.should_publish_now():
        print("✅ 当前在发布时间段内，可以发布")
    else:
        next_time = scheduler.get_next_publish_time()
        print(f"⏳ 不在发布时间段内")
        print(f"   下次可发布时间: {next_time.strftime('%Y-%m-%d %H:%M')}")
    
    # 4. 发布预览
    print("\n📤 步骤4: 发布预览")
    print("-" * 60)
    print(f"标题: {note.title}")
    print(f"图片: {len(cards)} 张")
    print(f"标签: {' '.join(['#' + t for t in note.hashtags[:10]])}")
    
    # 5. 模拟发布流程
    print("\n🎯 步骤5: 模拟发布流程")
    print("-" * 60)
    print("1. 启动浏览器...")
    print("2. 加载Cookie...")
    print("3. 访问创作者中心...")
    print("4. 上传图片...")
    print("5. 填写标题和正文...")
    print("6. 添加话题标签...")
    print("7. 点击发布按钮...")
    print("8. 等待发布完成...")
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("=" * 60)
    print("\n实际发布命令:")
    print("  python3 main.py publish")
    print("  或")
    print("  python3 quick_publish.py")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(demo_publish())
    sys.exit(0 if success else 1)
