# 🦞 OpenClaw 多 Agent 任务派发系统

智能识别 · 自动匹配 · 即时派发

## 系统状态

| 组件 | 状态 | 地址 |
|------|------|------|
| 派发服务器 | ✅ 运行中 | http://localhost:3100 |
| Dashboard | ✅ 可用 | http://localhost:3100/dashboard.html |
| API | ✅ 可用 | http://localhost:3100/api |

## 快速开始

### 启动服务器
```bash
./start_dispatch.sh
```

### 停止服务器
```bash
./stop_dispatch.sh
```

## 使用方式

### 1. Discord 直接输入
在总指挥频道发送任务描述，自动匹配 Agent：
```
帮我爬取 Twitter 数据，预算10美元
```

### 2. Dashboard 界面
打开 http://localhost:3100/dashboard.html 可视化操作

### 3. API 调用
```bash
curl -X POST http://localhost:3100/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"任务","description":"描述","budget":10}'
```

## Agent 团队

| Agent | 角色 | 技能关键词 |
|-------|------|-----------|
| @yitai | 技术官 | 编程、代码、脚本、开发、调试、爬取 |
| @bingbing | 创意官 | 设计、创意、封面、内容、文案、写作 |
| @daping | 检测官 | 分析、数据、检测、监控、竞品 |
| @spikey | 审计官 | 审计、复盘、质量、审查、检查 |
| @xiaohongcai | 运营官 | 社媒、运营、发布、小红书、公众号 |

## 任务状态

- `backlog` - 待处理
- `in_progress` - 进行中
- `review` - 审核中
- `done` - 已完成

## 文件结构

```
.
├── dispatch_server.py      # 主服务器
├── dashboard.html          # Web 界面
├── paperclip_bridge.py     # Paperclip 集成
├── quick_dispatch.sh       # 快速派发
├── start_dispatch.sh       # 启动脚本
├── stop_dispatch.sh        # 停止脚本
├── INTEGRATION.md          # 集成文档
└── README.md               # 本文档
```

## API 文档

### POST /api/tasks
创建新任务

**请求体:**
```json
{
  "title": "任务标题",
  "description": "任务描述",
  "budget": 10,
  "priority": "normal",
  "requester": "用户名"
}
```

**响应:**
```json
{
  "id": "TASK-0001",
  "agent_id": "yitai",
  "agent_name": "yitai",
  "agent_role": "技术官",
  "status": "backlog",
  "created_at": "2026-03-12T..."
}
```

### GET /api/tasks
获取所有任务

### GET /api/agents
获取所有 Agent 配置

### POST /api/match
匹配最佳 Agent

**请求体:**
```json
{"description": "任务描述"}
```

## 日志查看

```bash
tail -f dispatch_server.log
```

## 故障排除

| 问题 | 解决 |
|------|------|
| 端口占用 | `pkill -f dispatch_server.py` |
| 服务器无响应 | `./stop_dispatch.sh && ./start_dispatch.sh` |
| 数据库错误 | 检查 PostgreSQL 服务状态 |

## 许可证

MIT
