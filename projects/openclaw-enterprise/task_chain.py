"""
任务委派链 - Paperclip 核心特性
支持父任务 → 子任务的层级委派
"""

import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

API_URL = "http://localhost:3100"

@dataclass
class SubTask:
    """子任务"""
    title: str
    description: str
    agent_id: str
    budget: float
    depends_on: List[str] = None
    
    def __post_init__(self):
        if self.depends_on is None:
            self.depends_on = []


class TaskChain:
    """
    任务委派链
    
    Paperclip 特性：复杂任务可以拆分为子任务，形成依赖图
    """
    
    def __init__(self):
        self.subtask_templates = {
            "website": [
                SubTask("需求分析", "分析网站需求", "daping", 10),
                SubTask("UI设计", "设计网站界面", "bingbing", 20),
                SubTask("前端开发", "开发前端页面", "yitai", 30),
                SubTask("后端开发", "开发后端API", "yitai", 30),
                SubTask("测试验收", "测试并验收", "spikey", 10),
            ],
            "content": [
                SubTask("选题策划", "策划内容选题", "daping", 5),
                SubTask("文案撰写", "撰写文案内容", "bingbing", 15),
                SubTask("配图设计", "设计配图", "bingbing", 10),
                SubTask("发布运营", "发布并运营", "xiaohongcai", 5),
            ],
            "data": [
                SubTask("数据源调研", "调研数据来源", "daping", 10),
                SubTask("爬虫开发", "开发爬虫脚本", "yitai", 20),
                SubTask("数据清洗", "清洗数据", "yitai", 15),
                SubTask("分析报告", "生成分析报告", "daping", 15),
            ]
        }
    
    def decompose(self, parent_task: Dict) -> List[Dict]:
        """
        分解父任务为子任务
        
        Args:
            parent_task: 父任务信息
            
        Returns:
            创建的子任务列表
        """
        description = parent_task.get("description", "").lower()
        
        # 根据关键词选择模板
        template = None
        for key, subtasks in self.subtask_templates.items():
            if key in description:
                template = subtasks
                break
        
        if not template:
            # 默认不分解
            return []
        
        # 创建子任务
        created_tasks = []
        parent_id = parent_task.get("id")
        
        for i, subtask in enumerate(template):
            # 调整预算（按比例）
            ratio = subtask.budget / sum(t.budget for t in template)
            adjusted_budget = parent_task.get("budget", {}).get("total", 0) * ratio
            
            # 创建子任务
            result = self._create_subtask(
                parent_id=parent_id,
                title=f"[{parent_task.get('title', '父任务')}] {subtask.title}",
                description=subtask.description,
                agent_id=subtask.agent_id,
                budget=adjusted_budget,
                depends_on=[created_tasks[-1]["id"]] if created_tasks else []
            )
            
            if result:
                created_tasks.append(result)
        
        return created_tasks
    
    def _create_subtask(self, parent_id: str, title: str, description: str, agent_id: str, budget: float, depends_on: List[str]) -> Optional[Dict]:
        """创建子任务"""
        try:
            resp = requests.post(
                f"{API_URL}/api/tasks",
                json={
                    "title": title,
                    "description": description,
                    "budget": budget,
                    "priority": "normal",
                    "requester": f"parent:{parent_id}",
                    "tags": ["subtask", f"parent:{parent_id}"] + depends_on
                },
                timeout=10
            )
            return resp.json() if resp.status_code == 201 else None
        except Exception as e:
            print(f"[TaskChain] 创建子任务失败: {e}")
            return None
    
    def get_task_tree(self, parent_id: str) -> Dict:
        """
        获取任务树
        
        Args:
            parent_id: 父任务ID
            
        Returns:
            任务树结构
        """
        try:
            # 获取所有任务
            resp = requests.get(f"{API_URL}/api/tasks", timeout=5)
            all_tasks = resp.json()
            
            # 找到父任务
            parent = next((t for t in all_tasks if t["id"] == parent_id), None)
            if not parent:
                return {}
            
            # 找到子任务
            children = [
                t for t in all_tasks
                if f"parent:{parent_id}" in t.get("tags", [])
            ]
            
            return {
                "parent": parent,
                "children": children,
                "total_budget": parent.get("budget", {}).get("total", 0) + sum(
                    c.get("budget", {}).get("total", 0) for c in children
                ),
                "progress": self._calculate_progress([parent] + children)
            }
        except Exception as e:
            print(f"[TaskChain] 获取任务树失败: {e}")
            return {}
    
    def _calculate_progress(self, tasks: List[Dict]) -> float:
        """计算进度"""
        if not tasks:
            return 0.0
        
        done = sum(1 for t in tasks if t.get("status") == "done")
        return done / len(tasks)
    
    def auto_dispatch_complex(self, message: str, user: str) -> Dict:
        """
        自动识别复杂任务并委派
        
        如果任务复杂，自动创建子任务链
        """
        # 先创建父任务
        try:
            resp = requests.post(
                f"{API_URL}/api/tasks",
                json={
                    "title": message[:50],
                    "description": message,
                    "budget": 100,  # 默认预算
                    "priority": "normal",
                    "requester": user,
                    "tags": ["complex"]
                },
                timeout=10
            )
            
            if resp.status_code != 201:
                return {"error": "创建父任务失败"}
            
            parent = resp.json()
            
            # 尝试分解
            subtasks = self.decompose(parent)
            
            return {
                "parent": parent,
                "subtasks": subtasks,
                "decomposed": len(subtasks) > 0,
                "message": f"已创建父任务 + {len(subtasks)} 个子任务" if subtasks else "任务已创建（无需分解）"
            }
            
        except Exception as e:
            return {"error": str(e)}


# 全局实例
chain = TaskChain()


def test_task_chain():
    """测试任务链"""
    print("🔗 任务委派链测试\n")
    
    # 测试分解
    parent = {
        "id": "TASK-PARENT-001",
        "title": "开发一个网站",
        "description": "帮我开发一个公司官网，包含前后端",
        "budget": {"total": 100}
    }
    
    print(f"父任务: {parent['title']}")
    print(f"预算: ${parent['budget']['total']}\n")
    
    subtasks = chain.decompose(parent)
    
    print(f"分解为 {len(subtasks)} 个子任务:\n")
    for i, st in enumerate(subtasks, 1):
        print(f"{i}. {st['title']}")
        print(f"   Agent: @{st['agent_name']}")
        print(f"   预算: ${st['budget']['total']}")
        print(f"   状态: {st['status']}\n")


if __name__ == "__main__":
    test_task_chain()
