# 🦞 小红书矩阵运营系统

基于 OpenClaw + AI Agent 的小红书全自动矩阵运营方案。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    小红书矩阵运营系统                        │
├─────────────────────────────────────────────────────────────┤
│  5个账号 × 5种风格 × 每天3-5篇 = 日更15-25篇                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  数码虾  │  │  美学虾  │  │  职场虾  │  │  吃货虾  │   │
│  │ 科技极客 │  │ 生活美学 │  │ 职场成长 │  │ 美食探店 │   │
│  │ Terminal │  │ Botanical│  │Professional│  │  Retro   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│                        ┌──────────┐                        │
│                        │  潮虾    │                        │
│                        │ 潮流穿搭 │                        │
│                        │Neo-Brutal│                        │
│                        └──────────┘                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  核心功能:                                                  │
│  ✅ AI自动生成文案                                          │
│  ✅ Playwright渲染精美图片                                  │
│  ✅ 8套主题皮肤自动切换                                     │
│  ✅ 智能调度错峰发布                                        │
│  ✅ 自动回复评论                                            │
│  ✅ 爆款笔记复刻                                            │
└─────────────────────────────────────────────────────────────┘
```

## 快速开始

### 1. 安装
```bash
cd xiaohongshu-matrix
chmod +x install.sh
./install.sh
```

### 2. 配置Cookie
编辑各账号的配置文件：
```bash
# .env.tech-geek
# .env.life-aesthetics
# .env.career-growth
# .env.foodie
# .env.fashion
```

获取Cookie方式：
1. 浏览器登录小红书
2. F12打开开发者工具
3. Network → 任意请求
4. 复制Cookie头内容

### 3. 生成发布计划
```bash
python3 scheduler.py
```

### 4. 测试发布
```bash
python3 auto_post.py --once
```

### 5. 启动自动运营
```bash
python3 auto_post.py --daemon
```

## 账号定位

| 账号 | 定位 | 风格 | 发布时间窗口 |
|------|------|------|-------------|
| 数码虾 | 科技极客 | 专业、数据说话 | 7:30-9:00, 12:00-13:30, 18:30-20:00, 21:00-22:30 |
| 美学虾 | 生活美学 | 治愈、文艺 | 8:00-9:30, 12:30-14:00, 15:00-16:30, 20:00-21:30 |
| 职场虾 | 职场成长 | 干货、犀利 | 7:30-9:00, 12:00-13:30, 18:00-19:30, 21:30-23:00 |
| 吃货虾 | 美食探店 | 真实、幽默 | 11:30-13:00, 17:30-19:00, 20:00-21:30, 22:00-23:30 |
| 潮虾 | 潮流穿搭 | 自信、实用 | 8:30-10:00, 13:00-14:30, 16:00-17:30, 19:30-21:00 |

## 目录结构

```
xiaohongshu-matrix/
├── content-gen/          # Auto-Redbook-Skills (内容生成)
│   ├── scripts/
│   │   ├── render_xhs.py    # 图片渲染
│   │   └── publish_xhs.py   # 发布脚本
│   └── assets/themes/       # 8套主题
├── ops-skill/            # xiaohongshu-ops-skill (运营互动)
│   ├── SKILL.md
│   └── persona.md
├── personas/             # 5个账号人设
│   ├── tech-geek.md
│   ├── life-aesthetics.md
│   ├── career-growth.md
│   ├── foodie.md
│   └── fashion.md
├── generated/            # 生成的内容
├── scheduler.py          # 发布调度器
├── content_generator.py  # 内容生成器
├── auto_post.py          # 自动发布主程序
├── install.sh            # 安装脚本
└── README.md             # 本文档
```

## 主题皮肤

- **default**: 简约灰
- **playful-geometric**: 活泼几何
- **neo-brutalism**: 新粗野主义
- **botanical**: 植物自然
- **professional**: 专业商务
- **retro**: 复古风
- **terminal**: 代码风
- **sketch**: 手绘文艺

## 发布策略

- ✅ 每天3-5篇/账号
- ✅ 5个账号错峰发布
- ✅ 同账号间隔≥30分钟
- ✅ 随机时间窗口
- ✅ 自动避开风控时段

## 注意事项

1. **Cookie安全**: 不要提交到Git，定期更新
2. **发布频率**: 避免短时间内高频发布
3. **内容质量**: 定期人工审核，调整人设
4. **平台规则**: 遵守小红书社区规范

## 进阶功能

### 爆款复刻
```bash
# 输入爆款笔记链接，AI分析并生成类似内容
python3 ops-skill/scripts/clone_viral.py <url>
```

### 自动回复
```bash
# 检查并回复最新评论
python3 ops-skill/scripts/auto_reply.py
```

### 数据分析
```bash
# 查看账号数据
python3 analytics.py
```

## 技术栈

- **内容生成**: Python + OpenAI API
- **图片渲染**: Playwright + HTML/CSS
- **发布接口**: xhs (小红书API)
- **调度系统**: Python + JSON
- **浏览器自动化**: CDP (Chrome DevTools Protocol)

## 许可证

MIT License

---

🦞 让AI帮你运营小红书矩阵！
