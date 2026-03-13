#!/bin/bash
# OpenClaw Multi-Agent System 启动脚本

set -e

cd "$(dirname "$0")"

echo "🦞 OpenClaw Multi-Agent System"
echo "================================"

# 检查依赖
echo "📦 检查依赖..."
python3 -c "import flask, flask_cors" 2>/dev/null || {
    echo "❌ 缺少依赖，正在安装..."
    pip3 install flask flask-cors -q
}

# 检查端口
if lsof -i :3100 > /dev/null 2>&1; then
    echo "⚠️  端口 3100 已被占用"
    echo "   尝试停止旧进程..."
    pkill -f "server_v2.py" 2>/dev/null || true
    sleep 2
fi

# 启动服务器
echo "🚀 启动服务器..."
nohup python3 server_v2.py > logs/server.log 2>&1 &

# 等待启动
echo "⏳ 等待服务器启动..."
for i in {1..10}; do
    if curl -s http://localhost:3100/health > /dev/null 2>&1; then
        echo "✅ 服务器已启动"
        break
    fi
    sleep 1
done

# 显示状态
echo ""
echo "================================"
echo "📡 API: http://localhost:3100"
echo "🌐 Dashboard: http://localhost:3100/dashboard_v2.html"
echo "📊 CLI: python3 cli.py status"
echo "================================"
echo ""

# 显示状态
python3 cli.py status 2>/dev/null || echo "⚠️  无法连接服务器"

echo ""
echo "💡 提示:"
echo "   查看日志: tail -f logs/server.log"
echo "   停止服务: pkill -f server_v2.py"
