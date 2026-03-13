# Monica 自动派发执行指南

## 目标
让 Monica 在总指挥频道收到任务后，直接执行派发命令

## 当前问题
Monica 只回复文本建议，没有实际调用派发系统

## 解决方案

### 方案1：使用 OpenClaw 的 tool 调用（推荐）

配置 Monica 使用 `exec` tool 执行派发脚本：

```yaml
# 在 Monica 的配置中启用 exec tool
agents:
  main:
    tools:
      allowed:
        - exec
        - message
        - sessions_spawn
```

然后在 SOUL.md 中指示 Monica 执行：
```
当识别任务后，执行：
exec: cd /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise && ./quick_dispatch.sh "任务描述" "用户"
```

### 方案2：使用 sessions_spawn 调用派发 Agent

让 Monica 调用专门的派发 Agent：

```
sessions_spawn:
  agentId: dispatcher
  task: 派发任务到 Paperclip
  message: 用户任务描述
```

### 方案3：Webhook 方式

配置 OpenClaw 在收到消息时调用 Webhook：

```yaml
channels:
  discord:
    accounts:
      main:
        webhooks:
          on_message: http://localhost:3100/webhook/dispatch
```

## 立即实施方案

由于 OpenClaw 的配置限制，我们先使用**最简单的方式**：

### 方式：Monica 直接执行命令

修改 Monica 的回复逻辑，在回复中包含执行标记，然后由外部脚本解析执行。

或者，使用 OpenClaw 的 `heartbeat` 机制定期检查并派发。

## 当前立即可用的方式

由于自动派发需要 OpenClaw 内部配置，目前最可靠的方式是：

### 1. 命令行派发（100%可用）
```bash
./ask "帮我爬取数据，预算10美元"
```

### 2. Discord @Monica + 确认（需要用户回复"执行"）
用户: @龙虾总管 帮我爬取数据
Monica: 方案...
用户: 执行
Monica: 调用派发

### 3. 配置自动执行（需要重启 OpenClaw）
修改配置后重启服务。

## 推荐

现在先使用**方式1（命令行）**，同时配置**方式3（自动执行）**。
