#!/bin/bash
# 2026年AI智能体爆款执行计划
# 全自动搜索爆款 → 复刻 → 发布

set -euo pipefail

echo "🚀 2026年AI智能体爆款执行计划"
echo "================================"
echo ""

BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"
cd "$BASE_DIR"

# 步骤1: 检查登录
echo "步骤1: 检查登录状态"
echo "--------------------"
xhs status 2>&1 | grep -q "Login confirmed" || {
    echo "⚠️  未登录，请先扫码:"
    echo "   xhs login --qrcode"
    echo ""
    echo "登录后重新运行本脚本"
    exit 1
}
echo "✅ 已登录"
echo ""

# 步骤2: 搜索AI智能体爆款
echo "步骤2: 搜索AI智能体爆款"
echo "------------------------"

echo "🔍 搜索关键词: AI Agent"
xhs search "AI Agent" --sort popular --page 1 --yaml > /tmp/ai_agent_search.yaml

if [ $? -ne 0 ]; then
    echo "❌ 搜索失败"
    exit 1
fi

echo "✅ 搜索完成"
echo ""

# 步骤3: 显示搜索结果
echo "步骤3: 爆款笔记TOP5"
echo "-------------------"
head -100 /tmp/ai_agent_search.yaml
echo ""

# 步骤4: 选择最爆款（简化版，实际应该解析YAML）
echo "步骤4: 选择最爆款进行复刻"
echo "-------------------------"
echo "💡 请从上面的结果中选择一篇爆款笔记"
echo "   复制笔记URL，格式如:"
echo "   https://www.xiaohongshu.com/explore/xxxxxxxx"
echo ""

# 步骤5: 自动生成内容
echo "步骤5: 生成AI智能体内容"
echo "-----------------------"
python3 auto_select_category_2026.py | grep "爆款标题" -A 5
echo ""

# 步骤6: 准备发布
echo "步骤6: 准备发布"
echo "---------------"
echo "📋 执行计划:"
echo "   1. 搜索AI Agent爆款 ✓"
echo "   2. 选择最爆款"
echo "   3. 复刻生成内容"
echo "   4. 自动发布"
echo ""

echo "🎯 下一步操作:"
echo ""
echo "选项A: 手动选择爆款复刻"
echo "   1. 从上面选择一篇爆款"
echo "   2. 运行: python3 clone_viral.py <URL> --account tech-geek"
echo ""
echo "选项B: 自动生成内容"
echo "   1. 运行: python3 content_generator_v2.py"
echo "   2. 生成AI智能体原创内容"
echo ""
echo "选项C: 全自动执行（需要配置）"
echo "   1. 配置定时任务"
echo "   2. 每天自动搜索+复刻+发布"
echo ""

# 清理
rm -f /tmp/ai_agent_search.yaml

echo "================================"
echo "💡 推荐: 选择选项A或B立即开始"
echo ""
