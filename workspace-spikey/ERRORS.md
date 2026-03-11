# ERRORS.md - 错误知识库

> 记录所有错误及解决方案，防止重复犯错

## 错误分类

### 🔴 API错误

| 错误 | 原因 | 解决方案 | 首次发生 |
|------|------|----------|----------|
| 6551 API 401 | Token过期 | 更新OPENNEWS_TOKEN | 2026-03-06 |
| Twitter MCP失败 | 未配置或限额 | 使用xreach替代 | 2026-03-06 |
| MiniMax超时 | 网络问题 | 重试或切换模型 | - |

### 🟡 工具错误

| 错误 | 原因 | 解决方案 | 首次发生 |
|------|------|----------|----------|
| xreach未认证 | 缺少Cookie | 配置Twitter Token | 2026-03-06 |
| Nitter RSS失效 | 服务不稳定 | 使用6551+DDG替代 | 2026-03-06 |
| union-search依赖缺失 | pip未安装 | --break-system-packages | 2026-03-06 |

### 🟢 逻辑错误

| 错误 | 原因 | 解决方案 | 首次发生 |
|------|------|----------|----------|
| 情报重复收集 | 未检查已有数据 | 先读取再决定 | - |
| 内容风格不一致 | 未参考MEMORY.md | 每次读取长期记忆 | - |
| 任务遗漏 | 未检查队列 | 使用TASK_QUEUE.md | - |

## 快速修复命令

```bash
# 网关重启
openclaw gateway restart

# Cron任务强制运行
openclaw cron run <jobId> --force

# 检查API状态
curl -s https://ai.6551.io/health

# 查看日志
tail -f /tmp/openclaw/*.log
```

## 预防措施

1. **每次会话前** - 检查ERRORS.md相关条目
2. **遇到新错误** - 立即记录到本文档
3. **每周回顾** - Angela审计时检查新增错误
4. **每月归档** - 将已解决错误移到ARCHIVED_ERRORS.md