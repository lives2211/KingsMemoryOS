# 🦞 小红书矩阵运营系统 - 完整部署文档

## 系统概览

```
┌─────────────────────────────────────────────────────────────────────┐
│                    🦞 小红书矩阵运营系统                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│  │  Auto-Red   │  │ xiaohongshu │  │  union-     │               │
│  │  book-Skills│  │  -ops-skill │  │   search    │               │
│  │             │  │             │  │             │               │
│  │ • AI写文案  │  │ • 自动发布  │  │ • 多平台    │               │
│  │ • 生成封面  │  │ • 自动回复  │  │   搜索      │               │
│  │ • 8套主题   │  │ • 爆款复刻  │  │ • 趋势分析  │               │
│  └─────────────┘  └─────────────┘  └─────────────┘               │
│          │                │                │                      │
│          └────────────────┼────────────────┘                      │
│                           │                                       │
│                    ┌─────────────┐                               │
│                    │   aitu      │                               │
│                    │             │                               │
│                    │ • AI生图    │                               │
│                    │ • AI生视频  │                               │
│                    │ • 思维导图  │                               │
│                    └─────────────┘                               │
│                           │                                       │
│                           ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    5账号矩阵运营                              │ │
│  │                                                             │ │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │ │
│  │  │ 数码虾 │ │ 美学虾 │ │ 职场虾 │ │ 吃货虾 │ │  潮虾  │  │ │
│  │  │科技极客│ │生活美学│ │职场成长│ │美食探店│ │潮流穿搭│  │ │
│  │  │3-5篇/天│ │3-5篇/天│ │3-5篇/天│ │3-5篇/天│ │3-5篇/天│  │ │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘  │ │
│  │                                                             │ │
│  │  总计: 15-25篇/天 | 错峰发布 | 智能调度                      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. Auto-Redbook-Skills (内容生产)
**来源**: https://github.com/comeonzhj/Auto-Redbook-Skills

**功能**:
- ✅ AI自动生成小红书文案
- ✅ Playwright渲染精美图片
- ✅ 8套主题皮肤（Terminal/Retro/Botanical等）
- ✅ 4种分页模式
- ✅ 自动发布（支持私密/定时）

**位置**: `content-gen/`

### 2. xiaohongshu-ops-skill (运营互动)
**来源**: https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill

**功能**:
- ✅ 自动发布笔记
- ✅ 自动回复评论
- ✅ 爆款笔记复刻
- ✅ 自定义账号人设

**位置**: `ops-skill/`

### 3. union-search-skill (趋势研究)
**来源**: https://github.com/runningZ1/union-search-skill

**功能**:
- ✅ 30+平台统一搜索
- ✅ 小红书/抖音/B站/微博搜索
- ✅ 爆款内容分析
- ✅ 趋势数据研究

**位置**: `union-search/`

### 4. aitu (AI创作)
**来源**: https://github.com/ljquan/aitu

**功能**:
- ✅ AI图片生成（Gemini/Veo）
- ✅ AI视频生成
- ✅ 思维导图创建
- ✅ 流程图绘制

**位置**: `aitu/`

## 5账号矩阵定位

| 账号 | 昵称 | 定位 | 风格 | 主题 | 日更 |
|------|------|------|------|------|------|
| 1 | 数码虾 | 科技极客 | 专业数据 | Terminal | 3-5篇 |
| 2 | 美学虾 | 生活美学 | 治愈文艺 | Botanical | 3-5篇 |
| 3 | 职场虾 | 职场成长 | 干货犀利 | Professional | 3-5篇 |
| 4 | 吃货虾 | 美食探店 | 真实幽默 | Retro | 3-5篇 |
| 5 | 潮虾 | 潮流穿搭 | 自信实用 | Neo-Brutalism | 3-5篇 |

**总产出**: 15-25篇/天

## 快速开始

### 1. 一键启动
```bash
cd xiaohongshu-matrix

# 初始化系统
./start.sh init

