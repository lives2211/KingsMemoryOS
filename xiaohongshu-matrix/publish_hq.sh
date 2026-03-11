#!/bin/bash
# 发布高质量内容脚本

set -euo pipefail

echo "🚀 小红书高质量内容发布"
echo "========================"
echo ""

# 检查参数
if [ $# -lt 1 ]; then
    echo "用法: ./publish_hq.sh <账号>"
    echo ""
    echo "可用账号:"
    echo "  tech-geek      - 数码虾"
    echo "  career-growth  - 职场虾"
    echo ""
    echo "示例:"
    echo "  ./publish_hq.sh tech-geek"
    exit 1
fi

ACCOUNT=$1
BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"

# 检查账号配置
ENV_FILE="$BASE_DIR/.env.$ACCOUNT"
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ 账号配置不存在: $ENV_FILE"
    exit 1
fi

# 加载Cookie
echo "🍪 加载Cookie..."
export XHS_COOKIE=$(grep "XHS_COOKIE=" "$ENV_FILE" | cut -d'=' -f2-)

if [ -z "$XHS_COOKIE" ]; then
    echo "❌ Cookie未配置"
    exit 1
fi

echo "✅ Cookie已加载"
echo ""

# 查找最新内容
CONTENT_DIR="$BASE_DIR/generated/$ACCOUNT/high_quality"
if [ ! -d "$CONTENT_DIR" ]; then
    echo "❌ 内容目录不存在: $CONTENT_DIR"
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

# 提取正文（去掉第一行标题）
CONTENT=$(tail -n +3 "$LATEST_MD")
echo "📝 正文长度: ${#CONTENT} 字符"

# 查找图片
IMAGES=()
for img in "$CONTENT_DIR"/card_*.png; do
    if [ -f "$img" ]; then
        IMAGES+=("$img")
    fi
done

echo "🖼️  图片数量: ${#IMAGES[@]}"
for img in "${IMAGES[@]}"; do
    echo "   - $(basename $img)"
done

echo ""
echo "========================"
echo "准备发布..."
echo ""

# 使用浏览器自动化发布
cd "$BASE_DIR"
python3 browser_publisher.py << EOF
import os
from browser_publisher import publish_with_browser

cookie = os.getenv('XHS_COOKIE')
images = ${IMAGES[@]}

success = publish_with_browser(
    account="$ACCOUNT",
    title="$TITLE",
    content="""$CONTENT""",
    images=images,
    cookie=cookie
)

if success:
    print("✅ 发布成功")
else:
    print("❌ 发布失败")
EOF

echo ""
echo "========================"
if [ $? -eq 0 ]; then
    echo "✅ 发布完成！"
else
    echo "❌ 发布失败，请检查错误信息"
fi
