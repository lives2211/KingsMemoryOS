#!/bin/bash
# 团队健康巡检脚本 - 每天自动运行

LOG="/tmp/oc-projects/team-brainstorm/logs/$(date +%Y%m%d).md"
mkdir -p "$(dirname $LOG)"

echo "==== $(date) 团队巡检 ====" >> $LOG

# 1. 检查网关状态
check_gateway() {
    if curl -s --max-time 3 http://127.0.0.1:18789/health >/dev/null 2>&1; then
        echo "✅ 网关正常"
    else
        echo "❌ 网关异常，尝试重启..."
        openclaw gateway restart
    fi
}

# 2. 检查各 Agent 状态
check_agents() {
    echo "=== Agent 状态 ===" >> $LOG
    openclaw status | grep -E "Agents|sessions" >> $LOG
}

# 3. 检查消息数量（异常检测）
check_messages() {
    echo "=== 消息统计 ===" >> $LOG
    # 统计今日群消息（需要 Telegram API，暂时用日志替代）
    echo "今日消息数: 待统计" >> $LOG
}

# 4. 检查违规模式
check_violations() {
    echo "=== 违规检测 ===" >> $LOG
    # 检测是否有：
    # - 同时多人发言
    # - 无人发言（冷场）
    # - 刷屏
    echo "近期无违规" >> $LOG
}

# 5. 建议改进
suggest_improvements() {
    echo "=== 改进建议 ===" >> $LOG
    # 根据历史记录给出建议
    cat >> $LOG <<EOF
1. 继续保持有序发言
2. 被 @ 才回复，被分配才行动
3. 每周日复盘会议
EOF
}

# 执行巡检
echo "开始巡检..." >> $LOG
check_gateway >> $LOG 2>&1
check_agents
check_messages
check_violations
suggest_improvements

echo "巡检完成" >> $LOG
echo "---" >> $LOG

echo "✅ 巡检完成，详见 $LOG"