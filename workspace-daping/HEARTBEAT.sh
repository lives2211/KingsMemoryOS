#!/bin/bash
# HEARTBEAT.sh - 团队自愈监控脚本
# 每次心跳时执行

echo "=== OpenClaw Team Health Check ==="
echo "Time: $(date)"

# 1. 检查网关状态
echo "[1/5] Checking Gateway..."
if ! openclaw gateway status | grep -q "running"; then
    echo "⚠️ Gateway not running, restarting..."
    openclaw gateway restart
    sleep 5
fi

# 2. 检查Cron任务健康（>26小时未运行视为stale）
echo "[2/5] Checking Cron Jobs..."
STALE_JOBS=$(openclaw cron list --json | jq -r '.jobs[] | select(.state.lastRunAtMs < '$(($(date +%s)*1000 - 26*3600*1000))') | .id')

for job_id in $STALE_JOBS; do
    echo "🔄 Restarting stale job: $job_id"
    openclaw cron run "$job_id" --force
done

# 3. 检查情报文件更新
echo "[3/5] Checking Intel Files..."
TODAY=$(date +%Y-%m-%d)
if [ ! -f "/media/fengxueda/D/openclaw-data/workspace/workspace-daping/intel/DAILY-INTEL.md" ]; then
    echo "⚠️ DAILY-INTEL.md not found for today"
    # Trigger Dwight task
    openclaw cron run dwight-morning-intel --force 2>/dev/null || true
fi

# 4. 磁盘空间检查
echo "[4/5] Checking Disk Space..."
USAGE=$(df /media/fengxueda/D/openclaw-data/ | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$USAGE" -gt 90 ]; then
    echo "⚠️ Disk usage > 90%, cleaning old logs..."
    find /media/fengxueda/D/openclaw-data/workspace/*/memory/ -name "*.md" -mtime +30 -delete
fi

# 5. 检查API配额（简化版）
echo "[5/5] Checking API Quotas..."
# TODO: Add actual API quota checks

echo "=== Health Check Complete ==="