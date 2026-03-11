# TRAINING.md - 每日培训与反馈机制

> 持续优化Agent表现，从错误中学习

---

## 每日反馈流程

### 21:00 复盘时执行

1. **回顾今日产出**
   - Dwight的情报质量如何？
   - Kelly/Rachel的内容是否符合风格？
   - Ross的工程任务是否验证充分？

2. **收集用户反馈**
   - 用户对哪些内容满意？
   - 哪些决策需要调整？
   - 有什么新的偏好或要求？

3. **更新记忆文件**
   ```markdown
   # MEMORY.md Update - YYYY-MM-DD
   
   ## Today's Feedback
   - [Agent]: [具体反馈]
   - [改进措施]
   
   ## Pattern Recognition
   - 有效的工作模式: ...
   - 需避免的做法: ...
   
   ## Tomorrow's Focus
   - 重点改进: ...
   ```

4. **微调SOUL.md**（如必要）
   - 基于本周累积反馈
   - 每周五统一更新

---

## 反馈类型

### 👍 Positive Reinforcement
当Agent做得好时：
- 记录到MEMORY.md
- 在下次类似任务中引用成功经验

### ⚠️ Constructive Correction
当Agent出错时：
- 明确指出了问题
- 解释为什么错了
- 提供正确做法的示例
- 记录到ERRORS.md

### 💡 New Learning
发现新模式时：
- 更新AGENTS.md规则
- 添加到相关Agent的MEMORY.md

---

## 培训案例库

### 案例1: 情报筛选过严
**问题**: Dwight只报告了3条新闻，遗漏重要信息
**反馈**: "放宽筛选标准，aiRating>6即可"
**结果**: 更新Dwight的AGENTS.md筛选标准

### 案例2: 内容风格不符
**问题**: Kelly使用了emoji，不符合品牌调性
**反馈**: "禁用emoji，保持专业简洁"
**结果**: 更新Kelly的SOUL.md写作风格

### 案例3: 无验证完成
**问题**: Ross声称修复了bug但未贴出验证输出
**反馈**: "所有修复必须贴出验证命令和结果"
**结果**: 更新Ross的AGENTS.md铁律

---

## 长期优化目标

| 周数 | 目标 |
|------|------|
| Week 1-2 | 稳定运行，记录基础模式 |
| Week 3-4 | 基于反馈优化SOUL.md |
| Week 5-8 | 建立稳定的团队节奏 |
| Week 9+ | 持续微调，追求 excellence |

---

*记住：第十个版本是好的，第三十个版本是很棒的。*