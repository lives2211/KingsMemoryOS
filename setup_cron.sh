#!/bin/bash
# 设置系统定时任务

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_FILE="/tmp/twitter_news_cron"

echo "🕐 设置 Twitter 新闻定时任务"
echo "=============================="
echo ""

# 默认配置
INTERVAL=${1:-60}  # 默认 60 分钟
MAX_TWEETS=${2:-15}
HOURS=${3:-1}

echo "配置:"
echo "  - 运行间隔: 每 ${INTERVAL} 分钟"
echo "  - 每次获取: ${MAX_TWEETS} 条"
echo "  - 时间范围: ${HOURS} 小时"
echo ""

# 创建临时 cron 文件
cat > "$CRON_FILE" << EOF
# Twitter 新闻聚合推送定时任务
# 每 ${INTERVAL} 分钟运行一次

# 设置环境变量
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin:/home/fengxueda/.local/bin
HOME=/home/fengxueda

# Twitter 新闻抓取
*/${INTERVAL} * * * * cd ${SCRIPT_DIR} && /usr/bin/python3 ${SCRIPT_DIR}/twitter_news_full.py --once --max ${MAX_TWEETS} --hours ${HOURS} >> ${SCRIPT_DIR}/cron.log 2>&1

# 清理旧日志（每周一次）
0 0 * * 0 find ${SCRIPT_DIR} -name "*.log" -mtime +7 -delete
EOF

echo "📋 即将添加以下定时任务:"
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
    echo "✅ 定时任务已添加!"
    echo ""
    echo "当前定时任务:"
    crontab -l | tail -10
    echo ""
    echo "📁 日志文件: ${SCRIPT_DIR}/cron.log"
    echo ""
    echo "管理命令:"
    echo "  查看任务: crontab -l"
    echo "  编辑任务: crontab -e"
    echo "  删除任务: crontab -r"
    echo "  查看日志: tail -f ${SCRIPT_DIR}/cron.log"
else
    echo "已取消"
    exit 0
fi

# 清理
rm -f "$CRON_FILE"
