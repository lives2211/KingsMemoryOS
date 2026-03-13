# OpenClaw + Paperclip 集成方案

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                     Paperclip (Node.js)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   React UI   │  │  API Server  │  │  PostgreSQL  │      │
│  │   Port 3000  │  │  Port 3100   │  │   Port 5432  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              心跳调度 + 任务管理 + 预算控制              │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP API
                              │
┌─────────────────────────────────────────────────────────────┐
│                     OpenClaw (Python)                        │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐ │
│  │   Gateway  │ │    yitai   │ │  bingbing  │ │  daping  │ │
│  │  Port 18788│ │  (编程)    │ │  (创作)    │ │ (检测)   │ │
│  └────────────┘ └────────────┘ └────────────┘ └──────────┘ │
│                                                              │
│  ┌────────────┐ ┌────────────┐ ┌─────────────────────────┐ │
│  │   spikey   │ │xiaohongcai │ │       150+ Skills       │ │
│  │  (审计)    │ │  (运营)    │ │                         │ │
│  └────────────┘ └────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 核心功能

### 1. 总指挥频道自动派发

**场景**: 用户在 Discord #总指挥频道发送任务
```
用户: "帮我爬取twitter数据，预算10美元"
      ↓
Paperclip: 解析任务 → 匹配Agent → 创建Ticket
      ↓
OpenClaw: @yitai 执行 → 返回结果
      ↓
Paperclip: 记录完成 → 更新Dashboard
```

### 2. 心跳调度机制

| Agent | 心跳频率 | 职责 |
|-------|---------|------|
| yitai | 5分钟 | 技术任务检查 |
| bingbing | 5分钟 | 创意任务检查 |
| daping | 5分钟 | 检测任务检查 |
| spikey | 30分钟 | 审计任务检查 |
| xiaohongcai | 10分钟 | 社媒任务检查 |

### 3. 预算控制

```yaml
agents:
  yitai:
    monthly_budget: $50
    current_spend: $23.45
    
  bingbing:
    monthly_budget: $30
    current_spend: $12.80
    
  # 超出预算自动暂停
```

## 部署步骤

### 1. 部署 Paperclip

```bash
# 克隆
git clone https://github.com/paperclipai/paperclip.git
cd paperclip

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 配置数据库和API密钥

# 启动
npm run dev
```

### 2. 配置 OpenClaw 集成

```bash
# 安装 Paperclip CLI
npm install -g @paperclipai/cli

# 配置 OpenClaw Agent
paperclip agent add \
  --name "yitai" \
  --runtime "openclaw" \
  --endpoint "http://localhost:18788" \
  --skills "coding,debugging,architecture"
```

### 3. 配置心跳

```bash
# 添加 Cron 任务
crontab -e

# 每5分钟检查任务
*/5 * * * * paperclip heartbeat --agent yitai
*/5 * * * * paperclip heartbeat --agent bingbing
*/10 * * * * paperclip heartbeat --agent xiaohongcai
```

## API 集成

### Paperclip → OpenClaw

```javascript
// 派发任务
const response = await fetch('http://localhost:18788/api/dispatch', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    agent: 'yitai',
    task: '爬取Twitter数据',
    budget: 10,
    priority: 'high'
  })
});

const result = await response.json();
```

### OpenClaw → Paperclip

```python
# 任务完成回调
import requests

requests.post('http://localhost:3100/api/tasks/complete', json={
    'task_id': task_id,
    'agent': 'yitai',
    'result': result,
    'cost': actual_cost,
    'time_spent': time_spent
})
```

## Dashboard 功能

| 功能 | 说明 |
|------|------|
| **组织架构** | 可视化 Agent 团队 |
| **任务看板** | Kanban 风格任务管理 |
| **预算监控** | 实时成本和预算跟踪 |
| **审计日志** | 完整操作记录 |
| **性能指标** | Agent 效率和产出统计 |

## 与纯 OpenClaw 对比

| 维度 | 纯 OpenClaw | OpenClaw + Paperclip |
|------|------------|---------------------|
| Agent 数量 | 1 个模拟多角色 | ✅ 6 个真正独立 |
| UI Dashboard | 自建或命令行 | ✅ React 专业界面 |
| 任务管理 | Ticket 系统 | ✅ 企业级看板 |
| 心跳调度 | Cron 配置 | ✅ 内置心跳系统 |
| 预算控制 | 手动记录 | ✅ 自动预算管理 |
| 审计日志 | 自建 | ✅ 完整审计链 |
| 移动端 | 无 | ✅ 手机管理 |

## 下一步行动

1. ✅ 等待 npm install 完成
2. ⏳ 配置 PostgreSQL 数据库
3. ⏳ 启动 Paperclip 服务
4. ⏳ 配置 OpenClaw Agent 集成
5. ⏳ 测试自动派发流程

---

**状态**: 部署进行中...
