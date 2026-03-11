# HEARTBEAT.md - 团队自愈监控

> 每次心跳时执行的健康检查清单

---

## 检查项

### 1. Cron任务健康检查
```bash
# 检查是否有任务超过26小时未运行
openclaw cron list --include-disabled

# 如有 stale 任务，强制触发
openclaw cron run <jobId> --force
```

**待监控任务**：
- Dwight Morning (08:00): dwight-morning-intel
- Kelly Content (09:00): kelly-content-creation
- Rachel LinkedIn (09:00): rachel-linkedin-content
- Ross Engineering (10:00): ross-engineering-daily
- Angela Audit (18:00): angela-daily-audit
- Pam Newsletter (18:00): pam-newsletter-digest

### 2. 情报文件检查
- [ ] `intel/DAILY-INTEL.md` 今日是否更新
- [ ] `intel/data/YYYY-MM-DD.json` 是否存在
- [ ] 文件大小 > 0（非空文件）

### 3. 磁盘空间检查
```bash
# 检查可用空间
df -h /media/fengxueda/D/openclaw-data/

# 如 < 10GB，清理旧日志
find /media/fengxueda/D/openclaw-data/workspace/*/memory/ -name "*.md" -mtime +30 -delete
```

### 4. 网关状态检查
```bash
openclaw gateway status

# 如异常，重启
openclaw gateway restart
```

### 5. 记忆维护（每周五额外执行）
- [ ] 归档7天前的daily logs
- [ ] 提炼重要insight到MEMORY.md
- [ ] 清理临时文件

---

## 执行频率

- **常规检查**：每次心跳（每30分钟）
- **深度维护**：每周五 20:00

---

*自愈系统版本 1.0*