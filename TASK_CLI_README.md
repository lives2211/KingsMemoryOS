# 任务管理CLI工具

## 快速开始

```bash
# 添加任务
python3 task_cli.py add "完成任务报告" --priority high

# 列出所有任务
python3 task_cli.py list

# 列出待办任务
python3 task_cli.py list todo

# 标记完成
python3 task_cli.py done 1

# 删除任务
python3 task_cli.py delete 1
```

## 功能特性

- ✅ **add** - 添加任务，支持优先级 (high/medium/low)
- ✅ **list** - 列出任务，支持状态筛选
- ✅ **done** - 标记任务完成
- ✅ **delete** - 删除任务
- ✅ 数据持久化存储 (JSON格式)
- ✅ 自动ID生成
- ✅ 按优先级和创建时间排序

## 数据存储

任务数据存储在: `~/.task_cli/tasks.json`

## 文件位置

- 代码: `/home/fengxueda/.openclaw/workspace/task_cli.py`
- 说明: `/home/fengxueda/.openclaw/workspace/TASK_CLI_README.md`
