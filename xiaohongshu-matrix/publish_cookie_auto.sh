#!/bin/bash
# Cookie全自动发布脚本
# 无需扫码，直接使用Cookie发布

set -euo pipefail

echo "🚀 Cookie全自动发布"
echo "===================="
echo ""

if [ $# -lt 1 ]; then
    echo "用法: ./publish_cookie_auto.sh <账号>"
    echo ""
    echo "可用账号:"
    echo "  tech-geek      - 数码虾"
    echo "  career-growth  - 职场虾"
    echo ""
    exit 1
fi

ACCOUNT=$1
BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"
SKILLS_DIR="$BASE_DIR/xiaohongshu-skills"

cd "$BASE_DIR"

# 账号名称映射
declare -A ACCOUNT_NAMES=(
    ["tech-geek"]="数码虾"
    ["career-growth"]="职场虾"
)

ACCOUNT_NAME=${ACCOUNT_NAMES[$ACCOUNT]:-$ACCOUNT}

echo "📱 账号: $ACCOUNT_NAME ($ACCOUNT)"
echo ""

# 加载Cookie
ENV_FILE="$BASE_DIR/.env.$ACCOUNT"
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ 配置文件不存在: $ENV_FILE"
    exit 1
fi

export XHS_COOKIE=$(grep "^XHS_COOKIE=" "$ENV_FILE" | sed 's/XHS_COOKIE=//' | head -1)

if [ -z "$XHS_COOKIE" ]; then
    echo "❌ Cookie未配置"
    exit 1
fi

echo "✅ Cookie已加载 (${#XHS_COOKIE} 字符)"
echo ""

# 查找内容文件
CONTENT_DIR="$BASE_DIR/generated/$ACCOUNT/high_quality"
if [ ! -d "$CONTENT_DIR" ]; then
    echo "❌ 内容目录不存在"
    exit 1
fi

# 获取最新的markdown文件
LATEST_MD=$(ls -t "$CONTENT_DIR"/*.md 2>/dev/null | head -1)
if [ -z "$LATEST_MD" ]; then
    echo "❌ 未找到内容文件"
    exit 1
fi

echo "📄 内容文件: $(basename $LATEST_MD)"

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

# 使用XiaohongshuSkills的Cookie模式发布
echo "🚀 开始发布..."
echo ""

cd "$SKILLS_DIR"

# 创建标题文件
echo "$TITLE" > "$CONTENT_DIR/title.txt"

# 使用环境变量Cookie发布
python3 scripts/publish_pipeline.py \
    --title-file "$CONTENT_DIR/title.txt" \
    --content-file "$LATEST_MD" \
    --images ${IMAGES[@]} \
    --auto-publish \
    --headless

RESULT=$?

echo ""
echo "===================="
if [ $RESULT -eq 0 ]; then
    echo "✅ $ACCOUNT_NAME 发布成功！"
    echo ""
    echo "📋 发布信息:"
    echo "   账号: $ACCOUNT_NAME"
    echo "   标题: $TITLE"
    echo "   图片: ${#IMAGES[@]} 张"
else
    echo "❌ $ACCOUNT_NAME 发布失败"
    echo ""
    echo "💡 可能原因:"
    echo "   - Cookie已过期"
    echo "   - 需要使用浏览器扫码模式"
fi

echo ""
