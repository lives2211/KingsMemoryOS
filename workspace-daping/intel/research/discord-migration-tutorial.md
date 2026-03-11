# OpenClaw Telegram → Discord 详细迁移教程

> 手把手教你完成迁移，实现频道完全隔离

---

## 📋 前置准备

### 你需要准备

| 项目 | 数量 | 说明 |
|------|------|------|
| Discord 账号 | 1个 | 用于创建服务器 |
| Discord Server | 1个 | 你的 Agent 工作区 |
| Discord Bot Token | 6个 | 每个 Agent 一个 |
| OpenClaw 配置文件 | 1个 | `~/.openclaw/openclaw.json` |

---

## 第一部分：Discord 端设置

### 步骤 1：创建 Discord 服务器

1. 打开 Discord（网页版或客户端）
2. 点击左侧栏底部的 **+** 按钮
3. 选择 **"创建我的服务器"**
4. 服务器名称建议：`AI-Agent-Team`
5. 点击 **创建**

### 步骤 2：创建频道结构

在服务器中创建以下频道：

```
📋 任务派发 (text channel)
📊 汇总汇报 (text channel)
🔧 技术频道 (text channel) - 姨太专用
📈 分析频道 (text channel) - 大饼专用  
✍️ 创作频道 (text channel) - 冰冰专用
🔍 审计频道 (text channel) - Spikey专用
📰 情报频道 (text channel) - 小红财专用
💬 Agent-讨论 (text channel) - 全员讨论
```

**创建方法：**
1. 右键点击服务器名称
2. 选择 **"创建频道"**
3. 输入频道名称
4. 类型选择 **"文本频道"**
5. 点击 **创建频道**

### 步骤 3：获取频道 ID

1. 打开 Discord 用户设置（左下角齿轮图标）
2. 进入 **"高级"** 设置
3. 开启 **"开发者模式"**
4. 右键点击每个频道
5. 选择 **"复制频道 ID"**
6. 保存到文本文件备用

**记录格式：**
```
任务派发: 1234567890123456789
汇总汇报: 1234567890123456790
技术频道: 1234567890123456791
分析频道: 1234567890123456792
创作频道: 1234567890123456793
审计频道: 1234567890123456794
情报频道: 1234567890123456795
Agent-讨论: 1234567890123456796
```

### 步骤 4：获取服务器 ID

1. 右键点击服务器名称
2. 选择 **"复制服务器 ID"**
3. 保存备用

---

## 第二部分：创建 Discord Bot

### 步骤 5：创建第一个 Bot（龙虾总管）

1. 访问 https://discord.com/developers/applications
2. 点击 **"New Application"**
3. 名称填写：`龙虾总管`
4. 点击 **Create**

### 步骤 6：配置 Bot

1. 在左侧菜单点击 **"Bot"**
2. 点击 **"Add Bot"** → **"Yes, do it!"**
3. 在 **"Privileged Gateway Intents"** 部分：
   - ✅ 开启 **MESSAGE_CONTENT_INTENT**
4. 点击 **"Save Changes"**

### 步骤 7：获取 Bot Token

1. 在 Bot 页面，点击 **"Reset Token"**
2. 点击 **"Yes, do it!"**
3. **立即复制 Token**（只显示一次！）
4. 保存到安全位置

**Token 格式示例：**
```
MTI5ODc2NTQzMjEwOTg3NjU0MzIxMDk4.NzY1NDMy.xxxxxxxxxxxxxxxxxxxxxxxx
```

### 步骤 8：邀请 Bot 加入服务器

1. 在 Application 页面，点击 **"OAuth2"** → **"URL Generator"**
2. 在 **SCOPES** 部分勾选：
   - ✅ `bot`
3. 在 **BOT PERMISSIONS** 部分勾选：
   - ✅ `Send Messages`
   - ✅ `Read Message History`
   - ✅ `View Channels`
   - ✅ `Embed Links`
   - ✅ `Attach Files`
   - ✅ `Add Reactions`
   - ✅ `Use Slash Commands`
4. 复制底部生成的 URL
5. 在浏览器中打开该 URL
6. 选择你的服务器
7. 点击 **"授权"**

### 步骤 9：重复创建其他 5 个 Bot

按照步骤 5-8，创建以下 Bot：

| Bot 名称 | 对应 Agent | 用途 |
|---------|-----------|------|
| 龙虾总管 | main | 任务派发与汇总 |
| 分析师大饼 | daping | 市场分析 |
| 代码姨太 | yitai | 技术开发 |
| 推文冰冰 | bingbing | 内容创作 |
| 审计Spikey | spikey | 质量审计 |
| 小红财 | xiaohongcai | 情报收集 |

