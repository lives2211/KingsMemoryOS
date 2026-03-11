#!/usr/bin/env python3
"""
小红书封面生成器 - 简化版
生成 1080x1440 (3:4) 比例的封面图
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys
from datetime import datetime

def create_xhs_cover(emoji, title, subtitle, output_path, theme="default"):
    """创建小红书风格封面"""
    
    # 画布尺寸 (3:4比例)
    width, height = 1080, 1440
    
    # 主题配色
    themes = {
        "default": {
            "bg_top": "#667eea",
            "bg_bottom": "#764ba2",
            "card_bg": "#ffffff",
            "text_title": "#1a1a2e",
            "text_subtitle": "#4a4a6a",
            "accent": "#667eea"
        },
        "tech": {
            "bg_top": "#0f2027",
            "bg_bottom": "#203a43",
            "card_bg": "#ffffff",
            "text_title": "#0f2027",
            "text_subtitle": "#2c5364",
            "accent": "#00d2ff"
        },
        "warm": {
            "bg_top": "#ff9a9e",
            "bg_bottom": "#fecfef",
            "card_bg": "#ffffff",
            "text_title": "#5d4157",
            "text_subtitle": "#a8caba",
            "accent": "#ff9a9e"
        }
    }
    
    colors = themes.get(theme, themes["default"])
    
    # 创建渐变背景
    img = Image.new('RGB', (width, height), colors["bg_top"])
    draw = ImageDraw.Draw(img)
    
    # 绘制渐变
    for y in range(height):
        ratio = y / height
        r = int(int(colors["bg_top"][1:3], 16) * (1 - ratio) + int(colors["bg_bottom"][1:3], 16) * ratio)
        g = int(int(colors["bg_top"][3:5], 16) * (1 - ratio) + int(colors["bg_bottom"][3:5], 16) * ratio)
        b = int(int(colors["bg_top"][5:7], 16) * (1 - ratio) + int(colors["bg_bottom"][5:7], 16) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 白色卡片区域
    card_margin = 60
    card_top = 300
    card_height = height - card_top - card_margin
    draw.rounded_rectangle(
        [(card_margin, card_top), (width - card_margin, height - card_margin)],
        radius=30,
        fill=colors["card_bg"]
    )
    
    # 尝试加载字体
    try:
        # 尝试系统字体
        font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
            "/System/Library/Fonts/PingFang.ttc",  # macOS
            "C:/Windows/Fonts/msyh.ttc",  # Windows
        ]
        
        emoji_font = None
        title_font = None
        subtitle_font = None
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                emoji_font = ImageFont.truetype(font_path, 120)
                title_font = ImageFont.truetype(font_path, 70)
                subtitle_font = ImageFont.truetype(font_path, 40)
                break
        
        if not emoji_font:
            # 使用默认字体
            emoji_font = ImageFont.load_default()
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            
    except Exception as e:
        print(f"字体加载失败: {e}")
        emoji_font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # 绘制Emoji（顶部）
    emoji_y = 120
    bbox = draw.textbbox((0, 0), emoji, font=emoji_font)
    emoji_width = bbox[2] - bbox[0]
    emoji_x = (width - emoji_width) // 2
    draw.text((emoji_x, emoji_y), emoji, font=emoji_font, fill="white")
    
    # 绘制标题（卡片内）
    title_y = card_top + 150
    
    # 处理长标题换行
    max_width = width - 2 * card_margin - 80
    words = title
    lines = []
    current_line = ""
    
    for char in words:
        test_line = current_line + char
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char
    if current_line:
        lines.append(current_line)
    
    # 如果没有换行，直接使用原标题
    if not lines:
        lines = [title]
    
    # 绘制每一行
    line_height = 90
    total_height = len(lines) * line_height
    start_y = title_y - total_height // 2 + 100
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        line_width = bbox[2] - bbox[0]
        line_x = (width - line_width) // 2
        draw.text((line_x, start_y + i * line_height), line, font=title_font, fill=colors["text_title"])
    
    # 绘制副标题
    subtitle_y = start_y + len(lines) * line_height + 60
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=colors["text_subtitle"])
    
    # 保存
    img.save(output_path, quality=95)
    print(f"✅ 封面已生成: {output_path}")
    return output_path

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="生成小红书封面")
    parser.add_argument("--emoji", required=True, help="装饰Emoji")
    parser.add_argument("--title", required=True, help="主标题")
    parser.add_argument("--subtitle", required=True, help="副标题")
    parser.add_argument("--output", required=True, help="输出路径")
    parser.add_argument("--theme", default="default", choices=["default", "tech", "warm"])
    
    args = parser.parse_args()
    
    create_xhs_cover(args.emoji, args.title, args.subtitle, args.output, args.theme)