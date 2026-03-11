# 🤖 Agent团队协作流程 v1.0

## 每日时间表

```
08:00  Dwight    → 超级情报收集（6551+Union Search+GitHub）
09:00  Monica    → 读取情报，分配任务
09:00  Rachel    → LinkedIn专业内容创作
09:30  Kelly     → Twitter内容创作（基于情报生成推文）
10:00  Ross      → 工程任务（代码/脚本/工具）
14:00  Angela    → 质量检查（审核上午产出）
18:00  Monica    → 汇总日报，向您汇报
周五   Pam       → 撰写Weekly Intelligence Report
```

## 文件流转

```
Dwight          Monica           Kelly            You
  │               │                │               │
  ├─ intel/       │                │               │
  │   └── DAILY-INTEL.md ──────────┼───────────────┤
  │                                │               │
  │               ├─ 分配任务 ─────┤               │
  │               │                │               │
  │               │                ├─ drafts/      │
  │               │                │   └── YYYY-MM-DD.md
  │               │                │               │
  │               ├─ 审核 ─────────┘               │
  │               │                                │
  │               └─ 发布 ─────────────────────────┘
```

## 关键文件位置

| 用途 | 路径 |
|------|------|
| 每日情报 | `intel/DAILY-INTEL.md` |
| 内容草稿 | `agents/kelly/drafts/YYYY-MM-DD.md` |
| 任务队列 | `agents/ross/tasks/TASK_QUEUE.md` |
| 团队共享 | `memory/shared/` |
| 审计报告 | `agents/angela/reports/` |

## 沟通规则

1. **@必回** - 被@必须立即回复
2. **先确认** - 复杂任务先说"明白，让我了解背景"
3. **main汇总** - 所有决策由Monica汇总后向您汇报
4. **写结论** - 任务完成后写入对应memory目录

## 成功标准

- [ ] Dwight：每天08:30前完成情报收集
- [ ] Kelly：每天3条高质量推文草稿
- [ ] Ross：每周完成3个工程任务
- [ ] Angela：每周五输出质量审计报告
- [ ] Monica：每天18:00前发送日报

---

*最后更新：2026-03-06*