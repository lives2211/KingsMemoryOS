# 任务管理CLI工具 - 架构设计文档

## 1. 架构思路

### 1.1 设计原则

- **单一职责**：每个模块只做一件事，做好一件事
- **命令模式**：采用命令模式设计CLI接口，易于扩展新功能
- **数据驱动**：JSON作为数据存储格式，便于人工查看和版本控制
- **错误优先**：所有操作返回明确的成功/失败状态

### 1.2 架构分层

```
┌─────────────────────────────────────────────────────────┐
│                    CLI 界面层 (cli.py)                   │
│         - 参数解析、命令分发、输出格式化                   │
├─────────────────────────────────────────────────────────┤
│                   业务逻辑层 (commands/)                  │
│    - add, list, done, delete, edit 等命令实现            │
├─────────────────────────────────────────────────────────┤
│                   数据访问层 (storage.py)                 │
│         - JSON文件读写、数据验证、备份机制                 │
├─────────────────────────────────────────────────────────┤
│                   模型层 (models.py)                      │
│         - Task数据模型、序列化/反序列化                    │
└─────────────────────────────────────────────────────────┘
```

### 1.3 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| CLI框架 | argparse | Python标准库，无需额外依赖 |
| 数据存储 | JSON | 可读性强，便于版本控制 |
| 日期处理 | datetime | Python标准库 |
| 数据验证 | dataclasses + 自定义验证 | 类型安全，代码简洁 |

---

## 2. 数据模型

### 2.1 Task 模型

```python
@dataclass
class Task:
    """任务数据模型"""
    id: str                    # 唯一标识符 (UUID)
    title: str                 # 任务标题
    description: str           # 任务描述 (可选)
    priority: Priority         # 优先级: LOW, MEDIUM, HIGH, URGENT
    status: Status             # 状态: TODO, IN_PROGRESS, DONE
    due_date: Optional[datetime]  # 截止日期 (可选)
    created_at: datetime       # 创建时间
    updated_at: datetime       # 最后更新时间
    completed_at: Optional[datetime]  # 完成时间
    tags: List[str]            # 标签列表

class Priority(Enum):
    LOW = 1      # 低优先级
    MEDIUM = 2   # 中优先级
    HIGH = 3     # 高优先级
    URGENT = 4   # 紧急

class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
```

### 2.2 数据存储格式 (JSON)

```json
{
  "version": "1.0",
  "last_updated": "2026-03-13T16:45:00",
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "完成架构设计文档",
      "description": "设计任务管理CLI工具的完整架构",
      "priority": "high",
      "status": "done",
      "due_date": "2026-03-14T18:00:00",
      "created_at": "2026-03-13T10:00:00",
      "updated_at": "2026-03-13T16:45:00",
      "completed_at": "2026-03-13T16:45:00",
      "tags": ["设计", "文档"]
    }
  ],
  "metadata": {
    "total_tasks": 1,
    "completed_tasks": 1,
    "pending_tasks": 0
  }
}
```

---

## 3. 命令设计

### 3.1 命令列表

| 命令 | 功能 | 示例 |
|------|------|------|
| `add` | 添加新任务 | `task add "完成报告" --priority high --due 2026-03-15` |
| `list` | 列出任务 | `task list --status todo --priority high` |
| `done` | 标记完成 | `task done <id>` |
| `delete` | 删除任务 | `task delete <id>` |
| `edit` | 编辑任务 | `task edit <id> --title "新标题"` |
| `show` | 查看详情 | `task show <id>` |
| `clear` | 清空已完成 | `task clear --done` |

### 3.2 命令详细设计

#### task add
```
task add <title> [options]

Options:
  -d, --description TEXT    任务描述
  -p, --priority CHOICE     优先级: low/medium/high/urgent (默认: medium)
  --due DATE                截止日期 (格式: YYYY-MM-DD 或 YYYY-MM-DD HH:MM)
  -t, --tags TEXT           标签 (可多次使用)

Examples:
  task add "买牛奶" --priority low
  task add "完成项目报告" -p high --due "2026-03-15 17:00" -t 工作 -t 紧急
```

