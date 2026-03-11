#!/bin/bash
# 全自动多账号发布脚本
# 定时切换账号，分别发布到正确账号

set -euo pipefail

echo "🚀 小红书多账号全自动发布"
echo "=========================="
echo ""

BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"
SKILLS_DIR="$BASE_DIR/xiaohongshu-skills"

cd "$BASE_DIR"

# 账号列表
ACCOUNTS=("tech-geek" "career-growth")
ACCOUNT_NAMES=("数码虾" "职场虾")

# 发布单个账号
publish_account() {
    local account=$1
    local name=$2
    
    echo ""
    echo "📱 发布账号: $name ($account)"
    echo "------------------------------"
    
    # 1. 关闭Chrome
    echo "1️⃣ 关闭Chrome..."
    pkill -f "Google Chrome" 2>/dev/null || true
    sleep 2
    
    # 2. 启动Chrome
    echo "2️⃣ 启动Chrome..."
    cd "$SKILLS_DIR"
    python3 scripts/chrome_launcher.py &
    sleep 5
    
    # 3. 检查/等待登录
    echo "3️⃣ 检查登录状态..."
    python3 scripts/cdp_publish.py check-login 2>&1 | tee /tmp/login_$account.log
    
    if grep -q "NOT LOGGED IN" /tmp/login_$account.log; then
        echo ""
        echo "📱 请扫码登录 $name 账号"
        echo "   在Chrome窗口中找到二维码"
        echo "   用手机小红书APP扫码"
        echo ""
        read -p "登录完成后按回车继续..."
        
        # 再次检查
        python3 scripts/cdp_publish.py check-login
    fi
    
    echo "✅ $name 登录成功"
    
    # 4. 查找内容文件
    echo "4️⃣ 查找内容..."
    CONTENT_DIR="$BASE_DIR/generated/$account/high_quality"
    
    if [ ! -d "$CONTENT_DIR" ]; then
        echo "❌ 内容目录不存在: $CONTENT_DIR"
        return 1
    fi
    
    # 获取最新的markdown文件
    LATEST_MD=$(ls -t "$CONTENT_DIR"/*.md 2>/dev/null | head -1)
    if [ -z "$LATEST_MD" ]; then
        echo "❌ 未找到内容文件"
        return 1
    fi
    
    echo "   文件: $(basename $LATEST_MD)"
    
    # 创建标题文件
    TITLE=$(head -1 "$LATEST_MD" | sed 's/^# //')
    echo "$TITLE" > "$CONTENT_DIR/title.txt"
    
    # 查找图片
    IMAGES=()
    for img in "$CONTENT_DIR"/card_*.png; do
        if [ -f "$img" ]; then
            IMAGES+=("$img")
        fi
    done
    
    echo "   图片: ${#IMAGES[@]} 张"
    
    # 5. 发布
    echo "5️⃣ 发布内容..."
    python3 scripts/publish_pipeline.py \
        --title-file "$CONTENT_DIR/title.txt" \
        --content-file "$LATEST_MD" \
        --images ${IMAGES[@]} \
        --auto-publish
    
    if [ $? -eq 0 ]; then
        echo "✅ $name 发布成功！"
    else
        echo "❌ $name 发布失败"
        return 1
    fi
    
    # 清理
    rm -f /tmp/login_$account.log
    
    return 0
}

# 主流程
echo "开始发布 ${#ACCOUNTS[@]} 个账号..."
echo ""

SUCCESS_COUNT=0

for i in "${!ACCOUNTS[@]}"; do
    account="${ACCOUNTS[$i]}"
    name="${ACCOUNT_NAMES[$i]}"
    
    if publish_account "$account" "$name"; then
        ((SUCCESS_COUNT++))
    fi
    
    # 账号间延迟（避免频繁操作）
    if [ $i -lt $((${#ACCOUNTS[@]} - 1)) ]; then
        echo ""
        echo "⏳ 等待30秒后发布下一个账号..."
        sleep 30
    fi
done

# 关闭Chrome
echo ""
echo "关闭Chrome..."
pkill -f "Google Chrome" 2>/dev/null || true

echo ""
echo "=========================="
echo "发布完成"
echo "=========================="
echo "成功: $SUCCESS_COUNT / ${#ACCOUNTS[@]} 个账号"
echo ""

if [ $SUCCESS_COUNT -eq ${#ACCOUNTS[@]} ]; then
    echo "✅ 全部发布成功！"
    exit 0
else
    echo "⚠️  部分账号发布失败"
    exit 1
fi
