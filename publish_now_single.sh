#!/bin/bash
# 立即发布单条深度分析

cd /home/fengxueda/.openclaw/workspace

echo "🚀 发布深度分析内容"
echo "===================="

# 加载最新的深度分析
LATEST=$(ls -t deep_analysis_*.json | head -1)
echo "文件: $LATEST"

# 提取第一条推文
python3 << 'PYEOF'
import json
import subprocess
import sys

with open('deep_analysis_20260312_142625.json', 'r') as f:
    data = json.load(f)

tweets = data['tweets']
source = data['source']

print(f"来源: @{source['author']}")
print(f"主题: {source.get('topic', 'AI Skill')}")
print(f"推文数: {len(tweets)}")
print()

# 发布第一条
print("发布推文 1...")
result = subprocess.run(['twitter', 'post', tweets[0]], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("错误:", result.stderr)
    sys.exit(1)

print("✅ 推文 1 发布成功")
PYEOF
