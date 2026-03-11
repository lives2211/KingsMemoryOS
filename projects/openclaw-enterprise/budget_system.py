#!/usr/bin/env python3
"""
OpenClaw 企业版 - 预算控制系统
参考 Paperclip 的预算管理功能
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgentBudget:
    """Agent 预算配置"""
    agent_id: str
    agent_name: str
    monthly_budget_usd: float
    daily_budget_usd: float
    current_month_spent: float = 0.0
    current_day_spent: float = 0.0
    warning_threshold: float = 0.8  # 80%预警
    auto_pause: bool = True  # 超支自动暂停
    status: str = "active"  # active, paused, exceeded


class BudgetManager:
    """预算管理器"""
    
    def __init__(self, config_path: str = "config/budgets.json"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.budgets: Dict[str, AgentBudget] = {}
        self.load_budgets()
    
    def load_budgets(self):
        """加载预算配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for agent_id, budget_data in data.items():
                    self.budgets[agent_id] = AgentBudget(**budget_data)
            logger.info(f"✅ 已加载 {len(self.budgets)} 个Agent预算配置")
        else:
            # 初始化默认预算
            self.init_default_budgets()
    
    def init_default_budgets(self):
        """初始化默认预算"""
        default_budgets = {
            "main": AgentBudget(
                agent_id="main",
                agent_name="龙虾总管(Monica)",
                monthly_budget_usd=50.0,
                daily_budget_usd=5.0
            ),
            "bingbing": AgentBudget(
                agent_id="bingbing",
                agent_name="创意官(bingbing)",
                monthly_budget_usd=30.0,
                daily_budget_usd=3.0
            ),
            "yitai": AgentBudget(
                agent_id="yitai",
                agent_name="技术官(yitai)",
                monthly_budget_usd=40.0,
                daily_budget_usd=4.0
            ),
            "daping": AgentBudget(
                agent_id="daping",
                agent_name="检测官(daping)",
                monthly_budget_usd=20.0,
                daily_budget_usd=2.0
            ),
            "spikey": AgentBudget(
                agent_id="spikey",
                agent_name="审计官(spikey)",
                monthly_budget_usd=20.0,
                daily_budget_usd=2.0
            ),
            "xiaohongcai": AgentBudget(
                agent_id="xiaohongcai",
                agent_name="小红财",
                monthly_budget_usd=25.0,
                daily_budget_usd=2.5
            )
        }
        self.budgets = default_budgets
        self.save_budgets()
        logger.info(f"✅ 已初始化 {len(default_budgets)} 个默认预算")
    
    def save_budgets(self):
        """保存预算配置"""
        data = {agent_id: asdict(budget) for agent_id, budget in self.budgets.items()}
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def check_budget(self, agent_id: str, estimated_cost: float = 0.0) -> Dict:
        """
        检查预算状态
        
        Returns:
            {
                "allowed": bool,
                "reason": str,
                "remaining_monthly": float,
                "remaining_daily": float,
                "status": str
            }
        """
        if agent_id not in self.budgets:
            return {
                "allowed": True,
                "reason": "未设置预算限制",
                "remaining_monthly": float('inf'),
                "remaining_daily": float('inf'),
                "status": "unlimited"
            }
        
        budget = self.budgets[agent_id]
        
        # 检查状态
        if budget.status == "exceeded":
            return {
                "allowed": False,
                "reason": f"月度预算已超支 (${budget.current_month_spent:.2f} / ${budget.monthly_budget_usd:.2f})",
                "remaining_monthly": 0,
                "remaining_daily": 0,
                "status": "exceeded"
            }
        
        if budget.status == "paused":
            return {
                "allowed": False,
                "reason": "Agent已被手动暂停",
                "remaining_monthly": budget.monthly_budget_usd - budget.current_month_spent,
                "remaining_daily": budget.daily_budget_usd - budget.current_day_spent,
                "status": "paused"
            }
        
        # 计算剩余预算
        remaining_monthly = budget.monthly_budget_usd - budget.current_month_spent
        remaining_daily = budget.daily_budget_usd - budget.current_day_spent
        
        # 检查是否会超支
        if estimated_cost > 0:
            if estimated_cost > remaining_daily:
                return {
                    "allowed": False,
                    "reason": f"预估成本(${estimated_cost:.2f})超过今日剩余预算(${remaining_daily:.2f})",
                    "remaining_monthly": remaining_monthly,
                    "remaining_daily": remaining_daily,
                    "status": "daily_exceeded"
                }
            
            if estimated_cost > remaining_monthly:
                return {
                    "allowed": False,
                    "reason": f"预估成本(${estimated_cost:.2f})超过本月剩余预算(${remaining_monthly:.2f})",
                    "remaining_monthly": remaining_monthly,
                    "remaining_daily": remaining_daily,
                    "status": "monthly_exceeded"
                }
        
        # 检查预警阈值
        monthly_usage = budget.current_month_spent / budget.monthly_budget_usd
        daily_usage = budget.current_day_spent / budget.daily_budget_usd
        
        if monthly_usage >= budget.warning_threshold or daily_usage >= budget.warning_threshold:
            return {
                "allowed": True,
                "reason": f"⚠️ 预算使用超过{budget.warning_threshold*100:.0f}%",
                "remaining_monthly": remaining_monthly,
                "remaining_daily": remaining_daily,
                "status": "warning"
            }
        
        return {
            "allowed": True,
            "reason": "预算充足",
            "remaining_monthly": remaining_monthly,
            "remaining_daily": remaining_daily,
            "status": "healthy"
        }
    
    def record_cost(self, agent_id: str, cost_usd: float, task_name: str = ""):
        """记录成本消耗"""
        if agent_id not in self.budgets:
            logger.warning(f"Agent {agent_id} 未设置预算，无法记录成本")
            return
        
        budget = self.budgets[agent_id]
        budget.current_month_spent += cost_usd
        budget.current_day_spent += cost_usd
        
        # 检查是否超支
        if budget.auto_pause:
            if budget.current_month_spent >= budget.monthly_budget_usd:
                budget.status = "exceeded"
                logger.warning(f"🚨 {budget.agent_name} 月度预算已超支，已自动暂停")
            elif budget.current_day_spent >= budget.daily_budget_usd:
                logger.warning(f"⚠️ {budget.agent_name} 今日预算已用尽")
        
        self.save_budgets()
        
        # 记录详细日志
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "agent_name": budget.agent_name,
            "cost_usd": cost_usd,
            "task_name": task_name,
            "monthly_total": budget.current_month_spent,
            "daily_total": budget.current_day_spent
        }
        
        log_path = Path("logs/cost_log.jsonl")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        logger.info(f"💰 {budget.agent_name} 消耗 ${cost_usd:.3f} | 今日: ${budget.current_day_spent:.2f} | 本月: ${budget.current_month_spent:.2f}")
    
    def reset_daily_budgets(self):
        """重置每日预算（每天0点调用）"""
        for budget in self.budgets.values():
            budget.current_day_spent = 0.0
            if budget.status != "exceeded":  # 只有超支状态保持不变
                budget.status = "active"
        self.save_budgets()
        logger.info("✅ 每日预算已重置")
    
    def reset_monthly_budgets(self):
        """重置月度预算（每月1号调用）"""
        for budget in self.budgets.values():
            budget.current_month_spent = 0.0
            budget.current_day_spent = 0.0
            budget.status = "active"
        self.save_budgets()
        logger.info("✅ 月度预算已重置")
    
    def get_dashboard(self) -> Dict:
        """获取预算仪表盘数据"""
        total_budget = sum(b.monthly_budget_usd for b in self.budgets.values())
        total_spent = sum(b.current_month_spent for b in self.budgets.values())
        
        agent_status = []
        for budget in self.budgets.values():
            usage_pct = (budget.current_month_spent / budget.monthly_budget_usd * 100) if budget.monthly_budget_usd > 0 else 0
            agent_status.append({
                "agent_id": budget.agent_id,
                "agent_name": budget.agent_name,
                "monthly_budget": budget.monthly_budget_usd,
                "monthly_spent": budget.current_month_spent,
                "monthly_remaining": budget.monthly_budget_usd - budget.current_month_spent,
                "usage_pct": round(usage_pct, 1),
                "status": budget.status
            })
        
        # 按使用率排序
        agent_status.sort(key=lambda x: x["usage_pct"], reverse=True)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_budget": total_budget,
            "total_spent": total_spent,
            "total_remaining": total_budget - total_spent,
            "overall_usage_pct": round(total_spent / total_budget * 100, 1) if total_budget > 0 else 0,
            "agent_status": agent_status
        }
    
    def update_budget(self, agent_id: str, monthly_budget: Optional[float] = None, 
                     daily_budget: Optional[float] = None):
        """更新预算配置"""
        if agent_id not in self.budgets:
            logger.error(f"Agent {agent_id} 不存在")
            return False
        
        budget = self.budgets[agent_id]
        if monthly_budget is not None:
            budget.monthly_budget_usd = monthly_budget
        if daily_budget is not None:
            budget.daily_budget_usd = daily_budget
        
        self.save_budgets()
        logger.info(f"✅ {budget.agent_name} 预算已更新")
        return True
    
    def pause_agent(self, agent_id: str):
        """暂停Agent"""
        if agent_id in self.budgets:
            self.budgets[agent_id].status = "paused"
            self.save_budgets()
            logger.info(f"⏸️ {self.budgets[agent_id].agent_name} 已暂停")
    
    def resume_agent(self, agent_id: str):
        """恢复Agent"""
        if agent_id in self.budgets:
            budget = self.budgets[agent_id]
            if budget.current_month_spent < budget.monthly_budget_usd:
                budget.status = "active"
                self.save_budgets()
                logger.info(f"▶️ {budget.agent_name} 已恢复")
            else:
                logger.warning(f"❌ {budget.agent_name} 预算已超支，无法恢复")


