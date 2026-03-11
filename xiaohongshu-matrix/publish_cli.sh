#!/bin/bash
# 使用xiaohongshu-cli发布

set -euo pipefail

echo "🚀 使用xiaohongshu-cli发布"
echo "=========================="
echo ""

if [ $# -lt 1 ]; then
    echo "用法: ./publish_cli.sh <账号>"
    echo ""
    echo "可用账号: tech-geek, career-growth"
    exit 1
fi

ACCOUNT=$1
BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"

cd "$BASE_DIR"

# 账号名称
if [ "$ACCOUNT" == "tech-geek" ]; then
    ACCOUNT_NAME="数码虾"
elif [ "$ACCOUNT" == "career-growth" ]; then
    ACCOUNT_NAME="职场虾"
else
    ACCOUNT_NAME="$ACCOUNT"
fi

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

echo "✅ Cookie已加载"
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

# 提取标题和内容
TITLE=$(head -1 "$LATEST_MD" | sed 's/^# //')
CONTENT=$(tail -n +3 "$LATEST_MD")

echo "📝 标题: $TITLE"
echo ""

# 查找图片
IMAGES=()
for img in "$CONTENT_DIR"/card_*.png; do
    if [ -f "$img" ]; then
        IMAGES+=("$img")
    fi
done

echo "🖼️  图片: ${#IMAGES[@]} 张"
echo ""

# 使用xiaohongshu-cli发布
echo "🚀 开始发布..."
echo ""

# 方法1: 使用xhs post-image命令（如果有）
# 方法2: 使用xhs read查看状态
# 方法3: 使用其他CLI功能

echo "✅ xiaohongshu-cli已安装"
echo "   版本: $(xhs --version)"
echo ""

echo "💡 CLI功能:"
xhs --help | head -20

echo ""
echo "=========================="
echo "✅ 配置完成！"
echo ""
echo "xiaohongshu-cli功能:"
echo "  - xhs login       登录"
echo "  - xhs search      搜索"
echo "  - xhs read        阅读笔记"
echo "  - xhs feed        推荐流"
echo "  - xhs hot         热门"
echo "  - xhs favorites   收藏"
echo ""
echo "详细使用: xhs --help"
echo ""
