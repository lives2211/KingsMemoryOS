# OpenClaw + Paperclip 集成方案

## 🎯 架构设计

### 核心思路
Paperclip 作为**编排管理层**，OpenClaw 作为**执行层**，通过 API 集成。

```
┌─────────────────────────────────────────────────────────────┐
│                    Paperclip (Node.js)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   React UI  │  │  API Server │  │  PostgreSQL │         │
│  │  (Port 3000)│  │ (Port 3100) │  │   (Port 5432)│        │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  功能：                                                      │
│  • 组织架构管理                                              │
│  • 任务委派和追踪                                            │
│  • 预算控制                                                  │
│  • 心跳调度                                                  │
│  • Dashboard UI                                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP API
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                         │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │  Monica │  │  yitai  │  │bingbing │  │  daping │       │
│  │  (main) │  │(技术官) │  │(创意官) │  │(检测官) │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│                                                             │
│  ┌─────────┐  ┌─────────┐                                  │
│  │ spikey  │  │xiaohongc│                                  │
│  │(审计官) │  │ai(运营官)│                                  │
│  └─────────┘  └─────────┘                                  │
│                                                             │
│  功能：                                                      │
│  • 独立 AI 实例                                              │
│  • 技能执行                                                  │
│  • 任务处理                                                  │
│  • 结果返回                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 部署步骤

### Step 1: 部署 Paperclip

```bash
# 1. 克隆仓库
git clone https://github.com/paperclipai/paperclip.git
cd paperclip

# 2. 安装依赖
pnpm install

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 4. 启动开发服务器
pnpm dev
```

**默认端口：**
- API Server: http://localhost:3100
- React UI: http://localhost:3000

---

### Step 2: 配置 OpenClaw 多 Agent

编辑 `~/.openclaw/gateway.yaml`:

```yaml
agents:
  defaults:
    model: "kimi-k2.5"
    skills: []  # 所有 Agent 共享技能
    
  list:
    # Agent 1: Monica (总管)
    - id: main
      name: "Monica"
      default: true
      identity:
        name: "龙虾总管"
        role: "CEO"
        emoji: "🦞"
      # 连接到 Paperclip API
      runtime:
        type: "paperclip"
        api_url: "http://localhost:3100"
        agent_id: "main"
    
    # Agent 2: yitai (技术官)
    - id: yitai
      name: "yitai"
      identity:
        name: "技术官"
        role: "CTO"
        emoji: "💻"
      runtime:
        type: "paperclip"
        api_url: "http://localhost:3100"
        agent_id: "yitai"
    
    # Agent 3: bingbing (创意官)
    - id: bingbing
      name: "bingbing"
      identity:
        name: "创意官"
        role: "CCO"
        emoji: "🎨"
      runtime:
        type: "paperclip"
        api_url: "http://localhost:3100"
        agent_id: "bingbing"
    
    # Agent 4: daping (检测官)
    - id: daping
      name: "daping"
      identity:
        name: "检测官"
        role: "QA Lead"
        emoji: "🔍"
      runtime:
        type: "paperclip"
        api_url: "http://localhost:3100"
        agent_id: "daping"
    
    # Agent 5: spikey (审计官)
    - id: spikey
      name: "spikey"
      identity:
        name: "审计官"
        role: "Auditor"
        emoji: "📊"
      runtime:
        type: "paperclip"
        api_url: "http://localhost:3100"
        agent_id: "spikey"
    
    # Agent 6: xiaohongcai (运营官)
    - id: xiaohongcai
      name: "xiaohongcai"
      identity:
        name: "运营官"
        role: "COO"
        emoji: "📱"
      runtime:
        type: "paperclip"
        api_url: "http://localhost:3100"
        agent_id: "xiaohongcai"
```

---

### Step 3: 创建 Paperclip Agent 配置

在 Paperclip 中创建对应的 Agent：

```bash
# 通过 Paperclip CLI 创建 Agent
npx paperclipai agent create \
  --name "yitai" \
  --title "技术官" \
  --department "技术部" \
  --capabilities "编程,开发,架构,脚本" \
  --budget-monthly 100

npx paperclipai agent create \
  --name "bingbing" \
  --title "创意官" \
  --department "创作部" \
  --capabilities "内容,设计,文案,创意" \
  --budget-monthly 80

npx paperclipai agent create \
  --name "daping" \
  --title "检测官" \
  --department "质检部" \
  --capabilities "检测,分析,测试,数据" \
  --budget-monthly 60

npx paperclipai agent create \
  --name "spikey" \
  --title "审计官" \
  --department "审计部" \
  --capabilities "审计,复盘,质量,文档" \
  --budget-monthly 60

npx paperclipai agent create \
  --name "xiaohongcai" \
  --title "运营官" \
  --department "运营部" \
  --capabilities "社媒,运营,小红书,公众号" \
  --budget-monthly 70
