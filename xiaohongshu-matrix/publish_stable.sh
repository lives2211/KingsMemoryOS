#!/bin/bash
# 稳定版发布脚本
# 增加等待时间，适配新页面

set -euo pipefail

echo "🚀 稳定版自动发布"
echo "=================="
echo ""

if [ $# -lt 1 ]; then
    echo "用法: ./publish_stable.sh <账号>"
    echo ""
    echo "可用账号: tech-geek, career-growth"
    exit 1
fi

ACCOUNT=$1
BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"
SKILLS_DIR="$BASE_DIR/xiaohongshu-skills"

cd "$BASE_DIR"

# 账号名称
ACCOUNT_NAMES=("数码虾" "职场虾")
if [ "$ACCOUNT" == "tech-geek" ]; then
    ACCOUNT_NAME="数码虾"
elif [ "$ACCOUNT" == "career-growth" ]; then
    ACCOUNT_NAME="职场虾"
else
    ACCOUNT_NAME="$ACCOUNT"
fi

echo "📱 账号: $ACCOUNT_NAME ($ACCOUNT)"
echo ""

# 查找内容
CONTENT_DIR="$BASE_DIR/generated/$ACCOUNT/high_quality"
if [ ! -d "$CONTENT_DIR" ]; then
    echo "❌ 内容目录不存在"
    exit 1
fi

LATEST_MD=$(ls -t "$CONTENT_DIR"/*.md 2>/dev/null | head -1)
if [ -z "$LATEST_MD" ]; then
    echo "❌ 未找到内容文件"
    exit 1
fi

echo "📄 文件: $(basename $LATEST_MD)"

# 提取标题
TITLE=$(head -1 "$LATEST_MD" | sed 's/^# //')
echo "📝 标题: $TITLE"

# 查找图片
IMAGES=()
for img in "$CONTENT_DIR"/card_*.png; do
    if [ -f "$img" ]; then
        IMAGES+=("$img")
    fi
done

echo "🖼️  图片: ${#IMAGES[@]} 张"
echo ""

# 创建标题文件
echo "$TITLE" > "$CONTENT_DIR/title.txt"

echo "⏳ 等待5秒让系统准备..."
sleep 5

echo "🚀 开始发布（使用预览模式，你可以手动点击发布）..."
echo ""

cd "$SKILLS_DIR"

# 使用预览模式（只填充内容，不自动点击发布）
# 这样可以避免自动化问题，你手动确认后点击发布
python3 scripts/publish_pipeline.py \
    --title-file "$CONTENT_DIR/title.txt" \
    --content-file "$LATEST_MD" \
    --images ${IMAGES[@]} \
    --preview

echo ""
echo "=================="
echo "✅ 内容已填充到浏览器"
echo ""
echo "📋 请手动操作:"
echo "   1. 在Chrome窗口中检查内容"
echo "   2. 确认标题、正文、图片都正确"
echo "   3. 点击"发布"按钮"
echo ""
echo "💡 提示: 预览模式可以避免自动化错误"
echo "   同时确保发到正确的账号"
echo ""
