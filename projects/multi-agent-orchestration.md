# OpenClaw 多Agent协作实战指南

## 当前状态

✅ **已就绪：**
- Codex CLI → `/home/fengxueda/.nvm/versions/node/v25.6.0/bin/codex`
- Claude Code → `/home/fengxueda/.nvm/versions/node/v25.6.0/bin/claude`
- Gemini CLI → `/home/fengxueda/.nvm/versions/node/v25.6.0/bin/gemini` (v0.33.1)

❌ **待解决：**
- tmux（需要sudo权限安装）

## 方案A：使用OpenClaw原生sessions_spawn（推荐）

不需要tmux！OpenClaw自带`subagent`功能，可以创建持久化会话。

### 启动Codex Agent
```python
# 创建持久化的Codex会话
sessions_spawn(
    runtime="subagent",
    agentId="yitai",  # 或专门的codex-agent
    task="启动Codex CLI，使用o1-pro模型，Full Access权限，完成[任务描述]",
    mode="session",   # 持久化会话
    thread=True       # 绑定到线程
)
```

### 启动Claude Agent
```python
sessions_spawn(
    runtime="subagent",
    agentId="spikey",  # 或专门的claude-agent
    task="启动Claude Code，审核以下代码并提供改进建议",
    mode="session",
    thread=True
)
```

### 启动Gemini Agent
```python
sessions_spawn(
    runtime="subagent",
    agentId="bingbing",  # 或专门的gemini-agent
    task="启动Gemini CLI，设计前端界面并生成代码",
    mode="session",
    thread=True
)
```

## 方案B：使用nohup + 后台进程

如果一定要用CLI工具，可以用nohup让进程在后台运行：

```bash
# 启动Codex后台会话
nohup codex > /tmp/codex.log 2>&1 &

# 启动Claude后台会话
nohup claude > /tmp/claude.log 2>&1 &

# 启动Gemini后台会话
nohup gemini > /tmp/gemini.log 2>&1 &
```

然后OpenClaw定期读取日志文件监控进度。

## 实战演示

### 场景1：Codex写代码 + OpenClaw监控

让我演示如何启动一个长时间运行的Codex任务：

```
用户："帮我实现一个用户认证系统"

OpenClaw动作：
1. 创建subagent会话
2. 启动Codex CLI
3. 每5分钟检查进度
4. 完成后Review
```

### 场景2：三位大哥协作

```
用户："开发一个电商网站"

OpenClaw动作：
1. 启动Claude Agent（架构设计）
2. 启动Gemini Agent（前端开发）
3. 启动Codex Agent（后端开发）
4. 三方并行工作
5. 定期同步进度
6. 互相Review
7. 整合交付
```

## 监控机制

### 方法1：使用subagents管理
```python
# 列出所有运行的Agent
subagents(action="list")

# 向特定Agent发送消息
sessions_send(
    sessionKey="agent-session-key",
    message="检查当前进度"
)
```

### 方法2：使用cron定时检查
```python
# 每5分钟检查一次Agent状态
cron.add({
    "schedule": {"kind": "every", "everyMs": 300000},
    "payload": {
        "kind": "agentTurn",
        "message": "检查所有coding agent的进度并汇报"
    },
    "sessionTarget": "isolated"
})
```

## 现在开始实战！

你想先尝试哪种模式？

### 选项1：单Agent模式
启动Codex完成一个具体任务，OpenClaw全程监控。

### 选项2：双Agent模式  
Claude设计 + Codex实现，OpenClaw协调。

### 选项3：三Agent模式
Claude架构 + Gemini前端 + Codex后端，完整协作。

请选择一个场景，我立即开始演示！
