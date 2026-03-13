# OpenClaw + Paperclip 集成方案

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    用户交互层                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Discord 群聊  │  │ Dashboard    │  │ API 调用     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  OpenClaw-Dispatch                          │
│              (轻量级任务派发服务器)                            │
│  - 端口: 3100                                               │
│  - 自动 Agent 匹配                                           │
│  - 任务状态管理                                              │
│  - Web Dashboard                                            │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Agent 执行层                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │
│  │ @yitai │ │@bingbing│ │ @daping│ │@spikey │ │@xiaohong│   │
│  │ 技术官  │ │ 创意官  │ │ 检测官  │ │ 审计官  │ │ 运营官  │   │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 快速开始

### 1. 启动派发服务器

```bash
cd /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise
./start_dispatch.sh
```

### 2. 访问 Dashboard

打开浏览器访问: `http://localhost:3100/dashboard.html`

### 3. API 使用

#### 创建任务
```bash
curl -X POST http://localhost:3100/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "爬取 Twitter 数据",
    "description": "帮我爬取 Twitter 上关于 AI 的热门推文",
    "budget": 10,
    "priority": "normal",
    "requester": "candycion"
  }'
```

#### 查询任务列表
```bash
curl http://localhost:3100/api/tasks
```

#### 匹配 Agent
```bash
curl -X POST http://localhost:3100/api/match \
  -H "Content-Type: application/json" \
  -d '{"description": "设计一个小红书封面"}'
```

## Agent 配置

| Agent | 角色 | 关键词 | 模型 |
|-------|------|--------|------|
| yitai | 技术官 | 编程、代码、脚本、开发、调试、爬取、修复 | claude-3-5-sonnet |
| bingbing | 创意官 | 设计、创意、封面、内容、文案、写作、图像、视频 | claude-3-5-sonnet |
| daping | 检测官 | 分析、数据、检测、监控、竞品 | claude-3-5-sonnet |
| spikey | 审计官 | 审计、复盘、质量、审查、检查 | claude-3-5-sonnet |
| xiaohongcai | 运营官 | 社媒、运营、发布、小红书、公众号 | claude-3-5-sonnet |

## Discord 集成

在总指挥频道 (1480388799589515446) 发送消息：

```
帮我爬取 Twitter 数据，预算10美元
```

自动回复：
```
🤖 任务已派发

📋 爬取 Twitter 数据
👤 指派给: @yitai (技术官)
🆔 任务ID: TASK-0001
💰 预算: $10
✅ 状态: backlog

💡 查看详情: http://localhost:3100/dashboard.html
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `dispatch_server.py` | Flask 派发服务器 |
| `dashboard.html` | Web 管理界面 |
| `paperclip_bridge.py` | Paperclip 桥接器 |
| `quick_dispatch.sh` | 快速派发脚本 |
| `start_dispatch.sh` | 启动脚本 |
| `stop_dispatch.sh` | 停止脚本 |

## 进阶: Paperclip 完整版

Paperclip 完整版提供更强大的功能：

- 组织架构管理
- 预算控制
- 审计日志
- 多租户支持

启动命令：
```bash
cd /home/fengxueda/.openclaw/workspace/projects/paperclip
export DATABASE_URL=postgres://paperclip:paperclip@localhost:5432/paperclip
pnpm --filter @paperclipai/server dev
```

访问: `http://localhost:3200`

## 故障排除

### 端口占用
```bash
# 检查端口
lsof -i :3100
# 杀死进程
pkill -f dispatch_server.py
```

### 数据库连接失败
```bash
# 检查 PostgreSQL
sudo -u postgres psql -c "\l"
# 重新创建用户
sudo -u postgres psql -c "CREATE USER paperclip WITH PASSWORD 'paperclip';"
sudo -u postgres psql -c "CREATE DATABASE paperclip OWNER paperclip;"
```

### 查看日志
```bash
tail -f /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise/dispatch_server.log
```
