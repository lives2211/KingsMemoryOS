#!/bin/bash
# 设置完整自动增长系统

set -euo pipefail

cd "$(dirname "$0")"

echo "🚀 设置完整自动增长系统"
echo "======================================"
echo ""

# 创建每日任务脚本
cat > "daily_auto_growth.sh" << 'EOF'
#!/bin/bash
# 每日自动增长（随机时间执行）

cd /home/fengxueda/.openclaw/workspace

# 生成随机延迟（0-480分钟 = 8小时）
DELAY=$((RANDOM % 480))

# 记录
LOG="auto_growth.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 延迟 ${DELAY}分钟后开始" >> "$LOG"

# 等待
sleep $((DELAY * 60))

# 执行完整流程
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始执行..." >> "$LOG"
./auto_growth_system.sh >> "$LOG" 2>&1
EOF

chmod +x daily_auto_growth.sh

echo "✅ 创建任务脚本: daily_auto_growth.sh"

# 创建定时任务
crontab -l 2>/dev/null | grep -v "daily_auto_growth" > /tmp/new_crontab.txt || true

cat >> /tmp/new_crontab.txt << 'EOF'

# 自动增长系统（每天8:00启动，内部随机延迟）
0 8 * * * cd /home/fengxueda/.openclaw/workspace && ./daily_auto_growth.sh

# 每小时检查互动机会
0 * * * * cd /home/fengxueda/.openclaw/workspace && python3 growth_engagement_v2.py --count 3 >> hourly_engagement.log 2>&1

# 每天10:00发送策略报告
0 10 * * * cd /home/fengxueda/.openclaw/workspace && python3 safe_posting_strategy.py >> strategy_report.log 2>&1

# 每周清理日志（周日0:00）
0 0 * * 0 cd /home/fengxueda/.openclaw/workspace && find . -name "*.log" -mtime +7 -delete
EOF

crontab /tmp/new_crontab.txt

echo "✅ 定时任务已设置"
echo ""
echo "📋 当前任务:"
crontab -l | tail -10
echo ""
echo "🔧 管理命令:"
echo "  查看任务: crontab -l"
echo "  编辑任务: crontab -e"
echo "  查看日志: tail -f auto_growth.log"
echo "  立即执行: ./auto_growth_system.sh"
echo ""
echo "🎉 设置完成！"
echo ""
echo "系统将在每天 8:00 启动，随机延迟后执行:"
echo "  1. 发布中文区 Skill (英文 + GitHub)"
echo "  2. 分3批次互动 (共15条)"
echo "  3. 20%概率晚间二次发布"
echo "  4. 每小时额外互动3条"
echo ""
