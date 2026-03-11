#!/bin/bash
# 自动切号+发布脚本
# 先切号，再发布，确保发到正确账号

set -euo pipefail

echo "🚀 自动切号发布系统"
echo "===================="
echo ""

if [ $# -lt 2 ]; then
    echo "用法: ./auto_switch_publish.sh <账号名称> <账号类型>"
    echo ""
    echo "示例:"
    echo "  ./auto_switch_publish.sh '我的数码号' tech-geek"
    echo "  ./auto_switch_publish.sh '我的职场号' career-growth"
    echo ""
    exit 1
fi

ACCOUNT_NAME=$1
ACCOUNT_TYPE=$2
BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"

cd "$BASE_DIR"

echo "📱 目标账号: $ACCOUNT_NAME ($ACCOUNT_TYPE)"
echo ""

# 步骤1: 切换账号
echo "步骤1: 切换到 $ACCOUNT_NAME"
echo "------------------------------"
python3 switch_account.py "$ACCOUNT_NAME"

if [ $? -ne 0 ]; then
    echo "❌ 账号切换失败"
    exit 1
fi

echo ""

# 步骤2: 发布内容
echo "步骤2: 发布内容到 $ACCOUNT_NAME"
echo "------------------------------"
./publish_manual.sh "$ACCOUNT_TYPE"

echo ""
echo "===================="
if [ $? -eq 0 ]; then
    echo "✅ 全部完成！"
    echo "   账号: $ACCOUNT_NAME"
    echo "   内容已发布"
else
    echo "❌ 发布失败"
fi
echo ""
