# OpenClaw 多 Agent 架构设计 (借鉴 Paperclip)

## 核心架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        管理层 (OpenClaw Gateway)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Monica     │  │   Cron 调度   │  │   审计日志    │          │
│  │   (主Agent)   │  │   (心跳机制)  │  │   (追踪)     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼─────────────────┼─────────────────┼──────────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      编排层 (Dispatch Server)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   任务队列    │  │   Agent 匹配  │  │   预算控制    │          │
│  │   (SQLite)   │  │   (关键词)    │  │   (追踪)     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼─────────────────┼─────────────────┼──────────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        执行层 (独立 Agents)                       │
│                                                                 │
│   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐           │
│   │ @yitai │   │@bingbing│   │ @daping│   │@spikey │           │
│   │ 技术官  │   │ 创意官  │   │ 检测官  │   │ 审计官  │           │
│   │独立进程 │   │独立进程 │   │独立进程 │   │独立进程 │           │
│   └────────┘   └────────┘   └────────┘   └────────┘           │
│                                                                 │
│   ┌────────┐                                                   │
│   │@xiaohong│                                                   │
│   │ 运营官  │                                                   │
│   │独立进程 │                                                   │
│   └────────┘                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 借鉴 Paperclip 的核心特性

### 1. 心跳机制 (Heartbeat)

Paperclip 的核心创新——Agent 定期唤醒检查任务。

```python
# cron 配置示例
{
  "agent": "yitai",
  "schedule": "*/5 * * * *",  # 每5分钟检查一次
  "action": "check_tasks",
  "callback": "report_status"
}
```

**实现方案:**
- 使用 OpenClaw 内置 cron 系统
- 每个 Agent 独立心跳
- 自动领取任务、汇报进度

### 2. 组织架构 (Org Chart)

```
CEO (Monica)
├── CTO (yitai) - 技术决策
│   └── 工程师 Agent
├── CCO (bingbing) - 创意决策
│   └── 设计师 Agent
├── CDO (daping) - 数据决策
│   └── 分析师 Agent
├── CAO (spikey) - 审计决策
│   └── 质检 Agent
└── CMO (xiaohongcai) - 运营决策
    └── 运营 Agent
```

### 3. 任务生命周期

```
backlog → assigned → in_progress → review → done
   ↑                                    ↓
   └──────────── rejected ←─────────────┘
```

**状态流转:**
1. `backlog` - 待分配
2. `assigned` - 已指派，等待 Agent 确认
3. `in_progress` - Agent 执行中
4. `review` - 完成，等待审核
5. `done` - 已完成
6. `rejected` - 被拒绝，返回 backlog

### 4. 预算控制

```python
{
  "task_id": "TASK-0001",
  "budget": 10.0,           # USD
  "spent": 0.0,
  "currency": "USD",
  "alerts": [
    {"threshold": 0.8, "action": "warn"},    # 80% 警告
    {"threshold": 1.0, "action": "block"}    # 100% 阻止
  ]
}
```

### 5. 审计日志

```python
{
  "timestamp": "2026-03-12T18:30:00Z",
  "event": "task_assigned",
  "task_id": "TASK-0001",
  "from": "monica",
  "to": "yitai",
  "metadata": {
    "reason": "keyword_match",
    "confidence": 0.95
  }
}
```

## 与 Paperclip 的关键区别

| 特性 | Paperclip | OpenClaw 优化版 |
|------|-----------|-----------------|
| **Agent 实现** | HTTP 心跳回调 | OpenClaw 独立会话 |
| **数据存储** | PostgreSQL | SQLite (轻量) |
| **UI** | React 前端 | HTML + API |
| **部署复杂度** | 高 (Node + DB) | 低 (Python 单文件) |
| **内存占用** | ~500MB | ~50MB |
| **启动速度** | 慢 | 快 |

## 优化后的文件结构

```
openclaw-enterprise/
├── core/
│   ├── __init__.py
│   ├── agent.py          # Agent 基类
│   ├── task.py           # 任务模型
│   ├── heartbeat.py      # 心跳机制
│   └── budget.py         # 预算控制
├── agents/
│   ├── __init__.py
│   ├── yitai.py          # 技术官
│   ├── bingbing.py       # 创意官
│   ├── daping.py         # 检测官
│   ├── spikey.py         # 审计官
│   └── xiaohongcai.py    # 运营官
├── server/
│   ├── __init__.py
│   ├── dispatch.py       # 派发服务器
│   ├── api.py            # REST API
│   └── websocket.py      # 实时通知
├── ui/
│   └── dashboard.html    # Web 界面
├── storage/
│   └── tasks.db          # SQLite 数据库
├── config/
│   └── agents.yaml       # Agent 配置
├── logs/
│   └── audit.log         # 审计日志
├── tests/
│   └── test_dispatch.py
├── cli.py                # 命令行工具
├── server.py             # 启动入口
└── README.md
```

## 下一步优化

### Phase 1: 心跳机制 ✅ (当前)
- [x] 基础派发服务器
- [x] Agent 自动匹配
- [x] Dashboard UI

### Phase 2: 独立 Agent 进程
- [ ] 每个 Agent 独立 OpenClaw 会话
- [ ] Agent 自主心跳检查任务
- [ ] 任务自动领取机制

### Phase 3: 审计与预算
- [ ] 完整审计日志
- [ ] Token 使用追踪
- [ ] 预算告警系统

### Phase 4: 高级编排
- [ ] 任务依赖图
- [ ] 并行执行
- [ ] 结果汇总

## 参考

- Paperclip: https://github.com/paperclipai/paperclip
- OpenClaw: https://docs.openclaw.ai
