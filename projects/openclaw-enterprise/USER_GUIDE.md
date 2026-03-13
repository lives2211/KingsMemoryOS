# OpenClaw Enterprise - 实战使用指南

## 🎯 核心使用场景

### 场景1：日常任务管理（每天使用）

#### 早上第一件事 - 查看 Dashboard
```bash
# 浏览器打开
http://localhost:8089/dashboard

# 或者命令行查看
python3 budget_system.py --dashboard
python3 ticket_system.py --board
```

**看什么：**
- 今天有哪些任务待办？
- 哪些 Agent 有任务积压？
- 预算使用情况

#### 创建新任务
```bash
# 方式1：命令行
python3 ticket_system.py --create "任务标题" "任务描述" "yitai" "项目名称"

# 方式2：通过代码调用
from ticket_system import TicketSystem
ts = TicketSystem()
ticket = ts.create_ticket(
    title="生成小红书笔记",
    description="根据热点生成5篇笔记",
    assignee="xiaohongcai",
    project="content-farm",
    priority="P1"
)
```

#### 任务委派（总管 → 执行）
```bash
# Monica 把任务委派给具体执行人
python3 ticket_system.py --delegate TK-XXX yitai "编写爬虫" "爬取热点数据"
```

#### 完成任务
```bash
# 执行人完成任务
python3 ticket_system.py --complete TK-XXX "已完成，生成5篇笔记" --actual-cost 2.5

# Monica 审核通过
python3 ticket_system.py --review TK-XXX main true "审核通过"
```

---

### 场景2：项目管理（每周使用）

#### 项目初始化
```bash
# 创建项目任务组
python3 ticket_system.py --create "闲鱼运营项目" "启动虚拟资料销售" "main" "xianyu"
python3 ticket_system.py --create "内容农场项目" "每日内容生成" "main" "content-farm"
python3 ticket_system.py --create "市场分析项目" "闲鱼数据爬取" "main" "market-research"
```

#### 项目进度跟踪
```bash
# 查看项目看板
python3 ticket_system.py --board

# 生成项目报告
python3 -c "
from ticket_system import TicketSystem
ts = TicketSystem()
stats = ts.get_stats()
print(f'总任务: {stats[\"total_tickets\"]}')
print(f'完成率: {stats[\"completion_rate\"]:.1f}%')
print(f'按状态: {stats[\"by_status\"]}')
"
```

#### 周会数据
```bash
# 导出本周数据
python3 budget_system.py --dashboard > weekly_budget.json
python3 ticket_system.py --stats > weekly_tasks.json
```

---

### 场景3：成本控制（每月使用）

#### 查看成本分析
```bash
# 查看预算仪表盘
python3 budget_system.py --dashboard

# 查看详细成本日志
cat logs/cost_log.jsonl | tail -20
```

#### 调整预算
```bash
# 如果发现某个 Agent 成本过高，调整预算
python3 -c "
from budget_system import BudgetManager
bm = BudgetManager()
bm.update_budget('bingbing', monthly_budget=50.0, daily_budget=5.0)
print('预算已调整')
"
```

#### 月度报告
```bash
# 生成月度成本报告
python3 -c "
import json
from budget_system import BudgetManager
bm = BudgetManager()
dashboard = bm.get_dashboard()

report = {
    'month': '2026-03',
    'total_budget': dashboard['total_budget'],
    'total_spent': dashboard['total_spent'],
    'agent_breakdown': dashboard['agent_status']
}

with open('monthly_report.json', 'w') as f:
    json.dump(report, f, indent=2)

print('月度报告已生成')
"
```

---

### 场景4：团队协作（实时使用）

#### Agent 间协作流程
```
1. Monica 创建任务 → bingbing
   "设计闲鱼商品封面"
   
2. bingbing 需要技术实现 → 委派给 yitai
   "编写自动生成封面的脚本"
   
3. yitai 完成后 → bingbing 审核
   
4. bingbing 审核通过 → Monica 验收
   
5. Monica 完成主任务
```

