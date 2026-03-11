#!/usr/bin/env python3
"""
OpenClaw 企业版 - 组织架构可视化
生成层级汇报关系图、任务委派链展示
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Agent:
    """Agent 定义"""
    id: str
    name: str
    title: str
    department: str
    reports_to: Optional[str]  # 汇报给谁
    manages: List[str]  # 管理哪些Agent
    capabilities: List[str]  # 能力标签
    level: int  # 层级（0=CEO, 1=高管, 2=执行）


class OrgChart:
    """组织架构管理"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.init_org_structure()
    
    def init_org_structure(self):
        """初始化组织架构"""
        # CEO 层
        self.agents["main"] = Agent(
            id="main",
            name="Monica",
            title="龙虾总管",
            department="管理层",
            reports_to=None,
            manages=["bingbing", "yitai", "daping", "spikey", "xiaohongcai"],
            capabilities=["统筹", "决策", "协调"],
            level=0
        )
        
        # 高管层
        self.agents["bingbing"] = Agent(
            id="bingbing",
            name="bingbing",
            title="创意官",
            department="创作部",
            reports_to="main",
            manages=[],
            capabilities=["内容创作", "设计", "文案"],
            level=1
        )
        
        self.agents["yitai"] = Agent(
            id="yitai",
            name="yitai",
            title="技术官",
            department="技术部",
            reports_to="main",
            manages=[],
            capabilities=["编程", "开发", "技术架构"],
            level=1
        )
        
        self.agents["daping"] = Agent(
            id="daping",
            name="daping",
            title="检测官",
            department="质检部",
            reports_to="main",
            manages=[],
            capabilities=["检测", "分析", "测试"],
            level=1
        )
        
        self.agents["spikey"] = Agent(
            id="spikey",
            name="spikey",
            title="审计官",
            department="审计部",
            reports_to="main",
            manages=[],
            capabilities=["审计", "复盘", "质量"],
            level=1
        )
        
        self.agents["xiaohongcai"] = Agent(
            id="xiaohongcai",
            name="小红财",
            title="运营官",
            department="运营部",
            reports_to="main",
            manages=[],
            capabilities=["社媒运营", "小红书", "公众号"],
            level=1
        )
    
    def get_org_tree(self) -> Dict:
        """获取组织架构树"""
        tree = {
            "id": "main",
            "name": "Monica",
            "title": "龙虾总管",
            "department": "管理层",
            "level": 0,
            "children": []
        }
        
        for agent_id, agent in self.agents.items():
            if agent_id == "main":
                continue
            
            node = {
                "id": agent_id,
                "name": agent.name,
                "title": agent.title,
                "department": agent.department,
                "level": agent.level,
                "capabilities": agent.capabilities,
                "children": []
            }
            
            # 找到父节点并添加
            if agent.reports_to == "main":
                tree["children"].append(node)
        
        return tree
    
    def generate_org_chart_html(self) -> str:
        """生成组织架构图 HTML"""
        tree = self.get_org_tree()
        
        html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw 组织架构</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .header p {
            opacity: 0.9;
            font-size: 16px;
        }
        .org-chart {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 40px;
        }
        .level {
            display: flex;
            justify-content: center;
            gap: 30px;
            width: 100%;
        }
        .agent-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            min-width: 180px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
            position: relative;
        }
        .agent-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        }
        .agent-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
            margin: 0 auto 15px;
        }
        .agent-name {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        .agent-title {
            font-size: 14px;
            color: #667eea;
            font-weight: 500;
            margin-bottom: 8px;
        }
        .agent-dept {
            font-size: 12px;
            color: #999;
            margin-bottom: 10px;
        }
        .agent-caps {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            justify-content: center;
        }
        .cap-tag {
            background: #f0f0f0;
            color: #666;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
        }
        .connector {
            width: 2px;
            height: 30px;
            background: rgba(255,255,255,0.5);
            margin: -10px auto;
        }
        .level-label {
            text-align: center;
            color: rgba(255,255,255,0.8);
            font-size: 14px;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .level-0 .agent-card {
            border: 3px solid gold;
        }
        .level-0 .agent-title {
            color: #d4af37;
        }
        .report-line {
            position: absolute;
            top: -40px;
            left: 50%;
            width: 2px;
            height: 40px;
            background: rgba(255,255,255,0.5);
            transform: translateX(-50%);
        }
        @media (max-width: 768px) {
            .level {
                flex-direction: column;
                align-items: center;
            }
            .agent-card {
                min-width: 200px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦞 OpenClaw Enterprise</h1>
            <p>组织架构图 - Agent 团队层级</p>
        </div>
        
        <div class="org-chart">
            <!-- CEO 层 -->
            <div class="level level-0">
                <div class="agent-card">
                    <div class="agent-avatar">M</div>
                    <div class="agent-name">Monica</div>
                    <div class="agent-title">龙虾总管</div>
                    <div class="agent-dept">管理层</div>
                    <div class="agent-caps">
                        <span class="cap-tag">统筹</span>
                        <span class="cap-tag">决策</span>
                        <span class="cap-tag">协调</span>
                    </div>
                </div>
            </div>
            
            <div class="connector"></div>
            
            <!-- 高管层 -->
            <div class="level-label">Executive Team</div>
            <div class="level level-1">
"""
        
        # 添加高管层
        for agent_id, agent in self.agents.items():
            if agent.level == 1:
                caps_html = ''.join([f'<span class="cap-tag">{cap}</span>' for cap in agent.capabilities[:3]])
                html += f"""
                <div class="agent-card">
                    <div class="report-line"></div>
                    <div class="agent-avatar">{agent.name[0].upper()}</div>
                    <div class="agent-name">{agent.name}</div>
                    <div class="agent-title">{agent.title}</div>
                    <div class="agent-dept">{agent.department}</div>
                    <div class="agent-caps">
                        {caps_html}
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: rgba(255,255,255,0.6);">
            <p>💡 汇报关系: 所有 Agent 直接向 Monica 汇报</p>
            <p>🎯 任务委派: 通过 Ticket 系统层层分解</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_delegation_chain_html(self, ticket_system) -> str:
        """生成任务委派链 HTML"""
        
        html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>任务委派链</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 24px;
            color: #333;
        }
        .chain-item {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .chain-level {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
        }
        .chain-content {
            flex: 1;
        }
        .chain-title {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        .chain-meta {
            font-size: 13px;
            color: #666;
        }
        .chain-assignee {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 16px;
            background: #f8f9fa;
            border-radius: 20px;
        }
        .assignee-avatar {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
        }
        .arrow {
            text-align: center;
            color: #999;
            font-size: 24px;
            margin: 10px 0;
        }
        .status-badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        .status-backlog { background: #e9ecef; color: #666; }
        .status-todo { background: #cce5ff; color: #004085; }
        .status-in_progress { background: #fff3cd; color: #856404; }
        .status-review { background: #d4edda; color: #155724; }
        .status-done { background: #d1ecf1; color: #0c5460; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 任务委派链</h1>
            <p>当前活跃的任务委派关系</p>
        </div>
"""
        
        # 获取所有任务
        from ticket_system import TicketSystem
        ts = TicketSystem()
        
        # 找到有子任务的任务
        parent_tickets = []
        for ticket in ts.tickets.values():
            if ticket.sub_tickets:
                parent_tickets.append(ticket)
        
        if not parent_tickets:
            html += """
        <div style="text-align: center; padding: 60px; color: #999;">
            <p>暂无任务委派链</p>
            <p style="font-size: 14px; margin-top: 10px;">创建任务并委派子任务后可查看</p>
        </div>
"""
        else:
            for parent in parent_tickets:
                # 父任务
                html += f"""
        <div class="chain-item">
            <div class="chain-level">L0</div>
            <div class="chain-content">
                <div class="chain-title">{parent.title}</div>
                <div class="chain-meta">{parent.id} | 创建: {parent.created_at[:10]}</div>
            </div>
            <div class="chain-assignee">
                <div class="assignee-avatar">{parent.assignee[0].upper()}</div>
                <span>@{parent.assignee}</span>
            </div>
            <span class="status-badge status-{parent.status}">{parent.status}</span>
        </div>
"""
                
                # 子任务
                for i, sub_id in enumerate(parent.sub_tickets, 1):
                    if sub_id in ts.tickets:
                        sub = ts.tickets[sub_id]
                        html += f"""
        <div class="arrow">↓</div>
        <div class="chain-item" style="margin-left: 40px;">
            <div class="chain-level">L{i}</div>
            <div class="chain-content">
                <div class="chain-title">{sub.title}</div>
                <div class="chain-meta">{sub.id} | 父任务: {parent.id}</div>
            </div>
            <div class="chain-assignee">
                <div class="assignee-avatar">{sub.assignee[0].upper()}</div>
                <span>@{sub.assignee}</span>
            </div>
            <span class="status-badge status-{sub.status}">{sub.status}</span>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        
        return html
    
    def save_org_chart(self, output_dir: str = "data/org"):
        """保存组织架构文件"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存组织架构图
        org_html = self.generate_org_chart_html()
        with open(output_path / "org_chart.html", 'w', encoding='utf-8') as f:
            f.write(org_html)
        
        # 保存委派链
        delegation_html = self.generate_delegation_chain_html(None)
        with open(output_path / "delegation_chain.html", 'w', encoding='utf-8') as f:
            f.write(delegation_html)
        
        # 保存JSON数据
        org_data = {
            "generated_at": datetime.now().isoformat(),
            "total_agents": len(self.agents),
            "levels": 2,
            "structure": self.get_org_tree()
        }
        with open(output_path / "org_data.json", 'w', encoding='utf-8') as f:
            json.dump(org_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 组织架构文件已保存到: {output_path}")
        return output_path


if __name__ == "__main__":
    org = OrgChart()
    org.save_org_chart()
    print("\n📊 组织架构:")
    print("  Level 0: Monica (CEO)")
    print("  Level 1: bingbing, yitai, daping, spikey, xiaohongcai (高管)")
