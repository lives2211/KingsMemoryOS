# ERRORS.md - 团队错误记录与修复指南

> 记录所有错误、故障和解决方案，防止重复犯错

---

## 错误分类

### 🔴 Critical - 系统级故障
| 错误 | 原因 | 解决方案 | 首次发生 |
|------|------|---------|---------|
| Gateway崩溃 | 内存不足/进程冲突 | `openclaw gateway restart` | - |
| Cron任务全部停滞 | 调度器故障 | 检查systemd服务状态 | - |
| Disk满100% | 日志未清理 | 自动清理脚本+告警 | - |

### 🟡 High - 任务级故障
| 错误 | 原因 | 解决方案 | 首次发生 |
|------|------|---------|---------|
| 6551 API返回空 | Token过期/限流 | 检查token，添加重试逻辑 | - |
| Nitter无法访问 | 实例被封/IP限制 | 切换到备用实例 | - |
| Twitter发送失败 | MCP未配置/限流 | 检查MCP配置，改用草稿模式 | - |

### 🟢 Medium - 警告级别
| 错误 | 原因 | 解决方案 | 首次发生 |
|------|------|---------|---------|
| 情报文件为空 | 无新内容/筛选过严 | 放宽筛选条件 | - |
| 内容生成超时 | 模型响应慢 | 缩短prompt，增加timeout | - |
| 磁盘使用率>90% | 日志堆积 | 触发自动清理 | - |

---

## 常见错误快速修复

### 6551 API Error
```bash
# 检查token是否有效
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -d '{"q": "test", "limit": 1}'

# 如返回401，更新token
```

### Nitter RSS Timeout
```bash
# 主实例失败时切换
web_fetch "https://nitter.net/..." || \
web_fetch "https://nitter.it/..." || \
web_fetch "https://nitter.cz/..."
```

### Gateway Not Responding
```bash
# 三步重启法
1. openclaw gateway stop
2. sleep 5
3. openclaw gateway start
4. openclaw gateway status
```

---

## 预防措施

- [ ] 每日23:00成本监控（已配置）
- [ ] 每周五磁盘清理（已配置）
- [ ] 心跳自愈检查（已配置）
- [ ] API配额预警（待配置）

---

*最后更新：2026-03-06*