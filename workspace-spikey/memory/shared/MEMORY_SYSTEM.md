# 共享记忆系统

> 团队共享的长期记忆库 - 所有Agent可读可写

## 目录结构

```
memory/shared/
├── MEMORY_SYSTEM.md          # 本文件 - 使用指南
├── TEAM_KNOWLEDGE.md         # 团队共享知识
├── USER_PREFERENCES.md       # 用户偏好设置
├── BEST_PRACTICES.md         # 最佳实践总结
├── DECISION_LOG.md           # 重要决策记录
├── WEEKLY_REVIEWS/           # 每周复盘
│   └── 2026-03-W1.md
├── LEARNINGS/                # 学习沉淀
│   ├── dwight/
│   ├── kelly/
│   ├── rachel/
│   ├── ross/
│   ├── angela/
│   └── pam/
└── ARCHIVE/                  # 归档（超过30天）
    └── 2026-02/
```

## 记忆类型

### 1. 事实型记忆 (Facts)
- 用户明确说过的话
- 确定的事实和数据
- 已验证的信息

**格式：**
```markdown
## [日期] 事实标题
- **内容**: 具体信息
- **来源**: 谁说的/哪里看到的
- **确认**: ✅ 已验证 / ⏳ 待验证
```

### 2. 偏好型记忆 (Preferences)
- 用户的喜好和厌恶
- 风格偏好
- 工作习惯

**格式：**
```markdown
## [日期] 偏好名称
- **描述**: 具体偏好
- **发现场景**: 什么时候发现的
- **重要性**: 🔴 必须遵守 / 🟡 尽量满足 / 🟢 参考即可
```

### 3. 教训型记忆 (Lessons)
- 错误和解决方案
- 改进建议
- 成功经验

**格式：**
```markdown
## [日期] 教训标题
- **问题**: 发生了什么
- **原因**: 为什么会这样
- **解决**: 怎么解决的
- **预防**: 如何避免再次发生
```

## 写入规范

### 何时写入

| 场景 | 写入位置 | 负责人 |
|------|----------|--------|
| 用户明确说"记住..." | USER_PREFERENCES.md | 被@的Agent |
| 发现用户偏好 | USER_PREFERENCES.md | 发现的Agent |
| 遇到错误并解决 | ERRORS.md + 个人MEMORY.md | 解决问题的Agent |
| 完成任务有心得 | BEST_PRACTICES.md | 执行的Agent |
| 重大决策 | DECISION_LOG.md | Monica |
| 每周复盘 | WEEKLY_REVIEWS/ | Angela |

### 写入模板

```markdown
## [YYYY-MM-DD] 标题

**类型**: 事实/偏好/教训

**内容**:
详细描述...

**上下文**:
- 任务: XXX
- 相关Agent: XXX
- 用户反馈: XXX

**行动项**:
- [ ] 下次注意XXX
- [ ] 更新XXX文档
```

## 读取规范

### 每次会话启动时

1. **Monica** 读取：
   - TEAM_KNOWLEDGE.md
   - DECISION_LOG.md（最近7天）
   - USER_PREFERENCES.md

2. **其他Agent** 读取：
   - 自己的LEARNINGS/目录
   - 相关的BEST_PRACTICES.md章节
   - ERRORS.md中相关的错误条目

### 关键记忆提醒

在以下情况主动检查记忆：
- 开始新任务前
- 遇到类似之前的问题时
- 用户提到"像以前那样..."
- 不确定如何处理时

## 记忆维护

### 每日（心跳时）
- 回顾今日memory/YYYY-MM-DD.md
- 提取重要内容到共享记忆

### 每周（周五）
- Angela审计本周新增记忆
- 整理到WEEKLY_REVIEWS
- 删除过时/错误记忆

### 每月
- 归档超过30天的日常日志
- 更新TEAM_KNOWLEDGE.md
- 清理ARCHIVE/中超过90天的内容

## 记忆质量原则

1. **准确**: 不确定的标记[UNVERIFIED]
2. **简洁**: 一句话能说清不用两句
3. **结构化**: 使用统一的格式模板
4. **可追溯**: 注明来源和时间
5. **及时**: 当天的事当天记

## 禁止事项

❌ 不要记录敏感信息（密码、私钥等）
❌ 不要记录未经用户同意的个人信息
❌ 不要记录猜测或假设为事实
❌ 不要重复记录相同内容

---

*最后更新: 2026-03-06*
*维护者: 全体Agent*
*审计者: Angela