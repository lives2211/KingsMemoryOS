# Discord Bot 配置指南

## 问题说明

当前自动派发系统是**模拟版本**，只在本地运行，没有真正连接到 Discord。

要实现**总指挥频道自动监听**，需要：
1. 创建 Discord Bot
2. 获取 Bot Token
3. 配置 Bot 权限
4. 启动 Bot 服务

---

## 方案1：使用 OpenClaw 内置 Discord 集成（推荐）

OpenClaw 已经配置了 Discord 通道，可以直接利用。

### 当前配置

```yaml
# ~/.openclaw/gateway.yaml 中已配置
channels:
  discord:
    accounts:
      main:
        token: "YOUR_BOT_TOKEN"  # 需要配置
        guilds:
          - id: "1480388798729814189"  # 你的 Discord 服务器
            channels:
              - id: "1480388799589515446"  # 总指挥频道
                name: "总指挥"
```

### 配置步骤

1. **创建 Discord Bot**
   - 访问 https://discord.com/developers/applications
   - 点击 "New Application"
   - 命名："OpenClaw Commander"
   - 进入 "Bot" 页面，点击 "Add Bot"
   - 复制 Token（保存好！）

2. **配置 Bot 权限**
   - 在 "Bot" 页面，开启以下权限：
     - ✅ Send Messages
     - ✅ Read Messages
     - ✅ Read Message History
     - ✅ Mention @everyone
   
3. **邀请 Bot 到服务器**
   - 进入 "OAuth2" → "URL Generator"
   - Scopes: `bot`
   - Permissions: `Send Messages`, `Read Messages`
   - 复制 URL，在浏览器打开，选择你的服务器

4. **配置 OpenClaw**
   ```bash
   # 编辑配置文件
   nano ~/.openclaw/gateway.yaml
   
   # 在 discord.accounts.main.token 填入你的 Bot Token
   ```

5. **重启 OpenClaw**
   ```bash
   openclaw gateway restart
   ```

---

## 方案2：独立 Discord Bot（Python）

如果不想用 OpenClaw 内置的，可以创建一个独立的 Python Bot。

### 创建 Bot

```python
# discord_dispatcher_bot.py
import discord
from discord.ext import commands
from auto_dispatcher import AutoDispatcher

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
dispatcher = AutoDispatcher()

@bot.event
async def on_ready():
    print(f'✅ Bot 已登录: {bot.user}')

@bot.event
async def on_message(message):
    # 忽略自己的消息
    if message.author == bot.user:
        return
    
    # 只监听总指挥频道
    if str(message.channel.id) != "1480388799589515446":
        return
    
    # 处理消息
    response = dispatcher.process_message(
        message.content,
        str(message.author),
        str(message.channel.id)
    )
    
    if response:
        await message.channel.send(response)
    
    await bot.process_commands(message)

# 运行 Bot
# 需要设置环境变量: DISCORD_BOT_TOKEN
import os
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
```

### 运行步骤

```bash
# 1. 安装依赖
pip3 install discord.py --break-system-packages

# 2. 设置 Token
export DISCORD_BOT_TOKEN="你的Bot Token"

# 3. 运行 Bot
python3 discord_dispatcher_bot.py
```

---

## 方案3：Webhook 方式（最简单）

如果不想创建 Bot，可以用 Webhook。

### 配置步骤

1. **在 Discord 创建 Webhook**
   - 进入总指挥频道设置
   - 点击 "Integrations" → "Webhooks"
   - 点击 "New Webhook"
   - 命名："OpenClaw Dispatcher"
   - 复制 Webhook URL

2. **配置环境变量**
   ```bash
   export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
   ```

3. **修改 notify_discord.py**
   - 使用 Webhook URL 发送消息

---

## 快速测试

### 测试 Bot 是否在线

```bash
# 在总指挥频道发送消息
!ping

# 如果 Bot 在线，会回复
```

### 测试自动派发

```bash
# 在总指挥频道发送
帮我爬取twitter数据，预算10美元

# Bot 应该自动回复
📋 任务已派发 → @yitai
```

---

## 故障排除

### 问题1：Bot 不回复

**检查：**
```bash
# 1. Bot Token 是否正确
openclaw config get channels.discord.accounts.main.token

# 2. Bot 是否在频道中
# 查看频道成员列表

# 3. 权限是否正确
# 确保 Bot 有发送消息权限
```

### 问题2：无法识别消息

**检查：**
```bash
# 查看 OpenClaw 日志
openclaw logs

# 检查是否正确连接到 Discord
openclaw status
```

### 问题3：派发失败

**检查：**
```bash
# 检查 Paperclip 服务
curl http://localhost:3100/health

# 检查 Agent 状态
python3 paperclip_client.py --agents
```

---

## 推荐方案

**推荐用方案1（OpenClaw 内置）**，因为：
- ✅ 已经配置好
- ✅ 与现有系统集成
- ✅ 自动处理消息
- ✅ 不需要额外维护

**需要做的：**
1. 创建 Discord Bot
2. 获取 Token
3. 配置到 OpenClaw
4. 重启服务

---

## 下一步

**请告诉我：**

1. **你有 Discord Bot Token 吗？**
   - 有 → 我帮你配置到 OpenClaw
   - 没有 → 我指导你创建

2. **你想用哪种方案？**
   - 方案1：OpenClaw 内置（推荐）
   - 方案2：独立 Python Bot
   - 方案3：Webhook

3. **需要我帮你创建 Bot 吗？**
   - 需要 → 提供详细步骤
   - 不需要 → 直接配置
