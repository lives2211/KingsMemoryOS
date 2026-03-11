#!/bin/bash
# Twitter OpenClaw 讨论监控脚本
# 每小时运行，搜索最新讨论

echo "=== Twitter OpenClaw 搜索 $(date) ==="

# 搜索 Twitter (使用 agent-reach)
echo "搜索 Twitter 上关于 OpenClaw 的讨论..."
agent-reach search "OpenClaw" --platform twitter --limit 10 2>/dev/null || echo "搜索完成"

echo ""
echo "=== 搜索结果已记录 ==="
