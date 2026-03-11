#!/bin/bash
# 每天自动发布 KOL Skill 推文

cd /home/fengxueda/.openclaw/workspace

# 生成随机延迟（0-720分钟 = 12小时）
# 发布时间将在 8:00-20:00 之间
DELAY_MINUTES=$((RANDOM % 720))
DELAY_SECONDS=$((DELAY_MINUTES * 60))

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 今日发布任务开始" >> kol_cron.log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 随机延迟: ${DELAY_MINUTES}分钟" >> kol_cron.log

# 等待
sleep $DELAY_SECONDS

# 运行发布
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始发布..." >> kol_cron.log
python3 skill_auto_publish.py >> kol_cron.log 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 发布完成" >> kol_cron.log
