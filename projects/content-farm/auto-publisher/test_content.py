#!/usr/bin/env python3
"""
测试内容加载功能
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "core"))

from content_loader import ContentLoader


def test_content_loading():
    """测试内容加载"""
    print("📚 测试内容加载...")
    
    try:
        loader = ContentLoader("../xiaohongshu")
        
        # 列出可用日期
        dates = loader.list_available_dates()
        print(f"\n可用日期: {dates[:5]}")  # 只显示前5个
        
        # 加载今天的笔记
        notes = loader.load_notes_by_date(limit=3)
        
        print(f"\n加载到 {len(notes)} 篇笔记:")
        for i, note in enumerate(notes, 1):
            print(f"\n{i}. {note.title}")
            print(f"   标签: {note.hashtags}")
            print(f"   内容预览: {note.content[:80]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_content_loading()
    sys.exit(0 if success else 1)
