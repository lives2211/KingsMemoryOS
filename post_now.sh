#!/bin/bash
# 立即发布（跳过延迟）

cd /home/fengxueda/.openclaw/workspace

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🚀 立即发布模式"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ========================================"

# 发布中文区 Skill（带 GitHub）
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📝 发布中文区 Skill..."
python3 china_skill_github.py 2>&1 | tee -a post_now.log

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 发布完成"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ========================================"
