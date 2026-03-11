#!/bin/bash
# gateway-monitor.sh - 网关进程监控脚本
# 功能: 检查进程存活/自动重启/日志输出

LOG_FILE="/tmp/gateway-monitor.log"
PROCESS_NAME="openclaw"
RESTART_CMD="openclaw gateway start"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_process() {
    if pgrep -x "$PROCESS_NAME" > /dev/null 2>&1; then
        return 0  # 存活
    else
        return 1  # 挂了
    fi
}

restart_gateway() {
    log "⚠️ 进程已挂掉，尝试重启..."
    $RESTART_CMD >> "$LOG_FILE" 2>&1
    sleep 2
    if check_process; then
        log "✅ 重启成功"
    else
        log "❌ 重启失败"
    fi
}

# 主逻辑
log "=== 网关监控开始 ==="
log "进程: $PROCESS_NAME"

if check_process; then
    log "✅ 网关运行正常"
    # 输出进程详情
    ps aux | grep "$PROCESS_NAME" | grep -v grep >> "$LOG_FILE"
else
    restart_gateway
fi

log "=== 监控完成 ==="
echo "---"
echo "日志位置: $LOG_FILE"