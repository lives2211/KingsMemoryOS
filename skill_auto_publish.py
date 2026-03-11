#!/usr/bin/env python3
"""
自动发布 - 无需确认
"""

import sys
sys.path.insert(0, '/home/fengxueda/.openclaw/workspace')

from skill_kol_publisher import SkillKOLPublisher
import time

publisher = SkillKOLPublisher()

# 选择 Skill
skill = publisher.select_skill()
publisher._log(f"🎯 今日 Skill: {skill}")

# 生成推文
publisher._log("📝 生成 KOL 风格推文...")
tweets = publisher.analyzer.generate_kol_thread(skill)
publisher._log(f"✅ 生成 {len(tweets)} 条推文")

# 立即发布
publisher._log("📤 开始发布...")
if publisher.post_thread(tweets):
    publisher.published_skills.append(skill)
    publisher._save_history()
    publisher._log(f"✅ {skill} 发布完成并已记录")
else:
    publisher._log(f"❌ 发布失败")
