#!/bin/bash
# 爆款自动搜索复刻工具
# 一键搜索+选择+复刻

set -euo pipefail

echo "🚀 爆款自动搜索复刻"
echo "===================="
echo ""

if [ $# -lt 2 ]; then
    echo "用法: ./viral_auto.sh <账号> <关键词>"
    echo ""
    echo "示例:"
    echo "  ./viral_auto.sh tech-geek iPhone"
    echo "  ./viral_auto.sh career-growth 职场干货"
    echo "  ./viral_auto.sh life-aesthetics 家居布置"
    echo ""
    exit 1
fi

ACCOUNT=$1
KEYWORD=$2

echo "📱 账号: $ACCOUNT"
echo "🔍 关键词: $KEYWORD"
echo ""

# 检查登录
echo "🔐 检查登录状态..."
xhs status 2>&1 | grep -q "Login confirmed" || {
    echo "⚠️  未登录，请先扫码登录:"
    echo "   xhs login --qrcode"
    echo ""
    echo "登录完成后重新运行本脚本"
    exit 1
}

echo "✅ 已登录"
echo ""

# 执行搜索+复刻
cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix
python3 search_clone_auto.py "$ACCOUNT" "$KEYWORD"

echo ""
echo "===================="
echo "完成！"
echo ""
