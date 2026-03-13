#!/usr/bin/env python3
"""
OpenClaw → Paperclip 集成客户端
实现 OpenClaw Agent 与 Paperclip API 的双向通信
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Optional


class PaperclipClient:
    """
    Paperclip API 客户端
    
    功能：
    1. Agent 状态同步
    2. 任务创建和查询
    3. 预算检查
    4. 任务委派
    5. 组织架构获取
    """
    
    def __init__(self, base_url: str = "http://localhost:3100"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """发送 HTTP 请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    # ===== Agent API =====
    
    def list_agents(self) -> List[Dict]:
        """获取所有 Agent"""
        result = self._request("GET", "/api/agents")
        return result.get("agents", [])
    
    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """获取 Agent 详情"""
        result = self._request("GET", f"/api/agents/{agent_id}")
        return result if result.get("id") else None
    
    def update_agent_status(self, agent_id: str, status: str) -> Dict:
        """更新 Agent 状态"""
        return self._request("POST", f"/api/agents/{agent_id}/status", json={"status": status})
    
    # ===== Task API =====
    
    def create_task(self, title: str, description: str, assignee: str,
                   priority: str = "P2", budget: float = 0.0) -> Dict:
        """创建任务"""
        task_data = {
            "title": title,
            "description": description,
            "assignee": assignee,
            "priority": priority,
            "budget": budget,
            "status": "backlog"
        }
        return self._request("POST", f"/api/agents/{assignee}/tasks", json=task_data)
    
    def list_tasks(self, status: Optional[str] = None, assignee: Optional[str] = None) -> List[Dict]:
        """列出任务"""
        params = {}
        if status:
            params["status"] = status
        if assignee:
            params["assignee"] = assignee
        
        result = self._request("GET", "/api/tasks", params=params)
        return result.get("tasks", [])
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """获取任务详情"""
        result = self._request("GET", f"/api/tasks/{task_id}")
        return result if result.get("id") else None
    
    def complete_task(self, task_id: str, cost: float = 0.0) -> Dict:
        """完成任务"""
        return self._request("POST", f"/api/tasks/{task_id}/complete", json={"cost": cost})
    
    def delegate_task(self, parent_task_id: str, title: str, description: str,
                     sub_assignee: str) -> Dict:
        """委派子任务"""
        sub_task = {
            "title": title,
            "description": description,
            "assignee": sub_assignee,
            "priority": "P2",
            "budget": 0.0
        }
        return self._request("POST", f"/api/tasks/{parent_task_id}/delegate",
                           json={"sub_task": sub_task, "sub_assignee": sub_assignee})
    
    # ===== Budget API =====
    
    def check_budget(self, agent_id: str, estimated_cost: float) -> Dict:
        """检查预算"""
        agent = self.get_agent(agent_id)
        if not agent:
            return {"allowed": False, "error": "Agent not found"}
        
        remaining = agent["budget_monthly"] - agent["budget_used"]
        allowed = estimated_cost <= remaining
        
        return {
            "allowed": allowed,
            "remaining": remaining,
            "monthly_budget": agent["budget_monthly"],
            "used": agent["budget_used"],
            "usage_pct": (agent["budget_used"] / agent["budget_monthly"] * 100) if agent["budget_monthly"] > 0 else 0
        }
    
    # ===== Org Chart API =====
    
    def get_org_chart(self) -> Dict:
        """获取组织架构"""
        return self._request("GET", "/api/org/chart")
    
    # ===== Dashboard API =====
    
    def get_dashboard(self) -> Dict:
        """获取仪表盘数据"""
        return self._request("GET", "/api/dashboard")
    
    # ===== OpenClaw Integration =====
    
    def dispatch_to_openclaw(self, agent_id: str, task_title: str, task_desc: str) -> Dict:
        """派发任务到 OpenClaw"""
        return self._request("POST", "/api/openclaw/dispatch", json={
            "agent_id": agent_id,
            "task_title": task_title,
            "task_desc": task_desc
        })
    
    # ===== Smart Dispatch =====
    
    def smart_dispatch(self, title: str, description: str,
                      required_caps: List[str],
                      estimated_cost: float = 0.0) -> Dict:
        """
        智能任务派发
        
        根据所需能力自动匹配最佳 Agent
        """
        # 1. 获取所有 Agent
        agents = self.list_agents()
        
        # 2. 匹配能力
        matched = []
        for agent in agents:
            if agent["id"] == "main":  # 总管不执行
                continue
            
            agent_caps = set(agent.get("capabilities", []))
            required = set(required_caps)
            match_score = len(required & agent_caps)
            
            if match_score > 0:
                matched.append((agent, match_score))
        
        if not matched:
            return {"success": False, "error": "No matching agent found"}
        
        # 3. 按匹配度排序
        matched.sort(key=lambda x: x[1], reverse=True)
        
        # 4. 检查预算并创建任务
        for agent, score in matched:
            budget_check = self.check_budget(agent["id"], estimated_cost)
            if budget_check["allowed"]:
                try:
                    # 5. 创建任务
                    result = self.create_task(
                        title=title,
                        description=description,
                        assignee=agent["id"],
                        priority="P2",
                        budget=estimated_cost
                    )
                    
                    if result.get("success"):
                        return {
                            "success": True,
                            "task": result.get("task"),
                            "assigned_to": agent["id"],
                            "agent_name": agent["name"],
                            "match_score": score,
                            "budget_remaining": budget_check["remaining"]
                        }
                except Exception as e:
                    # 预算不足或创建失败，尝试下一个 Agent
                    continue
        
        # 如果没有 Agent 有足够预算，尝试创建 0 预算任务
        if estimated_cost > 0:
            return self.smart_dispatch(title, description, required_caps, 0.0)
        
        return {"success": False, "error": "All matching agents out of budget"}
    
    # ===== Standup Report =====
    
    def generate_standup_report(self) -> str:
        """生成站会报告"""
        dashboard = self.get_dashboard()
        agents = self.list_agents()
        tasks = self.list_tasks()
        
        report = f"""
📊 【Paperclip 站会报告】{datetime.now().strftime("%Y-%m-%d %H:%M")}

## 组织概况
- 总 Agent 数: {dashboard['agents']['total']}
- 活跃 Agent: {dashboard['agents']['active']}
- 总任务: {dashboard['tasks']['total']}
- 待办: {dashboard['tasks']['backlog']}
- 进行中: {dashboard['tasks']['in_progress']}
- 已完成: {dashboard['tasks']['done']}
- 预算使用: ${dashboard['budget']['used']:.2f} / ${dashboard['budget']['total']:.2f} ({dashboard['budget']['usage_pct']:.1f}%)

## Agent 状态
"""
        
        for agent in agents:
            # 获取该 Agent 的任务
            agent_tasks = [t for t in tasks if t["assignee"] == agent["id"]]
            active = [t for t in agent_tasks if t["status"] not in ["done", "cancelled"]]
            
            budget_pct = (agent["budget_used"] / agent["budget_monthly"] * 100) if agent["budget_monthly"] > 0 else 0
            
            report += f"\n🟢 **{agent['title']}** ({agent['name']})\n"
            report += f"   部门: {agent['department']} | 活跃任务: {len(active)}\n"
            report += f"   预算: ${agent['budget_used']:.2f} / ${agent['budget_monthly']:.2f} ({budget_pct:.1f}%)\n"
            
            if active:
                report += "   近期任务:\n"
                for t in active[:3]:
                    report += f"   - [{t['priority']}] {t['title']}\n"
        
        report += "\n---\n"
        report += "💡 Dashboard: http://localhost:3100\n"
        
        return report


