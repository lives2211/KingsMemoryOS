# 小红书自动发布系统

基于浏览器自动化(CDP)的小红书安全发布工具，模拟真人操作，降低封号风险。

## ✨ 特性

- 🎨 **AI生成卡片** - 8套主题皮肤，自动渲染小红书风格图片
- 🤖 **浏览器自动化** - 基于Playwright CDP，模拟真实用户操作
- 🛡️ **风控规避** - 随机延迟、鼠标移动、打字停顿、固定设备指纹
- ⏰ **智能调度** - 模拟真人作息，早中晚三个发布窗口
- 📱 **多账号支持** - Cookie隔离，支持多账号轮换
- 📊 **内容集成** - 无缝对接内容农场，自动读取Markdown笔记

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────┐
│                    小红书自动发布系统                      │
├─────────────────────────────────────────────────────────┤
│  1. 内容生成层  →  2. 图片渲染层  →  3. 浏览器自动化层      │
│     (AI写作)        (卡片生成)        (CDP模拟真人)        │
├─────────────────────────────────────────────────────────┤
│  4. 风控规避层  →  5. 账号管理层  →  6. 监控日志层         │
│   (行为模拟)        (Cookie隔离)       (异常检测)         │
└─────────────────────────────────────────────────────────┘
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /home/fengxueda/.openclaw/workspace/projects/content-farm/auto-publisher

# 安装Python依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install chromium

# 安装卡片渲染器依赖
cd card-renderer
pip install -r requirements.txt
playwright install chromium
```

### 2. 配置

编辑 `config.yaml`：

```yaml
# 账号配置
accounts:
  account_1:
    alias: "主账号"
    max_daily_posts: 3  # 每日最大3篇
    publish_windows:
      - { start: "08:00", end: "10:00", weight: 0.3 }  # 早上
      - { start: "12:00", end: "14:00", weight: 0.3 }  # 中午
      - { start: "19:00", end: "22:00", weight: 0.4 }  # 晚上

# 内容配置
content:
  source_dir: "../xiaohongshu"  # 内容来源
  image_generation:
    theme: "playful-geometric"  # 卡片主题
    mode: "auto-split"          # 分页模式
```

### 3. 首次登录

```bash
python main.py login
```

扫码登录小红书，Cookie会自动保存。

### 4. 发布笔记

```bash
# 查看状态
python main.py status

# 预览发布计划
python main.py preview --limit 5

# 发布单篇（第一篇）
python main.py publish

# 批量发布（带风控延迟）
python main.py batch --limit 3

# 无头模式（后台运行）
python main.py batch --headless
```

## 🎨 卡片主题

| 主题 | 风格 |
|------|------|
| default | 简约灰 |
| playful-geometric | 几何活泼 |
| neo-brutalism | 新粗野主义 |
| botanical | 植物自然 |
| professional | 专业商务 |
| retro | 复古风格 |
| terminal | 终端代码 |
| sketch | 手绘草图 |

## 🛡️ 风控策略

### 操作延迟
- 页面加载: 2-5秒
- 打字速度: 50-200ms/字符
- 点击间隔: 0.5-2秒
- 发布间隔: 30分钟-2小时

### 行为模拟
- ✅ 鼠标随机移动
- ✅ 页面滚动停顿
- ✅ 阅读时间模拟
- ✅ 固定设备指纹
- ✅ 随机发布时间

### 账号安全
- Cookie隔离存储
- 固定User-Agent
- 固定Viewport
- 隐藏webdriver特征

## 📁 项目结构

```
auto-publisher/
├── main.py                 # 主入口
├── config.yaml            # 配置文件
├── requirements.txt       # 依赖
├── README.md             # 本文档
├── core/                 # 核心模块
│   ├── publisher.py      # 浏览器发布
│   ├── card_generator.py # 卡片生成
│   ├── content_loader.py # 内容加载
│   └── scheduler.py      # 发布调度
├── card-renderer/        # 卡片渲染器（Git子模块）
├── cdp-publisher/        # CDP发布器（Git子模块）
├── xhs-ops/             # 小红书运营Skill（Git子模块）
├── cookies/             # Cookie存储
├── logs/                # 日志
└── output/              # 生成图片
```

## 🔧 集成内容农场

系统会自动读取 `../xiaohongshu/YYYY-MM-DD/` 目录下的Markdown文件：

```markdown
# 笔记标题

正文内容...
可以有多行

#标签1 #标签2 #标签3
```

## ⏰ 定时任务

添加到crontab实现全自动：

```bash
# 每天早上8点检查并发布
0 8 * * * cd /path/to/auto-publisher && python main.py batch --limit 1 --headless

# 中午12点
0 12 * * * cd /path/to/auto-publisher && python main.py batch --limit 1 --headless

# 晚上7点
0 19 * * * cd /path/to/auto-publisher && python main.py batch --limit 1 --headless
```

## ⚠️ 注意事项

1. **首次使用** - 必须手动扫码登录一次
2. **Cookie有效期** - 通常7-30天，过期需重新登录
3. **发布频率** - 建议每日不超过3篇，避免风控
4. **内容质量** - AI生成内容建议人工审核后再发布
5. **账号安全** - 不要在公共环境存储Cookie

## 📊 日志查看

```bash
# 实时查看日志
tail -f logs/auto-publisher.log

# 查看最近发布记录
grep "发布成功" logs/auto-publisher.log | tail -20
```

## 🛠️ 故障排查

### 无法启动浏览器
```bash
# 重新安装Playwright
playwright install chromium --force
```

### 登录失效
```bash
# 删除Cookie重新登录
rm cookies/account_1.json
python main.py login
```

### 发布失败
- 检查网络连接
- 查看日志 `logs/auto-publisher.log`
- 确认小红书页面结构未变更

## 📄 许可证

MIT License

## 🙏 致谢

- [Xiangyu-CAS/xiaohongshu-ops-skill](https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill)
- [comeonzhj/Auto-Redbook-Skills](https://github.com/comeonzhj/Auto-Redbook-Skills)
- [white0dew/XiaohongshuSkills](https://github.com/white0dew/XiaohongshuSkills)
