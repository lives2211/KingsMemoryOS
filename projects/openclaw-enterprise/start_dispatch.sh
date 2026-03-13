#!/bin/bash
# OpenClaw 任务派发服务器启动脚本

cd /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise

# 检查是否已在运行
if pgrep -f "dispatch_server.py" > /dev/null; then
    echo "✅ 派发服务器已在运行"
    echo "📡 API: http://localhost:3100"
    echo "🌐 Dashboard: http://localhost:3100/dashboard.html"
    exit 0
fi

echo "🚀 启动 OpenClaw 任务派发服务器..."
nohup python3 dispatch_server.py > dispatch_server.log 2>&1 &
sleep 2

if curl -s http://localhost:3100/health > /dev/null; then
    echo "✅ 服务器启动成功！"
    echo "📡 API: http://localhost:3100"
    echo "🌐 Dashboard: http://localhost:3100/dashboard.html"
    echo "📋 查看日志: tail -f dispatch_server.log"
else
    echo "❌ 启动失败，查看日志: dispatch_server.log"
fi
