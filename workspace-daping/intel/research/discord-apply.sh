#!/bin/bash
# Discord 配置快速应用脚本
# 使用方法: ./discord-apply.sh

echo "=========================================="
echo "OpenClaw Discord 配置应用工具"
echo "=========================================="
echo ""

CONFIG_FILE="/media/fengxueda/D/openclaw-data/workspace/workspace-daping/intel/research/discord-final-config.json"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 错误: 配置文件不存在"
    echo "请确保 discord-final-config.json 在当前目录"
    exit 1
fi

# 备份现有配置
echo "📦 备份现有配置..."
BACKUP_FILE="$OPENCLAW_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
cp "$OPENCLAW_CONFIG" "$BACKUP_FILE"
echo "✅ 备份完成: $BACKUP_FILE"
echo ""

# 检查 jq 是否安装
if ! command -v jq &> /dev/null; then
    echo "⚠️ 警告: 未安装 jq，将使用基础合并方式"
    echo "建议安装 jq: sudo apt-get install jq"
    USE_JQ=false
else
    USE_JQ=true
fi

echo "🔧 合并配置..."

if [ "$USE_JQ" = true ]; then
    # 使用 jq 精确合并
    # 保留原有配置，只更新 channels 和 bindings
    jq -s '
        .[0] as $original |
        .[1] as $discord |
        $original |
        .channels.telegram = $discord.channels.telegram |
        .channels.discord = $discord.channels.discord |
        .bindings = $discord.bindings
    ' "$OPENCLAW_CONFIG" "$CONFIG_FILE" > "${OPENCLAW_CONFIG}.tmp"
    
    if [ $? -eq 0 ]; then
        mv "${OPENCLAW_CONFIG}.tmp" "$OPENCLAW_CONFIG"
        echo "✅ 配置合并成功"
    else
        echo "❌ 配置合并失败"
        rm -f "${OPENCLAW_CONFIG}.tmp"
        exit 1
    fi
else
    # 基础方式：提示手动操作
    echo "⚠️ 请手动合并配置:"
    echo "1. 打开: $OPENCLAW_CONFIG"
    echo "2. 替换 channels 部分为:"
    cat "$CONFIG_FILE" | grep -A 200 '"channels"'
    echo ""
    echo "或运行: openclaw config patch $CONFIG_FILE"
    exit 0
fi

echo ""
echo "🔍 验证配置格式..."
if openclaw config validate > /dev/null 2>&1; then
    echo "✅ 配置格式正确"
else
    echo "❌ 配置验证失败，正在恢复备份..."
    cp "$BACKUP_FILE" "$OPENCLAW_CONFIG"
    echo "✅ 已恢复原配置"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 配置应用成功！"
echo "=========================================="
echo ""
echo "下一步操作："
echo ""
echo "1️⃣  替换 Bot Tokens"
echo "   编辑: $OPENCLAW_CONFIG"
echo "   将 YOUR_*_BOT_TOKEN 替换为实际的 Discord Bot Token"
echo ""
echo "2️⃣  安装 Discord 插件"
echo "   openclaw plugins install discord"
echo ""
echo "3️⃣  重启 Gateway"
echo "   openclaw gateway restart"
echo ""
echo "4️⃣  验证状态"
echo "   openclaw status"
echo ""
echo "📋 频道映射："
echo "   总频道:       1480388799589515446 (你在这里发命令)"
echo "   龙虾总管:     1480409331659968624"
echo "   大饼:         1480409519304609894"
echo "   冰冰:         1480409628214034503"
echo "   姨太:         1480409693469020292"
echo "   Spikey:       1480409775320600670"
echo "   小红财:       1480409885119348867"
echo ""
echo "⚠️  重要：在 Discord 中设置频道权限！"
echo "   每个 Bot 只能在自己的频道发言"
echo ""
