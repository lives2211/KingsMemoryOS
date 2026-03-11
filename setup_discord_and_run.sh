#!/bin/bash
# Discord Webhook 配置和测试脚本

set -euo pipefail

cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║           Discord Webhook 配置工具                               ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# 检查是否已有配置
if [ -f ".env.discord" ]; then
    echo "📋 发现已有配置文件:"
    grep "DISCORD_WEBHOOK_URL" .env.discord | head -1
    echo ""
    read -p "是否重新配置? (y/n): " reconfig
    if [ "$reconfig" != "y" ]; then
        echo "使用现有配置"
        WEBHOOK_URL=$(grep "DISCORD_WEBHOOK_URL" .env.discord | cut -d'=' -f2)
    else
        WEBHOOK_URL=""
    fi
else
    WEBHOOK_URL=""
fi

# 如果没有配置，交互式输入
if [ -z "$WEBHOOK_URL" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "步骤 1: 在 Discord 中创建 Webhook"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. 打开 Discord，进入你的服务器"
    echo "2. 选择你想接收推送的频道"
    echo "3. 点击频道名称右侧的 ⚙️ 设置图标"
    echo "4. 选择「集成」→「Webhooks」"
    echo "5. 点击「新建 Webhook」"
    echo "6. 设置名称和频道，然后点击「复制 Webhook URL」"
    echo ""
    echo "URL 格式: https://discord.com/api/webhooks/数字/字符串"
    echo ""
    
    read -p "请输入 Webhook URL: " WEBHOOK_URL
    
    if [ -z "$WEBHOOK_URL" ]; then
        echo "❌ 错误: URL 不能为空"
        exit 1
    fi
    
    # 保存配置
    cat > .env.discord << EOF
# Discord Webhook 配置
# 生成时间: $(date -Iseconds)

DISCORD_WEBHOOK_URL=$WEBHOOK_URL
DISCORD_CHANNEL_NAME=twitter-news
MAX_TWEETS_PER_MESSAGE=5
ENABLE_THREADING=true
EOF
    
    chmod 600 .env.discord
    echo ""
    echo "✅ 配置已保存到 .env.discord"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "步骤 2: 测试 Webhook"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 发送测试消息
TEST_RESULT=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"content":"🤖 **Twitter 新闻推送机器人已配置成功！**\n\n✅ Webhook 连接正常\n⏰ 每小时自动推送最新推文\n📊 包含完整链接和详细内容\n\n_配置时间: '$(date '+%Y-%m-%d %H:%M:%S')'_"}' \
    "$WEBHOOK_URL" 2>&1 || echo "000")

if [ "$TEST_RESULT" = "204" ] || [ "$TEST_RESULT" = "200" ]; then
    echo "✅ Webhook 测试成功！"
    echo ""
else
    echo "❌ Webhook 测试失败 (HTTP $TEST_RESULT)"
    echo ""
    echo "可能的原因："
    echo "  • URL 复制不完整"
    echo "  • Webhook 已被删除"
    echo "  • 网络连接问题"
    echo ""
    read -p "是否继续? (y/n): " continue_anyway
    if [ "$continue_anyway" != "y" ]; then
        exit 1
    fi
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "步骤 3: 运行抓取并推送"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "是否立即运行抓取并推送到 Discord? (y/n): " run_now

if [ "$run_now" = "y" ]; then
    echo ""
    echo "🚀 正在抓取 Twitter 新闻..."
    python3 twitter_news_full.py --once --max 5 --hours 24
    
    echo ""
    echo "📤 正在推送到 Discord..."
    python3 twitter_discord_pusher.py
    
    echo ""
    echo "✅ 完成！"
else
    echo ""
    echo "📋 手动运行命令："
    echo "  抓取推文: python3 twitter_news_full.py --once --max 10"
    echo "  推送到 Discord: python3 twitter_discord_pusher.py"
    echo "  或者一次性执行: python3 twitter_news_full.py --once --max 10 && python3 twitter_discord_pusher.py"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "配置完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 配置文件: .env.discord"
echo "📝 日志文件: twitter_news.log"
echo "💾 数据文件: news_YYYYMMDD_HHMMSS.json"
echo ""
echo "定时任务设置:"
echo "  ./setup_cron.sh 60 10 1  # 每小时运行，每次10条"
echo ""
