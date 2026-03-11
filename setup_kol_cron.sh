#!/bin/bash
# KOL Skill 发布系统定时任务配置

set -euo pipefail

cd "$(dirname "$0")"

echo "🕐 KOL Skill 发布系统 - 定时任务配置"
echo "======================================"
echo ""

# 配置
WORK_DIR="/home/fengxueda/.openclaw/workspace"
PUBLISH_SCRIPT="$WORK_DIR/skill_kol_publisher.py"
REPORT_SCRIPT="$WORK_DIR/send_daily_report.py"

# 检查脚本存在
if [ ! -f "$PUBLISH_SCRIPT" ]; then
    echo "❌ 错误: 找不到 $PUBLISH_SCRIPT"
    exit 1
fi

echo "📋 将配置以下定时任务："
echo ""
echo "1. 每天随机时间发布（8:00-20:00之间）"
echo "2. 每天早上 10:00 发送日报"
echo ""

# 创建发布脚本（带随机延迟）
cat > "$WORK_DIR/daily_publish.sh" << 'PUBLISH_EOF'
#!/bin/bash
# 每日发布脚本（带随机延迟）

set -euo pipefail
cd "$(dirname "$0")"

# 生成随机延迟（0-720分钟，即12小时）
# 这样发布时间会在 8:00-20:00 之间
DELAY_MINUTES=$((RANDOM % 720))
DELAY_SECONDS=$((DELAY_MINUTES * 60))

# 记录开始时间
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 今日发布任务开始" >> kol_cron.log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 随机延迟: ${DELAY_MINUTES}分钟" >> kol_cron.log

# 等待
sleep $DELAY_SECONDS

# 运行发布
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始发布..." >> kol_cron.log
python3 skill_kol_publisher.py >> kol_cron.log 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 发布完成" >> kol_cron.log
PUBLISH_EOF

chmod +x "$WORK_DIR/daily_publish.sh"

echo "✅ 创建发布脚本: $WORK_DIR/daily_publish.sh"

# 创建日报脚本
cat > "$REPORT_SCRIPT" << 'REPORT_EOF'
#!/usr/bin/env python3
"""发送每日汇报"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from skill_kol_publisher import SkillKOLPublisher

# 生成报告
publisher = SkillKOLPublisher()
report = publisher.generate_report()

# 输出报告
print(report)

# 保存到文件
report_file = Path("daily_report.txt")
with open(report_file, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"\n💾 报告已保存: {report_file}")
REPORT_EOF

chmod +x "$REPORT_SCRIPT"

echo "✅ 创建日报脚本: $REPORT_SCRIPT"

# 创建 cron 配置
CRON_FILE="/tmp/kol_cron_config"

cat > "$CRON_FILE" << EOF
# KOL Skill 发布系统定时任务
# 每天 8:00 启动发布任务（内部有随机延迟）
0 8 * * * cd $WORK_DIR && ./daily_publish.sh

# 每天 10:00 发送日报
0 10 * * * cd $WORK_DIR && python3 $REPORT_SCRIPT >> daily_report.log 2>&1

# 每周清理日志（周日 0:00）
0 0 * * 0 cd $WORK_DIR && find . -name "*.log" -mtime +7 -delete
EOF

echo ""
echo "📋 即将添加的定时任务："
echo "------------------------------"
cat "$CRON_FILE"
echo "------------------------------"
echo ""

read -p "确认添加? (y/n): " confirm

if [ "$confirm" = "y" ]; then
    # 备份现有 crontab
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null || true
    
    # 添加新任务
    (crontab -l 2>/dev/null || true; cat "$CRON_FILE") | crontab -
    
    echo ""
    echo "✅ 定时任务已添加！"
    echo ""
    echo "当前定时任务："
    crontab -l | tail -10
    echo ""
    echo "📁 相关文件："
    echo "  • 发布脚本: $WORK_DIR/daily_publish.sh"
    echo "  • 日报脚本: $REPORT_SCRIPT"
    echo "  • 日志文件: $WORK_DIR/kol_cron.log"
    echo "  • 日报文件: $WORK_DIR/daily_report.txt"
    echo ""
    echo "🔧 管理命令："
    echo "  查看任务: crontab -l"
    echo "  编辑任务: crontab -e"
    echo "  查看日志: tail -f $WORK_DIR/kol_cron.log"
    echo "  手动测试: python3 $PUBLISH_SCRIPT --dry-run"
else
    echo "已取消"
    rm -f "$CRON_FILE"
    exit 0
fi

# 清理
rm -f "$CRON_FILE"

echo ""
echo "🎉 配置完成！"
echo ""
echo "系统将在以下时间自动运行："
echo "  • 每天 8:00 启动发布（随机延迟到 8:00-20:00）"
echo "  • 每天 10:00 发送日报"
echo ""
