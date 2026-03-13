#!/bin/bash
# 全自动增长系统
# 每天随机时间发布，保证账号安全

set -euo pipefail

cd /home/fengxueda/.openclaw/workspace

LOG_FILE="auto_growth.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] ========================================" >> "$LOG_FILE"
echo "[$DATE] 🚀 全自动增长系统启动" >> "$LOG_FILE"
echo "[$DATE] ========================================" >> "$LOG_FILE"

# ========== 阶段 1: 随机延迟后发布 ==========
# 随机延迟 0-8 小时（发布时间: 8:00-16:00）
DELAY_HOURS=$((RANDOM % 8))
DELAY_MINUTES=$((RANDOM % 60))
TOTAL_DELAY_MINUTES=$((DELAY_HOURS * 60 + DELAY_MINUTES))

echo "[$DATE] ⏳ 随机延迟: ${DELAY_HOURS}小时${DELAY_MINUTES}分钟" >> "$LOG_FILE"
echo "[$DATE]    预计发布时间: $(date -d "+${TOTAL_DELAY_MINUTES} minutes" '+%H:%M')" >> "$LOG_FILE"

sleep $((TOTAL_DELAY_MINUTES * 60))

# 发布中文区 Skill（带 GitHub 链接）
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📝 开始发布..." >> "$LOG_FILE"
python3 china_skill_github.py >> "$LOG_FILE" 2>&1

# ========== 阶段 2: 等待后互动 ==========
# 等待 3-6 小时后互动
WAIT_HOURS=$((3 + RANDOM % 3))
WAIT_MINUTES=$((RANDOM % 60))
TOTAL_WAIT_MINUTES=$((WAIT_HOURS * 60 + WAIT_MINUTES))

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⏳ 等待 ${WAIT_HOURS}小时${WAIT_MINUTES}分钟后互动..." >> "$LOG_FILE"
sleep $((TOTAL_WAIT_MINUTES * 60))

# 互动最近24小时帖子（15条，分批次）
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🤝 开始互动..." >> "$LOG_FILE"

# 第一批: 5条
python3 growth_engagement_v2.py --count 5 >> "$LOG_FILE" 2>&1

# 等待 1-2 小时
BATCH_DELAY=$((60 + RANDOM % 60))
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⏳ 批次间隔: ${BATCH_DELAY}分钟" >> "$LOG_FILE"
sleep $((BATCH_DELAY * 60))

# 第二批: 5条
python3 growth_engagement_v2.py --count 5 >> "$LOG_FILE" 2>&1

# 等待 1-2 小时
BATCH_DELAY2=$((60 + RANDOM % 60))
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⏳ 批次间隔: ${BATCH_DELAY2}分钟" >> "$LOG_FILE"
sleep $((BATCH_DELAY2 * 60))

# 第三批: 5条
python3 growth_engagement_v2.py --count 5 >> "$LOG_FILE" 2>&1

# ========== 阶段 3: 晚间二次发布（可选）==========
# 20% 概率晚上再发一条
if [ $((RANDOM % 5)) -eq 0 ]; then
    NIGHT_DELAY=$((120 + RANDOM % 180))  # 2-5小时后
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🌙 晚间发布模式..." >> "$LOG_FILE"
    sleep $((NIGHT_DELAY * 60))
    python3 china_skill_github.py >> "$LOG_FILE" 2>&1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 今日任务完成" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
