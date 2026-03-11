#!/bin/bash
# Discord 配置生成脚本
# 使用方法：./discord-config-generator.sh

echo "=========================================="
echo "OpenClaw Discord 配置生成器"
echo "=========================================="
echo ""

# 检查 openclaw 是否安装
if ! command -v openclaw &> /dev/null; then
    echo "❌ 错误：openclaw 命令未找到"
    echo "请确保 OpenClaw 已正确安装"
    exit 1
fi

# 备份现有配置
echo "📦 步骤 1/5: 备份现有配置..."
BACKUP_FILE="$HOME/.openclaw/openclaw.json.backup.$(date +%Y%m%d_%H%M%S)"
cp "$HOME/.openclaw/openclaw.json" "$BACKUP_FILE"
echo "✅ 配置已备份到: $BACKUP_FILE"
echo ""

# 收集信息
echo "📝 步骤 2/5: 收集配置信息..."
echo "请准备好以下信息："
echo ""

read -p "你的 Discord User ID: " USER_ID
read -p "Discord Server (Guild) ID: " GUILD_ID

echo ""
echo "Bot Tokens (从 Discord Developer Portal 获取):"
read -p "龙虾总管 Bot Token: " TOKEN_MAIN
read -p "分析师大饼 Bot Token: " TOKEN_DAPING
read -p "代码姨太 Bot Token: " TOKEN_YITAI
read -p "推文冰冰 Bot Token: " TOKEN_BINGBING
read -p "审计Spikey Bot Token: " TOKEN_SPIKEY
read -p "小红财 Bot Token: " TOKEN_XIAOHONGCAI

echo ""
echo "频道 IDs (右键频道 -> 复制频道 ID):"
read -p "任务派发频道 ID: " CH_TASK
read -p "汇总汇报频道 ID: " CH_REPORT
read -p "分析频道 ID (大饼): " CH_ANALYSIS
read -p "技术频道 ID (姨太): " CH_TECH
read -p "创作频道 ID (冰冰): " CH_CONTENT
read -p "审计频道 ID (Spikey): " CH_AUDIT
read -p "情报频道 ID (小红财): " CH_INTEL

echo ""
echo "✅ 信息收集完成"
echo ""

# 生成配置
echo "⚙️ 步骤 3/5: 生成配置..."

# 创建临时配置文件
TEMP_CONFIG=$(mktemp)

cat > "$TEMP_CONFIG" << EOF
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
          "botToken": "$TOKEN_MAIN",
          "dmPolicy": "allowlist",
          "allowFrom": ["$USER_ID"],
          "guilds": {
            "$GUILD_ID": {
              "channels": {
                "任务派发": {
                  "channelId": "$CH_TASK",
                  "requireMention": false
                },
                "汇总汇报": {
                  "channelId": "$CH_REPORT",
                  "requireMention": false
                }
              }
            }
          }
        },
        "daping": {
          "name": "分析师大饼",
          "botToken": "$TOKEN_DAPING",
          "dmPolicy": "allowlist",
          "allowFrom": ["$USER_ID"],
          "guilds": {
            "$GUILD_ID": {
              "channels": {
                "分析频道": {
                  "channelId": "$CH_ANALYSIS",
                  "requireMention": false
                }
              }
            }
          }
        },
        "yitai": {
          "name": "代码姨太",
          "botToken": "$TOKEN_YITAI",
          "dmPolicy": "allowlist",
          "allowFrom": ["$USER_ID"],
          "guilds": {
            "$GUILD_ID": {
              "channels": {
                "技术频道": {
                  "channelId": "$CH_TECH",
                  "requireMention": false
                }
              }
            }
          }
        },
        "bingbing": {
          "name": "推文冰冰",
          "botToken": "$TOKEN_BINGBING",
          "dmPolicy": "allowlist",
          "allowFrom": ["$USER_ID"],
          "guilds": {
            "$GUILD_ID": {
              "channels": {
                "创作频道": {
                  "channelId": "$CH_CONTENT",
                  "requireMention": false
                }
              }
            }
          }
        },
        "spikey": {
          "name": "审计Spikey",
          "botToken": "$TOKEN_SPIKEY",
          "dmPolicy": "allowlist",
          "allowFrom": ["$USER_ID"],
          "guilds": {
            "$GUILD_ID": {
              "channels": {
                "审计频道": {
                  "channelId": "$CH_AUDIT",
                  "requireMention": false
                }
              }
            }
          }
        },
        "xiaohongcai": {
          "name": "小红财",
          "botToken": "$TOKEN_XIAOHONGCAI",
          "dmPolicy": "allowlist",
          "allowFrom": ["$USER_ID"],
          "guilds": {
            "$GUILD_ID": {
              "channels": {
                "情报频道": {
                  "channelId": "$CH_INTEL",
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
EOF

echo "✅ 配置已生成"
echo ""

# 验证 JSON 格式
echo "🔍 步骤 4/5: 验证配置格式..."
if command -v jq &> /dev/null; then
    if jq empty "$TEMP_CONFIG" 2>/dev/null; then
        echo "✅ JSON 格式正确"
    else
        echo "❌ JSON 格式错误"
        rm "$TEMP_CONFIG"
        exit 1
    fi
else
    echo "⚠️ 未安装 jq，跳过 JSON 验证"
fi
echo ""

# 应用配置
echo "💾 步骤 5/5: 应用配置..."
echo ""
echo "⚠️ 警告：这将修改你的 OpenClaw 配置！"
echo "备份文件已创建: $BACKUP_FILE"
echo ""
read -p "是否应用新配置？ (yes/no): " CONFIRM

if [ "$CONFIRM" = "yes" ] || [ "$CONFIRM" = "y" ]; then
    # 读取现有配置
    EXISTING_CONFIG="$HOME/.openclaw/openclaw.json"
    
    # 使用 jq 合并配置（如果可用）
    if command -v jq &> /dev/null; then
        # 保留原有配置，只更新 channels 和 bindings
        jq -s '.[0] * .[1]' "$EXISTING_CONFIG" "$TEMP_CONFIG" > "${EXISTING_CONFIG}.new"
        mv "${EXISTING_CONFIG}.new" "$EXISTING_CONFIG"
    else
        # 如果没有 jq，直接替换（不推荐）
        echo "⚠️ 未安装 jq，将只更新 channels 和 bindings 部分"
        echo "请手动合并配置"
        cp "$TEMP_CONFIG" "$HOME/.openclaw/discord-config.json"
        echo "新配置已保存到: $HOME/.openclaw/discord-config.json"
    fi
    
    rm "$TEMP_CONFIG"
    
    echo ""
    echo "✅ 配置已应用！"
    echo ""
    echo "下一步："
    echo "1. 安装 Discord 插件: openclaw plugins install discord"
    echo "2. 重启 Gateway: openclaw gateway restart"
    echo "3. 验证状态: openclaw status"
    echo ""
else
    echo "❌ 已取消"
    cp "$TEMP_CONFIG" "$HOME/.openclaw/discord-config-draft.json"
    echo "配置草稿已保存到: $HOME/.openclaw/discord-config-draft.json"
    rm "$TEMP_CONFIG"
fi

echo ""
echo "=========================================="
echo "配置生成完成"
echo "=========================================="
