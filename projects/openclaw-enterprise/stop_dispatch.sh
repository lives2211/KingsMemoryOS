#!/bin/bash
# 停止派发服务器

pkill -f "dispatch_server.py" 2>/dev/null
echo "🛑 派发服务器已停止"