#### task list
```
task list [options]

Options:
  -s, --status STATUS       按状态过滤: todo/in_progress/done/all (默认: todo)
  -p, --priority PRIORITY   按优先级过滤
  --due-before DATE         截止日期早于
  --due-after DATE          截止日期晚于
  -t, --tag TAG             按标签过滤
  --sort FIELD              排序字段: created/priority/due (默认: created)
  --reverse                 倒序排列
  -l, --limit N             限制显示数量

Examples:
  task list                    # 列出所有待办任务
  task list -s all --sort due  # 按截止日期排序显示所有任务
  task list -p high -t 工作     # 高优先级且标签为"工作"
```

#### task done
```
task done <id>

Arguments:
  id    任务ID (支持部分匹配，如 UUID 前8位)

Examples:
  task done 550e8400          # 完成任务
  task done 550e8400 --undo   # 取消完成
```

#### task delete
```
task delete <id> [options]

Options:
  -f, --force               强制删除，不确认

Examples:
  task delete 550e8400
  task delete 550e8400 -f
```

#### task edit
```
task edit <id> [options]

Options:
  --title TEXT              新标题
  --description TEXT        新描述
  --priority PRIORITY       新优先级
  --due DATE                新截止日期
  --add-tag TEXT            添加标签
  --remove-tag TEXT         移除标签

Examples:
  task edit 550e8400 --priority urgent
  task edit 550e8400 --due "2026-03-20" --add-tag 延期
```

---

## 4. 文件结构建议

```
task-cli/
├── README.md                 # 项目说明
├── DESIGN.md                 # 本设计文档
├── requirements.txt          # 依赖列表
├── setup.py                  # 安装配置
├── pyproject.toml            # 现代Python项目配置
│
├── src/
│   └── task_cli/
│       ├── __init__.py       # 包初始化
│       ├── __main__.py       # 入口点: python -m task_cli
│       ├── cli.py            # CLI主入口和参数解析
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── task.py       # Task数据模型
│       │   ├── priority.py   # Priority枚举
│       │   └── status.py     # Status枚举
│       │
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── add.py        # 添加任务
│       │   ├── list.py       # 列出任务
│       │   ├── done.py       # 完成任务
│       │   ├── delete.py     # 删除任务
│       │   ├── edit.py       # 编辑任务
│       │   ├── show.py       # 查看详情
│       │   └── clear.py      # 清理任务
│       │
│       ├── storage/
│       │   ├── __init__.py
│       │   ├── manager.py    # 存储管理器
│       │   ├── json_store.py # JSON存储实现
│       │   └── backup.py     # 备份机制
│       │
│       └── utils/
│           ├── __init__.py
│           ├── formatters.py # 输出格式化
│           ├── validators.py # 输入验证
│           ├── colors.py     # 终端颜色
│           └── id_utils.py   # ID生成和匹配
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py        # 模型测试
│   ├── test_commands.py      # 命令测试
│   ├── test_storage.py       # 存储测试
│   └── conftest.py           # pytest配置
│
└── docs/
    └── usage.md              # 使用文档
```

---

## 5. 核心接口定义

### 5.1 Task 模型接口

```python
# models/task.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: Status = Status.TODO
    due_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """序列化为字典"""
        pass

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """从字典反序列化"""
        pass

    def mark_done(self) -> None:
        """标记为完成"""
        pass

    def mark_todo(self) -> None:
        """标记为待办"""
        pass

    def is_overdue(self) -> bool:
        """检查是否逾期"""
        pass
```

### 5.2 存储接口

```python
# storage/manager.py

from typing import List, Optional
from ..models.task import Task

class StorageManager:
    """存储管理器接口"""

    def __init__(self, data_file: str):
        """
        初始化存储管理器
        
        Args:
            data_file: JSON数据文件路径
        """
        pass

    def