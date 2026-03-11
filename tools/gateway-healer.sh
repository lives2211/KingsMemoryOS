#!/bin/bash
# ========================================
# OpenClaw 自愈网关 v2.0
# 功能：检测 + 修复 + 通知 + 记录
# ========================================

LOG_FILE="$HOME/.openclaw/logs/gateway-healer.log"
TELEGRAM_CHAT="-1003762750497"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

notify() {
    MSG="$1"
    curl -s -X POST "https://api.telegram.org/bot$(cat ~/.openclaw/credentials/telegram-bot-token 2>/dev/null)/sendMessage" \
        -d chat_id="$TELEGRAM_CHAT" -d text="$MSG" 2>/dev/null
}

# 检查网关状态
check_gateway() {
    openclaw gateway status 2>&1
}

# 尝试修复
heal_gateway() {
    log "开始自愈流程..."
    
    # 方案1: 重启systemd
    log "尝试方案1: systemctl重启"
    systemctl --user daemon-reload
    if openclaw gateway restart 2>&1; then
        sleep 5
        if check_gateway | grep -q "Runtime: running"; then
            log "✅ 方案1成功"
            notify "🟢 网关已自动恢复（方案1：systemctl重启）"
            return 0
        fi
    fi
    
    # 方案2: 强制杀死进程后启动
    log "尝试方案2: 强制重启"
    pkill -f "openclaw.*gateway" 2>/dev/null
    sleep 2
    if openclaw gateway start 2>&1; then
        sleep 5
        if check_gateway | grep -q "Runtime: running"; then
            log "✅ 方案2成功"
            notify "🟢 网关已自动恢复（方案2：强制重启）"
            return 0
        fi
    fi
    
    # 方案3: 检查端口冲突
    log "尝试方案3: 检查端口"
    PORT=$(grep -i "port" ~/.openclaw/openclaw.json | head -1 | grep -oE '[0-9]+' | head -1)
    if lsof -i:$PORT 2>/dev/null | grep -v "openclaw" | grep -q "."; then
        log "⚠️ 端口$PORT被占用，尝试释放"
        lsof -ti:$PORT | xargs -r kill -9
        sleep 2
        openclaw gateway start
        sleep 5
        if check_gateway | grep -q "Runtime: running"; then
            log "✅ 方案3成功"
            notify "🟢 网关已自动恢复（方案3：释放端口）"
            return 0
        fi
    fi
    
    # 全部失败
    log "❌ 自愈失败，通知管理员"
    notify "🔴 网关自愈失败，请人工检查！"
    return 1
}

# 主流程
main() {
    log "========== 开始健康检查 =========="
    
    STATUS=$(check_gateway)
    
    if echo "$STATUS" | grep -q "Runtime: running"; then
        log "✅ 网关正常"
        # 额外检查RPC
        if echo "$STATUS" | grep -q "RPC probe: ok"; then
            log "✅ RPC正常"
        else
            log "⚠️ RPC异常，尝试重启"
            heal_gateway
        fi
    else
        log "❌ 网关异常: $STATUS"
        heal_gateway
    fi
    
    log "========== 健康检查完成 =========="
}

main
