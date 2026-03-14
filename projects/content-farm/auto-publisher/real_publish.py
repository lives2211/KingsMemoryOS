#!/usr/bin/env python3
"""
真实发布流程
完整的端到端发布，包括浏览器自动化
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path('.') / "core"))

from content_loader import ContentLoader
from card_generator import CardGenerator, CardConfig
from publisher import XHSPublisher, PublishConfig
from scheduler import PublishScheduler
from monitor import PublishMonitor, PublishRecord
from account_manager import AccountManager
from loguru import logger
import uuid


async def real_publish():
    """真实发布流程"""
    print("🚀 小红书真实发布流程")
    print("=" * 60)
    
    # 初始化组件
    monitor = PublishMonitor()
    account_manager = AccountManager()
    
    # 1. 检查账号
    print("\n👤 步骤1: 检查账号")
    print("-" * 60)
    
    account = account_manager.get_default()
    if not account:
        print("⚠️ 没有默认账号，创建默认账号...")
        account = account_manager.add_account("default", "默认账号")
    
    print(f"✅ 账号: {account.name} ({account.alias})")
    print(f"   状态: {account.status}")
    
    # 2. 检查Cookie
    print("\n🔐 步骤2: 检查Cookie")
    print("-" * 60)
    
    cookie_file = Path(f"cookies/{account.cookie_file}")
    if not cookie_file.exists():
        print("❌ Cookie不存在，请先登录:")
        print("   python3 manual_login.py")
        return False
    
    print(f"✅ Cookie文件存在: {cookie_file}")
    
    # 3. 加载内容
    print("\n📚 步骤3: 加载内容")
    print("-" * 60)
    
    loader = ContentLoader("../xiaohongshu")
    notes = loader.load_all_pending_notes(limit=1)
    
    if not notes:
        print("❌ 没有可发布的笔记")
        return False
    
    note = notes[0]
    print(f"✅ 找到笔记: {note.title}")
    print(f"   来源: {note.source_file}")
    
    # 4. 检查发布计划
    print("\n⏰ 步骤4: 检查发布计划")
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
    
    if not scheduler.should_publish_now():
        next_time = scheduler.get_next_publish_time()
        print(f"⏳ 不在发布时间段内")
        print(f"   下次可发布时间: {next_time.strftime('%Y-%m-%d %H:%M')}")
        print("\n是否强制发布? (y/n)")
        # 在自动化环境中默认继续
        print("   继续执行...")
    else:
        print("✅ 当前在发布时间段内")
    
    # 5. 生成卡片
    print("\n🎨 步骤5: 生成卡片")
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
        print(f"✅ 生成 {len(cards)} 张卡片")
        for card in cards:
            print(f"   - {Path(card).name}")
    except Exception as e:
        print(f"❌ 卡片生成失败: {e}")
        return False
    
    # 6. 创建发布记录
    print("\n📝 步骤6: 创建发布记录")
    print("-" * 60)
    
    record_id = str(uuid.uuid4())
    record = PublishRecord(
        id=record_id,
        title=note.title,
        account=account.name,
        status="pending",
        created_at=datetime.now().isoformat(),
        image_count=len(cards),
        hashtags_count=len(note.hashtags)
    )
    monitor.add_record(record)
    print(f"✅ 记录ID: {record_id}")
    
    # 7. 启动浏览器并发布
    print("\n🌐 步骤7: 浏览器发布")
    print("-" * 60)
    
    publisher = None
    try:
        publisher = XHSPublisher()
        
        print("1. 启动浏览器...")
        await publisher.launch_browser(headless=False)
        
        print("2. 加载Cookie...")
        if await publisher.load_cookies():
            print("   ✅ Cookie加载成功")
        else:
            print("   ⚠️ Cookie加载失败，尝试检查登录状态")
        
        print("3. 检查登录状态...")
        if await publisher.check_login():
            print("   ✅ 已登录")
        else:
            print("   ❌ 未登录，需要重新扫码")
            print("   请运行: python3 manual_login.py")
            monitor.update_record(record_id, status="failed", error_message="未登录")
            return False
        
        print("4. 准备发布配置...")
        publish_config = PublishConfig(
            title=note.title,
            content=note.content,
            images=cards,
            hashtags=note.hashtags
        )
        
        print("5. 执行发布...")
        print("   ⚠️ 注意: 实际发布需要人工确认")
        print("   浏览器将打开，请检查内容后手动点击发布")
        
        # 预览模式：只填充内容，不自动点击发布
        success = await publisher.publish(publish_config)
        
        if success:
            print("✅ 发布成功！")
            monitor.update_record(
                record_id,
                status="success",
                published_at=datetime.now().isoformat()
            )
            account_manager.update_status(account.name, "active")
            account_manager.increment_notes(account.name)
            scheduler.record_publish()
        else:
            print("❌ 发布失败")
            monitor.update_record(record_id, status="failed")
            return False
        
    except Exception as e:
        print(f"❌ 发布异常: {e}")
        monitor.update_record(record_id, status="failed", error_message=str(e))
        import traceback
        traceback.print_exc()
        return False
    finally:
        if publisher:
            await publisher.close()
    
    # 8. 完成
    print("\n" + "=" * 60)
    print("✅ 发布流程完成！")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = asyncio.run(real_publish())
    sys.exit(0 if success else 1)
