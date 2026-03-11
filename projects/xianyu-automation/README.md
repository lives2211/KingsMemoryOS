# 闲鱼自动化运营套件

基于 OpenClaw 生态的闲鱼自动化工具集，实现内容生成、商品管理、数据分析全流程自动化。

## 功能特性

### 1. xianyu_content - 内容生成
- ✅ 自动生成25字以内标题
- ✅ 三段式描述模板（出售原因+详细参数+配件保修）
- ✅ 5-8个关键词自动优化
- ✅ 吸睛标签智能添加

### 2. xianyu_manage - 商品管理
- ✅ 每日自动擦亮（最多50个商品）
- ✅ 1-3秒随机延迟防限流
- ✅ 流量高峰期检测
- ✅ 智能调价建议

### 3. xianyu_metrics - 数据分析
- ✅ 仪表盘总览（在售数、浏览量、想要数、收入）
- ✅ 7天/30天趋势分析
- ✅ 单品性能评级
- ✅ CSV数据导出

### 4. xianyu_publish - 商品发布
- ✅ 批量发布调度
- ✅ 智能发布时间规划
- ✅ 商品信息验证
- ✅ 防频繁发布保护

## 快速开始

### 安装
```bash
# 克隆项目
cd /home/fengxueda/.openclaw/workspace/projects/xianyu-automation

# 安装依赖（Python 3.8+）
chmod +x run.sh scripts/*.py
```

### 使用

#### 方式1：交互式菜单
```bash
./run.sh
```

#### 方式2：命令行直接调用

**生成内容**
```bash
python3 scripts/xianyu_content.py \
  --brand "Apple" \
  --model "iPhone 14 Pro" \
  --condition "99新" \
  --price 5800 \
  --reason "升级15了，这台14Pro出掉"
```

**擦亮商品**
```bash
python3 scripts/xianyu_manage.py \
  --config config/config.json \
  --items data/sample_items.json \
  --dry-run
```

**数据分析**
```bash
python3 scripts/xianyu_metrics.py \
  --items data/sample_items.json \
  --full-report \
  --export-csv
```

**批量发布**
```bash
python3 scripts/xianyu_publish.py \
  --items data/sample_items.json \
  --dry-run \
  --max-per-hour 5
```

## 项目结构

```
xianyu-automation/
├── scripts/
│   ├── xianyu_content.py    # 内容生成
│   ├── xianyu_manage.py     # 商品管理
│   ├── xianyu_metrics.py    # 数据分析
│   └── xianyu_publish.py    # 商品发布
├── config/
│   └── config.json          # 配置文件
├── data/
│   ├── sample_items.json    # 示例商品数据
│   └── *.csv                # 导出数据
├── logs/
│   └── *.log               # 运行日志
├── run.sh                   # 启动脚本
└── README.md               # 本文件
```

## 配置说明

编辑 `config/config.json`：

```json
{
  "xianyu_manage": {
    "max_items_per_day": 50,    // 每日擦亮上限
    "delay_min": 1,             // 最小延迟（秒）
    "delay_max": 3,             // 最大延迟（秒）
    "peak_hours": ["07:00-09:00", "19:00-21:00"]
  },
  "xianyu_publish": {
    "max_per_hour": 10,         // 每小时发布上限
    "dry_run": true             // 模拟模式（安全测试）
  }
}
```

## 工作流程

### 日常运营流程
1. **早上 7-9点**：运行 `xianyu_manage` 自动擦亮商品
2. **需要上新时**：运行 `xianyu_content` 生成内容，然后 `xianyu_publish` 发布
3. **每周一次**：运行 `xianyu_metrics` 分析数据，导出CSV

### 完整自动化（Cron定时任务）
```bash
# 每天早上8点自动擦亮
0 8 * * * cd /path/to/xianyu-automation && python3 scripts/xianyu_manage.py --items data/items.json

# 每周日晚上生成数据报告
0 21 * * 0 cd /path/to/xianyu-automation && python3 scripts/xianyu_metrics.py --items data/items.json --full-report
```

## 数据格式

### 商品数据格式 (data/items.json)
```json
[
  {
    "id": "item_001",
    "title": "商品标题",
    "price": 5800,
    "condition": "99新",
    "brand": "Apple",
    "model": "iPhone 14 Pro",
    "views": 156,
    "wants": 12,
    "status": "active",
    "created_at": "2026-03-01T10:00:00"
  }
]
```

## 注意事项

1. **模拟模式**：默认 `--dry-run` 模式，不会实际操作，测试通过后再关闭
2. **频率限制**：擦亮每天1次，发布每小时不超过10个
3. **随机延迟**：所有操作都有1-3秒随机延迟，模拟真人行为
4. **数据备份**：定期备份 `data/` 目录

## 与原版对比

| 功能 | 原版 Skills | 本版本 |
|------|------------|--------|
| 内容生成 | ✅ AI生成 | ✅ AI生成 |
| 自动擦亮 | ✅ API调用 | ✅ 模拟操作 |
| 数据分析 | ✅ 仪表盘 | ✅ 仪表盘+CSV |
| 批量发布 | ✅ API调用 | ✅ 模拟操作 |
| 接入难度 | 需私有仓库权限 | 即装即用 |

## 后续优化

- [ ] 对接闲鱼实际API（需开发者权限）
- [ ] 图片自动处理
- [ ] 智能定价算法
- [ ] 竞品价格监控
- [ ] 多账号管理

## License

MIT License - 基于 OpenClaw 生态开源
