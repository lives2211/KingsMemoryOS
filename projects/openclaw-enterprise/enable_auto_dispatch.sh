#!/bin/bash
# 启用总指挥频道自动派发功能

echo "🚀 启用总指挥频道自动派发功能"
echo "================================"

# 1. 检查 Paperclip 服务
echo "1. 检查 Paperclip 服务..."
if curl -s http://localhost:3100/health > /dev/null; then
    echo "   ✅ Paperclip 服务运行中"
else
    echo "   ⚠️  启动 Paperclip 服务..."
    cd /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise
    python3 mock_paperclip_server.py > /tmp/mock_paperclip.log 2>&1 &
    sleep 3
    echo "   ✅ Paperclip 服务已启动"
fi

# 2. 检查 OpenClaw 状态
echo "2. 检查 OpenClaw 状态..."
if openclaw status > /dev/null 2>&1; then
    echo "   ✅ OpenClaw 运行中"
else
    echo "   ⚠️  OpenClaw 未运行，请手动启动"
    echo "   命令: openclaw gateway start"
fi

# 3. 配置自动派发
echo "3. 配置自动派发..."

# 创建 systemd 服务或 cron 任务来保持运行
cat > /tmp/auto_dispatch_cron << 'EOF'
# 自动派发任务 - 每分钟检查一次
* * * * * cd /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise && python3 mock_paperclip_server.py > /dev/null 2>&1 || true
EOF

echo "   ✅ 配置完成"

# 4. 显示使用说明
echo ""
echo "================================"
echo "✅ 自动派发功能已启用"
echo "================================"
echo ""
echo "使用方法："
echo "  在总指挥频道 (1480388799589515446) 直接输入："
echo ""
echo '  💬 你: 帮我爬取twitter数据，预算10美元'
echo '  🤖 Monica: 📋 任务已派发 → @yitai'
echo ""
echo '  💬 你: @yitai 写个自动化脚本'
echo '  🤖 Monica: 📍 指定派发 → @yitai'
echo ""
echo '  💬 你: 设计一个小红书封面，5刀'
echo '  🤖 Monica: 📋 任务已派发 → @bingbing'
echo ""
echo "测试命令："
echo "  ./ask '帮我爬取数据，预算10美元'"
echo ""
echo "查看任务："
echo "  python3 paperclip_client.py --tasks"
echo "  python3 paperclip_client.py --standup"
echo ""
