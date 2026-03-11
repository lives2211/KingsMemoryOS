#!/bin/bash
# 每日完整涨粉流程
# 1. 发布英文内容
# 2. 互动最近24小时帖子

set -euo pipefail

cd /home/fengxueda/.openclaw/workspace

LOG_FILE="daily_growth.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] ========================================" >> "$LOG_FILE"
echo "[$DATE] 🚀 每日涨粉任务开始" >> "$LOG_FILE"
echo "[$DATE] ========================================" >> "$LOG_FILE"

# 步骤1: 发布英文内容（随机延迟 0-4小时）
echo "[$DATE] 步骤1: 准备发布内容..." >> "$LOG_FILE"

DELAY_MINUTES=$((RANDOM % 240))  # 0-4小时
echo "[$DATE] 随机延迟: ${DELAY_MINUTES}分钟" >> "$LOG_FILE"
sleep $((DELAY_MINUTES * 60))

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始发布..." >> "$LOG_FILE"
python3 skill_english_publisher.py >> "$LOG_FILE" 2>&1

# 步骤2: 等待 2-4 小时后互动
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 步骤2: 等待后互动..." >> "$LOG_FILE"

WAIT_MINUTES=$((120 + RANDOM % 120))  # 2-4小时
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 等待 ${WAIT_MINUTES}分钟后互动" >> "$LOG_FILE"
sleep $((WAIT_MINUTES * 60))

# 互动最近24小时的帖子
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始互动..." >> "$LOG_FILE"
python3 growth_engagement_v2.py --count 10 >> "$LOG_FILE" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 任务完成" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
