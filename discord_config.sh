#!/bin/bash
# Discord Webhook 配置脚本

echo "🤖 Discord Webhook 配置"
echo "========================"
echo ""
echo "步骤："
echo "1. 打开 Discord 服务器"
echo "2. 进入你想推送的频道"
echo "3. 点击频道设置（齿轮图标）"
echo "4. 选择 '集成' -> 'Webhooks'"
echo "5. 点击 '新建 Webhook'"
echo "6. 复制 Webhook URL"
echo ""
echo "Webhook URL 格式如下："
echo "https://discord.com/api/webhooks/WEBHOOK_ID/WEBHOOK_TOKEN"
echo ""

# 检查是否已有配置
CONFIG_FILE="/home/fengxueda/.openclaw/workspace/.env.discord"

if [ -f "$CONFIG_FILE" ]; then
    echo "✅ 已有配置文件: $CONFIG_FILE"
    echo ""
    read -p "是否更新配置? (y/n): " update
    if [ "$update" != "y" ]; then
        echo "保持现有配置"
        exit 0
    fi
fi

read -p "请输入 Discord Webhook URL: " webhook_url

if [ -z "$webhook_url" ]; then
    echo "❌ Webhook URL 不能为空"
    exit 1
fi

# 验证 URL 格式
if [[ ! "$webhook_url" =~ ^https://discord.com/api/webhooks/ ]]; then
    echo "⚠️ URL 格式可能不正确，但已保存"
fi

# 保存配置
echo "DISCORD_WEBHOOK_URL=$webhook_url" > "$CONFIG_FILE"
chmod 600 "$CONFIG_FILE"

echo ""
echo "✅ 配置已保存到: $CONFIG_FILE"
echo ""
echo "测试推送..."

# 发送测试消息
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"content":"🤖 Twitter 新闻机器人已配置成功！\n每小时自动推送最新推文。"}' \
    "$webhook_url"

echo ""
echo "✅ 测试完成！"
