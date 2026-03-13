#!/bin/bash
# Quick dispatch script for Paperclip tasks
# Usage: ./quick_dispatch.sh "任务描述" "用户"

TASK_DESC="$1"
USER="${2:-candycion}"

if [ -z "$TASK_DESC" ]; then
    echo "Usage: ./quick_dispatch.sh \"任务描述\" [用户]"
    exit 1
fi

# 匹配 Agent
AGENT=$(python3 paperclip_bridge.py match "$TASK_DESC" 2>/dev/null | grep "匹配成功" | sed 's/.*@\([^ ]*\).*/\1/')

if [ -z "$AGENT" ]; then
    AGENT="yitai"  # 默认技术官
fi

# 构建任务 JSON
TASK_JSON=$(cat <<EOF
{
  "title": "$TASK_DESC",
  "description": "$TASK_DESC",
  "requester": "$USER",
  "budget": 0,
  "priority": "normal",
  "created_at": "$(date -Iseconds)"
}
EOF
)

# 派发任务
echo "🤖 正在派发任务到 @$AGENT..."
python3 paperclip_bridge.py dispatch "$TASK_JSON"
