#!/bin/bash
# 手动填充内容脚本
# 打开浏览器，加载内容，手动发布

set -euo pipefail

echo "📝 内容填充助手"
echo "==============="
echo ""

if [ $# -lt 1 ]; then
    echo "用法: ./fill_content.sh <账号>"
    echo ""
    echo "示例: ./fill_content.sh career-growth"
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
for img in "${IMAGES[@]}"; do
    echo "   - $(basename $img)"
done

echo ""

# 显示内容
echo "📝 正文内容:"
echo "--------------"
echo "$CONTENT"
echo "--------------"
echo ""

# 打开小红书发布页面
echo "🌐 打开小红书发布页面..."
echo ""

# 使用xdg-open或python打开浏览器
python3 -c "
import webbrowser
webbrowser.open('https://creator.xiaohongshu.com/publish/publish')
" 2>/dev/null || echo "请手动打开: https://creator.xiaohongshu.com/publish/publish"

echo ""
echo "✅ 请按以下步骤操作:"
echo ""
echo "1️⃣ 在浏览器中登录小红书创作者中心"
echo "   https://creator.xiaohongshu.com/publish/publish"
echo ""
echo "2️⃣ 点击'上传图文'按钮"
echo ""
echo "3️⃣ 上传图片:"
for img in "${IMAGES[@]}"; do
    echo "   - $img"
done
echo ""
echo "4️⃣ 填写标题:"
echo "   $TITLE"
echo ""
echo "5️⃣ 填写正文（已复制到剪贴板）:"
echo "   （上面的内容）"
echo ""
echo "6️⃣ 点击'发布'按钮"
echo ""
echo "==============="
echo "💡 提示: 内容已准备好，请手动复制粘贴发布"
echo ""

# 尝试复制到剪贴板
python3 -c "
import pyperclip
try:
    pyperclip.copy('''$CONTENT''')
    print('✅ 正文已复制到剪贴板')
except:
    print('⚠️  请手动复制上面的正文内容')
" 2>/dev/null || echo "⚠️  请手动复制正文内容"

echo ""
