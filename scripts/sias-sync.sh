#!/bin/bash
# SIAS Cross-Agent Sync - 在 Agents 间同步重要学习

WORKSPACE="${HOME}/.openclaw/workspace"
SHARED_MEMORY="${WORKSPACE}/memory/shared"
DATE=$(date +%Y-%m-%d)

echo "=== SIAS Cross-Agent Sync (${DATE}) ==="

# 确保共享目录存在
mkdir -p "${SHARED_MEMORY}"

# 收集所有 Agents 的 critical 学习
echo "Collecting critical learnings from all agents..."

critical_learnings=""

# 主 Agent
if [[ -f "${WORKSPACE}/.learnings/LEARNINGS.md" ]]; then
    echo "  Checking main..."
    # 提取 critical + active 的学习
    awk '/^## \[.*\]/{entry=$0; getline; area=$0; getline; priority=$0; getline; status=$0; 
         if (priority ~ /critical/ && status ~ /active/) {
             print entry; print area; print priority; print status; print ""
         }
    }' "${WORKSPACE}/.learnings/LEARNINGS.md" >> /tmp/critical_main.txt 2>/dev/null || true
fi

# 其他 Agents
for agent in yitai bingbing daping spikey xiaohongcai; do
    agent_learnings="${WORKSPACE}/workspace-${agent}/.learnings/LEARNINGS.md"
    if [[ -f "$agent_learnings" ]]; then
        echo "  Checking ${agent}..."
        awk '/^## \[.*\]/{entry=$0; getline; area=$0; getline; priority=$0; getline; status=$0; 
             if (priority ~ /critical/ && status ~ /active/) {
                 print entry; print area; print priority; print status; print "Source: '${agent}'"; print ""
             }
        }' "$agent_learnings" >> /tmp/critical_${agent}.txt 2>/dev/null || true
    fi
done

# 合并到共享记忆
echo ""
echo "Syncing to shared memory..."

shared_file="${SHARED_MEMORY}/SIAS-sync-${DATE}.md"
{
    echo "# SIAS Cross-Agent Sync - ${DATE}"
    echo ""
    echo "## Critical Learnings from all agents"
    echo ""
} > "$shared_file"

for tmp_file in /tmp/critical_*.txt; do
    if [[ -f "$tmp_file" && -s "$tmp_file" ]]; then
        cat "$tmp_file" >> "$shared_file"
        echo "" >> "$shared_file"
        agent=$(basename "$tmp_file" .txt | sed 's/critical_//')
        echo "  Added learnings from ${agent}"
    fi
done

# 清理临时文件
rm -f /tmp/critical_*.txt

# 统计
echo ""
echo "=== Sync Complete ==="
if [[ -s "$shared_file" ]]; then
    count=$(grep -c "^## \[" "$shared_file" 2>/dev/null || echo 0)
    echo "✅ Synced $count critical learnings to:"
    echo "   ${shared_file}"
else
    echo "ℹ️  No critical learnings to sync"
    rm -f "$shared_file"
fi

echo ""
echo "Shared memory location: ${SHARED_MEMORY}/"
