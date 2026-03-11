#!/bin/bash
# OpenClaw 健康巡检脚本

echo "=== OpenClaw 健康巡检 ==="
echo "时间: $(date)"

# 1. Gateway 状态
echo -e "\n[1] Gateway 状态:"
systemctl --user is-active openclaw-gateway 2>/dev/null || echo "未运行"

# 2. 服务进程
echo -e "\n[2] 进程数:"
pgrep -c openclaw-gateway 2>/dev/null || echo "0"

# 3. 内存使用
echo -e "\n[3] 内存使用 (MB):"
ps aux | grep openclaw-gateway | grep -v grep | awk '{sum+=$6} END {print sum/1024}'

# 4. 磁盘空间
echo -e "\n[4] 磁盘空间:"
df -h ~/.openclaw | tail -1

# 5. 工作区文件数
echo -e "\n[5] 工作区文件:"
find ~/.openclaw/workspace -type f 2>/dev/null | wc -l

# 6. 日志大小
echo -e "\n[6] 日志目录大小 (MB):"
du -sm ~/.openclaw/logs 2>/dev/null | awk '{print $1}'

# 7. Cron 任务数
echo -e "\n[7] Cron 任务:"
openclaw cron list 2>/dev/null | grep -c "idle\|running" || echo "0"

# 8. Telegram 连接
echo -e "\n[8] Telegram Bot:"
systemctl --user is-active openclaw-gateway 2>/dev/null && echo "正常" || echo "异常"

echo -e "\n=== 巡检完成 ==="
