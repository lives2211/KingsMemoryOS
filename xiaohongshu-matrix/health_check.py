#!/usr/bin/env python3
"""
系统健康检查
- 检查磁盘空间
- 检查内存使用
- 检查日志文件大小
- 检查发布状态
"""

import os
import sys
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path

class HealthChecker:
    """健康检查器"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"):
        self.base_path = Path(base_path)
        self.issues = []
        self.warnings = []
        
    def check_disk_space(self):
        """检查磁盘空间"""
        stat = shutil.disk_usage(self.base_path)
        free_gb = stat.free / (1024**3)
        total_gb = stat.total / (1024**3)
        used_percent = (stat.used / stat.total) * 100
        
        print(f"💾 磁盘空间: {free_gb:.1f}GB / {total_gb:.1f}GB 可用")
        print(f"   使用率: {used_percent:.1f}%")
        
        if used_percent > 90:
            self.issues.append(f"磁盘空间不足: {used_percent:.1f}% 已使用")
        elif used_percent > 80:
            self.warnings.append(f"磁盘空间紧张: {used_percent:.1f}% 已使用")
        else:
            print("   ✅ 磁盘空间充足")
        
        return free_gb
    
    def check_memory(self):
        """检查内存"""
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            mem_total = 0
            mem_available = 0
            
            for line in meminfo.split('\n'):
                if 'MemTotal' in line:
                    mem_total = int(line.split()[1]) / 1024 / 1024
                elif 'MemAvailable' in line:
                    mem_available = int(line.split()[1]) / 1024 / 1024
            
            if mem_total > 0:
                used_percent = ((mem_total - mem_available) / mem_total) * 100
                print(f"🧠 内存使用: {mem_total - mem_available:.1f}GB / {mem_total:.1f}GB")
                print(f"   使用率: {used_percent:.1f}%")
                
                if used_percent > 90:
                    self.issues.append(f"内存使用率过高: {used_percent:.1f}%")
                elif used_percent > 80:
                    self.warnings.append(f"内存使用率偏高: {used_percent:.1f}%")
                else:
                    print("   ✅ 内存使用正常")
        except Exception as e:
            self.warnings.append(f"无法读取内存信息: {e}")
    
    def check_logs(self):
        """检查日志文件"""
        logs_dir = self.base_path / "logs"
        if not logs_dir.exists():
            return
        
        total_size = 0
        old_logs = []
        
        for log_file in logs_dir.glob("*.log"):
            size = log_file.stat().st_size
            total_size += size
            
            # 检查7天前的日志
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            if datetime.now() - mtime > timedelta(days=7):
                old_logs.append(log_file)
        
        print(f"📝 日志文件: {total_size / 1024 / 1024:.1f}MB")
        
        if total_size > 100 * 1024 * 1024:  # 100MB
            self.warnings.append(f"日志文件过大: {total_size / 1024 / 1024:.1f}MB")
        
        if old_logs:
            print(f"   发现 {len(old_logs)} 个旧日志文件")
            self.warnings.append(f"建议清理 {len(old_logs)} 个7天前的日志文件")
        else:
            print("   ✅ 日志文件正常")
    
    def check_generated_content(self):
        """检查生成内容"""
        generated_dir = self.base_path / "generated"
        if not generated_dir.exists():
            return
        
        total_files = 0
        total_size = 0
        
        for account_dir in generated_dir.iterdir():
            if account_dir.is_dir():
                files = list(account_dir.glob("*"))
                total_files += len(files)
                total_size += sum(f.stat().st_size for f in files if f.is_file())
        
        print(f"🎨 生成内容: {total_files} 个文件, {total_size / 1024 / 1024:.1f}MB")
        
        if total_size > 500 * 1024 * 1024:  # 500MB
            self.warnings.append(f"生成内容占用空间较大: {total_size / 1024 / 1024:.1f}MB")
        else:
            print("   ✅ 生成内容正常")
    
    def check_schedule(self):
        """检查发布计划"""
        schedule_file = self.base_path / "schedule.json"
        if not schedule_file.exists():
            self.warnings.append("未找到发布计划文件")
            return
        
        try:
            with open(schedule_file, 'r') as f:
                schedule = json.load(f)
            
            today = datetime.now().date().isoformat()
            today_posts = schedule.get(today, [])
            
            if not today_posts:
                self.warnings.append("今日无发布计划")
                return
            
            total = len(today_posts)
            posted = sum(1 for p in today_posts if p.get("status") == "posted")
            pending = total - posted
            
            print(f"📅 今日计划: {total} 篇")
            print(f"   已完成: {posted} 篇")
            print(f"   待发布: {pending} 篇")
            
            if pending == 0:
                print("   ✅ 今日任务全部完成")
            elif pending > total * 0.5:
                self.warnings.append(f"今日还有 {pending} 篇待发布")
            
            # 检查是否有逾期的
            now = datetime.now()
            overdue = 0
            for post in today_posts:
                if post.get("status") != "posted":
                    try:
                        post_time = datetime.fromisoformat(post["time"])
                        if post_time < now:
                            overdue += 1
                    except:
                        pass
            
            if overdue > 0:
                self.issues.append(f"有 {overdue} 篇内容已逾期")
        
        except Exception as e:
            self.issues.append(f"读取发布计划失败: {e}")
    
    def check_cookie_validity(self):
        """检查Cookie有效性"""
        accounts = ["tech-geek", "life-aesthetics", "career-growth", "foodie", "fashion"]
        valid_count = 0
        invalid_count = 0
        
        for account in accounts:
            env_file = self.base_path / f".env.{account}"
            if env_file.exists():
                content = env_file.read_text()
                if "XHS_COOKIE=" in content and len(content) > 100:
                    valid_count += 1
                else:
                    invalid_count += 1
        
        print(f"🔑 Cookie配置: {valid_count}/5 个账号已配置")
        
        if invalid_count > 0:
            self.warnings.append(f"{invalid_count} 个账号Cookie未配置")
        elif valid_count == 0:
            self.issues.append("所有账号Cookie未配置")
        else:
            print("   ✅ Cookie配置正常")
    
    def run_check(self):
        """运行健康检查"""
        print("=" * 60)
        print("🦞 系统健康检查")
        print("=" * 60)
        print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        self.check_disk_space()
        print()
        
        self.check_memory()
        print()
        
        self.check_logs()
        print()
        
        self.check_generated_content()
        print()
        
        self.check_schedule()
        print()
        
        self.check_cookie_validity()
        print()
        
        # 显示结果
        print("=" * 60)
        print("检查结果")
        print("=" * 60)
        
        if self.issues:
            print(f"\n❌ 发现 {len(self.issues)} 个问题:")
            for issue in self.issues:
                print(f"   - {issue}")
        
        if self.warnings:
            print(f"\n⚠️  发现 {len(self.warnings)} 个警告:")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        if not self.issues and not self.warnings:
            print("\n✅ 系统健康状况良好！")
        
        print()
        print("=" * 60)
        
        return len(self.issues) == 0
    
    def auto_fix(self):
        """自动修复"""
        print("\n🔧 尝试自动修复...")
        
        # 清理旧日志
        logs_dir = self.base_path / "logs"
        if logs_dir.exists():
            cleaned = 0
            for log_file in logs_dir.glob("*.log"):
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if datetime.now() - mtime > timedelta(days=7):
                    log_file.unlink()
                    cleaned += 1
            
            if cleaned > 0:
                print(f"✅ 已清理 {cleaned} 个旧日志文件")
        
        print("✅ 自动修复完成")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="系统健康检查")
    parser.add_argument("--fix", action="store_true", help="自动修复问题")
    
    args = parser.parse_args()
    
    checker = HealthChecker()
    healthy = checker.run_check()
    
    if args.fix and not healthy:
        checker.auto_fix()
    
    return 0 if healthy else 1

if __name__ == "__main__":
    sys.exit(main())
