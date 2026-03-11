#!/bin/bash
# OpenClaw 自愈网关 v2.4 - 精简版

LOG="/tmp/openclaw-heal.log"
GATEWAY_PORT=18789

echo "==== $(date) 自愈检查 v2.4 ====" >> $LOG

# 检查端口连通性
check_port() {
    curl -s --max-time 3 http://127.0.0.1:$GATEWAY_PORT/health >/dev/null 2>&1
    return $?
}

# 检查进程
check_process() {
    pgrep -f openclaw-gateway >/dev/null 2>&1
    return $?
}

# 主逻辑
main() {
    # 1. 端口检查
    if ! check_port; then
        echo "❌ 端口 $GATEWAY_PORT 不通，尝试重启..."
        openclaw gateway restart >> $LOG 2>&1
        sleep 5
        if check_port; then
            echo "✅ 重启成功"
        else
            echo "❌ 重启失败"
        fi
    else
        echo "✅ 网关正常"
    fi
    
    # 2. 进程检查
    if ! check_process; then
        echo "⚠️ 进程不存在，启动..."
        openclaw gateway start >> $LOG 2>&1
    fi
}

# 根据参数执行
case "${1:-check}" in
    check)
        check_port && echo "✅ 网关正常" || echo "❌ 网关异常"
        ;;
    *)
        main
        ;;
esac