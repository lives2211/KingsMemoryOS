# 真正的独立 Agent 架构

## 🎯 目标

恢复之前的架构：**每个 Agent 是真正的独立 OpenClaw 会话**

## 📁 现有配置 (已存在)

| Agent | 工作空间 | SOUL.md | 状态 |
|-------|----------|---------|------|
| @yitai | ✅ 存在 | ✅ 存在 | 待启动 |
| @bingbing | ✅ 存在 | ✅ 存在 | 待启动 |
| @daping | ✅ 存在 | ✅ 存在 | 待启动 |
| @spikey | ✅ 存在 | ✅ 存在 | 待启动 |
| @xiaohongcai | ❌ 不存在 | - | 需创建 |

## 🚀 启动方案

### 方案: 按需启动 (推荐)

当派发任务时，启动对应的 Agent 子会话：

```python
# 派发任务到 @yitai
def dispatch_to_yitai(task):
    # 1. 启动 yitai 子会话 (如果未运行)
    spawn_session("yitai")
    
    # 2. 发送任务
    send_message("yitai", task)
    
    # 3. yitai 独立执行
    # 4. yitai 汇报结果
```

### Agent 工作流

```
用户请求 → Monica → 匹配 Agent → 启动子会话 → Agent 执行 → 汇报结果
```

## 📝 实施步骤

### Step 1: 创建 Agent 启动脚本

```bash
#!/bin/bash
# start_agent.sh <agent_id>

AGENT_ID=$1
WORKSPACE="/home/fengxueda/.openclaw/workspace-${AGENT_ID}"

# 启动子会话
openclaw sessions spawn \
    --label ${AGENT_ID} \
    --mode session \
    --cwd ${WORKSPACE}
```

### Step 2: 修改派发逻辑

```python
# 在 dispatch_server.py 中
def dispatch_task(task, agent_id):
    # 1. 记录到数据库
    save_task(task)
    
    # 2. 启动 Agent 子会话
    spawn_agent_session(agent_id)
    
    # 3. 发送任务到 Agent
    send_to_agent(agent_id, task)
```

### Step 3: Agent 执行流程

```
@yitai (子会话)
├── 接收任务
├── 自主分析
├── 自主执行
├── 生成结果
└── 汇报给 Monica
```

## 🎉 预期效果

| 维度 | V2.0 (当前) | V3.0 (修复后) |
|------|-------------|---------------|
| Agent 类型 | 内存模拟对象 | 真正独立 AI |
| 执行能力 | ❌ 无 | ✅ 有 |
| 自主决策 | ❌ 无 | ✅ 有 |
| 独立记忆 | ❌ 无 | ✅ 有 |
| Token 消耗 | 1x | 5x |

## ⚠️ 注意事项

1. **Token 成本**: 5 个独立 Agent = 5 倍 Token 消耗
2. **会话管理**: 需要管理多个子会话生命周期
3. **任务协调**: Monica 需要协调多个 Agent 的结果

## ❓ 确认

是否确认恢复真正的独立 Agent 架构？

- ✅ **是** - 恢复独立 Agent (高成本，真独立)
- ❌ **否** - 保持当前架构 (低成本，模拟)
