#!/bin/bash
# OpenClaw Content Farm - 每日运行脚本
# 生成并发布推文

set -e

# 配置
PROJECT_DIR="/home/fengxueda/.openclaw/workspace/projects/openclaw-content-farm"
LOG_FILE="$PROJECT_DIR/logs/daily_$(date +%Y-%m-%d).log"
COOKIES_FILE="/tmp/twitter_cookies.txt"

# 确保日志目录存在
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/generated_tweets"

# 加载 Twitter cookies
if [ -f "$COOKIES_FILE" ]; then
    export TWITTER_COOKIES=$(cat "$COOKIES_FILE")
else
    echo "❌ Twitter cookies not found!"
    exit 1
fi

# 记录开始时间
echo "========================================" >> "$LOG_FILE"
echo "🚀 OpenClaw Content Farm - Daily Run" >> "$LOG_FILE"
echo "📅 Date: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# 进入项目目录
cd "$PROJECT_DIR"

# Step 1: 生成推文
echo "📝 Step 1: Generating tweets..." >> "$LOG_FILE"
python3 content_generator.py >> "$LOG_FILE" 2>&1

# Step 2: 发布推文
echo "📤 Step 2: Publishing tweets..." >> "$LOG_FILE"
python3 auto_publisher.py >> "$LOG_FILE" 2>&1

# 记录完成
echo "✅ Daily run completed at $(date '+%H:%M:%S')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 发送通知（可选）
# echo "OpenClaw Content Farm: Daily tweets published!" | mail -s "Content Farm Daily" admin@example.com
