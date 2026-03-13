"""
任务链自动化 V3.0
复杂任务自动分解为子任务链，并行执行
"""

import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from simple_dispatcher import TRUE_AGENTS, SHARED_TASKS_DIR, ensure_shared_dir


@dataclass
class SubTask:
    """子任务定义"""
    id: str
    title: str
    description: str
    agent_id: str
    depends_on: List[str]
    estimated_time: int
    deliverables: List[str]


class TaskChainAutomator:
    """任务链自动化器"""
    
    TEMPLATES = {
        "website": {
            "subtasks": [
                {"title": "需求分析", "agent": "daping", "time": 60},
                {"title": "UI设计", "agent": "bingbing", "time": 120},
                {"title": "前端开发", "agent": "yitai", "time": 240},
                {"title": "后端开发", "agent": "yitai", "time": 300},
                {"title": "测试验收", "agent": "spikey", "time": 120},
            ]
        },
        "content": {
            "subtasks": [
                {"title": "选题策划", "agent": "daping", "time": 30},
                {"title": "文案撰写", "agent": "bingbing", "time": 90},
                {"title": "配图设计", "agent": "bingbing", "time": 60},
                {"title": "发布运营", "agent": "xiaohongcai", "time": 30},
            ]
        }
    }
    
    def detect_task_type(self, description: str) -> Optional[str]:
        """检测任务类型"""
        desc_lower = description.lower()
        keywords = {
            "website": ["网站", "web", "前端", "后端"],
            "content": ["内容", "文章", "文案", "公众号"]
        }
        for task_type, words in keywords.items():
            if any(w in desc_lower for w in words):
                return task_type
        return None
    
    def decompose_task(self, parent_task: Dict) -> List[SubTask]:
        """分解父任务为子任务链"""
        task_type = self.detect_task_type(parent_task.get("description", ""))
        
        if not task_type or task_type not in self.TEMPLATES:
            return [SubTask(
                id=f"{parent_task['id']}-001",
                title=parent_task['title'],
                description=parent_task['description'],
                agent_id="yitai",
                depends_on=[],
                estimated_time=120,
                deliverables=["交付物"]
            )]
        
        template = self.TEMPLATES[task_type]
        subtasks = []
        
        for i, sub in enumerate(template["subtasks"]):
            depends = [f"{parent_task['id']}-{i:03d}"] if i > 0 else []
            
            subtask = SubTask(
                id=f"{parent_task['id']}-{i+1:03d}",
                title=f"[{parent_task['title']}] {sub['title']}",
                description=sub['title'],
                agent_id=sub['agent'],
                depends_on=depends,
                estimated_time=sub['time'],
                deliverables=[]
            )
            subtasks.append(subtask)
        
        return subtasks
    
    def create_chain(self, parent_task: Dict) -> Dict:
        """创建任务链"""
        subtasks = self.decompose_task(parent_task)
        
        return {
            "parent": parent_task,
            "subtasks": [
                {
                    "id": s.id,
                    "title": s.title,
                    "agent_id": s.agent_id,
                    "agent_role": TRUE_AGENTS.get(s.agent_id, {}).get("role", "未知"),
                    "depends_on": s.depends_on,
                    "estimated_time": s.estimated_time
                }
                for s in subtasks
            ],
            "total_time": sum(s.estimated_time for s in subtasks),
            "status": "created"
        }


if __name__ == "__main__":
    automator = TaskChainAutomator()
    
    parent_task = {
        'id': 'WEBSITE-001',
        'title': '开发公司官网',
        'description': '帮我开发一个公司官网',
        'budget': {'total': 500}
    }
    
    chain = automator.create_chain(parent_task)
    print(json.dumps(chain, ensure_ascii=False, indent=2))
