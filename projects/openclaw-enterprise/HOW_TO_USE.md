# OpenClaw + Paperclip 使用指南

## 🚀 快速开始

### 1. 确认服务运行

```bash
# 检查服务状态
curl http://localhost:3100/health

# 预期输出
{"status":"ok","agents":6,"tasks":2}
```

如果服务没运行，启动它：

```bash
cd /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise
python3 mock_paperclip_server.py &
```

---

## 📋 功能 1：智能任务派发（能力匹配 + 预算检查）

### 命令行方式

```bash
cd /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise

# 派发任务给最匹配的 Agent
python3 paperclip_client.py --dispatch \
  "任务标题" \
  "任务描述" \
  "所需能力1,能力2" \
  预算金额
```

### 示例

```bash
# 需要编程能力 → 自动匹配 yitai
python3 paperclip_client.py --dispatch \
  "编写闲鱼爬虫" \
  "爬取商品数据并保存到Excel" \
  "编程,脚本,爬虫" \
  10.0
```

**输出：**
```json
{
  "success": true,
  "task": {
    "id": "c8d83f0d",
    "title": "编写闲鱼爬虫",
    "assignee": "yitai",      // 自动分配给技术官
    "status": "backlog"
  },
  "assigned_to": "yitai",
  "match_score": 3,           // 匹配度 3/3
  "budget_remaining": 70.0    // 剩余预算
}
```

### Python 代码方式

```python
from paperclip_client import PaperclipClient

client = PaperclipClient()

# 智能派发
result = client.smart_dispatch(
    title="设计商品封面",
    description="为虚拟资料设计封面图",
    required_caps=["设计", "创意", "内容"],  # 需要这些能力
    estimated_cost=8.0
)

if result["success"]:
    print(f"✅ 任务已派发")
    print(f"   分配给: {result['agent_name']}")  # bingbing
    print(f"   匹配度: {result['match_score']}")
    print(f"   任务ID: {result['task']['id']}")
else:
    print(f"❌ 派发失败: {result['error']}")
```

### 能力匹配规则

| 能力关键词 | 匹配 Agent | 说明 |
|-----------|-----------|------|
| 编程/代码/脚本/开发 | yitai | 技术官 |
| 设计/创意/内容/文案 | bingbing | 创意官 |
| 检测/测试/分析/数据 | daping | 检测官 |
| 审计/复盘/质量/文档 | spikey | 审计官 |
| 社媒/运营/小红书/公众号 | xiaohongcai | 运营官 |
| 统筹/决策/协调/审核 | main | 总管 |

---

## 📋 功能 2：任务委派链（父任务 → 子任务）

### 场景示例

```
Monica (总管)
└── 任务："闲鱼运营项目" (预算 $50)
    └── 委派给 yitai："编写爬虫脚本" (预算 $20)
        └── yitai 完成
    └── 委派给 bingbing："设计商品封面" (预算 $15)
        └── bingbing 完成
    └── Monica 验收项目
```

### 命令行方式

```bash
# 1. 创建父任务
python3 -c "
from paperclip_client import PaperclipClient
c = PaperclipClient()
result = c.create_task(
    '闲鱼运营项目',
    '完整的闲鱼虚拟资料运营',
    'main',
    'P0',
    50.0
)
print(f'父任务ID: {result[\"task\"][\"id\"]}')
"

# 2. 委派子任务（替换 PARENT_ID）
curl -X POST http://localhost:3100/api/tasks/PARENT_ID/delegate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "编写爬虫脚本",
    "description": "爬取闲鱼商品数据",
    "assignee": "yitai",
    "budget": 20.0
  }'
```

### Python 代码方式

```python
from paperclip_client import PaperclipClient

client = PaperclipClient()

# 1. Monica 创建父任务
parent = client.create_task(
    title="闲鱼运营项目",
    description="完整的闲鱼虚拟资料运营方案",
    assignee="main",           # 总管负责
    priority="P0",
    budget=50.0
)
parent_id = parent["task"]["id"]
print(f"父任务创建: {parent_id}")

# 2. 委派子任务给 yitai
sub1 = client.delegate_task(
    parent_task_id=parent_id,
    title="编写爬虫脚本",
    description="爬取商品数据并分析",
    sub_assignee="yitai"
)
print(f"子任务1: {sub1['sub_task']['id']} → yitai")

# 3. 委派子任务给 bingbing
sub2 = client.delegate_task(
    parent_task_id=parent_id,
    title="设计商品封面",
    description="为6个商品设计封面图",
    sub_assignee="bingbing"
)
print(f"子任务2: {sub2['sub_task']['id']} → bingbing")

# 4. 查看委派链
org = client.get_org_chart()
print(json.dumps(org, indent=2))
```

### 查看委派关系

```bash
# 查看所有任务
python3 paperclip_client.py --tasks

# 查看具体任务详情
curl http://localhost:3100/api/tasks/任务ID
```

---

## 📋 功能 3：预算控制（月度预算 + 实时检查）

### 查看预算状态

```bash
# 查看所有 Agent 预算
python3 paperclip_client.py --agents

# 查看仪表盘
curl http://localhost:3100/api/dashboard | python3 -m json.tool
```

**输出示例：**
```json
{
  "agents": {
    "total": 6,
    "active": 6
  },
  "budget": {
    "total": 440.0,        // 总预算
    "used": 35.0,          // 已使用
    "remaining": 405.0,    // 剩余
    "usage_pct": 8.0       // 使用率 8%
  }
}
```

### 预算检查