# 查看状态
./start.sh status
```

### 2. 配置账号
编辑5个账号的Cookie配置：
```bash
# .env.tech-geek
# .env.life-aesthetics
# .env.career-growth
# .env.foodie
# .env.fashion
```

获取Cookie：
1. 浏览器登录小红书
2. F12 → Network → 任意请求
3. 复制Cookie头内容

### 3. 生成发布计划
```bash
./start.sh schedule
```

### 4. 测试运行
```bash
# 测试生成内容
./start.sh test

# 执行一次发布
./start.sh post
```

### 5. 启动自动运营
```bash
# 启动守护进程
./start.sh daemon
```

## 命令速查

```bash
./start.sh init          # 初始化系统
./start.sh status        # 查看状态
./start.sh schedule      # 生成今日计划
./start.sh test          # 测试生成
./start.sh post          # 执行发布
./start.sh daemon        # 启动守护进程
./start.sh research      # 研究热门话题
./start.sh aitu          # 启动AI绘图服务
```

## 增强功能

### 爆款研究
```bash
# 研究各账号领域的热门话题
./start.sh research

# 或使用Python直接调用
python3 enhanced_content_generator.py
```

### AI绘图
```bash
# 启动aitu服务
./start.sh aitu

# 访问 http://localhost:7200
# 使用AI生成封面图和素材
```

### 多平台搜索
```bash
# 搜索小红书
python3 union-search/union_search_cli.py xiaohongshu "关键词"

# 搜索抖音
python3 union-search/union_search_cli.py douyin "关键词"

# 搜索B站
python3 union-search/union_search_cli.py bilibili "关键词"
```

## 文件结构

```
xiaohongshu-matrix/
├── content-gen/              # Auto-Redbook-Skills
│   ├── scripts/
│   │   ├── render_xhs.py     # 图片渲染
│   │   └── publish_xhs.py    # 发布脚本
│   └── assets/themes/        # 8套主题
├── ops-skill/                # xiaohongshu-ops-skill
│   ├── SKILL.md
│   └── persona.md
├── union-search/             # union-search-skill
│   ├── union_search_cli.py
│   └── scripts/
├── aitu/                     # aitu
│   └── apps/web/
├── personas/                 # 5账号人设
│   ├── tech-geek.md
│   ├── life-aesthetics.md
│   ├── career-growth.md
│   ├── foodie.md
│   └── fashion.md
├── generated/                # 生成内容
├── research/                 # 研究数据
├── scheduler.py              # 发布调度器
├── content_generator.py      # 内容生成器
├── enhanced_content_generator.py  # 增强版生成器
├── assistant_tools.py        # 辅助工具集成
├── auto_post.py              # 自动发布主程序
├── start.sh                  # 一键启动脚本
├── install.sh                # 基础安装脚本
├── install_enhanced.sh       # 增强版安装脚本
└── README.md                 # 说明文档
```

## 发布策略

### 时间窗口
- **早高峰**: 7:30-9:00
- **午休**: 12:00-13:30
- **下午茶**: 15:00-16:30
- **晚高峰**: 18:30-20:00
- **睡前**: 21:00-23:00

### 错峰规则
- 5账号发布时间错开≥30分钟
- 同账号两篇间隔≥1小时
- 日总量控制在15-25篇
- 周末增加生活类内容

## 注意事项

1. **Cookie安全**: 不要提交到Git，定期更新
2. **发布频率**: 避免短时间内高频发布
3. **内容质量**: 定期人工审核，调整人设
4. **平台规则**: 遵守小红书社区规范
5. **风控策略**: 新号先养号，逐步增加频率

## 技术栈

- **内容生成**: Python + OpenAI API
- **图片渲染**: Playwright + HTML/CSS
- **发布接口**: xhs (小红书API)
- **搜索研究**: union-search (30+平台)
- **AI创作**: aitu (Gemini/Veo)
- **调度系统**: Python + JSON
- **浏览器自动化**: CDP

## 许可证

各组件遵循原项目许可证：
- Auto-Redbook-Skills: MIT
- xiaohongshu-ops-skill: MIT
- union-search-skill: MIT
- aitu: MIT

---

🦞 **让AI帮你运营小红书矩阵！**

系统已就绪，配置Cookie后即可开始全自动运营！
