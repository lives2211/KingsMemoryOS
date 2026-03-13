"""
心跳调度器 - 借鉴 Paperclip 的核心机制
Agent 定期唤醒，自主检查任务
"""

import threading
import time
from typing import Dict, List, Callable, Optional
from datetime import datetime, timedelta
import json
from .agent import BaseAgent, AgentConfig

class HeartbeatScheduler:
    """
    心跳调度器
    
    Paperclip 的核心创新:
    - Agent 不是被动等待，而是主动心跳
    - 定期唤醒检查任务队列
    - 自主决策是否领取任务
    - 汇报进度和状态
    """
    
    def __init__(self, check_interval: int = 60):
        self.agents: Dict[str, BaseAgent] = {}
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.check_interval = check_interval  # 全局检查间隔
        self.callbacks: List[Callable] = []
        self._lock = threading.Lock()
        
    def register_agent(self, agent: BaseAgent):
        """注册 Agent"""
        with self._lock:
            self.agents[agent.config.id] = agent
        print(f"[Heartbeat] Agent {agent.config.id} 已注册")
        
    def unregister_agent(self, agent_id: str):
        """注销 Agent"""
        with self._lock:
            if agent_id in self.agents:
                del self.agents[agent_id]
        print(f"[Heartbeat] Agent {agent_id} 已注销")
        
    def on_heartbeat(self, callback: Callable):
        """注册心跳回调"""
        self.callbacks.append(callback)
        
    def start(self):
        """启动调度器"""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print(f"[Heartbeat] 调度器已启动，检查间隔: {self.check_interval}s")
        
    def stop(self):
        """停止调度器"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("[Heartbeat] 调度器已停止")
        
    def _run(self):
        """主循环"""
        while self.running:
            self._check_all_agents()
            time.sleep(self.check_interval)
            
    def _check_all_agents(self):
        """检查所有 Agent"""
        with self._lock:
            agents = list(self.agents.values())
            
        for agent in agents:
            try:
                result = agent.heartbeat()
                
                # 触发回调
                for callback in self.callbacks:
                    try:
                        callback(agent.config.id, result)
                    except Exception as e:
                        print(f"[Heartbeat] 回调错误: {e}")
                        
            except Exception as e:
                print(f"[Heartbeat] Agent {agent.config.id} 心跳失败: {e}")
                
    def get_status(self) -> Dict:
        """获取调度器状态"""
        with self._lock:
            return {
                "running": self.running,
                "check_interval": self.check_interval,
                "agents_count": len(self.agents),
                "agents": {
                    agent_id: agent.to_dict()
                    for agent_id, agent in self.agents.items()
                }
            }


class CronHeartbeat:
    """
    基于 OpenClaw Cron 的心跳
    
    替代方案: 使用 OpenClaw 内置 cron 系统
    每个 Agent 独立调度
    """
    
    def __init__(self):
        self.agent_configs: Dict[str, AgentConfig] = {}
        
    def register(self, config: AgentConfig):
        """注册 Agent 到 Cron"""
        self.agent_configs[config.id] = config
        
        # 创建 cron job
        self._create_cron_job(config)
        
    def _create_cron_job(self, config: AgentConfig):
        """为 Agent 创建 cron job"""
        # 转换秒数为 cron 表达式
        interval_min = max(1, config.heartbeat_interval // 60)
        
        # 使用 OpenClaw cron 系统
        import subprocess
        
        cron_expr = f"*/{interval_min} * * * *"
        
        # 构建 cron job
        job = {
            "name": f"agent-{config.id}-heartbeat",
            "schedule": {"kind": "cron", "expr": cron_expr, "tz": "Asia/Shanghai"},
            "payload": {
                "kind": "systemEvent",
                "text": f"HEARTBEAT: Agent {config.id} check tasks"
            },
            "sessionTarget": "main",
            "enabled": True
        }
        
        print(f"[Cron] Agent {config.id} 心跳任务: 每 {interval_min} 分钟")
        
    def trigger_heartbeat(self, agent_id: str):
        """手动触发心跳"""
        if agent_id in self.agent_configs:
            config = self.agent_configs[agent_id]
            print(f"[Cron] 触发 Agent {agent_id} 心跳")
            # 这里可以调用 Agent 的心跳方法
            return True
        return False


# 全局调度器实例
scheduler = HeartbeatScheduler()


def init_heartbeat_system():
    """初始化心跳系统"""
    # 创建 Agent 配置
    agents_config = [
        AgentConfig(
            id="yitai",
            name="yitai",
            role="技术官",
            skills=["编程", "代码", "脚本", "开发", "调试", "爬取", "修复"],
            model="claude-3-5-sonnet",
            heartbeat_interval=300  # 5分钟
        ),
        AgentConfig(
            id="bingbing",
            name="bingbing",
            role="创意官",
            skills=["设计", "创意", "封面", "内容", "文案", "写作", "图像", "视频"],
            model="claude-3-5-sonnet",
            heartbeat_interval=300
        ),
        AgentConfig(
            id="daping",
            name="daping",
            role="检测官",
            skills=["分析", "数据", "检测", "监控", "竞品"],
            model="claude-3-5-sonnet",
            heartbeat_interval=600  # 10分钟
        ),
        AgentConfig(
            id="spikey",
            name="spikey",
            role="审计官",
            skills=["审计", "复盘", "质量", "审查", "检查"],
            model="claude-3-5-sonnet",
            heartbeat_interval=600
        ),
        AgentConfig(
            id="xiaohongcai",
            name="xiaohongcai",
            role="运营官",
            skills=["社媒", "运营", "发布", "小红书", "公众号"],
            model="claude-3-5-sonnet",
            heartbeat_interval=300
        )
    ]
    
    # 注册所有 Agent
    for config in agents_config:
        agent = BaseAgent(config)
        scheduler.register_agent(agent)
    
    # 启动调度器
    scheduler.start()
    
    return scheduler


if __name__ == "__main__":
    # 测试
    init_heartbeat_system()
    
    # 运行一段时间
    time.sleep(60)
    
    print(json.dumps(scheduler.get_status(), indent=2, ensure_ascii=False))
