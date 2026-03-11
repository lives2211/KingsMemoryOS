# 小红书AI矩阵账号配置

## 🛠️ 运营工具栈

| 工具 | 功能 | 路径 |
|------|------|------|
| Auto-Redbook-Skills | AI写笔记 + 封面生成 | `~/Auto-Redbook-Skills/` |
| xiaohongshu-ops-skill | 自动发布 + 评论回复 | `~/xiaohongshu-ops-skill/` |
| union-search-skill | 全网搜索 + 热点追踪 | `~/union-search-skill/` |

## 账号矩阵规划

| 账号 | 定位 | 内容方向 | 发布频率 |
|------|------|----------|----------|
| AI工具侠 | AI工具测评 | 实测推荐、避坑指南 | 每日1-2篇 |
| AI情报局 | AI资讯解读 | 前沿动态、行业分析 | 每日2-3篇 |
| AI学习日记 | AI学习教程 | 零基础教学、实战案例 | 每日1篇 |
| AI搞钱笔记 | AI副业变现 | 搞钱案例、项目拆解 | 每周3-4篇 |

## 文件结构
```
xiaohongshu-accounts/
├── README.md                 # 本文件
├── persona-ai-tools.md       # AI工具测评号人设
├── persona-ai-news.md        # AI资讯解读号人设
├── persona-ai-learning.md    # AI学习教程号人设
├── persona-ai-money.md       # AI搞钱副业号人设
├── cookies/                  # 各账号Cookie (gitignore)
│   ├── account-tools.env
│   ├── account-news.env
│   ├── account-learning.env
│   └── account-money.env
└── content/                  # 内容产出目录
    ├── tools/
    ├── news/
    ├── learning/
    └── money/
```

## 🔍 热点追踪工作流（union-search-skill）

### 每日热点扫描
```bash
cd ~/union-search-skill

# 1. 搜AI最新动态（多平台聚合）
python3 union_search_cli.py search "AI artificial intelligence" --group social --limit 5 --pretty

# 2. 搜小红书热门话题
python3 union_search_cli.py platform xiaohongshu "AI工具" --limit 10

# 3. 搜抖音热门视频
python3 union_search_cli.py platform douyin "人工智能" --limit 5

# 4. 搜知乎热门讨论
python3 union_search_cli.py platform zhihu "AI副业" --limit 5
```

### 竞品分析
```bash
# 搜GitHub热门AI项目（找灵感）
python3 union_search_cli.py github "AI agent" --limit 10

# 搜Twitter AI话题
python3 union_search_cli.py twitter "#AI" --limit 10

# 搜B站AI视频
python3 union_search_cli.py bilibili "AI教程" --limit 5
```

### 内容素材收集
```bash
# 图片搜索（做封面用）
python3 union_search_cli.py image "AI technology" --platforms pixabay pexels --limit 10 --output-dir ./images

# RSS订阅聚合
python3 union_search_cli.py rss "artificial intelligence" --limit 10
```

---

## 使用流程

### 1. 获取Cookie
- 浏览器登录小红书
- F12 → Network → 任意请求 → 复制Cookie
- 保存到对应账号的.env文件

### 2. 生成内容
```bash
# AI工具测评
python scripts/render_xhs.py content/tools/post.md -t professional -m auto-split

# AI资讯
python scripts/render_xhs.py content/news/post.md -t terminal -m auto-split

# AI学习
python scripts/render_xhs.py content/learning/post.md -t playful-geometric -m auto-split

# AI搞钱
python scripts/render_xhs.py content/money/post.md -t neo-brutalism -m auto-split
```

### 3. 发布内容
```bash
python scripts/publish_xhs.py \
  --title "笔记标题" \
  --desc "笔记正文" \
  --images cover.png card_1.png card_2.png
```

## 主题配色建议

| 账号 | 推荐主题 | 原因 |
|------|----------|------|
| AI工具侠 | professional | 专业、可信 |
| AI情报局 | terminal | 科技感、信息感 |
| AI学习日记 | playful-geometric | 活泼、易亲近 |
| AI搞钱笔记 | neo-brutalism | 醒目、有冲击力 |

## 注意事项

1. **Cookie安全**: 不要提交到Git，定期更新
2. **发布频率**: 每个账号每天不超过5篇，避免风控
3. **内容原创**: AI生成内容需人工审核后再发布
4. **评论互动**: 每天至少回复10条评论，保持活跃
5. **数据监控**: 记录每篇笔记的赞藏评数据
