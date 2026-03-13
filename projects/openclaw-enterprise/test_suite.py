#!/usr/bin/env python3
"""
OpenClaw Enterprise - 自动化测试套件
测试所有 Phase 功能
"""

import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from budget_system import BudgetManager
from ticket_system import TicketSystem


class TestSuite:
    """测试套件"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
        
    def log(self, message, level="INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def test(self, name, func):
        """运行单个测试"""
        try:
            self.log(f"🧪 测试: {name}")
            func()
            self.tests_passed += 1
            self.test_results.append({"name": name, "status": "PASSED"})
            self.log(f"✅ 通过: {name}")
        except Exception as e:
            self.tests_failed += 1
            self.test_results.append({"name": name, "status": "FAILED", "error": str(e)})
            self.log(f"❌ 失败: {name} - {e}", "ERROR")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("🚀 OpenClaw Enterprise 自动化测试")
        print("=" * 60)
        print()
        
        # Phase 1: 预算系统测试
        print("📊 Phase 1: 预算控制系统")
        print("-" * 60)
        self.test("预算管理器初始化", self.test_budget_init)
        self.test("预算检查", self.test_budget_check)
        self.test("成本记录", self.test_budget_record)
        self.test("仪表盘生成", self.test_budget_dashboard)
        print()
        
        # Phase 2: 任务系统测试
        print("📋 Phase 2: Ticket 任务系统")
        print("-" * 60)
        self.test("任务创建", self.test_ticket_create)
        self.test("状态流转", self.test_ticket_status)
        self.test("任务委派", self.test_ticket_delegate)
        self.test("任务完成", self.test_ticket_complete)
        self.test("任务审核", self.test_ticket_review)
        self.test("看板生成", self.test_ticket_board)
        print()
        
        # Phase 3: Dashboard API 测试
        print("🌐 Phase 3: Dashboard API")
        print("-" * 60)
        self.test("API 服务启动", self.test_api_running)
        self.test("Stats API", self.test_api_stats)
        self.test("Agents API", self.test_api_agents)
        self.test("Tickets API", self.test_api_tickets)
        self.test("Budget API", self.test_api_budget)
        print()
        
        # Phase 4: 组织架构测试
        print("🏗️ Phase 4: 组织架构")
        print("-" * 60)
        self.test("组织架构初始化", self.test_org_init)
        self.test("层级结构", self.test_org_tree)
        self.test("HTML 生成", self.test_org_html)
        print()
        
        # 生成报告
        self.generate_report()
    
    # ===== Phase 1: 预算系统测试 =====
    def test_budget_init(self):
        """测试预算管理器初始化"""
        bm = BudgetManager()
        assert len(bm.budgets) == 6, "应该有6个Agent预算"
        assert "main" in bm.budgets, "应该有main的预算"
        
    def test_budget_check(self):
        """测试预算检查"""
        bm = BudgetManager()
        result = bm.check_budget("main", 10.0)
        assert result["allowed"] == True, "预算应该充足"
        assert result["status"] == "healthy", "状态应该是healthy"
        
    def test_budget_record(self):
        """测试成本记录"""
        bm = BudgetManager()
        initial = bm.budgets["bingbing"].current_month_spent
        bm.record_cost("bingbing", 5.0, "测试任务")
        assert bm.budgets["bingbing"].current_month_spent == initial + 5.0, "成本应该被记录"
        
    def test_budget_dashboard(self):
        """测试预算仪表盘"""
        bm = BudgetManager()
        dashboard = bm.get_dashboard()
        assert "total_budget" in dashboard, "应该有总预算"
        assert "agent_status" in dashboard, "应该有Agent状态"
        assert len(dashboard["agent_status"]) == 6, "应该有6个Agent"
    
    # ===== Phase 2: 任务系统测试 =====
    def test_ticket_create(self):
        """测试任务创建"""
        ts = TicketSystem()
        ticket = ts.create_ticket(
            title="测试任务",
            description="这是一个测试",
            assignee="yitai",
            project="test"
        )
        assert ticket.id.startswith("TK-"), "任务ID应该以TK-开头"
        assert ticket.status == "backlog", "初始状态应该是backlog"
        
    def test_ticket_status(self):
        """测试状态流转"""
        ts = TicketSystem()
        ticket = ts.create_ticket("状态测试", "测试", "yitai", "test")
        
        # backlog -> todo
        result = ts.update_status(ticket.id, "todo")
        assert result == True, "状态更新应该成功"
        assert ts.tickets[ticket.id].status == "todo", "状态应该变为todo"
        
        # todo -> in_progress
        result = ts.update_status(ticket.id, "in_progress")
        assert result == True
        assert ts.tickets[ticket.id].status == "in_progress"
        
    def test_ticket_delegate(self):
        """测试任务委派"""
        ts = TicketSystem()
        parent = ts.create_ticket("父任务", "父任务描述", "main", "test")
        sub = ts.delegate_ticket(
            parent.id,
            "yitai",
            "子任务",
            "子任务描述"
        )
        assert sub is not None, "子任务应该被创建"
        assert sub.parent_ticket == parent.id, "子任务应该有父任务ID"
        assert sub.id in ts.tickets[parent.id].sub_tickets, "父任务应该记录子任务"
        
    def test_ticket_complete(self):
        """测试任务完成"""
        ts = TicketSystem()
        ticket = ts.create_ticket("完成测试", "测试", "yitai", "test")
        ts.update_status(ticket.id, "in_progress")
        
        result = ts.complete_ticket(ticket.id, "已完成", actual_cost=2.0)
        assert result == True, "完成任务应该成功"
        assert ts.tickets[ticket.id].status == "review", "状态应该变为review"
        assert ts.tickets[ticket.id].result == "已完成", "应该有完成结果"
        
    def test_ticket_review(self):
        """测试任务审核"""
        ts = TicketSystem()
        ticket = ts.create_ticket("审核测试", "测试", "yitai", "test")
        ts.update_status(ticket.id, "in_progress")
        ts.complete_ticket(ticket.id, "完成")
        
        result = ts.review_ticket(ticket.id, "main", True, "审核通过")
        assert result == True, "审核应该成功"
        assert ts.tickets[ticket.id].status == "done", "状态应该变为done"
        
    def test_ticket_board(self):
        """测试看板生成"""
        ts = TicketSystem()
        ts.create_ticket("看板测试1", "测试", "yitai", "test")
        ts.create_ticket("看板测试2", "测试", "bingbing", "test")
        
        board = ts.get_ticket_board()
        assert "backlog" in board, "看板应该有backlog列"
        assert len(board["backlog"]) >= 2, "backlog应该有至少2个任务"
    
    # ===== Phase 3: Dashboard API 测试 =====
    def test_api_running(self):
        """测试 API 服务是否运行"""
        try:
            response = requests.get("http://localhost:8089/api/stats", timeout=5)
            assert response.status_code == 200, "API应该返回200"
        except requests.exceptions.ConnectionError:
            raise Exception("Dashboard服务未运行，请先在8089端口启动服务")
        
    def test_api_stats(self):
        """测试 Stats API"""
        response = requests.get("http://localhost:8089/api/stats", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data, "应该有agents字段"
        assert "budget" in data, "应该有budget字段"
        
    def test_api_agents(self):
        """测试 Agents API"""
        response = requests.get("http://localhost:8089/api/agents", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data, "应该有agents字段"
        assert len(data["agents"]) == 6, "应该有6个Agent"
        
    def test_api_tickets(self):
        """测试 Tickets API"""
        response = requests.get("http://localhost:8089/api/tickets", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "board" in data, "应该有board字段"
        
    def test_api_budget(self):
        """测试 Budget API"""
        response = requests.get("http://localhost:8089/api/budget", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "total_budget" in data, "应该有total_budget"
        assert "agent_status" in data, "应该有agent_status"
    
    # ===== Phase 4: 组织架构测试 =====
    def test_org_init(self):
        """测试组织架构初始化"""
        from org_chart import OrgChart
        org = OrgChart()
        assert len(org.agents) == 6, "应该有6个Agent"
        assert "main" in org.agents, "应该有main"
        assert org.agents["main"].level == 0, "main应该是level 0"
        
    def test_org_tree(self):
        """测试组织架构树"""
        from org_chart import OrgChart
        org = OrgChart()
        tree = org.get_org_tree()
        assert tree["id"] == "main", "树根应该是main"
        assert len(tree["children"]) == 5, "应该有5个子节点"
        
    def test_org_html(self):
        """测试 HTML 生成"""
        from org_chart import OrgChart
        org = OrgChart()
        html = org.generate_org_chart_html()
        assert "Monica" in html, "HTML应该包含Monica"
        assert "org-chart" in html, "HTML应该有org-chart类"
        
        # 检查文件是否生成
        output_path = org.save_org_chart()
        assert (output_path / "org_chart.html").exists(), "org_chart.html应该存在"
        assert (output_path / "delegation_chain.html").exists(), "delegation_chain.html应该存在"
    
    def generate_report(self):
        """生成测试报告"""
        print()
        print("=" * 60)
        print("📊 测试报告")
        print("=" * 60)
        print()
        
        total = self.tests_passed + self.tests_failed
        pass_rate = (self.tests_passed / total * 100) if total > 0 else 0
        
        print(f"总计测试: {total}")
        print(f"✅ 通过: {self.tests_passed}")
        print(f"❌ 失败: {self.tests_failed}")
        print(f"📈 通过率: {pass_rate:.1f}%")
        print()
        
        if self.tests_failed > 0:
            print("失败的测试:")
            for result in self.test_results:
                if result["status"] == "FAILED":
                    print(f"  ❌ {result['name']}: {result.get('error', '')}")
            print()
        
        print("=" * 60)
        
        # 保存报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "total": total,
            "passed": self.tests_passed,
            "failed": self.tests_failed,
            "pass_rate": pass_rate,
            "results": self.test_results
        }
        
        report_path = Path("data/test_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 报告已保存: {report_path}")
        
        # 返回退出码
        return 0 if self.tests_failed == 0 else 1


if __name__ == "__main__":
    suite = TestSuite()
    exit_code = suite.run_all_tests()
    sys.exit(exit_code)