**重要：** 每个 Bot 都需要独立的 Token！

---

## 第三部分：配置频道权限

### 步骤 10：设置频道权限（关键！）

**目标：每个 Bot 只能在自己的频道发言**

#### 配置 "任务派发" 频道：

1. 右键点击 **"任务派发"** 频道
2. 选择 **"编辑频道"**
3. 点击 **"权限"** 标签
4. 点击 **"+"** 添加成员/角色
5. 选择 **"龙虾总管"** Bot
6. 设置权限：
   - ✅ 查看频道
   - ✅ 发送消息
   - ✅ 读取消息历史
   - ❌ 其他权限保持关闭
7. 点击 **保存更改**

#### 配置 "分析频道" 权限：

1. 右键点击 **"分析频道"**
2. 选择 **"编辑频道"** → **"权限"**
3. 先点击 **"@everyone"** 角色
4. 关闭 **"查看频道"** 权限
5. 点击 **"+"** 添加成员
6. 添加 **"分析师大饼"** Bot
7. 设置权限：
   - ✅ 查看频道
   - ✅ 发送消息
   - ✅ 读取消息历史
8. 再次点击 **"+"**
9. 添加 **"龙虾总管"** Bot
10. 设置权限：
    - ✅ 查看频道（只读）
    - ❌ 发送消息（关闭）
    - ✅ 读取消息历史
11. 点击 **保存更改**

#### 重复配置其他频道：

按照上述模式，为每个专属频道配置权限：

| 频道 | 可发言 Bot | 只读 Bot |
|------|-----------|---------|
| 技术频道 | 代码姨太 | 龙虾总管 |
| 创作频道 | 推文冰冰 | 龙虾总管 |
| 审计频道 | 审计Spikey | 龙虾总管 |
| 情报频道 | 小红财 | 龙虾总管 |

---

## 第四部分：OpenClaw 配置

### 步骤 11：备份现有配置

```bash
# 打开终端，运行以下命令
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d)

# 确认备份成功
ls -la ~/.openclaw/openclaw.json.backup.*
```

### 步骤 12：编辑配置文件

```bash
# 使用你喜欢的编辑器打开配置文件
nano ~/.openclaw/openclaw.json
# 或
vim ~/.openclaw/openclaw.json
```

### 步骤 13：修改 channels 部分

找到 `channels` 部分，替换为以下内容：

```json
{
  "channels": {
    "telegram": {
      "enabled": false
    },
    "discord": {
      "enabled": true,
      "accounts": {
        "default": {
          "name": "龙虾总管",
          "botToken": "YOUR_MAIN_BOT_TOKEN_HERE",
          "dmPolicy": "allowlist",
          "allowFrom": ["YOUR_DISCORD_USER_ID"],
          "guilds": {
            "YOUR_GUILD_ID_HERE": {
              "channels": {
                "任务派发": {
                  "channelId": "TASK_CHANNEL_ID_HERE",
                  "requireMention": false
                },
                "汇总汇报": {
                  "channelId": "REPORT_CHANNEL_ID_HERE",
                  "requireMention": false
                }
              }
            }
          }
        },
        "daping": {
          "name": "分析师大饼",
          "botToken": "YOUR_DAPING_BOT_TOKEN_HERE",
          "dmPolicy": "allowlist",
          "allowFrom": ["YOUR_DISCORD_USER_ID"],
          "guilds": {
            "YOUR_GUILD_ID_HERE": {
              "channels": {
                "分析频道": {
                  "channelId": "ANALYSIS_CHANNEL_ID_HERE",
                  "requireMention": false
                }
              }
            }
          }
        },
        "yitai": {
          "name": "代码姨太",
          "botToken": "YOUR_YITAI_BOT_TOKEN_HERE",
          "dmPolicy": "allowlist",
          "allowFrom": ["YOUR_DISCORD_USER_ID"],
          "guilds": {
            "YOUR_GUILD_ID_HERE": {
              "channels": {
                "技术频道": {
                  "channelId": "TECH_CHANNEL_ID_HERE",
                  "requireMention": false
                }
              }
            }
          }
        },
        "bingbing": {
          "name": "推文冰冰",
          "botToken": "YOUR_BINGBING_BOT_TOKEN_HERE",
          "dmPolicy": "allowlist",
          "allowFrom": ["YOUR_DISCORD_USER_ID"],
          "guilds": {
            "YOUR_GUILD_ID_HERE": {
              "channels": {
                "创作频道": {
                  "channelId": "CONTENT_CHANNEL_ID_HERE",
                  "requireMention": false
                }
              }
            }
          }
        },
        "spikey": {
          "name": "审计Spikey",
          "botToken": "YOUR_SPIKEY_BOT_TOKEN_HERE",
          "dmPolicy": "allowlist",
          "allowFrom": ["YOUR_DISCORD_USER_ID"],
          "guilds": {
            "YOUR_GUILD_ID_HERE": {
              "channels": {
                "审计频道": {
                  "channelId": "AUDIT_CHANNEL_ID_HERE",
                  "requireMention": false
                }
              }
            }
          }
        },
        "xiaohongcai": {
          "name": "小红财",
          "botToken": "YOUR_XIAOHONGCAI_BOT_TOKEN_HERE",
          "dmPolicy": "allowlist",
          "allowFrom": ["YOUR_DISCORD_USER_ID"],
          "guilds": {
            "YOUR_GUILD_ID_HERE": {
              "channels": {
                "情报频道": {
                  "channelId": "INTEL_CHANNEL_ID_HERE",
                  "requireMention": false
                }
              }
            }
          }
        }
      }
    }
  }
}
```

