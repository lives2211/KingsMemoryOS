# OpenClaw Telegram → Discord 迁移方案

> 目标：将 Telegram 控制转换为 Discord 控制，实现频道间互相隔离

---

## 📊 当前架构分析

### Telegram 现状
- 6个 Agent：龙虾总管(main)、大饼、冰冰、姨太、Spikey、小红财
- 所有 Agent 绑定到同一个 Telegram 群组 `-1003762750497`
- 通过 `accountId` 区分不同 Bot

### 核心问题
当前配置中所有 Agent 共享同一个群组，消息会互相干扰。

---

## 🎯 Discord 隔离方案

### 方案 A：Discord Server + 多频道（推荐）

```
Discord Server (你的服务器)
├── 📋 任务派发 (只读，只有龙虾总管)
├── 💬 Agent-讨论 (全员可发言)
├── 🔧 技术频道 (姨太专属)
├── 📈 分析频道 (大饼专属)
├── ✍️ 创作频道 (冰冰专属)
├── 🔍 审计频道 (Spikey专属)
└── 📊 汇总汇报 (龙虾总管汇总)
```

### 方案 B：Discord Server + 私密线程

```
Discord Server
├── 📋 任务中心
│   ├── 线程：任务-001 (仅相关Agent可见)
│   ├── 线程：任务-002
│   └── ...
└── 📊 汇报大厅
```

---

## 🔧 具体配置步骤

### 步骤 1：创建 Discord Bot

1. 访问 https://discord.com/developers/applications
2. 创建 6 个 Application（每个 Agent 一个）
3. 获取 Bot Token
4. 邀请 Bot 加入你的 Discord Server

### 步骤 2：配置 OpenClaw

