#!/usr/bin/env python3
"""
测试卡片生成功能
"""

import sys
from pathlib import Path

# 添加core目录到路径
sys.path.insert(0, str(Path(__file__).parent / "core"))

from card_generator import CardGenerator, CardConfig


def test_card_generation():
    """测试卡片生成"""
    print("🎨 测试卡片生成...")
    
    try:
        generator = CardGenerator("./card-renderer")
        
        # 测试内容
        title = "🔥马化腾官宣！腾讯'龙虾'AI Agent来了"
        content = """腾讯正式发布"龙虾"AI Agent矩阵！

🎯 WorkBuddy：1分钟连接企微
- 自动回复消息
- 智能会议记录
- 任务自动分配

💡 亮点功能：
✅ 兼容OpenClaw技能包
✅ 零代码接入企业微信
✅ 支持自定义工作流

打工人效率神器，赶紧试试吧！"""
        
        # 生成卡片
        config = CardConfig(
            theme="playful-geometric",
            mode="auto-split",
            width=1080,
            height=1440,
            dpr=2
        )
        
        cards = generator.generate_from_content(
            title=title,
            content=content,
            output_dir="./output/test",
            config=config
        )
        
        print(f"✅ 成功生成 {len(cards)} 张卡片:")
        for card in cards:
            print(f"   - {card}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_card_generation()
    sys.exit(0 if success else 1)
