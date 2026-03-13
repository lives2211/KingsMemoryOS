#!/bin/bash
# 完整工作流程
# 1. 爬取中文 KOL
# 2. 分析 Skill 文件
# 3. 生成英文推文
# 4. 发布

cd /home/fengxueda/.openclaw/workspace

echo "======================================"
echo "🚀 完整工作流程启动"
echo "======================================"

# 步骤1: 爬取中文 KOL 推文
echo ""
echo "📱 步骤1: 爬取中文 KOL 推文..."
python3 chinese_kol_crawler.py > kol_crawler_output.txt 2>&1 &
CRAWLER_PID=$!

# 等待爬取完成
sleep 120

# 检查爬取结果
if [ -f "kol_crawled_*.json" ]; then
    echo "✅ 爬取完成"
    LATEST_KOL=$(ls -t kol_crawled_*.json | head -1)
    echo "   文件: $LATEST_KOL"
else
    echo "⚠️ 爬取未完成，使用示例数据"
fi

# 步骤2: 深度分析 Skill
echo ""
echo "🔍 步骤2: 深度分析 Skill..."
python3 deep_skill_analyzer.py > skill_analyzer_output.txt 2>&1

# 检查分析结果
if [ -f "deep_english_*.json" ]; then
    echo "✅ 分析完成"
    LATEST_ENGLISH=$(ls -t deep_english_*.json | head -1)
    echo "   文件: $LATEST_ENGLISH"
else
    echo "❌ 分析失败"
    exit 1
fi

# 步骤3: 显示预览
echo ""
echo "📝 步骤3: 内容预览"
echo "======================================"
python3 << 'PYEOF'
import json
import glob

files = sorted(glob.glob('deep_english_*.json'), reverse=True)
if files:
    with open(files[0], 'r') as f:
        data = json.load(f)
    
    print(f"\n技能: {data['analysis']['display_name']}")
    print(f"推文数: {data['count']}")
    print(f"\n推文预览:\n")
    
    for i, tweet in enumerate(data['tweets'][:5], 1):
        print(f"Tweet {i} ({len(tweet)} chars):")
        print(tweet[:120] + "..." if len(tweet) > 120 else tweet)
        print()
PYEOF

echo "======================================"
echo "✅ 工作流程完成"
echo "======================================"
echo ""
echo "生成的文件:"
ls -la deep_english_*.json 2>/dev/null | head -3
echo ""
echo "要发布请运行:"
echo "  python3 publish_english_thread.py"
