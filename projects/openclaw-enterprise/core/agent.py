"""
Agent 基类 - 借鉴 Paperclip 的 Agent 架构
每个 Agent 是独立的 OpenClaw 会话，通过心跳机制自主运行
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from datetime import datetime
import json

@dataclass
class AgentConfig:
    """Agent 配置"""
    id: str
    name: str
    role: str
    skills: List[str]
    model: str = "claude-3-5-sonnet"
    session_label: str = ""
    heartbeat_interval: int = 300  # 5分钟
    max_concurrent_tasks: int = 3
    cost_per_token: float = 0.0001
    
    def __post_init__(self):
        if not self.session_label:
            self.session_label = self.id

@dataclass
class AgentState:
    """Agent 运行状态"""
    status: str = "idle"  # idle, busy, offline
    current_task: Optional[str] = None
    task_history: List[str] = field(default_factory=list)
    last_heartbeat: Optional[datetime] = None
    total_cost: float = 0.0
    tokens_used: int = 0

class BaseAgent:
    """
    Agent 基类
    
    借鉴 Paperclip 的设计理念:
    1. 每个 Agent 是独立的执行单元
    2. 通过心跳机制自主检查任务
    3. 有自己的状态、成本追踪
    4. 可以接收委派、汇报进度
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.state = AgentState()
        self.task_handlers: Dict[str, Callable] = {}
        
    def register_handler(self, task_type: str, handler: Callable):
        """注册任务处理器"""
        self.task_handlers[task_type] = handler
        
    def heartbeat(self) -> Dict:
        """
        心跳方法 - 核心机制
        
        Paperclip 的核心创新: Agent 定期唤醒，自主决策
        """
        self.state.last_heartbeat = datetime.now()
        
        # 检查是否有新任务
        pending_tasks = self._fetch_pending_tasks()
        
        if pending_tasks and self.state.status == "idle":
            # 自动领取任务
            task = pending_tasks[0]
            self._claim_task(task)
            
        return {
            "agent_id": self.config.id,
            "status": self.state.status,
            "current_task": self.state.current_task,
            "last_heartbeat": self.state.last_heartbeat.isoformat(),
            "total_cost": self.state.total_cost
        }
        
    def _fetch_pending_tasks(self) -> List[Dict]:
        """获取待处理任务"""
        # 通过 API 查询分配给自己的任务
        import requests
        try:
            resp = requests.get(
                f"http://localhost:3100/api/tasks?agent={self.config.id}&status=assigned",
                timeout=5
            )
            return resp.json() if resp.status_code == 200 else []
        except:
            return []
        
    def _claim_task(self, task: Dict):
        """领取任务"""
        self.state.status = "busy"
        self.state.current_task = task["id"]
        self.state.task_history.append(task["id"])
        
        # 通知 OpenClaw 会话
        self._notify_openclaw(task)
        
    def _notify_openclaw(self, task: Dict):
        """通知 OpenClaw Agent 会话"""
        import subprocess
        
        message = f"""【新任务】{task['title']}
【描述】{task['description']}
【任务ID】{task['id']}
【预算】${task.get('budget', 0)}

请回复"收到"确认，并开始执行。
完成后使用 /complete {task['id']} 汇报结果。
"""
        
        try:
            subprocess.run(
                ["openclaw", "sessions", "send",
                 "--label", self.config.session_label,
                 "--message", message],
                capture_output=True,
                timeout=10
            )
        except Exception as e:
            print(f"[Agent {self.config.id}] 通知失败: {e}")
            
    def complete_task(self, task_id: str, result: Dict):
        """完成任务"""
        if self.state.current_task == task_id:
            self.state.status = "idle"
            self.state.current_task = None
            
            # 更新成本
            tokens = result.get('tokens_used', 0)
            self.state.tokens_used += tokens
            self.state.total_cost += tokens * self.config.cost_per_token
            
            # 上报结果
            self._report_completion(task_id, result)
            
    def _report_completion(self, task_id: str, result: Dict):
        """上报任务完成"""
        import requests
        try:
            requests.post(
                f"http://localhost:3100/api/tasks/{task_id}/complete",
                json=result,
                timeout=5
            )
        except Exception as e:
            print(f"[Agent {self.config.id}] 上报失败: {e}")
            
    def to_dict(self) -> Dict:
        """序列化"""
        return {
            "config": {
                "id": self.config.id,
                "name": self.config.name,
                "role": self.config.role,
                "skills": self.config.skills,
                "model": self.config.model
            },
            "state": {
                "status": self.state.status,
                "current_task": self.state.current_task,
                "task_count": len(self.state.task_history),
                "last_heartbeat": self.state.last_heartbeat.isoformat() if self.state.last_heartbeat else None,
                "total_cost": round(self.state.total_cost, 4),
                "tokens_used": self.state.tokens_used
            }
        }
