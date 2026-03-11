#!/usr/bin/env python3
"""
立即发布 - 跳过随机延迟
"""

import sys
sys.path.insert(0, '/home/fengxueda/.openclaw/workspace')

from skill_kol_publisher import SkillKOLPublisher

publisher = SkillKOLPublisher()

# 选择 Skill
skill = publisher.select_skill()
print(f"🎯 今日 Skill: {skill}")

# 生成推文
print("📝 生成 KOL 风格推文...")
tweets = publisher.analyzer.generate_kol_thread(skill)
print(f"✅ 生成 {len(tweets)} 条推文")

# 显示预览
print(f"\n{'='*60}")
print("预览:")
print(f"{'='*60}\n")
for i, tweet in enumerate(tweets, 1):
    print(f"推文 {i}:")
    print(tweet[:150] + "..." if len(tweet) > 150 else tweet)
    print()

# 立即发布
print("📤 立即发布...")
response = input("确认发布? (y/n): ")

if response.lower() == 'y':
    if publisher.post_thread(tweets):
        publisher.published_skills.append(skill)
        publisher._save_history()
        print(f"✅ {skill} 已记录")
    else:
        print("❌ 发布失败")
else:
    print("⏸️ 已取消")
