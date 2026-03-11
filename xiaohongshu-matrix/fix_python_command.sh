#!/bin/bash
# 修复小红书工具中的 python 命令为 python3

echo "=== 修复 python 命令 ==="

# 查找并替换所有使用 "python" 的地方
find ~/.openclaw/workspace/xiaohongshu-matrix -name "*.py" -type f ! -path "*/__pycache__/*" -exec grep -l '"python"' {} \; 2>/dev/null | while read file; do
    echo "修复: $file"
    sed -i 's/"python"/"python3"/g' "$file"
done

echo "✅ 修复完成"

# 验证
echo ""
echo "=== 验证修复 ==="
grep -rn '"python"' ~/.openclaw/workspace/xiaohongshu-matrix/ 2>/dev/null | grep -v __pycache__ | grep -v python3 | head -5 || echo "✅ 所有 python 已替换为 python3"
