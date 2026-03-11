# 小红书AI矩阵 - 每日运营工作流

## 🌅 早间流程 (8:00-9:00)

### 1. 热点扫描
```bash
cd ~/union-search-skill

# AI圈最新动态
python3 union_search_cli.py search "AI news today" --group social --limit 5

# 小红书热门话题
python3 union_search_cli.py platform xiaohongshu "AI" --limit 10

# 知乎热门讨论
python3 union_search_cli.py platform zhihu "人工智能" --limit 5
```

### 2. 竞品监控
```bash
# 搜同类账号最新内容
python3 union_search_cli.py platform xiaohongshu "AI工具推荐" --limit 10
python3 union_search_cli.py platform xiaohongshu "AI搞钱" --limit 10
```

### 3. 选题确定
根据搜索结果，确定今日发布计划：
- AI工具侠：1篇工具测评
- AI情报局：2-3篇资讯解读
- AI学习日记：1篇教程
- AI搞钱笔记：1篇案例（隔天发）

---

## 📝 内容生产 (9:00-12:00)

### 步骤1：AI写内容
根据选题用Claude/OpenClaw生成笔记文案

### 步骤2：生成封面
```bash
cd ~/Auto-Redbook-Skills

# AI工具侠 - professional主题
python3 scripts/render_xhs.py content/tools/post.md -t professional -m auto-split

# AI情报局 - terminal主题
python3 scripts/render_xhs.py content/news/post.md -t terminal -m auto-split

# AI学习日记 - playful-geometric主题
python3 scripts/render_xhs.py content/learning/post.md -t playful-geometric -m auto-split

# AI搞钱笔记 - neo-brutalism主题
python3 scripts/render_xhs.py content/money/post.md -t neo-brutalism -m auto-split
```

### 步骤3：人工审核
- 检查文案是否自然
- 确认封面无错别字
- 核实数据/事实准确性

---

## 🚀 发布运营 (14:00-16:00)

### 批量发布
```bash
cd ~/Auto-Redbook-Skills

# 发布到对应账号
python3 scripts/publish_xhs.py \
  --title "标题" \
  --desc "正文内容" \
  --images cover.png card_1.png
```

### 发布节奏
| 时间 | 账号 | 内容类型 |
|------|------|----------|
| 14:00 | AI情报局 | 午间资讯快讯 |
| 15:00 | AI工具侠 | 工具测评 |
| 16:00 | AI学习日记 | 教程分享 |
| 20:00 | AI情报局 | 深度分析 |
| 21:00 | AI搞钱笔记 | 副业案例（隔天） |

---

## 💬 互动回复 (20:00-21:00)

```bash
cd ~/xiaohongshu-ops-skill

# 检查并回复评论
# 使用对应账号的persona配置
```

回复原则：
- 每条评论都回复（前10条）
- 按人设语气回复
- 引导关注/点赞/收藏

---

## 📊 数据复盘 (每周日晚)

### 数据记录
记录每个账号本周数据：
- 发布笔记数
- 总阅读量
- 总点赞数
- 总收藏数
- 新增粉丝数

### 爆款分析
```bash
# 搜本周爆款话题
python3 union_search_cli.py search "AI trending" --group social --limit 20

# 分析竞品爆款
python3 union_search_cli.py platform xiaohongshu "AI爆款" --limit 10
```

### 优化调整
- 分析哪种内容表现最好
- 调整下周选题方向
- 优化发布时间点

---

## 🔄 自动化脚本

### 一键热点追踪
```bash
#!/bin/bash
# daily-hot-topics.sh

cd ~/union-search-skill

echo "=== AI圈热点 ==="
python3 union_search_cli.py search "AI news" --limit 5 --format text

echo "=== 小红书热门 ==="
python3 union_search_cli.py platform xiaohongshu "AI" --limit 5 --format text

echo "=== 知乎讨论 ==="
python3 union_search_cli.py platform zhihu "人工智能" --limit 5 --format text
```

### 定时任务建议
```bash
# 每天早上8点扫描热点
0 8 * * * cd ~/xiaohongshu-accounts && ./daily-hot-topics.sh >> logs/hot-topics-$(date +\%Y\%m\%d).log

# 每天晚上10点备份数据
0 22 * * * cd ~/xiaohongshu-accounts && python3 backup-data.py
```

---

## ⚠️ 风控注意事项

1. **发布频率**：每个账号每天≤5篇，间隔≥2小时
2. **内容原创**：AI生成内容必须人工审核
3. **评论互动**：每天至少回复10条，保持活跃
4. **Cookie更新**：每周检查一次Cookie是否过期
5. **IP稳定**：尽量固定网络环境，避免频繁切换
