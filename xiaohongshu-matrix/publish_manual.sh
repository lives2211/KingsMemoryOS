#!/bin/bash
# 手动区分发布脚本
# 每个账号单独登录、单独发布

set -euo pipefail

echo "🚀 小红书多账号手动发布"
echo "========================"
echo ""

# 检查参数
if [ $# -lt 1 ]; then
    echo "用法: ./publish_manual.sh <账号>"
    echo ""
    echo "可用账号:"
    echo "  tech-geek      - 数码虾"
    echo "  career-growth  - 职场虾"
    echo ""
    echo "步骤:"
    echo "  1. 运行脚本选择账号"
    echo "  2. 扫码登录该账号"
    echo "  3. 自动发布内容"
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

# 查找内容文件
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
echo ""

# 步骤1: 关闭现有Chrome
echo "1️⃣ 关闭现有Chrome..."
pkill -f "Google Chrome" 2>/dev/null || true
sleep 2
echo "✅ Chrome已关闭"
echo ""

# 步骤2: 启动Chrome（有窗口，用于扫码）
echo "2️⃣ 启动Chrome浏览器..."
echo "   请等待Chrome窗口弹出"
echo ""

cd "$SKILLS_DIR"
python3 scripts/chrome_launcher.py &
CHROME_PID=$!

sleep 5

echo "✅ Chrome已启动 (PID: $CHROME_PID)"
echo ""

# 步骤3: 检查登录
echo "3️⃣ 检查登录状态..."
echo ""

# 尝试检查登录，如果需要会提示扫码
python3 scripts/cdp_publish.py check-login 2>&1 | tee /tmp/login_check.log

if grep -q "NOT LOGGED IN" /tmp/login_check.log; then
    echo ""
    echo "📱 请扫码登录"
    echo "   1. 在Chrome窗口中找到二维码"
    echo "   2. 用手机小红书APP扫码"
    echo "   3. 登录成功后按回车继续"
    echo ""
    read -p "登录完成后按回车继续..."
    
    # 再次检查
    python3 scripts/cdp_publish.py check-login
fi

echo "✅ 登录成功"
echo ""

# 步骤4: 发布内容
echo "4️⃣ 发布内容..."
echo ""

cd "$BASE_DIR"

# 创建标题文件
TITLE=$(head -1 "$LATEST_MD" | sed 's/^# //')
echo "$TITLE" > "$CONTENT_DIR/title.txt"

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

# 发布
cd "$SKILLS_DIR"

python3 scripts/publish_pipeline.py \
    --title-file "$CONTENT_DIR/title.txt" \
    --content-file "$LATEST_MD" \
    --images ${IMAGES[@]} \
    --auto-publish

PUBLISH_RESULT=$?

echo ""
echo "========================"

if [ $PUBLISH_RESULT -eq 0 ]; then
    echo "✅ $ACCOUNT_NAME 发布成功！"
else
    echo "❌ $ACCOUNT_NAME 发布失败"
fi

echo ""
echo "📋 发布完成"
echo "   账号: $ACCOUNT_NAME"
echo "   文件: $(basename $LATEST_MD)"
echo ""

# 清理
rm -f /tmp/login_check.log

echo "💡 提示:"
echo "   - 如需发布另一个账号，请重新运行脚本"
echo "   - 每个账号需要单独扫码登录"
echo "   - 登录状态会保存12小时"
echo ""
