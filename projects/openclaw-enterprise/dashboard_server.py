#!/usr/bin/env python3
"""
OpenClaw 企业版 - 移动端 Dashboard Server
提供 Web 界面查看 Agent 状态、任务看板、预算情况
"""

import json
import http.server
import socketserver
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from budget_system import BudgetManager
from ticket_system import TicketSystem, TicketStatus

PORT = 8088


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Dashboard 请求处理器"""
    
    def __init__(self, *args, **kwargs):
        self.budget_manager = BudgetManager()
        self.ticket_system = TicketSystem()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        if path == "/" or path == "/dashboard":
            self.serve_dashboard()
        elif path == "/org":
            self.serve_org_chart()
        elif path == "/delegation":
            self.serve_delegation_chain()
        elif path == "/api/agents":
            self.serve_agents_api()
        elif path == "/api/tickets":
            self.serve_tickets_api()
        elif path == "/api/budget":
            self.serve_budget_api()
        elif path == "/api/stats":
            self.serve_stats_api()
        else:
            self.serve_static_file(path)
    
    def serve_dashboard(self):
        """服务主页面"""
        html = self.generate_dashboard_html()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_org_chart(self):
        """服务组织架构图"""
        try:
            with open("data/org/org_chart.html", 'r', encoding='utf-8') as f:
                html = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "组织架构图未生成")
    
    def serve_delegation_chain(self):
        """服务任务委派链"""
        try:
            with open("data/org/delegation_chain.html", 'r', encoding='utf-8') as f:
                html = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "委派链未生成")
    
    def serve_agents_api(self):
        """Agent 状态 API"""
        budget_data = self.budget_manager.get_dashboard()
        
        agents = []
        for agent in budget_data["agent_status"]:
            # 获取该 Agent 的任务
            tickets = self.ticket_system.get_tickets_by_agent(agent["agent_id"])
            active_tickets = [t for t in tickets if t.status not in ["done", "cancelled"]]
            
            agents.append({
                "id": agent["agent_id"],
                "name": agent["agent_name"],
                "status": agent["status"],
                "budget_usage": agent["usage_pct"],
                "active_tasks": len(active_tickets),
                "monthly_spent": agent["monthly_spent"],
                "monthly_budget": agent["monthly_budget"]
            })
        
        self.send_json({"agents": agents})
    
    def serve_tickets_api(self):
        """任务看板 API"""
        board = self.ticket_system.get_ticket_board()
        
        # 简化数据
        simplified_board = {}
        for status, tickets in board.items():
            simplified_board[status] = [
                {
                    "id": t["id"],
                    "title": t["title"][:30] + "..." if len(t["title"]) > 30 else t["title"],
                    "priority": t["priority"],
                    "assignee": t["assignee"]
                }
                for t in tickets
            ]
        
        self.send_json({"board": simplified_board})
    
    def serve_budget_api(self):
        """预算 API"""
        data = self.budget_manager.get_dashboard()
        self.send_json(data)
    
    def serve_stats_api(self):
        """统计 API"""
        budget_data = self.budget_manager.get_dashboard()
        ticket_stats = self.ticket_system.get_stats()
        
        stats = {
            "timestamp": datetime.now().isoformat(),
            "agents": {
                "total": len(budget_data["agent_status"]),
                "active": sum(1 for a in budget_data["agent_status"] if a["status"] == "active"),
                "paused": sum(1 for a in budget_data["agent_status"] if a["status"] == "paused")
            },
            "budget": {
                "total": budget_data["total_budget"],
                "spent": budget_data["total_spent"],
                "remaining": budget_data["total_remaining"],
                "usage_pct": budget_data["overall_usage_pct"]
            },
            "tickets": ticket_stats
        }
        
        self.send_json(stats)
    
    def serve_static_file(self, path):
        """服务静态文件"""
        # 简化处理，直接返回 404
        self.send_error(404)
    
    def send_json(self, data):
        """发送 JSON 响应"""
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def generate_dashboard_html(self) -> str:
        """生成 Dashboard HTML"""
        
        # 获取数据
        budget_data = self.budget_manager.get_dashboard()
        ticket_board = self.ticket_system.get_ticket_board()
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw Enterprise Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 24px;
            margin-bottom: 5px;
        }}
        
        .header .subtitle {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .stat-card .label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}
        
        .stat-card .value {{
            font-size: 28px;
            font-weight: bold;
            color: #333;
        }}
        
        .stat-card .subvalue {{
            font-size: 14px;
            color: #999;
            margin-top: 5px;
        }}
        
        .section {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .section h2 {{
            font-size: 18px;
            margin-bottom: 15px;
            color: #333;
        }}
        
        .agent-list {{
            display: grid;
            gap: 10px;
        }}
        
        .agent-item {{
            display: flex;
            align-items: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #ddd;
        }}
        
        .agent-item.active {{ border-left-color: #28a745; }}
        .agent-item.paused {{ border-left-color: #ffc107; }}
        .agent-item.exceeded {{ border-left-color: #dc3545; }}
        
        .agent-avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }}
        
        .agent-info {{
            flex: 1;
        }}
        
        .agent-name {{
            font-weight: 600;
            margin-bottom: 3px;
        }}
        
        .agent-status {{
            font-size: 12px;
            color: #666;
        }}
        
        .agent-budget {{
            text-align: right;
        }}
        
        .budget-bar {{
            width: 100px;
            height: 6px;
            background: #e9ecef;
            border-radius: 3px;
            overflow: hidden;
            margin-bottom: 5px;
        }}
        
        .budget-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
            transition: width 0.3s;
        }}
        
        .budget-text {{
            font-size: 12px;
            color: #666;
        }}
        
        .board-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}
        
        .board-column {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
        }}
        
        .board-column h3 {{
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        
        .ticket-card {{
            background: white;
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .ticket-id {{
            font-size: 11px;
            color: #999;
            margin-bottom: 5px;
        }}
        
        .ticket-title {{
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 8px;
        }}
        
        .ticket-meta {{
            display: flex;
            gap: 10px;
            font-size: 12px;
        }}
        
        .priority {{
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
        }}
        
        .priority.P0 {{ background: #dc3545; color: white; }}
        .priority.P1 {{ background: #fd7e14; color: white; }}
        .priority.P2 {{ background: #ffc107; color: #333; }}
        .priority.P3 {{ background: #6c757d; color: white; }}
        
        .assignee {{
            color: #666;
        }}
        
        .refresh-btn {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 10px; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .board-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦞 OpenClaw Enterprise</h1>
        <div class="subtitle">Agent 团队管理 Dashboard</div>
    </div>
    
    <div class="container">
        <!-- 统计卡片 -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="label">活跃 Agent</div>
                <div class="value">{sum(1 for a in budget_data["agent_status"] if a["status"] == "active")}</div>
                <div class="subvalue">/ {len(budget_data["agent_status"])} 总计</div>
            </div>
            <div class="stat-card">
                <div class="label">本月支出</div>
                <div class="value">${budget_data["total_spent"]:.2f}</div>
                <div class="subvalue">预算: ${budget_data["total_budget"]:.0f}</div>
            </div>
            <div class="stat-card">
                <div class="label">进行中的任务</div>
                <div class="value">{len(ticket_board.get("in_progress", []))}</div>
                <div class="subvalue">待办: {len(ticket_board.get("backlog", []))}</div>
            </div>
            <div class="stat-card">
                <div class="label">已完成</div>
                <div class="value">{len(ticket_board.get("done", []))}</div>
                <div class="subvalue">审核中: {len(ticket_board.get("review", []))}</div>
            </div>
        </div>
        
        <!-- Agent 状态 -->
        <div class="section">
            <h2>👥 Agent 状态</h2>
            <div class="agent-list">
"""
        
        # 添加 Agent 列表
        for agent in budget_data["agent_status"]:
            status_class = agent["status"]
            usage_pct = agent["usage_pct"]
            
            html += f"""
                <div class="agent-item {status_class}">
                    <div class="agent-avatar">{agent["agent_name"][0]}</div>
                    <div class="agent-info">
                        <div class="agent-name">{agent["agent_name"]}</div>
                        <div class="agent-status">{agent["status"]} | 本月: ${agent["monthly_spent"]:.2f}</div>
                    </div>
                    <div class="agent-budget">
                        <div class="budget-bar">
                            <div class="budget-fill" style="width: {min(usage_pct, 100)}%"></div>
                        </div>
                        <div class="budget-text">{usage_pct:.1f}%</div>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
        
        <!-- 任务看板 -->
        <div class="section">
            <h2>📋 任务看板</h2>
            <div class="board-grid">
"""
        
        # 添加看板列
        status_names = {
            "backlog": "📥 待办",
            "todo": "📋 准备",
            "in_progress": "🔨 进行中",
            "review": "👀 审核中",
            "done": "✅ 已完成",
            "blocked": "🚫 阻塞"
        }
        
        for status, tickets in ticket_board.items():
            if status in status_names:
                html += f"""
                <div class="board-column">
                    <h3>{status_names[status]} ({len(tickets)})</h3>
"""
                for ticket in tickets[:5]:  # 最多显示5个
                    html += f"""
                    <div class="ticket-card">
                        <div class="ticket-id">{ticket["id"]}</div>
                        <div class="ticket-title">{ticket["title"]}</div>
                        <div class="ticket-meta">
                            <span class="priority {ticket["priority"]}">{ticket["priority"]}</span>
                            <span class="assignee">@{ticket["assignee"]}</span>
                        </div>
                    </div>
"""
                
                if len(tickets) > 5:
                    html += f'<div style="text-align:center;color:#999;font-size:12px;">+{len(tickets)-5} 更多</div>'
                
                html += "</div>"
        
        html += """
            </div>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="location.reload()">↻</button>
    
    <script>
        // 自动刷新（每30秒）
        setInterval(() => {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
"""
        
        return html


def run_server(port=PORT):
    """启动 Dashboard 服务器"""
    with socketserver.TCPServer(("", port), DashboardHandler) as httpd:
        print(f"🚀 Dashboard 服务器已启动")
        print(f"📱 访问地址: http://localhost:{port}")
        print(f"🌐 局域网地址: http://0.0.0.0:{port}")
        print(f"\n按 Ctrl+C 停止服务器")
        httpd.serve_forever()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Dashboard Server")
    parser.add_argument("--port", type=int, default=PORT, help="端口号")
    
    args = parser.parse_args()
    
    run_server(args.port)
