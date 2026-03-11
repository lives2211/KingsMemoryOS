#!/bin/bash
# 使用 agentic-browser 自动发布到小红书

set -euo pipefail

echo "🌐 使用浏览器自动化发布"
echo "========================"
echo ""

if [ $# -lt 1 ]; then
    echo "用法: ./publish_with_browser.sh <账号>"
    echo ""
    echo "示例: ./publish_with_browser.sh tech-geek"
    exit 1
fi

ACCOUNT=$1
BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"

cd "$BASE_DIR"

# 查找内容文件
CONTENT_DIR="$BASE_DIR/generated/$ACCOUNT"
MD_FILES=$(find "$CONTENT_DIR" -name "ai_*.md" -type f 2>/dev/null | head -1)

if [ -z "$MD_FILES" ]; then
    echo "❌ 未找到内容文件"
    exit 1
fi

LATEST_MD="$MD_FILES"
TITLE=$(head -1 "$LATEST_MD" | sed 's/^# //')

echo "📱 账号: $ACCOUNT"
echo "📝 标题: $TITLE"
echo "📄 文件: $(basename $LATEST_MD)"
echo ""

# 使用 agentic-browser 发布
echo "🌐 启动浏览器自动化..."
echo ""

# 步骤1: 打开小红书创作者中心
echo "1️⃣ 打开发布页面..."

SESSION=$(infsh app run agent-browser --function open \
    --session new \
    --input '{
        "url": "https://creator.xiaohongshu.com/publish/publish",
        "headless": false,
        "viewport": {"width": 1920, "height": 1080}
    }' 2>&1)

echo "$SESSION" | head -20

# 提取 session_id
SESSION_ID=$(echo "$SESSION" | grep -o '"session_id": "[^"]*"' | cut -d'"' -f4)

if [ -z "$SESSION_ID" ]; then
    echo "❌ 无法获取session_id"
    echo "   请确保已安装 agentic-browser: infsh app install agent-browser"
    exit 1
fi

echo "✅ Session ID: $SESSION_ID"
echo ""

# 步骤2: 等待页面加载并获取元素
echo "2️⃣ 获取页面元素..."

sleep 3

SNAPSHOT=$(infsh app run agent-browser --function snapshot \
    --session "$SESSION_ID" \
    --input '{}' 2>&1)

echo "$SNAPSHOT" | head -30

# 步骤3: 点击"上传图文"按钮
echo "3️⃣ 点击上传图文..."

# 查找上传图文按钮的ref
UPLOAD_REF=$(echo "$SNAPSHOT" | grep -i "上传图文" | grep -o '@e[0-9]*' | head -1)

if [ -n "$UPLOAD_REF" ]; then
    infsh app run agent-browser --function interact \
        --session "$SESSION_ID" \
        --input "{\"action\": \"click\", \"ref\": \"$UPLOAD_REF\"}" 2>&1
else
    echo "⚠️  未找到上传图文按钮，可能页面已加载"
fi

echo ""
echo "💡 浏览器已打开，请手动完成以下步骤:"
echo "   1. 扫码登录（如果需要）"
echo "   2. 点击'上传图文'"
echo "   3. 上传图片"
echo "   4. 填写标题: $TITLE"
echo "   5. 复制正文内容"
echo "   6. 点击发布"
echo ""

# 显示内容
echo "📝 正文内容预览:"
echo "-------------------"
tail -n +3 "$LATEST_MD" | head -20
echo "..."
echo "-------------------"
echo ""

# 保持会话打开
echo "⏳ 浏览器保持打开，请完成发布..."
echo "   按 Ctrl+C 结束后关闭浏览器"
echo ""

# 等待用户完成
read -p "发布完成后按回车关闭浏览器..."

# 关闭浏览器
echo "4️⃣ 关闭浏览器..."
infsh app run agent-browser --function close \
    --session "$SESSION_ID" \
    --input '{}' 2>&1

echo ""
echo "✅ 发布流程完成！"
