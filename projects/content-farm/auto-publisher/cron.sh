#!/bin/bash
# 小红书自动发布系统 - Cron定时任务脚本
# 添加到crontab: crontab -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 日志文件
LOG_FILE="logs/cron-$(date +%Y%m%d).log"
mkdir -p logs

# 记录开始时间
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始执行定时任务" >> "$LOG_FILE"

# 运行批量发布（限制1篇，无头模式）
python3 main.py batch --limit 1 --headless >> "$LOG_FILE" 2>&1

# 记录结束时间
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 定时任务完成" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
