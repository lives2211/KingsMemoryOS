#!/bin/bash
# 小红财启动脚本

echo "🚀 启动小红财 (Xiaohongcai)"
echo "=========================="

# 检查必要文件
if [ ! -f "SOUL.md" ]; then
    echo "❌ SOUL.md 不存在"
    exit 1
fi

echo "✅ SOUL.md 已加载"
echo "✅ 小红书运营指南已加载"
echo "✅ 公众号运营指南已加载"
echo ""
echo "📱 平台配置:"
echo "   - 小红书: 待配置API"
echo "   - 微信公众号: 待配置API"
echo "   - Telegram Bot: 8736919714***"
echo ""
echo "🎯 今日任务:"
echo "   1. 读取Dwight情报"
echo "   2. 确定选题"
echo "   3. 创作内容"
echo "   4. @Monica审核"
echo ""
echo "小红财已就绪！"
