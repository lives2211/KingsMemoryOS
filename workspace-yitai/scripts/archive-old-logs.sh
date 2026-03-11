#!/bin/bash
# 自动归档7天前的日志文件

WORKSPACE="/media/fengxueda/D/openclaw-data/workspace/workspace-yitai"
ARCHIVE_DIR="$WORKSPACE/memory/archive"
CUTOFF_DATE=$(date -d "7 days ago" +%Y-%m-%d)

echo "[$DATE] 开始归档7天前的日志..."

# 创建归档目录
mkdir -p "$ARCHIVE_DIR"

# 归档agents/*/memory/下的旧日志
for agent_dir in "$WORKSPACE"/agents/*/memory; do
    if [ -d "$agent_dir" ]; then
        agent_name=$(basename $(dirname "$agent_dir"))
        for file in "$agent_dir"/*.md; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                # 提取日期 (格式: YYYY-MM-DD.md)
                file_date=${filename%.md}
                if [[ "$file_date" < "$CUTOFF_DATE" ]]; then
                    mkdir -p "$ARCHIVE_DIR/$agent_name"
                    mv "$file" "$ARCHIVE_DIR/$agent_name/"
                    echo "已归档: $agent_name/$filename"
                fi
            fi
        done
    fi
done

# 归档intel/logs/下的旧日志
if [ -d "$WORKSPACE/intel/logs" ]; then
    for file in "$WORKSPACE/intel/logs"/*.log; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            file_date=${filename%.log}
            if [[ "$file_date" < "$CUTOFF_DATE" ]]; then
                mkdir -p "$ARCHIVE_DIR/intel-logs"
                mv "$file" "$ARCHIVE_DIR/intel-logs/"
                echo "已归档: intel-logs/$filename"
            fi
        fi
    done
fi

echo "[$DATE] 归档完成"