```

---

### Step 4: 配置心跳和任务调度

在 Paperclip 中配置心跳任务：

```bash
# 每天早上8点：站会
npx paperclipai cron create \
  --name "daily-standup" \
  --schedule "0 8 * * *" \
  --agent "main" \
  --task "生成站会报告"

# 每天下午6点：日报
npx paperclipai cron create \
  --name "daily-report" \
  --schedule "0 18 * * *" \
  --agent "main" \
  --task "生成日报"

# 每周五：周复盘
npx paperclipai cron create \
  --name "weekly-review" \
  --schedule "0 21 * * 5" \
  --agent "spikey" \
  --task "周复盘"
```

---

## 🔌 API 集成

### Paperclip → OpenClaw API 调用

```javascript
// Paperclip 中调用 OpenClaw Agent
const openclaw = {
  baseUrl: 'http://localhost:18788',  // OpenClaw Gateway
  
  async dispatch(agentId, task) {
    const response = await fetch(`${this.baseUrl}/v1/sessions/spawn`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        agentId: agentId,
        task: task,
        runtime: 'subagent'
      })
    });
    return response.json();
  }
};

// 使用示例
await openclaw.dispatch('yitai', '编写爬虫脚本');
```

### OpenClaw → Paperclip API 调用

```python
# OpenClaw 中调用 Paperclip
import requests

class PaperclipClient:
    def __init__(self, base_url='http://localhost:3100'):
        self.base_url = base_url
    
    def create_task(self, title, description, assignee, budget):
        response = requests.post(f'{self.base_url}/api/tasks', json={
            'title': title,
            'description': description,
            'assignee': assignee,
            'budget': budget
        })
        return response.json()
    
    def get_agent_status(self, agent_id):
        response = requests.get(f'{self.base_url}/api/agents/{agent_id}')
        return response.json()

# 使用示例
client = PaperclipClient()
client.create_task('编写爬虫', '爬取数据', 'yitai', 10.0)
```

---

## 📊 工作流程

### 1. 任务创建流程

```
用户 → Paperclip UI
         ↓
    创建 Task
         ↓
    Paperclip 选择 Agent
         ↓
    调用 OpenClaw API
         ↓
    OpenClaw Agent 执行
         ↓
    返回结果给 Paperclip
         ↓
    Paperclip 更新任务状态
```

### 2. 心跳调度流程

```
Paperclip Cron (定时触发)
         ↓
    唤醒 Agent
         ↓
    检查待办任务
         ↓
    调用 OpenClaw
         ↓
    Agent 处理任务
         ↓
    返回结果
         ↓
    更新 Dashboard
```

---

## 🎨 Dashboard 功能

Paperclip 提供：

1. **组织架构图** - 可视化汇报关系
2. **任务看板** - Kanban 风格任务管理
3. **预算监控** - 实时成本追踪
4. **Agent 状态** - 在线/离线/忙碌
5. **委派链** - 任务层级关系
6. **审计日志** - 所有操作记录

---

## 💡 优势对比

| 功能 | 纯 OpenClaw | OpenClaw + Paperclip |
|------|------------|---------------------|
| **多 Agent** | 模拟 | ✅ 真正独立 |
| **UI 界面** | 自建 Dashboard | ✅ 开箱即用 |
| **任务管理** | Ticket 系统 | ✅ 企业级 |
| **预算控制** | 自建 | ✅ 内置 |
| **心跳调度** | Cron | ✅ 内置 |
| **审计日志** | 自建 | ✅ 内置 |
| **成本** | 低 | 中等 |

---

## 🚀 快速启动

### 一键启动脚本

```bash
#!/bin/bash
# start-paperclip-openclaw.sh

echo "🚀 启动 Paperclip + OpenClaw 集成环境"

# 1. 启动 Paperclip
cd /path/to/paperclip
pnpm dev &
PAPERCLIP_PID=$!
echo "✅ Paperclip 启动 (PID: $PAPERCLIP_PID)"

# 2. 等待 Paperclip 就绪
sleep 5

# 3. 启动 OpenClaw
openclaw gateway start &
OPENCLAW_PID=$!
echo "✅ OpenClaw 启动 (PID: $OPENCLAW_PID)"

# 4. 等待 OpenClaw 就绪
sleep 3

# 5. 初始化配置
python3 init_agents.py

echo "✅ 集成环境就绪"
echo ""
echo "📱 Dashboard: http://localhost:3000"
echo "🔌 API: http://localhost:3100"
echo "🦞 OpenClaw: http://localhost:18788"

# 保持运行
wait
```

---

## 📚 参考文档

- Paperclip Docs: https://paperclip.ing/docs
- OpenClaw Docs: https://docs.openclaw.ai
- API Reference: http://localhost:3100/docs

---

**下一步：需要我帮你完成部署吗？**

1. 等待 `pnpm install` 完成
2. 配置 Paperclip 环境变量
3. 启动 Paperclip 服务
4. 配置 OpenClaw 多 Agent
5. 测试集成
