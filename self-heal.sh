#!/bin/bash
# 自愈网关7.2 - 只检查OpenClaw相关服务

LOG="/media/fengxueda/D/openclaw-data/logs/self-heal.log"
RECORD="/media/fengxueda/D/openclaw-data/logs/heal-record.log"
TG_CHAT_ID="-1003762750497"

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG"; }
record() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$RECORD"; }

send_notify() {
    curl -s -X POST "https://api.telegram.org/bot$(grep -oP 'botToken.*' ~/.openclaw/openclaw.json | head -1 | cut -d'"' -f4)/sendMessage" \
        -d "chat_id=$TG_CHAT_ID" -d "text=$1" > /dev/null 2>&1
}

# 只检查OpenClaw
check_openclaw() {
    timeout 1 bash -c "echo >/dev/tcp/127.0.0.1/18789" 2>/dev/null
    [ $? -eq 0 ] && echo "ok" || echo "fail"
}

check_pinchtab() {
    curl -s http://localhost:9867/health 2>/dev/null | grep -q "ok" && echo "ok" || echo "fail"
}

fix_openclaw() {
    log "🔧 OpenClaw异常，重启..."
    pkill -f "openclaw-gateway"
    sleep 2
    nohup openclaw gateway start > /dev/null 2>&1 &
    sleep 8
    if [ "$(check_openclaw)" = "ok" ]; then
        log "✅ OpenClaw已恢复"
        record "OpenClaw修复成功"
        send_notify "✅ OpenClaw Gateway已自动恢复"
    else
        log "❌ OpenClaw修复失败"
        record "OpenClaw修复失败"
        send_notify "⚠️ OpenClaw修复失败，请检查！"
    fi
}

fix_pinchtab() {
    log "🔧 Pinchtab异常，重启..."
    pkill -f pinchtab
    sleep 2
    cd /media/fengxueda/D/openclaw-data/workspace
    nohup ./pinchtab > /media/fengxueda/D/openclaw-data/logs/pinchtab.log 2>&1 &
    sleep 5
    [ "$(check_pinchtab)" = "ok" ] && log "✅ Pinchtab已恢复" || log "❌ Pinchtab修复失败"
}

check_disk() {
    USE=$(df /media/fengxueda/D 2>/dev/null | tail -1 | awk '{print $5}' | sed 's/%//')
    [ "$USE" -gt 85 ] && find /media/fengxueda/D/openclaw-data/logs -name "*.log" -mtime +3 -delete
}

# 主流程
log "══════════════════"
OC=$(check_openclaw)
log "OpenClaw: $OC"
[ "$OC" = "fail" ] && fix_openclaw

PT=$(check_pinchtab)
log "Pinchtab: $PT"
[ "$PT" = "fail" ] && fix_pinchtab

check_disk
log "✅ 完成"
