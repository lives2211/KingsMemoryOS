#!/bin/bash
# AI Skill 每日分析定时任务
# 每天自动分析一个优质 Skill 并发布到 Twitter

set -euo pipefail

cd "$(dirname "$0")"

LOG_FILE="skill_cron.log"
DATE=$(date '+%Y-%m-%d')

echo "========================================" >> "$LOG_FILE"
echo "[$DATE] 开始每日 Skill 分析任务" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# 1. 发现所有 Skill
echo "[$DATE] 正在发现 Skill..." >> "$LOG_FILE"
python3 skill_analyzer.py --discover >> "$LOG_FILE" 2>&1

# 2. 分析今日 Skill 并保存草稿
echo "[$DATE] 正在分析今日 Skill..." >> "$LOG_FILE"
python3 skill_analyzer.py --analyze --draft >> "$LOG_FILE" 2>&1

# 3. 发布到 Twitter
echo "[$DATE] 正在发布到 Twitter..." >> "$LOG_FILE"
python3 skill_analyzer.py --post >> "$LOG_FILE" 2>&1

# 4. 记录完成
echo "[$DATE] 任务完成" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 清理旧日志（保留30天）
find . -name "skill_cron.log" -mtime +30 -delete 2>/dev/null || true
