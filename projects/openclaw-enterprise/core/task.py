"""
任务模型 - 借鉴 Paperclip 的任务生命周期管理
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum
import json

class TaskStatus(Enum):
    """任务状态 - Paperclip 风格"""
    BACKLOG = "backlog"           # 待分配
    ASSIGNED = "assigned"         # 已指派
    IN_PROGRESS = "in_progress"   # 进行中
    REVIEW = "review"             # 审核中
    DONE = "done"                 # 已完成
    REJECTED = "rejected"         # 被拒绝
    BLOCKED = "blocked"           # 被阻塞

class TaskPriority(Enum):
    """任务优先级"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class TaskBudget:
    """预算控制 - Paperclip 核心特性"""
    total: float = 0.0
    spent: float = 0.0
    currency: str = "USD"
    alerts: List[Dict] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.alerts:
            self.alerts = [
                {"threshold": 0.8, "action": "warn"},
                {"threshold": 1.0, "action": "block"}
            ]
    
    @property
    def remaining(self) -> float:
        return self.total - self.spent
    
    @property
    def utilization(self) -> float:
        return self.spent / self.total if self.total > 0 else 0
    
    def check_alerts(self) -> Optional[str]:
        """检查预算告警"""
        util = self.utilization
        for alert in sorted(self.alerts, key=lambda x: x["threshold"]):
            if util >= alert["threshold"]:
                return alert["action"]
        return None
    
    def spend(self, amount: float) -> bool:
        """花费预算，返回是否允许"""
        if self.spent + amount > self.total:
            return False
        self.spent += amount
        return True

@dataclass
class TaskAudit:
    """审计日志条目"""
    timestamp: datetime
    event: str
    actor: str
    details: Dict[str, Any]

@dataclass
class Task:
    """
    任务模型 - 借鉴 Paperclip
    
    核心字段:
    - id: 唯一标识
    - title/description: 任务内容
    - status: 生命周期状态
    - agent_id: 指派给哪个 Agent
    - budget: 预算控制
    - audit_log: 完整审计追踪
    """
    
    # 基础信息
    id: str
    title: str
    description: str
    
    # 状态
    status: TaskStatus = TaskStatus.BACKLOG
    priority: TaskPriority = TaskPriority.NORMAL
    
    # 指派
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    
    # 预算
    budget: TaskBudget = field(default_factory=TaskBudget)
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    assigned_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # 元数据
    requester: str = "unknown"
    tags: List[str] = field(default_factory=list)
    
    # 审计日志
    audit_log: List[TaskAudit] = field(default_factory=list)
    
    # 结果
    result: Optional[Dict] = None
    deliverables: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)
        if isinstance(self.priority, str):
            self.priority = TaskPriority(self.priority)
    
    def assign(self, agent_id: str, agent_name: str):
        """指派任务"""
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.status = TaskStatus.ASSIGNED
        self.assigned_at = datetime.now()
        self._log_audit("assigned", "system", {"agent_id": agent_id})
    
    def start(self):
        """开始执行"""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()
        self._log_audit("started", self.agent_id or "unknown", {})
    
    def complete(self, result: Dict, deliverables: List[str] = None):
        """完成任务"""
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now()
        self.result = result
        if deliverables:
            self.deliverables = deliverables
        self._log_audit("completed", self.agent_id or "unknown", {"result": result})
    
    def reject(self, reason: str):
        """拒绝任务"""
        self.status = TaskStatus.REJECTED
        self._log_audit("rejected", self.agent_id or "unknown", {"reason": reason})
    
    def spend_budget(self, amount: float, reason: str = "") -> bool:
        """花费预算"""
        if not self.budget.spend(amount):
            self._log_audit("budget_exceeded", self.agent_id or "system", {"attempted": amount})
            return False
        
        self._log_audit("budget_spent", self.agent_id or "system", {"amount": amount, "reason": reason})
        
        # 检查告警
        alert = self.budget.check_alerts()
        if alert:
            self._log_audit("budget_alert", "system", {"alert": alert, "utilization": self.budget.utilization})
        
        return True
    
    def _log_audit(self, event: str, actor: str, details: Dict):
        """记录审计日志"""
        self.audit_log.append(TaskAudit(
            timestamp=datetime.now(),
            event=event,
            actor=actor,
            details=details
        ))
    
    def to_dict(self) -> Dict:
        """序列化"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "budget": {
                "total": self.budget.total,
                "spent": self.budget.spent,
                "remaining": self.budget.remaining,
                "utilization": round(self.budget.utilization, 2)
            },
            "created_at": self.created_at.isoformat(),
            "assigned_at": self.assigned_at.isoformat() if self.assigned_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "requester": self.requester,
            "tags": self.tags,
            "audit_log": [
                {
                    "timestamp": a.timestamp.isoformat(),
                    "event": a.event,
                    "actor": a.actor,
                    "details": a.details
                }
                for a in self.audit_log
            ],
            "result": self.result,
            "deliverables": self.deliverables
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Task":
        """反序列化"""
        task = cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            status=TaskStatus(data.get("status", "backlog")),
            priority=TaskPriority(data.get("priority", "normal")),
            agent_id=data.get("agent_id"),
            agent_name=data.get("agent_name"),
            budget=TaskBudget(
                total=data.get("budget", {}).get("total", 0),
                spent=data.get("budget", {}).get("spent", 0)
            ),
            requester=data.get("requester", "unknown"),
            tags=data.get("tags", []),
            result=data.get("result"),
            deliverables=data.get("deliverables", [])
        )
        
        # 解析时间戳
        if data.get("created_at"):
            task.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("assigned_at"):
            task.assigned_at = datetime.fromisoformat(data["assigned_at"])
        if data.get("started_at"):
            task.started_at = datetime.fromisoformat(data["started_at"])
        if data.get("completed_at"):
            task.completed_at = datetime.fromisoformat(data["completed_at"])
        
        return task
