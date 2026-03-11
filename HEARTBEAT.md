# HEARTBEAT.md - 团队自愈监控

## 每次心跳执行（每30分钟）

### 1. Cron任务健康检查

检查以下任务是否超过26小时未运行：

| 任务 | Job ID | 检查命令 |
|------|--------|---------|
| Dwight 08:00 | e81155c7-91ed-4441-b466-cbfe36626728 | `openclaw cron runs e81155c7-91ed-4441-b466-cbfe36626728` |
| Kelly 09:00 | 6d286f90-7ad2-4ba7-9db6-3f3c9e1ac7f0 | `openclaw cron runs 6d286f90-7ad2-4ba7-9db6-3f3c9e1ac7f0` |
| Rachel 09:00 | 3a75fe8c-a8ab-4f6e-8adc-663d5ec516fe | `openclaw cron runs 3a75fe8c-a8ab-4f6e-8adc-663d5ec516fe` |
| Ross 10:00 | 4845fbc0-e046-4511-b956-e54ab936fd8e | `openclaw cron runs 4845fbc0-e046-4511-b956-e54ab936fd8e` |
| Angela 18:00 | 7941585e-bbc5-4d6c-82d0-21b148bfca4f | `openclaw cron runs 7941585e-bbc5-4d6c-82d0-21b148bfca4f` |
| Pam 18:00 | 272a7a85-6666-4c9d-a592-cb22c8f5f5de | `openclaw cron runs 272a7a85-6666-4c9d-a592-cb22c8f5f5de` |

**如果stale > 26小时**：
```bash
openclaw cron run <jobId> --force
```

### 2. 系统资源检查

```bash
# 磁盘空间检查
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    echo "⚠️ 磁盘空间不足: ${DISK_USAGE}%"
    # 自动清理7天前的日志
    find /media/fengxueda/D/openclaw-data/workspace -name "*.log" -mtime +7 -delete
fi

# 内存检查
MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100)}')
if [ "$MEMORY_USAGE" -gt 90 ]; then
    echo "⚠️ 内存使用过高: ${MEMORY_USAGE}%"
    # 重启Gateway释放内存
    openclaw gateway restart
fi
```

### 3. 文件一致性检查

检查关键文件是否存在：
- [ ] intel/DAILY-INTEL.md （Dwight产出）
- [ ] memory/shared/*.md （各Agent产出）
- [ ] agents/*/SOUL.md （角色定义）

### 4. API配额监控

记录今日API调用次数到：
`memory/cost-tracking/YYYY-MM-DD.json`

```json
{
  "date": "2026-03-06",
  "api_calls": {
    "6551": 45,
    "union_search": 120,
    "other": 30
  },
  "estimated_cost_usd": 2.5
}
```

---

## Backup Check

每天执行：

```bash
./backup.sh
```

如果 push 成功：
BACKUP_OK

如果 push 失败：
BACKUP_FAILED

---

## 紧急处理流程

### Gateway崩溃
```bash
openclaw gateway restart
```

### Agent无响应
1. 检查该Agent的session状态
2. 如卡住，kill session后重建
3. 重新触发任务

### 文件冲突
如果发现两个Agent同时写入同一文件：
1. 立即停止相关任务
2. 手动合并文件内容
3. 更新AGENTS.md明确写入权限
4. 重启任务