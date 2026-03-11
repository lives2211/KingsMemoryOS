#!/bin/bash
# 全自动发布系统
# 定时任务 + 自动登录 + 自动发布

set -euo pipefail

echo "🤖 全自动AI发布系统"
echo "====================="
echo ""

BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"
cd "$BASE_DIR"

# 配置定时任务
echo "📝 配置定时任务..."

cat > /tmp/full_auto_cron.txt << 'EOF'
# 全自动小红书发布系统

# 每天早上9点自动生成内容
0 9 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 content_generator_v2.py >> logs/content_gen.log 2>&1

# 每天上午10点发布数码虾
0 10 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && ./publish_auto_fixed.sh tech-geek >> logs/publish_tech.log 2>&1

# 每天下午2点发布职场虾
0 14 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && ./publish_auto_fixed.sh career-growth >> logs/publish_career.log 2>&1

# 每天晚上8点搜索爆款复刻
0 20 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 auto_find_and_clone.py --account tech-geek >> logs/clone.log 2>&1

# 每天晚上10点生成数据报告
0 22 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 analytics.py --report >> logs/analytics.log 2>&1
EOF

echo "✅ 定时任务配置完成"
echo ""

# 创建日志目录
mkdir -p logs

# 安装定时任务
echo "📝 安装定时任务..."
crontab /tmp/full_auto_cron.txt

echo "✅ 定时任务已安装"
echo ""

# 显示当前定时任务
echo "📋 当前定时任务:"
crontab -l
echo ""

# 创建启动脚本
cat > start_full_auto.sh << 'EOF'
#!/bin/bash
# 启动全自动系统

echo "🚀 启动全自动小红书运营系统"
echo "=============================="
echo ""

cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix

# 检查登录状态
echo "🔐 检查登录状态..."

if ! xhs status 2>&1 | grep -q "Login confirmed"; then
    echo "⚠️  需要登录"
    echo "   运行: xhs login --qrcode"
    echo "   扫码登录后，系统会自动运行"
    exit 1
fi

echo "✅ 已登录"
echo ""

# 启动定时任务
echo "📝 启动定时任务..."
crontab /tmp/full_auto_cron.txt

echo "✅ 全自动系统已启动"
echo ""
echo "📅 运行计划:"
echo "   09:00 - 自动生成内容"
echo "   10:00 - 发布数码虾"
echo "   14:00 - 发布职场虾"
echo "   20:00 - 搜索爆款复刻"
echo "   22:00 - 生成数据报告"
echo ""
echo "💡 系统现在全自动运行，无需人工干预"
echo "   查看日志: tail -f logs/*.log"
echo ""
EOF

chmod +x start_full_auto.sh

echo "✅ 启动脚本已创建: start_full_auto.sh"
echo ""

# 创建状态检查脚本
cat > check_status.sh << 'EOF'
#!/bin/bash
# 检查系统状态

echo "📊 系统状态检查"
echo "==============="
echo ""

cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix

# 检查定时任务
echo "📝 定时任务:"
crontab -l | head -10
echo ""

# 检查日志
echo "📄 最新日志:"
ls -lt logs/*.log 2>/dev/null | head -5 || echo "   暂无日志"
echo ""

# 检查登录状态
echo "🔐 登录状态:"
xhs status 2>&1 | head -3
echo ""

# 检查内容文件
echo "📁 内容文件:"
ls -lt generated/*/ai_*.md 2>/dev/null | head -5 || echo "   暂无内容"
echo ""

echo "==============="
EOF

chmod +x check_status.sh

echo "✅ 状态检查脚本已创建: check_status.sh"
echo ""

echo "====================="
echo "✅ 全自动系统配置完成！"
echo ""
echo "🚀 使用方法:"
echo ""
echo "1. 首次启动（需要登录）:"
echo "   xhs login --qrcode"
echo "   ./start_full_auto.sh"
echo ""
echo "2. 查看状态:"
echo "   ./check_status.sh"
echo ""
echo "3. 查看日志:"
echo "   tail -f logs/*.log"
echo ""
echo "4. 停止系统:"
echo "   crontab -r"
echo ""
echo "💡 系统现在全自动运行:"
echo "   - 自动生成内容"
echo "   - 自动发布到两个账号"
echo "   - 自动搜索爆款复刻"
echo "   - 自动生成数据报告"
echo ""
echo "🎯 立即执行: ./start_full_auto.sh"
echo ""
