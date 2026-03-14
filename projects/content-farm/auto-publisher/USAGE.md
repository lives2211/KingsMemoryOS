# 小红书自动发布系统 - 使用指南

## 🚀 快速开始

### 1. 环境准备

```bash
cd /home/fengxueda/.openclaw/workspace/projects/content-farm/auto-publisher

# 安装依赖
pip install -r requirements.txt
playwright install chromium

# 安装 xiaohongshu-cli (可选，用于API方式)
pip install xiaohongshu-cli
```

### 2. 首次登录

```bash
# 方式1: 手动登录（推荐）
python3 manual_login.py
```

这将：
1. 打开浏览器
2. 显示小红书登录页面
3. 等待90秒让你扫码
4. 自动保存Cookie

### 3. 发布笔记

```bash
# 完整发布流程
python3 real_publish.py
```

## 📋 可用脚本

| 脚本 | 功能 |
|------|------|
| `manual_login.py` | 手动扫码登录 |
| `real_publish.py` | 完整发布流程 |
| `quick_publish.py` | 快速发布（生成卡片+检查状态） |
| `demo_publish.py` | 演示模式（不实际发布） |
| `test_login.py` | 测试登录状态 |
| `main.py` | CLI主入口 |
| `web_dashboard.py` | Web仪表盘 |

## 🛠️ 工具脚本

```bash
# 自动互动
./tools/auto_interact.py browse --category food --limit 20
./tools/auto_interact.py comment --limit 10

# 内容分析
./tools/content_analyzer.py --category food --limit 50
```

## ⚙️ 配置说明

### 发布时间段 (config.yaml)

```yaml
publish_windows:
  - { start: "08:00", end: "10:00", weight: 0.3 }  # 早上
  - { start: "12:00", end: "14:00", weight: 0.3 }  # 中午
  - { start: "19:00", end: "22:00", weight: 0.4 }  # 晚上
```

### 风控配置

```yaml
safety:
  delays:
    typing: { min: 0.05, max: 0.2 }  # 打字延迟
    between_actions: { min: 1, max: 3 }  # 操作间隔
  random_behavior:
    simulate_mouse: true    # 模拟鼠标移动
    simulate_scroll: true   # 模拟页面滚动
```

## 📊 监控和日志

```bash
# 查看日志
tail -f logs/auto-publisher.log

# 启动Web仪表盘
python3 web_dashboard.py --port 8088
# 访问 http://localhost:8088
```

## 🔧 故障排查

### Cookie过期

```bash
# 重新登录
python3 manual_login.py
```

### 浏览器启动失败

```bash
# 重新安装Playwright
playwright install chromium --force
```

### 发布失败

1. 检查网络连接
2. 查看日志 `logs/auto-publisher.log`
3. 确认小红书页面结构未变更
4. 检查Cookie是否有效

## 📁 目录结构

```
auto-publisher/
├── cookies/          # Cookie存储
├── data/             # 发布记录
├── logs/             # 日志
├── output/           # 生成图片
├── core/             # 核心模块
├── tools/            # 工具脚本
└── *.py              # 各种脚本
```

## 🎯 发布流程

```
1. 检查账号 → 2. 检查Cookie → 3. 加载内容
4. 检查计划 → 5. 生成卡片 → 6. 创建记录
7. 启动浏览器 → 8. 加载Cookie → 9. 检查登录
10. 填充内容 → 11. 上传图片 → 12. 点击发布
```

## 💡 最佳实践

1. **首次使用**: 先运行 `manual_login.py` 完成登录
2. **定时发布**: 添加到crontab实现自动发布
3. **监控状态**: 定期查看Web仪表盘
4. **风控规避**: 遵守发布频率限制
5. **内容审核**: 发布前人工检查内容

## 📞 支持

如有问题，请查看：
- 日志: `logs/auto-publisher.log`
- 文档: `README.md`
- 配置: `config.yaml`
