#!/bin/bash
# 使用xiaohongshu-cli搜索并复刻

set -euo pipefail

echo "🔍 小红书搜索+复刻工具"
echo "======================"
echo ""

if [ $# -lt 2 ]; then
    echo "用法: ./search_and_clone.sh <账号> <关键词>"
    echo ""
    echo "示例:"
    echo "  ./search_and_clone.sh tech-geek iPhone"
    echo "  ./search_and_clone.sh career-growth 职场干货"
    exit 1
fi

ACCOUNT=$1
KEYWORD=$2

echo "📱 账号: $ACCOUNT"
echo "🔍 关键词: $KEYWORD"
echo ""

# 检查登录状态
echo "🔐 检查登录状态..."
xhs status 2>&1 | grep -q "Login confirmed" || {
    echo "❌ 未登录，请先登录:"
    echo "   xhs login --qrcode"
    exit 1
}

echo "✅ 已登录"
echo ""

# 搜索爆款笔记
echo "🔍 搜索爆款笔记..."
xhs search "$KEYWORD" --sort popular --page 1 --yaml > /tmp/search_result.yaml

if [ $? -ne 0 ]; then
    echo "❌ 搜索失败"
    exit 1
fi

echo "✅ 搜索完成"
echo ""

# 解析搜索结果（简化版，实际需要解析YAML）
echo "📊 搜索结果:"
cat /tmp/search_result.yaml | head -50
echo ""

# 提示用户选择
echo "💡 请从搜索结果中选择一篇爆款笔记"
echo "   复制笔记URL，然后运行:"
echo ""
echo "   python3 clone_viral.py <笔记URL> --account $ACCOUNT"
echo ""

# 清理
rm -f /tmp/search_result.yaml
