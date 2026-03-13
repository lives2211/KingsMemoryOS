#!/bin/bash
# 发布标准长度推文

cd /home/fengxueda/.openclaw/workspace

echo "🚀 发布深度分析 (标准长度)"
echo "============================"

python3 << 'PYEOF'
import json
import subprocess
import time
import random
from datetime import datetime

# 加载内容
with open('deep_analysis_20260312_142625.json', 'r') as f:
    data = json.load(f)

tweets = data['tweets_standard']
source = data['source']

print(f"来源: @{source['author']}")
print(f"主题: {source.get('topic', 'AI Skill')}")
print(f"推文: {len(tweets)} 条")
print(f"限制: {data.get('limit_detected', 280)} 字符")
print()

# 发布
success = 0
for i, tweet in enumerate(tweets, 1):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 推文 {i}/{len(tweets)} ({len(tweet)} 字符)")
    
    result = subprocess.run(['twitter', 'post', tweet], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 成功")
        success += 1
        try:
            d = json.loads(result.stdout)
            if d.get('ok') and d.get('data', {}).get('url'):
                print(f"🔗 {d['data']['url']}")
        except:
            pass
    else:
        print(f"❌ 失败")
        print(f"   错误: {result.stderr[:100]}")
    
    if i < len(tweets):
        delay = random.randint(180, 300)
        print(f"⏳ 等待 {delay//60} 分钟...\n")
        time.sleep(delay)

print(f"\n✅ 完成: {success}/{len(tweets)} 条成功")
PYEOF

echo "============================"
echo "✅ 发布完成"