# CLI 接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Paperclip Client")
    parser.add_argument("--agents", action="store_true", help="列出所有 Agent")
    parser.add_argument("--tasks", action="store_true", help="列出所有任务")
    parser.add_argument("--dashboard", action="store_true", help="查看仪表盘")
    parser.add_argument("--dispatch", nargs=4, metavar=("TITLE", "DESC", "CAPS", "BUDGET"),
                       help="智能派发任务")
    parser.add_argument("--standup", action="store_true", help="生成站会报告")
    parser.add_argument("--org", action="store_true", help="查看组织架构")
    
    args = parser.parse_args()
    
    client = PaperclipClient()
    
    if args.agents:
        agents = client.list_agents()
        print(f"\n👥 Agent 列表 ({len(agents)} 个):")
        print("-" * 60)
        for agent in agents:
            print(f"🟢 {agent['title']} ({agent['name']})")
            print(f"   部门: {agent['department']}")
            print(f"   能力: {', '.join(agent['capabilities'])}")
            print(f"   预算: ${agent['budget_used']:.2f} / ${agent['budget_monthly']:.2f}")
            print()
    
    elif args.tasks:
        tasks = client.list_tasks()
        print(f"\n📋 任务列表 ({len(tasks)} 个):")
        print("-" * 60)
        for task in tasks:
            print(f"[{task['status']}] {task['title']}")
            print(f"   指派: @{task['assignee']} | 优先级: {task['priority']}")
            print()
    
    elif args.dashboard:
        dashboard = client.get_dashboard()
        print(json.dumps(dashboard, indent=2, ensure_ascii=False))
    
    elif args.dispatch:
        caps = args.dispatch[2].split(",")
        budget = float(args.dispatch[3])
        result = client.smart_dispatch(args.dispatch[0], args.dispatch[1], caps, budget)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.standup:
        print(client.generate_standup_report())
    
    elif args.org:
        org = client.get_org_chart()
        print(json.dumps(org, indent=2, ensure_ascii=False))
    
    else:
        print("Paperclip Client")
        print("\n示例:")
        print("  python3 paperclip_client.py --agents")
        print("  python3 paperclip_client.py --standup")
        print("  python3 paperclip_client.py --dispatch '写代码' '编写爬虫' '编程,脚本' 10.0")