**替换所有占位符：**
- `YOUR_MAIN_BOT_TOKEN_HERE` → 龙虾总管 Bot Token
- `YOUR_DAPING_BOT_TOKEN_HERE` → 大饼 Bot Token
- ...以此类推
- `YOUR_DISCORD_USER_ID` → 你的 Discord 用户 ID
- `YOUR_GUILD_ID_HERE` → 服务器 ID
- `TASK_CHANNEL_ID_HERE` → 任务派发频道 ID
- ...以此类推

### 步骤 14：修改 bindings 部分

找到 `bindings` 部分，替换为：

```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "discord",
        "accountId": "default"
      }
    },
    {
      "agentId": "daping",
      "match": {
        "channel": "discord",
        "accountId": "daping"
      }
    },
    {
      "agentId": "yitai",
      "match": {
        "channel": "discord",
        "accountId": "yitai"
      }
    },
    {
      "agentId": "bingbing",
      "match": {
        "channel": "discord",
        "accountId": "bingbing"
      }
    },
    {
      "agentId": "spikey",
      "match": {
        "channel": "discord",
        "accountId": "spikey"
      }
    },
    {
      "agentId": "xiaohongcai",
      "match": {
        "channel": "discord",
        "accountId": "xiaohongcai"
      }
    }
  ]
}
```

### 步骤 15：修改 plugins 部分

找到 `plugins` 部分，修改为：

```json
{
  "plugins": {
    "allow": [
      "memory-lancedb-pro",
      "discord"
    ],
    "load": {
      "paths": [
        "/home/fengxueda/plugins/memory-lancedb-pro"
      ]
    },
    "slots": {
      "memory": "memory-lancedb-pro"
    },
    "entries": {
      "discord": {
        "enabled": true
      },
      "telegram": {
        "enabled": false
      },
      "memory-lancedb-pro": {
        "enabled": true,
        "config": {
          "embedding": {
            "apiKey": "YOUR_JINA_API_KEY",
            "model": "jina-embeddings-v5-text-small",
            "baseURL": "https://api.jina.ai/v1",
            "dimensions": 1024,
            "taskQuery": "retrieval.query",
            "taskPassage": "retrieval.passage",
            "normalized": true
          }
        }
      }
    }
  }
}
```

### 步骤 16：验证配置格式

```bash
# 验证 JSON 格式是否正确
openclaw config validate

# 如果显示 "valid": true，则配置正确
```

---

## 第五部分：启动与测试

### 步骤 17：安装 Discord 插件

```bash
# 安装 Discord 插件
openclaw plugins install discord

# 等待安装完成
```

### 步骤 18：重启 Gateway

```bash
# 重启 OpenClaw Gateway
openclaw gateway restart

# 或完全重启
openclaw restart
```

### 步骤 19：验证 Bot 状态

```bash
# 检查状态
openclaw status

# 应该看到 Discord 频道已启用
```

### 步骤 20：测试每个 Bot

在 Discord 中测试：

1. 进入 **"任务派发"** 频道
2. 输入：`@龙虾总管 测试连接`
3. 应该收到回复

4. 进入 **"分析频道"**
5. 输入：`@分析师大饼 测试连接`
6. 应该收到回复

7. 重复测试其他频道...

### 步骤 21：测试频道隔离

