#!/usr/bin/env python3
"""
设置Cron定时任务
- 每日生成发布计划
- 定时检查并发布内容
- 定时数据分析
"""

import json
from datetime import datetime
from pathlib import Path

CRON_JOBS = {
    "xhs_generate_schedule": {
        "description": "每日生成小红书发布计划",
        "schedule": "0 6 * * *",  # 每天6:00
        "command": "cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 scheduler.py >> logs/scheduler.log 2>&1"
    },
    "xhs_auto_post": {
        "description": "小红书自动发布检查",
        "schedule": "*/10 * * * *",  # 每10分钟
        "command": "cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 auto_post.py --once >> logs/auto_post.log 2>&1"
    },
    "xhs_daily_report": {
        "description": "每日数据报告",
        "schedule": "0 23 * * *",  # 每天23:00
        "command": "cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 analytics.py --report >> logs/daily_report.log 2>&1"
    },
    "xhs_weekly_export": {
        "description": "每周数据导出",
        "schedule": "0 0 * * 0",  # 每周日0:00
        "command": "cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 analytics.py --export >> logs/weekly_export.log 2>&1"
    }
}

def generate_cron_file():
    """生成cron配置文件"""
    cron_content = """# 小红书矩阵运营系统 - Cron配置
# 生成时间: {timestamp}
# 
# 安装方法:
#   crontab cron.txt
#
# 查看任务:
#   crontab -l
#
# 删除任务:
#   crontab -r

SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
HOME=/home/fengxueda

""".format(timestamp=datetime.now().isoformat())
    
    for job_name, job_config in CRON_JOBS.items():
        cron_content += f"# {job_config['description']}\n"
        cron_content += f"{job_config['schedule']} {job_config['command']}\n\n"
    
    return cron_content

def save_cron_file():
    """保存cron文件"""
    base_path = Path("/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix")
    cron_file = base_path / "cron.txt"
    
    content = generate_cron_file()
    
    with open(cron_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Cron配置已保存: {cron_file}")
    return cron_file

def print_install_instructions():
    """打印安装说明"""
    print("\n" + "=" * 60)
    print("🦞 Cron定时任务配置")
    print("=" * 60)
    print("\n已生成的任务:")
    print()
    
    for job_name, job_config in CRON_JOBS.items():
        print(f"📋 {job_config['description']}")
        print(f"   时间: {job_config['schedule']}")
        print(f"   命令: {job_config['command'][:50]}...")
        print()
    
    print("=" * 60)
    print("\n安装方法:")
    print("  1. 安装cron任务:")
    print("     crontab cron.txt")
    print()
    print("  2. 查看已安装任务:")
    print("     crontab -l")
    print()
    print("  3. 删除所有任务:")
    print("     crontab -r")
    print()
    print("  4. 编辑任务:")
    print("     crontab -e")
    print()
    print("=" * 60)

def main():
    """主函数"""
    cron_file = save_cron_file()
    print_install_instructions()
    
    # 显示文件内容
    print("\n生成的配置文件内容:")
    print("-" * 60)
    with open(cron_file, 'r') as f:
        print(f.read())

if __name__ == "__main__":
    main()
