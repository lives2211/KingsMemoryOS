# HEARTBEAT.md - 团队健康监控

## 目的
确保所有Agent按时运行，自动检测并修复故障。

## 每次心跳检查项

### 1. Cron任务健康检查
```bash
# 检查是否有任务超过26小时未运行
openclaw cron list | grep -E "(dwight|kelly|rachel|ross|angela|pam)"
```

**关键任务监控：**
| 任务 | 计划时间 | 最大延迟 |
|------|---------|---------|
| dwight-morning-intel | 08:00 | 26h |
| dwight-midday-intel | 12:00 | 26h |
| dwight-evening-intel | 18:00 | 26h |
| kelly-content-pipeline | 09:30 | 26h |
| rachel-linkedin-content | 09:00 | 26h |
| pam-weekly-newsletter | 周五18:00 | 7d |

### 2. 如果任务失效，强制重启
```bash
openclaw cron run <jobId> --force
```

### 3. 文件系统检查
- intel/DAILY-INTEL.md 是否存在且今日更新
- memory/ 目录是否正常写入
- agents/*/memory/ 各Agent记忆是否正常

### 4. API配额检查
- 6551 API剩余额度
- MiniMax API调用情况

## 自动化脚本

```bash
#!/bin/bash
# save as: scripts/health-check.sh

echo "=== Agent Team Health Check ==="
date

# Check cron jobs
echo "Checking cron jobs..."
openclaw cron list | grep -E "(stale|failed)" && echo "⚠️ 发现异常任务"

# Check today's intel file
TODAY=$(date +%Y-%m-%d)
if [ ! -f "intel/data/${TODAY}.json" ]; then
    echo "⚠️ 今日情报文件缺失，触发Dwight紧急收集"
    openclaw cron run dwight-morning-intel --force
fi

echo "=== Health Check Complete ==="
```

## 告警阈值

| 指标 | 正常 | 警告 | 严重 |
|------|------|------|------|
| 任务延迟 | <1h | 1-6h | >6h |
| API剩余 | >20% | 10-20% | <10% |
| 磁盘空间 | >20GB | 10-20GB | <10GB |

## 升级路径

1. **自动修复失败** → @Monica通知用户
2. **API配额耗尽** → 切换备用方案
3. **连续3天异常** → 全面系统审查