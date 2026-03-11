# Twitter 新闻聚合推送系统 - 配置指南

## 📦 系统功能

- **多源聚合**: Twitter + RSS (Hacker News, AI News 等)
- **智能去重**: 基于内容 ID 自动去重
- **时间过滤**: 只保留最近 N 小时的内容
- **互动排序**: 按点赞/转发/评论综合排序
- **定时推送**: 每小时自动推送 10-20 条
- **多格式输出**: 控制台 + Discord + JSON 文件

---

## 1️⃣ 配置 Discord 自动推送

### 步骤 1: 创建 Discord Webhook

1. 打开 Discord，进入你想推送的服务器
2. 选择目标频道，点击右侧的 ⚙️ **设置**（齿轮图标）
3. 选择 **集成** → **Webhooks**
4. 点击 **新建 Webhook**
5. 设置名称（如：Twitter-News-Bot）
6. 点击 **复制 Webhook URL**

### 步骤 2: 配置 Webhook

编辑 `.env.discord` 文件：

```bash
# 替换为你的实际 Webhook URL
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz

# 可选配置
DISCORD_CHANNEL_NAME=twitter-news
MAX_TWEETS_PER_MESSAGE=5
ENABLE_THREADING=true
```

### 步骤 3: 测试推送

```bash
# 测试 Discord 推送
python3 twitter_news_full.py --once --max 5
```

---

## 2️⃣ 添加更多数据源

### 编辑数据源配置

打开 `twitter_news_full.py`，找到 `_setup_sources` 方法：

```python
def _setup_sources(self):
    """配置数据源"""
    # Twitter
    twitter = TwitterFetcher()
    self.aggregator.add_fetcher(twitter)
    
    # RSS 源
    rss = RSSFetcher()
    
    # 添加自定义 RSS 源
    rss.add_feed("Hacker News", "https://news.ycombinator.com/rss", ["tech", "hn"])
    rss.add_feed("AI News", "https://www.artificialintelligence-news.com/feed/", ["ai"])
    rss.add_feed("MIT Tech Review", "https://www.technologyreview.com/feed/", ["tech"])
    rss.add_feed("VentureBeat AI", "https://venturebeat.com/category/ai/feed/", ["ai"])
    
    # 添加更多 RSS 源
    rss.add_feed("OpenAI Blog", "https://openai.com/blog/rss.xml", ["ai", "openai"])
    rss.add_feed("Anthropic", "https://www.anthropic.com/blog/rss.xml", ["ai", "claude"])
    rss.add_feed("Google AI", "https://ai.googleblog.com/feeds/posts/default", ["ai", "google"])
    
    self.aggregator.add_fetcher(rss)
```

### 推荐的 RSS 源

| 名称 | URL | 标签 |
|------|-----|------|
| Hacker News | https://news.ycombinator.com/rss | tech |
| AI News | https://www.artificialintelligence-news.com/feed/ | ai |
| MIT Tech Review | https://www.technologyreview.com/feed/ | tech |
| VentureBeat AI | https://venturebeat.com/category/ai/feed/ | ai |
| OpenAI Blog | https://openai.com/blog/rss.xml | ai, openai |
| Anthropic | https://www.anthropic.com/blog/rss.xml | ai, claude |
| Google AI | https://ai.googleblog.com/feeds/posts/default | ai, google |
| DeepMind | https://deepmind.com/blog/rss.xml | ai, deepmind |
| Hugging Face | https://huggingface.co/blog/feed.xml | ai, ml |
| Papers With Code | https://paperswithcode.com/rss | ai, research |

---

## 3️⃣ 设置系统 Cron 定时任务

### 方式一：使用自动配置脚本（推荐）

```bash
# 进入工作目录
cd /home/fengxueda/.openclaw/workspace

# 运行配置脚本（参数：间隔分钟数 每次条数 时间范围小时）
./setup_cron.sh 60 15 1
```

脚本会交互式地添加定时任务。

### 方式二：手动配置

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每小时运行一次，获取15条）
0 * * * * cd /home/fengxueda/.openclaw/workspace && /usr/bin/python3 twitter_news_full.py --once --max 15 --hours 1 >> /home/fengxueda/.openclaw/workspace/cron.log 2>&1

# 或者每30分钟运行一次
*/30 * * * * cd /home/fengxueda/.openclaw/workspace && /usr/bin/python3 twitter_news_full.py --once --max 10 --hours 1 >> /home/fengxueda/.openclaw/workspace/cron.log 2>&1
```

### 常用 Cron 表达式

| 频率 | Cron 表达式 |
|------|------------|
| 每 30 分钟 | `*/30 * * * *` |
| 每小时 | `0 * * * *` |
| 每 2 小时 | `0 */2 * * *` |
| 每天 9:00 | `0 9 * * *` |
| 每天 9:00 和 18:00 | `0 9,18 * * *` |

### 管理定时任务

```bash
# 查看当前任务
crontab -l