#### 代码实现
```python
from ticket_system import TicketSystem
from budget_system import BudgetManager

ts = TicketSystem()
bm = BudgetManager()

# 1. Monica 创建任务
main_task = ts.create_ticket(
    title="设计闲鱼商品封面",
    description="为6个虚拟资料设计封面图",
    assignee="bingbing",
    project="xianyu",
    priority="P1",
    estimated_cost=10.0
)

# 检查预算
budget_check = bm.check_budget("bingbing", 10.0)
if not budget_check["allowed"]:
    print(f"预算不足: {budget_check['reason']}")
    exit()

# 2. bingbing 委派技术子任务
sub_task = ts.delegate_ticket(
    parent_ticket=main_task.id,
    sub_assignee="yitai",
    sub_title="编写封面生成脚本",
    sub_description="用Python+PIL自动生成封面"
)

# 3. yitai 完成并记录成本
bm.record_cost("yitai", 5.0, "编写封面脚本")
ts.complete_ticket(sub_task.id, "脚本已完成，可生成6种风格封面")

# 4. bingbing 审核
ts.review_ticket(sub_task.id, "bingbing", True, "代码质量OK")

# 5. bingbing 完成主任务
bm.record_cost("bingbing", 8.0, "设计封面")
ts.complete_ticket(main_task.id, "6个封面已完成", artifacts=["covers.zip"])

# 6. Monica 审核
ts.review_ticket(main_task.id, "main", True, "验收通过")

print(f"✅ 任务完成！总成本: ${5.0 + 8.0}")
```

---

## 🚀 进阶用法

### 用法1：自动化工作流

#### 定时任务（Cron）
```bash
# 每天早上8点：检查任务并派发
0 8 * * * cd /path/to/openclaw-enterprise && python3 auto_dispatch.py

# 每天晚上9点：生成日报
0 21 * * * cd /path/to/openclaw-enterprise && python3 daily_report.py
```

#### auto_dispatch.py 示例
```python
#!/usr/bin/env python3
"""自动派发任务"""
from ticket_system import TicketSystem
from budget_system import BudgetManager

ts = TicketSystem()
bm = BudgetManager()

# 获取待办任务
todo_tasks = ts.get_tickets_by_agent("main", status="todo")

for task in todo_tasks:
    # 根据任务类型自动指派
    if "代码" in task.title or "脚本" in task.title:
        ts.assign_ticket(task.id, "yitai")
        print(f"自动指派给 yitai: {task.title}")
    elif "设计" in task.title or "内容" in task.title:
        ts.assign_ticket(task.id, "bingbing")
        print(f"自动指派给 bingbing: {task.title}")
    elif "数据" in task.title or "分析" in task.title:
        ts.assign_ticket(task.id, "daping")
        print(f"自动指派给 daping: {task.title}")
```

### 用法2：智能告警

#### 预算告警
```python
#!/usr/bin/env python3
"""预算告警"""
from budget_system import BudgetManager
import requests

bm = BudgetManager()
dashboard = bm.get_dashboard()

# 检查是否有Agent预算使用超过80%
for agent in dashboard["agent_status"]:
    if agent["usage_pct"] > 80:
        message = f"🚨 预算告警: {agent['agent_name']} 已使用 {agent['usage_pct']:.1f}%"
        # 发送到 Discord
        requests.post("YOUR_DISCORD_WEBHOOK", json={"content": message})
```

#### 任务积压告警
```python
#!/usr/bin/env python3
"""任务积压告警"""
from ticket_system import TicketSystem

ts = TicketSystem()

for agent_id in ["bingbing", "yitai", "daping"]:
    backlog = ts.get_tickets_by_agent(agent_id, status="backlog")
    if len(backlog) > 5:
        print(f"⚠️ {agent_id} 有 {len(backlog)} 个积压任务")
```

### 用法3：数据可视化

