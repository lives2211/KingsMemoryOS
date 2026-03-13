#!/bin/bash
# 启动真正的独立 Agent 子会话

echo "🚀 启动真正的独立 Agent..."

AGENTS=("yitai" "bingbing" "daping" "spikey")

for agent in "${AGENTS[@]}"; do
    WORKSPACE="/home/fengxueda/.openclaw/workspace-${agent}"
    
    if [ -d "$WORKSPACE" ]; then
        echo "启动 @${agent}..."
        
        # 使用 sessions_spawn 启动独立 Agent
        cd "$WORKSPACE"
        nohup openclaw sessions spawn \
            --label "${agent}" \
            --mode session \
            --cwd "$WORKSPACE" \
            > "/tmp/${agent}.log" 2>&1 &
        
        sleep 2
    else
        echo "❌ @${agent} 工作空间不存在"
    fi
done

echo "✅ Agent 启动完成"
echo "检查状态: openclaw sessions list"
