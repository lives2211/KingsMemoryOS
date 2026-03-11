#!/bin/bash
# 设置随机时间发布定时任务

set -euo pipefail

echo "🎲 设置随机时间发布"
echo "===================="
echo ""

BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"

# 创建定时任务文件
cat > /tmp/random_cron.txt << 'EOF'
# 小红书随机时间发布定时任务

# 每天早上8点生成今日发布计划
0 8 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 scheduler.py >> logs/scheduler.log 2>&1

# 随机时间发布（每天执行随机发布脚本）
0 7 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && ./publish_random.sh >> logs/publish_random.log 2>&1

# 每天生成数据报告
0 22 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 analytics.py --report >> logs/analytics.log 2>&1
EOF

echo "📋 定时任务内容:"
cat /tmp/random_cron.txt
echo ""

# 安装定时任务
echo "📝 安装定时任务..."
crontab /tmp/random_cron.txt

echo "✅ 定时任务已安装"
echo ""

# 显示当前定时任务
echo "当前定时任务:"
crontab -l
echo ""

# 清理
rm -f /tmp/random_cron.txt

echo "===================="
echo "✅ 配置完成！"
echo ""
echo "发布策略:"
echo "  📅 每天 08:00 - 生成新计划"
echo "  🎲 每天 07:00 - 随机时间发布（在7:30-21:00之间随机）"
echo "  📊 每天 22:00 - 生成数据报告"
echo ""
echo "💡 特点:"
echo "  - 随机选择发布时间（避免规律）"
echo "  - 随机选择账号（数码虾或职场虾）"
echo "  - 随机选择时间窗口（早/中/下午/晚）"
echo "  - 更符合真人发布习惯"
echo ""