**测试 1：跨频道隔离**
1. 在 **"分析频道"** 输入：`@代码姨太 你能看到吗？`
2. 姨太 Bot **不应该** 回复（因为它只能看到技术频道）

**测试 2：龙虾总管监控**
1. 在 **"技术频道"** 让姨太执行一个任务
2. 龙虾总管应该能在 **"汇总汇报"** 看到汇总

---

## 第六部分：工作流程

### 新的工作流程

```
你（用户）
  ↓
在"任务派发"频道 @龙虾总管
  ↓
龙虾总管接收任务
  ↓
龙虾总管在对应频道 @相关Agent
  ↓
Agent 在专属频道工作
  ↓
Agent 完成后向龙虾总管汇报
  ↓
龙虾总管在"汇总汇报"频道汇总结果
```

### 示例场景

**场景：让大饼做市场研究**

```
[任务派发频道]
你: @龙虾总管 让大饼研究一下 Bitcoin 最新趋势

龙虾总管: 📋 收到任务
         任务：Bitcoin 趋势研究
         派发对象：@分析师大饼
         
[分析频道]
龙虾总管: @分析师大饼 请研究 Bitcoin 最新趋势

大饼: ✅ 收到任务，开始研究...
      ...（研究过程）...
      📊 研究完成
      关键发现：...
      报告已保存至：intel/market/bitcoin-analysis.md

[汇总汇报频道]
龙虾总管: 📊 任务完成报告
         ─────────────────
         任务：Bitcoin 趋势研究
         执行：分析师大饼
         状态：✅ 完成
         耗时：15分钟
         报告：intel/market/bitcoin-analysis.md
         关键结论：...
```

---

## 🛠️ 故障排除

### 问题 1：Bot 不响应

**检查清单：**
- [ ] Bot Token 是否正确
- [ ] Bot 是否已加入服务器
- [ ] 频道权限是否正确设置
- [ ] Gateway 是否已重启

**诊断命令：**
```bash
openclaw status
openclaw logs --follow
```

### 问题 2：配置验证失败

**常见错误：**
```bash
# JSON 格式错误
openclaw config validate

# 查看具体错误位置
openclaw config get --raw | jq
```

### 问题 3：权限错误

**Discord 权限问题：**
1. 检查 Bot 是否有 `MESSAGE_CONTENT` Intent
2. 检查频道权限是否设置正确
3. 检查 Bot 是否有 `View Channel` 权限

---

## 📎 附录：完整配置示例

### 最小可用配置

```json
{
  "channels": {
    "telegram": {
      "enabled": false
    },
    "discord": {
      "enabled": true,
      "accounts": {
        "default": {
          "name": "龙虾总管",
          "botToken": "MTI5ODc2...",
          "dmPolicy": "allowlist",
          "allowFrom": ["123456789012345678"],
          "guilds": {
            "987654321098765432": {
              "channels": {
                "任务派发": {
                  "channelId": "111111111111111111",
                  "requireMention": false
                }
              }
            }
          }
        }
      }
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "discord",
        "accountId": "default"
      }
    }
  ],
  "plugins": {
    "allow": ["discord"],
    "entries": {
      "discord": {
        "enabled": true
      }
    }
  }
}
```

---

## ✅ 完成检查清单

### Discord 端
- [ ] 创建了 Discord 服务器
- [ ] 创建了 7 个频道
- [ ] 获取了所有频道 ID
- [ ] 获取了服务器 ID
- [ ] 创建了 6 个 Discord Application
- [ ] 获取了 6 个 Bot Token
- [ ] 所有 Bot 已加入服务器
- [ ] 设置了频道权限

### OpenClaw 端
- [ ] 备份了原配置
- [ ] 修改了 channels 配置
- [ ] 修改了 bindings 配置
- [ ] 修改了 plugins 配置
- [ ] 验证了配置格式
- [ ] 安装了 Discord 插件
- [ ] 重启了 Gateway

### 测试验证
- [ ] 龙虾总管响应正常
- [ ] 大饼响应正常
- [ ] 姨太响应正常
- [ ] 冰冰响应正常
- [ ] Spikey 响应正常
- [ ] 小红财响应正常
- [ ] 频道隔离生效
- [ ] 任务派发流程正常

---

## 📞 需要帮助？

如果遇到问题：
1. 检查 `openclaw status` 输出
2. 查看日志：`openclaw logs --follow`
3. 验证配置：`openclaw config validate`
4. 参考文档：https://docs.openclaw.ai

---

*教程版本：1.0*
*最后更新：2026-03-09*