# 编辑任务
crontab -e

# 删除所有任务
crontab -r

# 查看日志
tail -f /home/fengxueda/.openclaw/workspace/cron.log
```

---

## 🚀 快速启动

### 单次运行（测试）

```bash
# 获取 15 条最近 1 小时的新闻
python3 twitter_news_full.py --once --max 15 --hours 1

# 获取 20 条最近 24 小时的新闻
python3 twitter_news_full.py --once --max 20 --hours 24
```

### 后台守护进程

```bash
# 每 60 分钟抓取 15 条
python3 twitter_news_full.py --daemon --interval 60 --max 15

# 每 30 分钟抓取 10 条
python3 twitter_news_full.py --daemon --interval 30 --max 10
```

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `twitter_news_full.py` | 主程序（完整版） |
| `twitter_news_bot.py` | 简化版（仅 Twitter） |
| `twitter_fetcher.py` | Twitter 抓取工具 |
| `.env.discord` | Discord 配置 |
| `setup_cron.sh` | Cron 配置脚本 |
| `discord_config.sh` | Discord 配置脚本 |
| `twitter_cron.sh` | 定时执行脚本 |
| `news_YYYYMMDD_HHMMSS.json` | 抓取结果（自动保存） |
| `twitter_news.log` | 运行日志 |
| `cron.log` | 定时任务日志 |

---

## 🔧 故障排除

### Discord 推送失败

1. 检查 Webhook URL 是否正确
2. 检查网络连接
3. 查看日志：`tail -f twitter_news.log`

### RSS 获取失败

1. 检查 RSS URL 是否可访问
2. 某些 RSS 可能需要代理
3. 检查 feedparser 是否安装：`pip3 show feedparser`

### Cron 任务不执行

1. 检查 cron 服务状态：`systemctl status cron`
2. 检查日志：`tail -f /var/log/syslog | grep CRON`
3. 检查路径是否正确
4. 检查权限：`chmod +x twitter_news_full.py`

### Twitter 抓取失败

1. 检查 Cookie 是否有效
2. 检查 twitter-cli 是否安装：`which twitter`
3. 测试：`twitter feed --max 5`

---

## 📊 输出格式

### Discord 推送格式

```
🐦 [1] Twitter
继 twitter-cli 和 tg-cli 之后，小红书 CLI 也来了！
🔗 https://x.com/jakevin7/status/2031411127532343318
👤 卡比卡比 (@jakevin7)
🕐 Tue Mar 10 16:45:29 +0000 2026

继 twitter-cli 和 tg-cli 之后，小红书 CLI 也来了！
逆向了小红书 Web 端的接口...

🖼️ 媒体: 0 个
📊 ❤️482 🔁79 💬23 👁️25085 🔖610
```

### JSON 输出格式

```json
{
  "fetch_time": "2026-03-11T11:15:25",
  "count": 5,
  "items": [
    {
      "id": "2031411127532343318",
      "title": "继 twitter-cli 和 tg-cli 之后...",
      "content": "继 twitter-cli 和 tg-cli 之后...",
      "url": "https://x.com/jakevin7/status/2031411127532343318",
      "author": "卡比卡比 (@jakevin7)",
      "source": "twitter",
      "source_name": "Twitter",
      "likes": 482,
      "retweets": 79,
      ...
    }
  ]
}
```

---

## 💡 高级用法

### 自定义过滤规则

编辑 `twitter_news_full.py`，在 `fetch_all` 方法中添加：

```python
def fetch_all(self, hours: int = 1) -> List[NewsItem]:
    # ... 现有代码 ...
    
    # 添加关键词过滤
    keywords = ["OpenClaw", "AI", "Claude", "GPT"]
    filtered = [item for item in filtered if any(kw.lower() in item.content.lower() for kw in keywords)]
    
    return filtered
```

### 添加自定义数据源

创建新的 Fetcher 类：

```python
class CustomFetcher:
    def __init__(self):
        self.name = "Custom"
    
    def fetch(self) -> List[NewsItem]:
        # 实现你的抓取逻辑
        items = []
        # ...
        return items

# 添加到聚合器
custom = CustomFetcher()
self.aggregator.add_fetcher(custom)
```

---

## ✅ 检查清单

配置完成后，确认以下事项：

- [ ] Discord Webhook URL 已配置
- [ ] `.env.discord` 文件已保存
- [ ] 测试推送成功
- [ ] RSS 源已添加
- [ ] Cron 任务已设置
- [ ] 日志文件正常生成
- [ ] JSON 输出文件正常保存

---

## 📞 支持

如有问题，请检查：
1. 日志文件：`twitter_news.log` 和 `cron.log`
2. 配置文件：`.env.discord`
3. 系统状态：`crontab -l` 和 `systemctl status cron`