```python
from paperclip_client import PaperclipClient

client = PaperclipClient()

# 检查 yitai 的预算
check = client.check_budget("yitai", estimated_cost=50.0)

print(f"预算检查:")
print(f"  月度预算: ${check['monthly_budget']}")
print(f"  已使用: ${check['used']}")
print(f"  剩余: ${check['remaining']}")
print(f"  使用率: {check['usage_pct']:.1f}%")
print(f"  是否允许: {check['allowed']}")  # False（如果超预算）
```

### 预算告警

当 Agent 预算使用超过 80% 时，系统会自动阻止新任务派发。

---

## 📋 功能 4：组织架构（层级汇报关系）

### 查看组织架构

```bash
# 命令行
python3 paperclip_client.py --org

# 直接访问 API
curl http://localhost:3100/api/org/chart | python3 -m json.tool
```

**输出：**
```json
{
  "id": "main",
  "name": "Monica",
  "title": "龙虾总管",
  "children": [
    {
      "id": "yitai",
      "name": "yitai",
      "title": "技术官",
      "department": "技术部"
    },
    {
      "id": "bingbing",
      "name": "bingbing",
      "title": "创意官",
      "department": "创作部"
    },
    {
      "id": "daping",
      "name": "daping",
      "title": "检测官",
      "department": "质检部"
    },
    {
      "id": "spikey",
      "name": "spikey",
      "title": "审计官",
      "department": "审计部"
    },
    {
      "id": "xiaohongcai",
      "name": "xiaohongcai",
      "title": "运营官",
      "department": "运营部"
    }
  ]
}
```

### 组织架构图

```
                    🦞 Monica
                   龙虾总管 (CEO)
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   yitai            bingbing        daping
   技术官            创意官          检测官
   (技术部)          (创作部)        (质检部)
   
   spikey       xiaohongcai
   审计官           运营官
   (审计部)        (运营部)
```

### 汇报关系

- **Monica** → 汇报给：无（CEO）
- **yitai/bingbing/daping/spikey/xiaohongcai** → 汇报给：Monica

---

## 🔧 解决 API 访问问题

### 问题 1：浏览器打不开 http://localhost:3100

**原因：** 浏览器访问需要完整的 URL 路径

**解决：**

```bash
# ✅ 正确的 API 访问方式

# 1. 健康检查
curl http://localhost:3100/health

# 2. 查看 Agent 列表
curl http://localhost:3100/api/agents

# 3. 查看任务列表
curl http://localhost:3100/api/tasks

# 4. 查看仪表盘
curl http://localhost:3100/api/dashboard

# 5. 查看组织架构
curl http://localhost:3100/api/org/chart
```

### 问题 2：服务没运行

```bash
# 检查服务
ps aux | grep mock_paperclip

# 如果没运行，启动它
cd /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise
python3 mock_paperclip_server.py &

# 验证
sleep 3
curl http://localhost:3100/health
```

### 问题 3：端口被占用

```bash
# 查看端口占用
netstat -tlnp | grep 3100

# 杀死占用进程
kill -9 PID

# 重新启动
python3 mock_paperclip_server.py &
```

---

## 📱 完整工作流示例

### 场景：启动闲鱼运营项目

```bash
cd /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise

# Step 1: Monica 创建项目任务
python3 -c "
from paperclip_client import PaperclipClient
c = PaperclipClient()

# 创建父任务
parent = c.create_task(
    '闲鱼虚拟资料运营项目',
    '完整的闲鱼运营方案，包括商品上架、自动擦亮、数据分析',
    'main',
    'P0',
    100.0
)
print(f'✅ 项目创建: {parent[\"task\"][\"id\"]}')

# Step 2: 委派技术任务给 yitai
sub1 = c.delegate_task(
    parent['task']['id'],
    '编写闲鱼自动化脚本',
    '自动擦亮、数据监控、价格调整',
    'yitai'
)
print(f'✅ 技术任务: {sub1[\"sub_task\"][\"id\"]} → yitai')

# Step 3: 委派设计任务给 bingbing
sub2 = c.delegate_task(
    parent['task']['id'],
    '设计商品封面',
    '6个虚拟资料的封面设计',
    'bingbing'
)
print(f'✅ 设计任务: {sub2[\"sub_task\"][\"id\"]} → bingbing')

# Step 4: 委派运营任务给 xiaohongcai
sub3 = c.delegate_task(
    parent['task']['id'],
    '社媒推广',
    '小红书、公众号推广',
    'xiaohongcai'
)
print(f'✅ 运营任务: {sub3[\"sub_task\"][\"id\"]} → xiaohongcai')

# Step 5: 生成站会报告
print()
print(c.generate_standup_report())
"
```

---

## 💡 常用命令速查

| 命令 | 说明 |
|------|------|
| `python3 paperclip_client.py --agents` | 查看所有 Agent |
| `python3 paperclip_client.py --tasks` | 查看所有任务 |
| `python3 paperclip_client.py --dashboard` | 查看仪表盘 |
| `python3 paperclip_client.py --standup` | 生成站会报告 |
| `python3 paperclip_client.py --org` | 查看组织架构 |
| `python3 paperclip_client.py --dispatch "标题" "描述" "能力" 预算` | 智能派发任务 |

---

## 📞 故障排除

### 问题：命令报错 "Connection refused"

**解决：**
```bash
# 1. 检查服务
ps aux | grep mock_paperclip

# 2. 如果没运行，启动
python3 mock_paperclip_server.py &

# 3. 等待 3 秒再试
sleep 3
curl http://localhost:3100/health
```

### 问题：Python 导入错误

**解决：**
```bash
# 确保在正确目录
cd /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise

# 使用完整路径
python3 /home/fengxueda/.openclaw/workspace/projects/openclaw-enterprise/paperclip_client.py --agents
```

---

**现在你可以开始使用所有功能了！**

试试这个命令：
```bash
python3 paperclip_client.py --standup
```
