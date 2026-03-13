#!/usr/bin/env python3
"""
完整增长系统
1. 发布中文区热门 Skill（英文）
2. 自动互动最近24小时帖子
3. 配合 Rube MCP 进行 Reddit 养号
"""

import subprocess
import json
import time
import random
from datetime import datetime
from pathlib import Path


class CompleteGrowthSystem:
    """完整增长系统"""
    
    def __init__(self):
        self.log_file = Path("growth_system.log")
    
    def _log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] {message}\n"
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
        print(log_line, end='')
    
    def post_china_skill(self):
        """发布中文区 Skill"""
        self._log("🚀 Step 1: Posting China Skill (English)")
        
        result = subprocess.run(
            ['python3', 'china_skill_exporter.py', '--dry-run'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            self._log("✅ Generated content")
            # 实际发布
            result = subprocess.run(
                ['python3', 'china_skill_exporter.py'],
                capture_output=True,
                text=True,
                timeout=600
            )
            if result.returncode == 0:
                self._log("✅ Posted successfully")
                return True
        
        self._log("❌ Posting failed")
        return False
    
    def engage_recent_posts(self):
        """互动最近24小时帖子"""
        self._log("🤝 Step 2: Engaging with recent posts")
        
        result = subprocess.run(
            ['python3', 'growth_engagement_v2.py', '--count', '10'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            self._log("✅ Engagement completed")
            return True
        else:
            self._log(f"❌ Engagement failed: {result.stderr[:100]}")
            return False
    
    def generate_rube_commands(self):
        """生成 Rube 命令"""
        self._log("🛠️ Step 3: Rube MCP Commands for Reddit")
        
        commands = [
            "Rube, help me post 10 valuable comments on r/artificialintelligence about AI automation",
            "Rube, find trending posts on r/productivity and add helpful replies",
            "Rube, engage with 5 posts on r/sidehustle about automation tools",
            "Rube, comment on r/entrepreneur posts about scaling with AI",
        ]
        
        print("\n" + "="*60)
        print("Rube MCP Commands (Run in Claude Code CLI):")
        print("="*60 + "\n")
        
        for i, cmd in enumerate(commands, 1):
            print(f"{i}. {cmd}\n")
        
        print("Setup Steps:")
        print("1. Install Rube: https://rube.app")
        print("2. Add to Claude Code: claude mcp add rube")
        print("3. Run commands above")
        print("4. Authorize Reddit when prompted")
        print("5. Start gaining Karma automatically")
        print("="*60)
    
    def run_daily(self):
        """运行每日增长流程"""
        self._log("="*60)
        self._log("🚀 Complete Growth System - Daily Run")
        self._log(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self._log("="*60)
        
        # 1. 发布内容
        self.post_china_skill()
        
        # 2. 等待后互动
        wait_min = random.randint(120, 240)
        self._log(f"⏳ Waiting {wait_min} minutes before engagement...")
        time.sleep(wait_min * 60)
        
        # 3. 互动
        self.engage_recent_posts()
        
        # 4. 显示 Rube 命令
        self.generate_rube_commands()
        
        self._log("✅ Daily growth cycle completed")
        self._log("="*60)
    
    def show_strategy(self):
        """显示完整策略"""
        strategy = """
╔══════════════════════════════════════════════════════════════════╗
║           完整涨粉策略 (Twitter + Reddit)                         ║
╚══════════════════════════════════════════════════════════════════╝

📈 目标：每天涨 10+ 粉丝 (英文区)

🐦 Twitter 策略 (每天):
  1. 发布 1 条 Thread (中文区热门 Skill)
     → 详细拆解，数据驱动
     → 12 条推文，价值满满
  
  2. 互动 10 条最近24小时帖子
     → 高互动帖子优先
     → 相关评论，提供价值
     → 随机间隔 1-2 分钟

🔥 Reddit 策略 (配合 Rube):
  1. 安装 Rube MCP
  2. 自动评论 10 条/天
  3. 积累 Karma 值
  4. 后期发外链引流

⏰ 时间安排:
  09:00 - 发布 Twitter Thread
  11:00-15:00 - 互动最近帖子
  随时 - Rube 自动 Reddit 互动

📊 预期效果:
  Week 1: +50-70 粉丝
  Week 2: +100-150 粉丝
  Week 3: +200-300 粉丝
  Month 1: 1000+ 粉丝，开始变现

💰 变现路径:
  1000 followers → Twitter 广告分成
  5000 followers → 付费咨询、课程
  10000 followers → 品牌合作、赞助

🎯 关键成功因素:
  1. 内容质量 > 数量
  2. 互动真实 > 机器人
  3. 持续输出 > 爆发式
  4. 价值优先 > 推销

═══════════════════════════════════════════════════════════════════
"""
        print(strategy)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true', help='Run daily cycle')
    parser.add_argument('--strategy', action='store_true', help='Show strategy')
    
    args = parser.parse_args()
    
    system = CompleteGrowthSystem()
    
    if args.strategy:
        system.show_strategy()
    elif args.run:
        system.run_daily()
    else:
        print("Usage:")
        print("  python3 complete_growth_system.py --strategy  # 查看策略")
        print("  python3 complete_growth_system.py --run       # 运行每日流程")


if __name__ == "__main__":
    main()
