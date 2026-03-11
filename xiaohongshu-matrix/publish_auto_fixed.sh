#!/bin/bash
# 修复版自动发布脚本
# 增加重试机制和错误处理

set -euo pipefail

echo "🚀 修复版自动发布"
echo "=================="
echo ""

if [ $# -lt 1 ]; then
    echo "用法: ./publish_auto_fixed.sh <账号>"
    echo ""
    echo "可用账号: tech-geek, career-growth"
    exit 1
fi

ACCOUNT=$1
BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"
SKILLS_DIR="$BASE_DIR/xiaohongshu-skills"

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

echo "⏳ 准备发布..."
echo "   等待10秒让页面加载..."
sleep 10
echo ""

# 尝试发布（带重试）
MAX_RETRIES=3
RETRY_COUNT=0

cd "$SKILLS_DIR"

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    echo "🚀 尝试发布 (第 $((RETRY_COUNT + 1))/$MAX_RETRIES 次)..."
    echo ""
    
    # 使用预览模式（只填充，不自动发布）
    python3 scripts/publish_pipeline.py \
        --title-file "$CONTENT_DIR/title.txt" \
        --content-file "$LATEST_MD" \
        --images ${IMAGES[@]} \
        --preview \
        --headless 2>&1 | tee /tmp/publish_log.txt
    
    RESULT=${PIPESTATUS[0]}
    
    if [ $RESULT -eq 0 ]; then
        echo ""
        echo "✅ 内容填充成功！"
        echo ""
        echo "📋 请检查浏览器中的内容:"
        echo "   1. 标题是否正确"
        echo "   2. 正文是否完整"
        echo "   3. 图片是否上传成功"
        echo ""
        echo "👆 确认无误后，请手动点击"发布"按钮"
        echo ""
        exit 0
    else
        echo ""
        echo "⚠️  填充失败，分析错误..."
        
        if grep -q "上传图文" /tmp/publish_log.txt; then
            echo "   错误: 找不到'上传图文'按钮"
            echo "   可能原因: 页面结构变化或加载未完成"
        fi
        
        RETRY_COUNT=$((RETRY_COUNT + 1))
        
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "   等待5秒后重试..."
            sleep 5
        fi
    fi
done

echo ""
echo "❌ 自动填充失败 ($MAX_RETRIES 次尝试)"
echo ""
echo "💡 建议:"
echo "   1. 检查Chrome是否正常运行"
echo "   2. 手动访问发布页面"
echo "   3. 使用 fill_content.sh 手动复制内容"
echo ""

exit 1
