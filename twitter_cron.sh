#!/bin/bash
# Twitter 新闻定时抓取脚本
# 每小时运行一次，获取 15-20 条最新推文

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/twitter_cron.log"
LOCK_FILE="/tmp/twitter_cron.lock"

# 防止重复运行
if [ -f "$LOCK_FILE" ]; then
    PID=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
        echo "$(date): 另一个实例正在运行 (PID: $PID)" >> "$LOG_FILE"
        exit 1
    fi
fi

echo $$ > "$LOCK_FILE"

# 清理函数
cleanup() {
    rm -f "$LOCK_FILE"
}
trap cleanup EXIT

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "开始 Twitter 新闻抓取任务"

# 运行抓取脚本
if python3 "$SCRIPT_DIR/twitter_news_bot.py" --once --max 20 --hours 1 >> "$LOG_FILE" 2>&1; then
    log "✅ 抓取成功完成"
else
    log "❌ 抓取失败"
    exit 1
fi

log "任务结束"
log "=========================================="