#### 生成周报图表
```python
#!/usr/bin/env python3
"""生成周报"""
import matplotlib.pyplot as plt
from ticket_system import TicketSystem
from budget_system import BudgetManager

ts = TicketSystem()
bm = BudgetManager()

# 任务完成趋势
stats = ts.get_stats()
plt.figure(figsize=(10, 6))
plt.bar(stats["by_status"].keys(), stats["by_status"].values())
plt.title("任务状态分布")
plt.savefig("weekly_tasks.png")

# 预算使用
budget = bm.get_dashboard()
agent_names = [a["agent_name"] for a in budget["agent_status"]]
usage = [a["usage_pct"] for a in budget["agent_status"]]
plt.figure(figsize=(10, 6))
plt.barh(agent_names, usage)
plt.title("预算使用率")
plt.savefig("weekly_budget.png")

print("✅ 周报图表已生成")
```

---

## 💡 最佳实践

### 1. 任务命名规范
```
[项目名] 动作 + 对象

✅ 好例子：
- [闲鱼] 生成ChatGPT提示词内容
- [内容农场] 爬取今日AI热点
- [小红书] 设计笔记封面模板

❌ 坏例子：
- 做个东西
- 处理一下
- 那个任务
```

### 2. 优先级使用
```
P0 - 紧急（立即处理，如系统故障）
P1 - 高（当天完成，如项目 deadline）
P2 - 中（本周完成，常规任务）
P3 - 低（有空再做，优化类）
```

### 3. 成本估算
```python
# 参考标准（USD）
cost_reference = {
    "简单任务（1-2步）": 0.5,
    "中等任务（3-5步）": 2.0,
    "复杂任务（5步+）": 5.0,
    "研究类任务": 3.0,
    "代码编写": 2.0,
    "内容生成": 1.0,
}
```

### 4. 委派原则
```
- 总管(Monica)：决策、协调、审核
- 创意官(bingbing)：内容、设计、文案
- 技术官(yitai)：编程、脚本、技术架构
- 检测官(daping)：测试、数据、分析
- 审计官(spikey)：复盘、质量、文档
- 小红财(xiaohongcai)：社媒、运营、发布
```

---

## 📱 移动端使用

### 手机访问 Dashboard
```
1. 确保 Dashboard 服务运行
2. 手机浏览器访问：http://YOUR_IP:8089/dashboard
3. 添加到主屏幕（像 App 一样使用）
```

### 快捷指令（iOS）
```
创建快捷指令：
- 名称：查看任务
- 操作：打开URL http://localhost:8089/dashboard
- 添加到主屏幕
```

---

## 🔗 与其他系统集成

### 集成 Discord
```python
# 任务完成时自动通知
import requests

def notify_discord(ticket, message):
    webhook = "YOUR_DISCORD_WEBHOOK_URL"
    requests.post(webhook, json={
        "content": f"📋 {message}\n任务: {ticket.title}\nAgent: @{ticket.assignee}"
    })
```

### 集成 OpenClaw
```python
# 在 OpenClaw 中调用
from ticket_system import TicketSystem

ts = TicketSystem()

# 当用户提出需求时，自动创建任务
def handle_request(user_message):
    ticket = ts.create_ticket(
        title=user_message[:50],
        description=user_message,
        assignee="main",
        project="user-requests"
    )
    return f"已创建任务: {ticket.id}"
```

---

## 📊 效果评估

### 关键指标
```
1. 任务完成率 > 80%
2. 平均任务周期 < 3天
3. 预算使用率 60-80%
4. 委派层级 < 3层
```

### 每月复盘
```bash
# 生成月度报告
python3 -c "
from ticket_system import TicketSystem
from budget_system import BudgetManager

ts = TicketSystem()
bm = BudgetManager()

print('=== 月度复盘 ===')
print(f'总任务: {ts.get_stats()[\"total_tickets\"]}')
print(f'完成率: {ts.get_stats()[\"completion_rate\"]:.1f}%')
print(f'总成本: ${bm.get_dashboard()[\"total_spent\"]:.2f}')
print('===============')
"
```

---

**现在就开始使用吧！建议从创建第一个任务开始：**

```bash
python3 ticket_system.py --create "我的第一个任务" "测试OpenClaw Enterprise系统" "yitai" "test"
```
