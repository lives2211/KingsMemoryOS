# Claude Code 任务派发详细教程

## 前提条件

已安装好的组件：
- ✅ dispatch-claude-code.sh - 派发脚本
- ✅ claude_code_run.py - 运行器
- ✅ notify-agi.sh - 完成后自动通知
- ✅ 群 ID: -1003762750497

---

## 基础用法

### 1. 派发一个简单任务

```bash
~/clawd/scripts/dispatch-claude-code.sh \
  -p "用Python写一个Hello World程序" \
  -n "hello-test" \
  -g "-1003762750497"
```

**参数说明：**
- `-p` : 任务描述（你让AI做什么）
- `-n` : 任务名称（方便识别）
- `-g` : 群ID（通知发送到哪）

---

### 2. 派发到指定工作目录

```bash
~/clawd/scripts/dispatch-claude-code.sh \
  -p "帮我写一个计算器程序" \
  -n "calculator" \
  -g "-1003762750497" \
  -w "/home/fengxueda/projects/calculator"
```

---

### 3. 使用 Agent Teams（多Agent协作）

```bash
~/clawd/scripts/dispatch-claude-code.sh \
  -p "重构整个项目的代码" \
  -n "refactor-project" \
  -g "-1003762750497" \
  -w "/home/fengxueda/your-project" \
  --agent-teams \
  --teammate-mode auto
```

---

## 常用命令示例

### 示例1：写一个爬虫
```bash
~/clawd/scripts/dispatch-claude-code.sh \
  -p "用Python requests库写一个简单的网页爬虫，抓取豆瓣电影Top250" \
  -n "douban-spider" \
  -g "-1003762750497" \
  -w "/home/fengxueda/projects"
```

### 示例2：写一个API
```bash
~/clawd/scripts/dispatch-claude-code.sh \
  -p "用FastAPI写一个简单的REST API，包含用户增删改查接口" \
  -n "fastapi-crud" \
  -g "-1003762750497" \
  -w "/home/fengxueda/projects"
```

### 示例3：代码审查
```bash
~/clawd/scripts/dispatch-claude-code.sh \
  -p "审查 /home/fengxueda/projects/myapp/src 目录下的代码，找出问题和优化点" \
  -n "code-review" \
  -g "-1003762750497"
```

---

## 查看结果

### 1. Telegram 群里会收到通知

任务完成后自动发送结果到群里。

### 2. 查看JSON结果文件
```bash
cat ~/clawd/data/claude-code-results/latest.json
```

### 3. 查看日志
```bash
cat ~/clawd/data/claude-code-results/hook.log
```

---

## 注意事项

1. **任务运行中**：派发后任务会在后台运行
2. **等待完成**：根据任务复杂度，可能需要几分钟到几十分钟
3. **自动通知**：任务完成后会自动在群里发通知
4. **结果保存**：每次结果会保存到 latest.json（会覆盖）

---

## 快速测试

先试试最简单的任务：

```bash
~/clawd/scripts/dispatch-claude-code.sh -p "说Hello World" -n "test" -g "-1003762750497"
```

这会让 Claude Code 回复 "Hello World"，验证配置是否正常。