修改 `~/.openclaw/openclaw.json`：

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
          "botToken": "YOUR_MAIN_BOT_TOKEN",
          "dmPolicy": "allowlist",
          "allowFrom": ["YOUR_DISCORD_USER_ID"],
          "guilds": {
            "YOUR_GUILD_ID": {
              "channels": {
                "任务派发": {
                  "channelId": "TASK_CHANNEL_ID",
                  "requireMention": false
                },
                "汇总汇报": {
                  "channelId": "REPORT_CHANNEL_ID",
                  "requireMention": false
                }
              }
            }
          }
        },
        "daping": {
          "name": "分析师大饼",
          "botToken": "YOUR_DAPING_BOT_TOKEN",
          "dmPolicy": "allowlist",
          "allowFrom": ["YOUR_DISCORD_USER_ID"],
          "guilds": {
            "YOUR_GUILD_ID": {
              "channels": {
                "分析频道": {
                  "channelId": "ANALYSIS_CHANNEL_ID",
                  "requireMention": false
                }
              }
            }
          }
        },
        "yitai": {
          "name": "代码姨太",
          "botToken": "YOUR_YITAI_BOT_TOKEN",
          "guilds": {
            "YOUR_GUILD_ID": {
              "channels": {
                "技术频道": {
                  "channelId": "TECH_CHANNEL_ID"
                }
              }
            }
          }
        },
        "bingbing": {
          "name": "推文冰冰",
          "botToken": "YOUR_BINGBING_BOT_TOKEN",
          "guilds": {
            "YOUR_GUILD_ID": {
              "channels": {
                "创作频道": {
                  "channelId": "CONTENT_CHANNEL_ID"
                }
              }
            }
          }
        },
        "spikey": {
          "name": "审计Spikey",
          "botToken": "YOUR_SPIKEY_BOT_TOKEN",
          "guilds": {
            "YOUR_GUILD_ID": {
              "channels": {
                "审计频道": {
                  "channelId": "AUDIT_CHANNEL_ID"
                }
              }
            }
          }
        },
        "xiaohongcai": {
          "name": "小红财",
          "botToken": "YOUR_XIAOHONGCAI_BOT_TOKEN",
          "guilds": {
            "YOUR_GUILD_ID": {
              "channels": {
                "情报频道": {
                  "channelId": "INTEL_CHANNEL_ID"
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

### 步骤 3：更新 plugins 配置

```json
{
  "plugins": {
    "allow": [
      "memory-lancedb-pro",
      "discord"
    ],
    "entries": {
      "discord": {
        "enabled": true
      },
      "telegram": {
        "enabled": false
      }
    }
  }
}
```

---

## 🛡️ 频道隔离机制

### 隔离策略

| Agent | 专属频道 | 可见范围 | 功能 |
|-------|---------|---------|------|
| 龙虾总管 | 任务派发、汇总汇报 | 所有频道只读 | 任务分发、结果汇总 |
| 大饼 | 分析频道 | 仅自己和龙虾 | 市场分析、数据研究 |
| 姨太 | 技术频道 | 仅自己和龙虾 | 编程、脚本开发 |
| 冰冰 | 创作频道 | 仅自己和龙虾 | 内容创作 |
| Spikey | 审计频道 | 仅自己和龙虾 | 质量审计 |
| 小红财 | 情报频道 | 仅自己和龙虾 | 情报收集 |

### 权限矩阵

```
用户(你)
  ├── 所有频道管理员权限
  └── 可以@任何 Agent

龙虾总管
  ├── 任务派发频道：读写
  ├── 汇总汇报频道：读写
  └── 其他频道：只读（监控）

其他 Agent
  ├── 专属频道：读写
  └── 其他频道：无权限
```

---

## 🔄 工作流程示例

### 场景：派发研究任务

```
[任务派发频道]
你: @龙虾总管 让大饼研究一下 OpenClaw Discord 配置

龙虾总管: 📋 收到任务，派发中...
         @大饼 请研究 OpenClaw Discord 配置

[分析频道]
大饼: ✅ 收到任务，开始研究...
     ...（研究过程）...
     📊 研究完成，报告已生成

[汇总汇报频道]
龙虾总管: 📋 任务完成汇总
         任务：OpenClaw Discord 配置研究
         执行：大饼
         结果：已完成
         报告位置：intel/research/discord-config.md
```

---

## 📋 实施检查清单

### Phase 1: 准备工作
- [ ] 创建 Discord Server
- [ ] 创建 6 个 Discord Application
- [ ] 获取 6 个 Bot Token
- [ ] 创建 6 个专属频道
- [ ] 记录所有 Channel ID

### Phase 2: 配置更新
- [ ] 备份现有 `openclaw.json`
- [ ] 修改 channels 配置
- [ ] 修改 bindings 配置
- [ ] 更新 plugins 配置
- [ ] 验证配置格式

### Phase 3: 测试验证
- [ ] 重启 OpenClaw Gateway
- [ ] 测试每个 Agent 响应
- [ ] 测试频道隔离效果
- [ ] 测试任务派发流程

### Phase 4: 切换
- [ ] 禁用 Telegram
- [ ] 启用 Discord
- [ ] 通知团队成员

---

## ⚠️ 注意事项

### 1. Discord 限制
- Bot 需要 `MESSAGE_CONTENT` Intent 权限
- 频道权限需要正确设置
- Webhook 可能需要额外配置

### 2. 数据迁移
- 历史消息不会自动迁移
- 建议保留 Telegram 作为备份

### 3. 成本考虑
- Discord Bot 免费
- 但消息频率有限制

---

## 🚀 快速启动脚本

```bash
#!/bin/bash
# discord-setup.sh

echo "=== OpenClaw Discord 迁移脚本 ==="

# 1. 备份配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d)

# 2. 安装 Discord 插件
openclaw plugins install discord

# 3. 验证配置
echo "请按以下步骤操作："
echo "1. 访问 https://discord.com/developers/applications"
echo "2. 创建 6 个 Bot"
echo "3. 获取 Token"
echo "4. 运行: openclaw configure"

echo "配置完成后运行: openclaw gateway restart"
```

---

## 📚 参考文档

- [OpenClaw Discord 配置文档](https://docs.openclaw.ai/channels/discord)
- [Discord Bot 开发指南](https://discord.com/developers/docs/intro)
- [Discord 权限设置](https://discord.com/developers/docs/topics/permissions)

---

*方案版本：1.0*
*创建时间：2026-03-09*
