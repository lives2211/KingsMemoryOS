#!/usr/bin/env python3
"""
OpenClaw 企业版 - Ticket 任务系统
参考 Paperclip 的任务管理功能
"""

import json
import uuid
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TicketStatus(Enum):
    """任务状态"""
    BACKLOG = "backlog"      # 待办
    TODO = "todo"            # 准备就绪
    IN_PROGRESS = "in_progress"  # 进行中
    REVIEW = "review"        # 审核中
    DONE = "done"            # 已完成
    BLOCKED = "blocked"      # 被阻塞
    CANCELLED = "cancelled"  # 已取消


class TicketPriority(Enum):
    """任务优先级"""
    P0 = "P0"  # 紧急
    P1 = "P1"  # 高
    P2 = "P2"  # 中
    P3 = "P3"  # 低


@dataclass
class Ticket:
    """任务票"""
    id: str
    title: str
    description: str
    status: str
    priority: str
    assignee: str  # 指派给哪个Agent
    creator: str   # 创建者
    project: str   # 所属项目
    
    # 时间戳
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    deadline: Optional[str] = None
    
    # 执行信息
    estimated_cost: float = 0.0  # 预估成本
    actual_cost: float = 0.0     # 实际成本
    
    # 委派链
    parent_ticket: Optional[str] = None  # 父任务
    sub_tickets: List[str] = field(default_factory=list)  # 子任务
    
    # 上下文
    context: Dict = field(default_factory=dict)
    
    # 审核
    reviewer: Optional[str] = None
    review_notes: Optional[str] = None
    
    # 结果
    result: Optional[str] = None
    artifacts: List[str] = field(default_factory=list)  # 产出物路径


