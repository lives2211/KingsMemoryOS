# Agent 共享记忆方案

## 目录结构
```
memory/shared/
├── README.md          # 本文件
├── TEMPLATE.md        # 任务模板
└── YYYY-MM-DD-xxx.md  # 各任务记忆
```

## 完整流程

### 1. 子Agent完成工作后
写入共享记忆到 `memory/shared/YYYY-MM-DD-任务名.md`

### 2. 派发新任务时
主Agent自动：
1. 读取 `memory/shared/` 下的最新任务文件
2. 获取上下文，附带到新任务指令中

### 3. 调用其他Agent历史（备选）
用 `sessions_history` 获取其他Agent最近的对话

---

## 示例：完整协作流程

**Step 1: 编程Agent完成 → 写记忆**
```markdown
# 任务：用户中心API

- **负责人**: @编程助手
- **完成时间**: 2026-03-06 09:00
- **关键结论**: 完成了 /api/user/profile 接口
- **输出物**: /workspace/user-api.js
- **待办事项**: @检测助手 验证接口 + @创作助手 写文档
```

**Step 2: 主Agent派发给检测Agent**
```
@检测助手 

【上下文】编程助手刚完成：
- 文件：/workspace/user-api.js
- 接口：GET /api/user/profile

【任务】验证这个接口：
1. 检查返回JSON结构
2. 测试HTTP状态码
```

---

## 5个Agent名单
- main (主Agent)
- bingbing (创意)
- daping (大屏/监控)
- spikey (待确认)
- yitai (待确认)