# SIAS 训练计划

## 目标
通过 5 个训练会话，让 Agent 掌握 SIAS 自我改进框架的核心机制。

## 训练会话安排

### Session 1: 基础认知 (10 分钟)
**目标**: 理解 WAL 协议和基本规则

**练习内容**:
1. 告诉 Agent 一个简单偏好:
   - "我喜欢用 pnpm 而不是 npm"
2. 观察 Agent 是否:
   - ✅ 先保存到 CORRECTIONS.md
   - ✅ 然后才回复 "明白"
3. 检查 .learnings/CORRECTIONS.md 是否有记录

**验证标准**:
- [ ] WAL 协议执行正确 (先保存，后回复)
- [ ] 日志格式符合规范
- [ ] 文件位置正确

---

### Session 2: 错误处理 (10 分钟)
**目标**: 学习记录和反思错误

**练习内容**:
1. 故意让 Agent 犯错:
   - 让 Agent 执行一个会失败的命令
   - 例如: "运行一个不存在的服务"
2. 纠正 Agent:
   - "这个服务不存在，你应该先检查"
3. 观察 Agent 是否:
   - ✅ 记录错误到 ERRORS.md
   - ✅ 分析原因和解决方案

**验证标准**:
- [ ] 错误被正确分类 (ERR)
- [ ] 包含 Area/Priority/Status
- [ ] 有明确的 Action 项

---

### Session 3: 最佳实践 (10 分钟)
**目标**: 学习记录和积累知识

**练习内容**:
1. 教 Agent 一个新技能:
   - "使用 `openclaw config validate` 验证配置"
2. 让 Agent 总结为最佳实践
3. 观察 Agent 是否:
   - ✅ 记录到 LEARNINGS.md
   - ✅ 标注 Area 和 Priority

**验证标准**:
- [ ] 学习被正确分类 (LRN)
- [ ] 内容清晰可复用
- [ ] 有明确的 Trigger 和 Action

---

### Session 4: 知识升级 (15 分钟)
**目标**: 掌握 Promotion 机制

**练习内容**:
1. 多次重复一个重要偏好:
   - 在不同会话中重复 3 次相同纠正
   - 例如: "总是使用 sudo 运行 systemctl"
2. 观察 Agent 是否:
   - ✅ 识别为 critical 或重复 >3 次
   - ✅ 自动升级到 MEMORY.md
3. 检查 MEMORY.md 是否有永久记录

**验证标准**:
- [ ] 临时日志标记为 archived
- [ ] MEMORY.md 有永久记录
- [ ] 升级过程符合规则

---

### Session 5: 自我审计 (15 分钟)
**目标**: 定期反思和总结

**练习内容**:
1. 让 Agent 回顾本周学习:
   - "总结本周的错误和学习"
2. Agent 应该:
   - ✅ 读取所有 .learnings/ 文件
   - ✅ 生成 SESSION-STATE.md 更新
   - ✅ 提出改进建议
3. 检查 SESSION-STATE.md 是否更新

**验证标准**:
- [ ] 完整回顾所有日志
- [ ] 生成有意义的总结
- [ ] 提出可执行的改进

---

## 训练检查清单

### 文件检查
- [ ] SOUL.md 存在且内容正确
- [ ] MEMORY.md 可写入
- [ ] SESSION-STATE.md 可更新
- [ ] .learnings/ 目录有 4 个文件

### 行为检查
- [ ] 每次纠正都先保存
- [ ] 日志格式符合规范
- [ ] 自动升级到 MEMORY.md
- [ ] 定期更新 SESSION-STATE.md

### 质量检查
- [ ] 日志内容清晰完整
- [ ] Area/Priority/Status 正确
- [ ] Action 项可执行
- [ ] 无重复或冗余记录

---

## 训练后状态

完成 5 个 Session 后，Agent 应该:
1. ✅ 自动执行 WAL 协议
2. ✅ 正确分类和记录所有学习
3. ✅ 主动识别需要升级的知识
4. ✅ 定期自我审计和改进

---

## 开始训练

**Session 1 开始指令**:
```
我是 candycion。现在开始 SIAS 训练 Session 1。

请阅读 ~/.openclaw/workspace/SOUL.md 确保理解所有规则。

我的第一个偏好: "我喜欢用 pnpm 而不是 npm"

请按照 WAL 协议: 先保存这个偏好，然后回复我。
```

---

*训练计划创建时间: 2026-03-10*
*预计完成时间: 1 小时内*
