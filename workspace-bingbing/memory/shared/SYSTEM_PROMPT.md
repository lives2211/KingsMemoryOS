# Agent 共享记忆 - 系统指令

## 主Agent派发任务时自动执行

### 1. 读取最近共享记忆
派发任务给子Agent前，先读取 `memory/shared/` 目录下最近的任务文件：

```
读取: memory/shared/
```

### 2. 提取上下文
从最新文件中提取：
- 上一Agent完成了什么
- 输出物路径
- 待办事项

### 3. 附带上下文派发
将上下文附带到新任务指令中：

```
【上下文】
- 上一任务：xxx
- 输出物：xxx
- 待办：@xxx

【新任务】
...
```

---

## 子Agent完成后自动执行

### 1. 写入共享记忆
完成任务后，写入 `memory/shared/YYYY-MM-DD-任务名.md`：

```markdown
# 任务：xxx

- **负责人**: @agent名
- **完成时间**: YYYY-MM-DD HH:MM
- **关键结论**: 完成了xxx
- **输出物**: /path/to/output
- **待办事项**: @下一个Agent需要做什么

---

### 上下文

（你的产出 + 建议下一Agent注意什么）
```

---

## 快速调用

在对话中可直接使用：
- `read(memory/shared/)` - 读取最近记忆
- `write(memory/shared/xxx.md, content)` - 写入新记忆