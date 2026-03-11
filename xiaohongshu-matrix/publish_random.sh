#!/bin/bash
# 随机时间自动发布脚本
# 在指定时间窗口内随机时间发布

set -euo pipefail

echo "🎲 随机时间自动发布"
echo "===================="
echo ""

BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"

cd "$BASE_DIR"

# 账号配置
ACCOUNTS=("tech-geek" "career-growth")
ACCOUNT_NAMES=("数码虾" "职场虾")

# 发布时间窗口（小时:分钟）
# 格式: "开始小时 开始分钟 结束小时 结束分钟"
declare -A TIME_WINDOWS=(
    ["morning"]="7 30 9 30"      # 早上 7:30-9:30
    ["noon"]="11 30 13 30"      # 中午 11:30-13:30
    ["afternoon"]="15 0 17 0"   # 下午 15:00-17:00
    ["evening"]="19 0 21 0"     # 晚上 19:00-21:00
)

# 随机选择时间窗口
WINDOW_KEYS=("morning" "noon" "afternoon" "evening")
RANDOM_WINDOW=${WINDOW_KEYS[$RANDOM % ${#WINDOW_KEYS[@]}]}

read START_H START_M END_H END_M <<< "${TIME_WINDOWS[$RANDOM_WINDOW]}"

echo "📅 时间窗口: $RANDOM_WINDOW"
echo "   ${START_H}:${START_M} - ${END_H}:${END_M}"
echo ""

# 计算随机发布时间
START_MIN=$((START_H * 60 + START_M))
END_MIN=$((END_H * 60 + END_M))
RANDOM_MIN=$((START_MIN + RANDOM % (END_MIN - START_MIN)))

PUBLISH_H=$((RANDOM_MIN / 60))
PUBLISH_M=$((RANDOM_MIN % 60))

echo "🎯 随机发布时间: ${PUBLISH_H}:${PUBLISH_M}"
echo ""

# 计算等待时间（分钟）
CURRENT_MIN=$(date +%H)*60 + $(date +%M)
if [ $RANDOM_MIN -gt $CURRENT_MIN ]; then
    WAIT_MIN=$((RANDOM_MIN - CURRENT_MIN))
else
    # 如果已经过了今天的时间，等到明天
    echo "⏰ 今天时间已过，等到明天..."
    WAIT_MIN=$((RANDOM_MIN + 24*60 - CURRENT_MIN))
fi

echo "⏳ 等待 ${WAIT_MIN} 分钟后发布..."
echo "   预计发布时间: $(date -d "+$WAIT_MIN minutes" "+%H:%M")"
echo ""

# 等待
sleep ${WAIT_MIN}m

echo "🚀 开始发布..."
echo ""

# 随机选择账号
RANDOM_INDEX=$((RANDOM % ${#ACCOUNTS[@]}))
ACCOUNT=${ACCOUNTS[$RANDOM_INDEX]}
ACCOUNT_NAME=${ACCOUNT_NAMES[$RANDOM_INDEX]}

echo "📱 选择账号: $ACCOUNT_NAME ($ACCOUNT)"
echo ""

# 执行发布
./publish_stable.sh "$ACCOUNT"

echo ""
echo "===================="
echo "✅ 随机发布完成！"
echo ""
echo "📊 发布信息:"
echo "   时间窗口: $RANDOM_WINDOW"
echo "   发布时间: ${PUBLISH_H}:${PUBLISH_M}"
echo "   账号: $ACCOUNT_NAME"
echo ""
