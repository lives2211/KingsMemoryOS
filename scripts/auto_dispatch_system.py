#!/usr/bin/env python3
"""
总指挥自动派发系统
自动监控任务队列，智能分发给各 Agent
"""

import json
import time
import random
from datetime import datetime
from pathlib import Path
import subprocess
import sys

class AutoDispatchSystem:
    """自动派发系统"""
    
    def __init__(self):
        self.base_path = Path("/home/fengxueda/.openclaw/workspace")
        self.memory_path = self.base_path / "memory" / "shared"
        self.dispatch_log = self.base_path / "logs" / "dispatch_system.log"
        
        # Agent 配置
        self.agents = {
            "yitai": {"role": "编程", "skills": ["coding", "debugging", "architecture"]},
            "bingbing": {"role": "创作", "skills": ["content", "design", "creative"]},
            "daping": {"role": "检测", "skills": ["testing", "analysis", "monitoring"]},
            "spikey": {"role": "审计", "skills": ["review", "audit", "quality"]},
            "xiaohongcai": {"role": "运营", "skills": ["social_media", "growth", "analytics"]},
        }
    
    def _log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] {message}"
        print(log_line)
        
        # 写入日志文件
        self.dispatch_log.parent.mkdir(parents=True, exist_ok=True)
        with open(self.dispatch_log, 'a', encoding='utf-8') as f:
            f.write(log_line + '\n')
    
    def check_pending_tasks(self) -> list:
        """检查待处理任务"""
        tasks = []
        
        # 检查共享记忆目录
        if self.memory_path.exists():
            for task_file in self.memory_path.glob("*-task.json"):
                try:
                    with open(task_file, 'r', encoding='utf-8') as f:
                        task = json.load(f)
                        task['file'] = str(task_file)
                        if task.get('status') == 'pending':
                            tasks.append(task)
                except Exception as e:
                    self._log(f"❌ 读取任务文件失败: {task_file}, 错误: {e}")
        
        return tasks
    
    def match_agent(self, task: dict) -> str:
        """匹配最适合的 Agent"""
        task_type = task.get('type', '').lower()
        task_skills = task.get('skills', [])
        
        best_agent = None
        best_score = 0
        
        for agent_id, agent_info in self.agents.items():
            score = 0
            
            # 技能匹配
            for skill in task_skills:
                if skill in agent_info['skills']:
                    score += 2
            
            # 类型匹配
            if task_type in agent_info['role'].lower():
                score += 3
            
            # 检查 Agent 是否可用
            agent_session = f"agent:{agent_id}:discord:channel"
            # TODO: 检查 session 状态
            
            if score > best_score:
                best_score = score
                best_agent = agent_id
        
        # 如果没有匹配，随机分配
        if not best_agent:
            best_agent = random.choice(list(self.agents.keys()))
        
        return best_agent
    
    def dispatch_task(self, task: dict, agent_id: str) -> bool:
        """派发任务给 Agent"""
        try:
            self._log(f"📤 派发任务: {task.get('id', 'unknown')} -> {agent_id}")
            
            # 构建派发消息
            dispatch_msg = {
                "type": "task_dispatch",
                "task_id": task.get('id'),
                "title": task.get('title'),
                "description": task.get('description'),
                "requirements": task.get('requirements', []),
                "priority": task.get('priority', 'normal'),
                "deadline": task.get('deadline'),
                "source": "auto_dispatch_system"
            }
            
            # 保存派发记录
            dispatch_file = self.memory_path / f"dispatched_{task.get('id')}_{agent_id}.json"
            with open(dispatch_file, 'w', encoding='utf-8') as f:
                json.dump(dispatch_msg, f, ensure_ascii=False, indent=2)
            
            # 更新任务状态
            task['status'] = 'dispatched'
            task['assigned_to'] = agent_id
            task['dispatched_at'] = datetime.now().isoformat()
            
            # 保存更新后的任务
            task_file = Path(task['file'])
            with open(task_file, 'w', encoding='utf-8') as f:
                json.dump(task, f, ensure_ascii=False, indent=2)
            
            self._log(f"✅ 任务已派发: {task.get('id')} -> {agent_id}")
            return True
            
        except Exception as e:
            self._log(f"❌ 派发失败: {e}")
            return False
    
    def run_cycle(self):
        """运行一个检查周期"""
        self._log("🔄 开始任务检查周期...")
        
        # 检查待处理任务
        pending_tasks = self.check_pending_tasks()
        
        if not pending_tasks:
            self._log("ℹ️  暂无待处理任务")
            return
        
        self._log(f"📋 发现 {len(pending_tasks)} 个待处理任务")
        
        # 派发任务
        dispatched_count = 0
        for task in pending_tasks:
            agent_id = self.match_agent(task)
            if self.dispatch_task(task, agent_id):
                dispatched_count += 1
            
            # 避免过快派发
            time.sleep(1)
        
        self._log(f"✅ 周期完成: 派发 {dispatched_count}/{len(pending_tasks)} 个任务")
    
    def run_daemon(self, interval: int = 300):
        """守护进程模式运行"""
        self._log("🚀 总指挥自动派发系统启动")
        self._log(f"⏱️  检查间隔: {interval}秒")
        self._log("按 Ctrl+C 停止\n")
        
        try:
            while True:
                self.run_cycle()
                time.sleep(interval)
        except KeyboardInterrupt:
            self._log("\n👋 系统已停止")


def create_sample_task():
    """创建示例任务"""
    task = {
        "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "type": "coding",
        "title": "修复小红书发布功能",
        "description": "小红财出现 HTTP 400 错误，需要修复",
        "skills": ["debugging", "python"],
        "priority": "high",
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    # 保存任务文件
    memory_path = Path("/home/fengxueda/.openclaw/workspace/memory/shared")
    memory_path.mkdir(parents=True, exist_ok=True)
    
    task_file = memory_path / f"{task['id']}-task.json"
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(task, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 示例任务已创建: {task_file}")
    return task


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="总指挥自动派发系统")
    parser.add_argument("--daemon", action="store_true", help="守护进程模式")
    parser.add_argument("--once", action="store_true", help="运行一次")
    parser.add_argument("--interval", type=int, default=300, help="检查间隔(秒)")
    parser.add_argument("--create-sample", action="store_true", help="创建示例任务")
    
    args = parser.parse_args()
    
    if args.create_sample:
        create_sample_task()
    elif args.daemon:
        dispatcher = AutoDispatchSystem()
        dispatcher.run_daemon(args.interval)
    elif args.once:
        dispatcher = AutoDispatchSystem()
        dispatcher.run_cycle()
    else:
        print("总指挥自动派发系统")
        print("\n用法:")
        print("  python3 auto_dispatch_system.py --daemon          # 守护进程模式")
        print("  python3 auto_dispatch_system.py --once            # 运行一次")
        print("  python3 auto_dispatch_system.py --create-sample   # 创建示例任务")