class TicketSystem:
    """Ticket 任务系统"""
    
    def __init__(self, data_dir: str = "data/tickets"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.tickets: Dict[str, Ticket] = {}
        self.load_tickets()
        
        # 状态流转规则
        self.status_flow = {
            TicketStatus.BACKLOG.value: [TicketStatus.TODO.value, TicketStatus.CANCELLED.value],
            TicketStatus.TODO.value: [TicketStatus.IN_PROGRESS.value, TicketStatus.BLOCKED.value],
            TicketStatus.IN_PROGRESS.value: [TicketStatus.REVIEW.value, TicketStatus.BLOCKED.value],
            TicketStatus.REVIEW.value: [TicketStatus.DONE.value, TicketStatus.IN_PROGRESS.value],
            TicketStatus.BLOCKED.value: [TicketStatus.IN_PROGRESS.value, TicketStatus.TODO.value],
            TicketStatus.DONE.value: [],
            TicketStatus.CANCELLED.value: []
        }
        
        # Agent 能力映射
        self.agent_capabilities = {
            "main": ["dispatch", "review", "coordinate"],
            "bingbing": ["content", "design", "creative"],
            "yitai": ["coding", "debug", "technical"],
            "daping": ["monitor", "analyze", "test"],
            "spikey": ["audit", "review", "quality"],
            "xiaohongcai": ["social", "xiaohongshu", "wechat"]
        }
    
    def load_tickets(self):
        """加载任务"""
        tickets_file = self.data_dir / "tickets.json"
        if tickets_file.exists():
            with open(tickets_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for ticket_id, ticket_data in data.items():
                    self.tickets[ticket_id] = Ticket(**ticket_data)
            logger.info(f"✅ 已加载 {len(self.tickets)} 个任务")
    
    def save_tickets(self):
        """保存任务"""
        tickets_file = self.data_dir / "tickets.json"
        data = {tid: asdict(ticket) for tid, ticket in self.tickets.items()}
        with open(tickets_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_ticket(self, title: str, description: str, 
                     assignee: str, project: str = "default",
                     priority: str = TicketPriority.P2.value,
                     parent_ticket: Optional[str] = None,
                     deadline: Optional[str] = None,
                     estimated_cost: float = 0.0,
                     context: Optional[Dict] = None) -> Ticket:
        """创建任务"""
        ticket_id = f"TK-{uuid.uuid4().hex[:8].upper()}"
        
        ticket = Ticket(
            id=ticket_id,
            title=title,
            description=description,
            status=TicketStatus.BACKLOG.value,
            priority=priority,
            assignee=assignee,
            creator="main",  # 默认由总管创建
            project=project,
            created_at=datetime.now().isoformat(),
            deadline=deadline,
            estimated_cost=estimated_cost,
            parent_ticket=parent_ticket,
            context=context or {}
        )
        
        self.tickets[ticket_id] = ticket
        self.save_tickets()
        
        logger.info(f"✅ 任务已创建: {ticket_id} - {title} → @{assignee}")
        
        # 如果有父任务，更新父任务的子任务列表
        if parent_ticket and parent_ticket in self.tickets:
            self.tickets[parent_ticket].sub_tickets.append(ticket_id)
            self.save_tickets()
        
        return ticket
    
    def update_status(self, ticket_id: str, new_status: str, 
                     notes: Optional[str] = None) -> bool:
        """更新任务状态"""
        if ticket_id not in self.tickets:
            logger.error(f"❌ 任务不存在: {ticket_id}")
            return False
        
        ticket = self.tickets[ticket_id]
        current_status = ticket.status
        
        # 检查状态流转是否合法
        if new_status not in self.status_flow.get(current_status, []):
            logger.error(f"❌ 非法状态流转: {current_status} → {new_status}")
            return False
        
        # 更新状态
        ticket.status = new_status
        
        # 更新时间戳
        if new_status == TicketStatus.IN_PROGRESS.value and not ticket.started_at:
            ticket.started_at = datetime.now().isoformat()
        elif new_status == TicketStatus.DONE.value:
            ticket.completed_at = datetime.now().isoformat()
        
        # 添加备注
        if notes:
            ticket.context["status_notes"] = notes
        
        self.save_tickets()
        logger.info(f"✅ 任务状态更新: {ticket_id} → {new_status}")
        
        return True
    
    def assign_ticket(self, ticket_id: str, new_assignee: str) -> bool:
        """重新指派任务"""
        if ticket_id not in self.tickets:
            return False
        
        old_assignee = self.tickets[ticket_id].assignee
        self.tickets[ticket_id].assignee = new_assignee
        self.save_tickets()
        
        logger.info(f"✅ 任务重新指派: {ticket_id} {old_assignee} → {new_assignee}")
        return True
    
    def delegate_ticket(self, ticket_id: str, sub_assignee: str,
                       sub_title: str, sub_description: str) -> Optional[Ticket]:
        """
        委派子任务
        
        例如：总管(main)把任务委派给技术官(yitai)
        """
        if ticket_id not in self.tickets:
            return None
        
        parent = self.tickets[ticket_id]
        
        # 创建子任务
        sub_ticket = self.create_ticket(
            title=sub_title,
            description=sub_description,
            assignee=sub_assignee,
            project=parent.project,
            priority=parent.priority,
            parent_ticket=ticket_id,
            deadline=parent.deadline
        )
        
        # 更新父任务状态为进行中
        if parent.status == TicketStatus.TODO.value:
            self.update_status(ticket_id, TicketStatus.IN_PROGRESS.value, 
                             f"已委派子任务: {sub_ticket.id}")
        
        logger.info(f"✅ 任务委派: {ticket_id} → {sub_ticket.id} @{sub_assignee}")
        
        return sub_ticket
    
    def complete_ticket(self, ticket_id: str, result: str,
                       artifacts: Optional[List[str]] = None,
                       actual_cost: float = 0.0) -> bool:
        """完成任务"""
        if ticket_id not in self.tickets:
            return False
        
        ticket = self.tickets[ticket_id]
        ticket.result = result
        ticket.artifacts = artifacts or []
        ticket.actual_cost = actual_cost
        
        # 更新状态为审核中（需要审核后才算完成）
        self.update_status(ticket_id, TicketStatus.REVIEW.value, 
                         f"任务完成，等待审核")
        
        # 如果有父任务，检查是否所有子任务都完成
        if ticket.parent_ticket:
            self._check_parent_completion(ticket.parent_ticket)
        
        self.save_tickets()
        logger.info(f"✅ 任务完成，等待审核: {ticket_id}")
        
        return True
    
    def review_ticket(self, ticket_id: str, reviewer: str,
                     approved: bool, notes: Optional[str] = None) -> bool:
        """审核任务"""
        if ticket_id not in self.tickets:
            return False
        
        ticket = self.tickets[ticket_id]
        ticket.reviewer = reviewer
        ticket.review_notes = notes
        
        if approved:
            self.update_status(ticket_id, TicketStatus.DONE.value, 
                             f"审核通过 by {reviewer}")
            logger.info(f"✅ 任务审核通过: {ticket_id} by {reviewer}")
        else:
            self.update_status(ticket_id, TicketStatus.IN_PROGRESS.value,
                             f"审核未通过 by {reviewer}: {notes}")
            logger.info(f"❌ 任务审核未通过: {ticket_id} by {reviewer}")
        
        self.save_tickets()
        return True
    
    def _check_parent_completion(self, parent_id: str):
        """检查父任务是否所有子任务都完成"""
        if parent_id not in self.tickets:
            return
        
        parent = self.tickets[parent_id]
        if not parent.sub_tickets:
            return
        
        all_done = all(
            self.tickets[sub_id].status == TicketStatus.DONE.value
            for sub_id in parent.sub_tickets
            if sub_id in self.tickets
        )
        
        if all_done:
            self.update_status(parent_id, TicketStatus.REVIEW.value,
                             "所有子任务已完成")
            logger.info(f"✅ 父任务所有子任务完成: {parent_id}")
    
    def get_tickets_by_agent(self, agent_id: str, 
                            status: Optional[str] = None) -> List[Ticket]:
        """获取Agent的任务列表"""
        tickets = [t for t in self.tickets.values() if t.assignee == agent_id]
        
        if status:
            tickets = [t for t in tickets if t.status == status]
        
        # 按优先级排序
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        tickets.sort(key=lambda x: priority_order.get(x.priority, 99))
        
        return tickets
    
    def get_ticket_board(self, project: Optional[str] = None) -> Dict:
        """获取任务看板"""
        tickets = self.tickets.values()
        
        if project:
            tickets = [t for t in tickets if t.project == project]
        
        board = {
            "backlog": [],
            "todo": [],
            "in_progress": [],
            "review": [],
            "done": [],
            "blocked": []
        }
        
        for ticket in tickets:
            if ticket.status in board:
                board[ticket.status].append({
                    "id": ticket.id,
                    "title": ticket.title,
                    "priority": ticket.priority,
                    "assignee": ticket.assignee,
                    "deadline": ticket.deadline
                })
        
        return board
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = len(self.tickets)
        by_status = {}
        by_agent = {}
        
        for ticket in self.tickets.values():
            # 按状态统计
            by_status[ticket.status] = by_status.get(ticket.status, 0) + 1
            
            # 按Agent统计
            by_agent[ticket.assignee] = by_agent.get(ticket.assignee, 0) + 1
        
        return {
            "total_tickets": total,
            "by_status": by_status,
            "by_agent": by_agent,
            "completion_rate": (
                by_status.get(TicketStatus.DONE.value, 0) / total * 100
                if total > 0 else 0
            )
        }


# CLI 接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ticket 任务系统")
    parser.add_argument("--create", nargs=4, metavar=("TITLE", "DESC", "ASSIGNEE", "PROJECT"),
                       help="创建任务")
    parser.add_argument("--status", nargs=2, metavar=("TICKET_ID", "NEW_STATUS"),
                       help="更新任务状态")
    parser.add_argument("--delegate", nargs=4, metavar=("TICKET_ID", "SUB_ASSIGNEE", "SUB_TITLE", "SUB_DESC"),
                       help="委派子任务")
    parser.add_argument("--complete", nargs=2, metavar=("TICKET_ID", "RESULT"),
                       help="完成任务")
    parser.add_argument("--review", nargs=4, metavar=("TICKET_ID", "REVIEWER", "APPROVED", "NOTES"),
                       help="审核任务")
    parser.add_argument("--board", action="store_true", help="显示任务看板")
    parser.add_argument("--list", help="列出Agent的任务")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    
    args = parser.parse_args()
    
    system = TicketSystem()
    
    if args.create:
        ticket = system.create_ticket(
            title=args.create[0],
            description=args.create[1],
            assignee=args.create[2],
            project=args.create[3]
        )
        print(f"✅ 任务已创建: {ticket.id}")
    elif args.status:
        system.update_status(args.status[0], args.status[1])
    elif args.delegate:
        sub = system.delegate_ticket(
            args.delegate[0], args.delegate[1], args.delegate[2], args.delegate[3]
        )
        if sub:
            print(f"✅ 子任务已创建: {sub.id}")
    elif args.complete:
        system.complete_ticket(args.complete[0], args.complete[1])
    elif args.review:
        approved = args.review[2].lower() == "true"
        system.review_ticket(args.review[0], args.review[1], approved, args.review[3])
    elif args.board:
        board = system.get_ticket_board()
        print(json.dumps(board, ensure_ascii=False, indent=2))
    elif args.list:
        tickets = system.get_tickets_by_agent(args.list)
        for t in tickets:
            print(f"[{t.priority}] {t.id}: {t.title} ({t.status})")
    elif args.stats:
        stats = system.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print("请指定操作，使用 --help 查看帮助")
