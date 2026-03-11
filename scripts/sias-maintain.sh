#!/bin/bash
# SIAS 维护脚本 - 自动化日常维护任务

set -e

WORKSPACE="${HOME}/.openclaw/workspace"
LEARNINGS_DIR="${WORKSPACE}/.learnings"
MEMORY_DIR="${WORKSPACE}/memory"
DATE=$(date +%Y-%m-%d)

echo "=== SIAS 日常维护 ($(date '+%Y-%m-%d %H:%M:%S')) ==="

# 1. 检查 .learnings/ 文件是否存在
echo "[1/5] 检查学习日志文件..."
for file in ERRORS.md LEARNINGS.md CORRECTIONS.md FEATURE_REQUESTS.md; do
    if [[ ! -f "${LEARNINGS_DIR}/${file}" ]]; then
        echo "  创建 ${file}..."
        echo "# ${file}" > "${LEARNINGS_DIR}/${file}"
    fi
done
echo "  ✅ 学习日志文件检查完成"

# 2. 检查今日记忆文件
echo "[2/5] 检查今日记忆文件..."
TODAY_MEMORY="${MEMORY_DIR}/${DATE}.md"
if [[ ! -f "${TODAY_MEMORY}" ]]; then
    echo "  创建 ${DATE}.md..."
    cat > "${TODAY_MEMORY}" << EOF
# ${DATE} - Daily Log

## 会话记录

## 重要决策

## 学习总结

EOF
fi
echo "  ✅ 今日记忆文件检查完成"

# 3. 统计今日学习
echo "[3/5] 统计今日学习..."
# Count entries (subtract 1 for header line)
ERRORS_COUNT=$(grep "^## \[" "${LEARNINGS_DIR}/ERRORS.md" 2>/dev/null | wc -l)
LEARNINGS_COUNT=$(grep "^## \[" "${LEARNINGS_DIR}/LEARNINGS.md" 2>/dev/null | wc -l)
CORRECTIONS_COUNT=$(grep "^## \[" "${LEARNINGS_DIR}/CORRECTIONS.md" 2>/dev/null | wc -l)
FEATURES_COUNT=$(grep "^## \[" "${LEARNINGS_DIR}/FEATURE_REQUESTS.md" 2>/dev/null | wc -l)

echo "  今日统计:"
echo "    - 错误记录: ${ERRORS_COUNT}"
echo "    - 学习记录: ${LEARNINGS_COUNT}"
echo "    - 纠正记录: ${CORRECTIONS_COUNT}"
echo "    - 功能请求: ${FEATURES_COUNT}"

# 4. 检查需要升级的知识
echo "[4/5] 检查需要升级的知识..."
# 检查是否有重复 3 次以上的学习
# 这里简化处理，实际应该解析文件内容
CRITICAL_COUNT=$(grep -h "Priority.*critical" "${LEARNINGS_DIR}"/*.md 2>/dev/null | wc -l)
if [[ ${CRITICAL_COUNT} -gt 0 ]]; then
    echo "  ⚠️ 发现 ${CRITICAL_COUNT} 个 critical 优先级学习，建议升级到 MEMORY.md"
fi
echo "  ✅ 升级检查完成"

# 5. 备份 .learnings/
echo "[5/5] 备份学习日志..."
BACKUP_DIR="${WORKSPACE}/.learnings-backup/${DATE}"
if [[ ! -d "${BACKUP_DIR}" ]]; then
    mkdir -p "${BACKUP_DIR}"
    cp "${LEARNINGS_DIR}"/*.md "${BACKUP_DIR}/"
    echo "  备份已创建: ${BACKUP_DIR}"
fi
echo "  ✅ 备份完成"

echo ""
echo "=== 维护完成 ==="
echo "建议操作:"
echo "  1. 定期回顾 .learnings/ 文件"
echo "  2. 将重要知识升级到 MEMORY.md"
echo "  3. 更新 SESSION-STATE.md"
