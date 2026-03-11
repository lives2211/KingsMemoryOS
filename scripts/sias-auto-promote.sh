#!/bin/bash
# SIAS 自动 Promotion 脚本 (简化版)

WORKSPACE="${HOME}/.openclaw/workspace"
LEARNINGS_DIR="${WORKSPACE}/.learnings"
MEMORY_FILE="${WORKSPACE}/MEMORY.md"
DATE=$(date +%Y-%m-%d)

echo "=== SIAS Auto-Promote (${DATE}) ==="

promoted=0

# 遍历所有学习文件
for file in "${LEARNINGS_DIR}"/*.md; do
    [[ -f "$file" ]] || continue
    
    filename=$(basename "$file")
    echo ""
    echo "Checking: $filename"
    
    # 提取所有 active 且 critical 的条目
    while IFS= read -r line; do
        if [[ "$line" =~ ^##\ \[(LRN|ERR|COR|FEAT)-[0-9]+-[0-9]+\] ]]; then
            id="${BASH_REMATCH[0]}"
            id=$(echo "$id" | sed 's/## \[//' | sed 's/\].*//')
            
            # 读取接下来的几行检查 priority
            priority=""
            status=""
            
            # 使用 grep 查找 Priority 和 Status
            priority=$(grep -A 3 "## \[$id\]" "$file" | grep "Priority" | grep -o "critical\|high\|medium\|low" || echo "")
            status=$(grep -A 3 "## \[$id\]" "$file" | grep "Status" | grep -o "active\|archived\|resolved" || echo "")
            
            # 只处理 active + critical
            if [[ "$status" == "active" ]] && [[ "$priority" == "critical" ]]; then
                echo "  Found CRITICAL: $id"
                
                # 检查是否已在 MEMORY.md
                if ! grep -q "$id" "$MEMORY_FILE" 2>/dev/null; then
                    echo "  -> Promoting to MEMORY.md"
                    
                    # 提取标题
                    title=$(grep "## \[$id\]" "$file" | sed 's/## \[.*\] //')
                    
                    # 添加到 MEMORY.md
                    {
                        echo ""
                        echo "## [$id] $title"
                        echo "- **Priority**: critical"
                        echo "- **Promoted**: $DATE"
                        echo "- **Source**: $filename"
                    } >> "$MEMORY_FILE"
                    
                    # 标记为 archived
                    sed -i "/## \[$id\]/,/- \*\*Status\*\*:/s/Status: active/Status: archived/" "$file"
                    
                    ((promoted++))
                else
                    echo "  -> Already in MEMORY.md"
                fi
            fi
        fi
    done < "$file"
done

echo ""
echo "=== Result ==="
if [[ $promoted -gt 0 ]]; then
    echo "✅ Promoted $promoted entries"
else
    echo "ℹ️  No critical entries to promote"
fi
