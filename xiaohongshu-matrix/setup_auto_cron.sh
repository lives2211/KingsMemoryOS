#!/bin/bash
# 设置自动发布定时任务

set -euo pipefail

echo "🕐 设置自动发布定时任务"
echo "========================"
echo ""

BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"

# 创建定时任务文件
cat > /tmp/xhs_cron.txt << 'EOF'
# 小红书自动发布定时任务
# 每天自动发布到两个账号

# 每天上午10:00发布数码虾
0 10 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && ./publish_manual.sh tech-geek >> logs/publish_tech.log 2>&1

# 每天下午14:00发布职场虾
0 14 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && ./publish_manual.sh career-growth >> logs/publish_career.log 2>&1

# 每天生成新的发布计划
0 8 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 scheduler.py >> logs/scheduler.log 2>&1

# 每天生成数据报告
0 22 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 analytics.py --report >> logs/analytics.log 2>&1
EOF

echo "📋 定时任务内容:"
cat /tmp/xhs_cron.txt
echo ""

# 安装定时任务
echo "📝 安装定时任务..."
crontab /tmp/xhs_cron.txt

echo "✅ 定时任务已安装"
echo ""

# 显示当前定时任务
echo "当前定时任务:"
crontab -l
echo ""

# 清理
rm -f /tmp/xhs_cron.txt

echo "========================"
echo "✅ 配置完成！"
echo ""
echo "发布计划:"
echo "  每天 08:00 - 生成新计划"
echo "  每天 10:00 - 发布数码虾"
echo "  每天 14:00 - 发布职场虾"
echo "  每天 22:00 - 生成数据报告"
echo ""
echo "💡 注意:"
echo "  - 首次运行需要扫码登录"
echo "  - 登录状态保持12小时"
echo "  - 查看日志: tail -f logs/publish_*.log"
echo ""
