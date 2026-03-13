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