# CLI 接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="预算管理系统")
    parser.add_argument("--dashboard", action="store_true", help="显示预算仪表盘")
    parser.add_argument("--check", help="检查指定Agent预算状态")
    parser.add_argument("--record", nargs=3, metavar=("AGENT", "COST", "TASK"), help="记录成本")
    parser.add_argument("--reset-daily", action="store_true", help="重置每日预算")
    parser.add_argument("--reset-monthly", action="store_true", help="重置月度预算")
    parser.add_argument("--pause", help="暂停Agent")
    parser.add_argument("--resume", help="恢复Agent")
    
    args = parser.parse_args()
    
    manager = BudgetManager()
    
    if args.dashboard:
        dashboard = manager.get_dashboard()
        print(json.dumps(dashboard, ensure_ascii=False, indent=2))
    elif args.check:
        result = manager.check_budget(args.check)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.record:
        manager.record_cost(args.record[0], float(args.record[1]), args.record[2])
    elif args.reset_daily:
        manager.reset_daily_budgets()
    elif args.reset_monthly:
        manager.reset_monthly_budgets()
    elif args.pause:
        manager.pause_agent(args.pause)
    elif args.resume:
        manager.resume_agent(args.resume)
    else:
        print("请指定操作，使用 --help 查看帮助")
