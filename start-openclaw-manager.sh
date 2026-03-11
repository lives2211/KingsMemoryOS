#!/bin/bash
# OpenClaw Manager 启动脚本
# 配置环境变量使其连接到本地 OpenClaw

export OPENCLAW_DATA_DIR="$HOME/.openclaw"
export OPENCLAW_GATEWAY_URL="http://localhost:18789"
export OPENCLAW_MODE="local"

# 启动 OpenClaw Manager AppImage
exec "$HOME/.openclaw/workspace/OpenClaw.Manager_0.0.7_amd64.AppImage"
