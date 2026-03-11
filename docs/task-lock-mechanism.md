# 🔒 任务锁机制
*防止重复执行*

## 核心规则

每个Agent开始任务前，必须检查是否已有"完成标记"

## 实现方式

### 方法1: 文件锁
```bash
# 开始任务前检查
if [ -f "agents/rachel/drafts/2026-03-06.done" ]; then
    echo "今日任务已完成，跳过"
    exit 0
fi

# 执行任务...

# 完成后创建标记
touch "agents/rachel/drafts/2026-03-06.done"
```

### 方法2: 内存标记
写入 `memory/shared/task-status.json`:
```json
{
  "2026-03-06": {
    "rachel-linkedin": "completed",
    "completedAt": "2026-03-06T10:30:00Z"
  }
}
```

## 检查清单

Agent每次执行前自检：
- [ ] 今日任务是否已标记完成？
- [ ] 是 → 直接退出，不再执行
- [ ] 否 → 正常执行，完成后标记

## 应用到所有Agent

| Agent | 锁文件位置 |
|-------|-----------|
| Dwight | `intel/.done` |
| Kelly | `agents/kelly/drafts/.done` |
| Rachel | `agents/rachel/drafts/.done` |
| Ross | `agents/ross/tasks/.done` |
| Angela | `agents/angela/reports/.done` |
| Pam | `agents/pam/newsletter/.done` |
| Lily | `agents/lily/notes/.done` |
| Skeptic | `agents/skeptic/challenges/.done` |