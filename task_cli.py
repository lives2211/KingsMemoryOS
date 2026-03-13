#!/usr/bin/env python3
"""
任务管理CLI工具 - 核心功能实现
支持: add, list, done, delete
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 数据文件路径
DATA_FILE = Path.home() / ".task_cli" / "tasks.json"

def ensure_data_dir():
    """确保数据目录存在"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_tasks():
    """加载所有任务"""
    ensure_data_dir()
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    """保存所有任务"""
    ensure_data_dir()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def generate_id(tasks):
    """生成新任务ID"""
    if not tasks:
        return 1
    return max(t.get('id', 0) for t in tasks) + 1

def add_task(title, priority='medium'):
    """添加新任务"""
    tasks = load_tasks()
    task = {
        'id': generate_id(tasks),
        'title': title,
        'priority': priority,
        'status': 'todo',
        'created_at': datetime.now().isoformat(),
        'completed_at': None
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ 任务已添加: [{task['id']}] {title}")
    return task['id']

def list_tasks(status=None):
    """列出任务"""
    tasks = load_tasks()
    if not tasks:
        print("📭 暂无任务")
        return
    
    # 过滤状态
    if status:
        tasks = [t for t in tasks if t.get('status') == status]
    
    # 排序: 优先级 > 创建时间
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    tasks.sort(key=lambda x: (priority_order.get(x.get('priority', 'medium'), 1), x.get('created_at', '')))
    
    print(f"\n📋 任务列表 (共{len(tasks)}个):\n")
    print(f"{'ID':<6}{'状态':<10}{'优先级':<10}{'标题':<40}{'创建时间'}")
    print("-" * 80)
    
    for task in tasks:
        status_icon = "✅" if task.get('status') == 'done' else "⏳"
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.get('priority', 'medium'), "🟡")
        created = task.get('created_at', '')[:10]
        print(f"{task['id']:<6}{status_icon:<10}{priority_icon:<10}{task.get('title', '')[:38]:<40}{created}")
    print()

def done_task(task_id):
    """标记任务完成"""
    tasks = load_tasks()
    for task in tasks:
        if task.get('id') == int(task_id):
            task['status'] = 'done'
            task['completed_at'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"✅ 任务已完成: [{task_id}] {task.get('title', '')}")
            return True
    print(f"❌ 任务未找到: {task_id}")
    return False

def delete_task(task_id):
    """删除任务"""
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task.get('id') == int(task_id):
            deleted = tasks.pop(i)
            save_tasks(tasks)
            print(f"🗑️ 任务已删除: [{task_id}] {deleted.get('title', '')}")
            return True
    print(f"❌ 任务未找到: {task_id}")
    return False

def show_help():
    """显示帮助信息"""
    print("""
📋 任务管理CLI工具

用法: python task_cli.py <命令> [参数]

命令:
    add <标题> [--priority high|medium|low]  添加新任务
    list [todo|done]                         列出任务
    done <任务ID>                            标记任务完成
    delete <任务ID>                          删除任务
    help                                     显示帮助

示例:
    python task_cli.py add "完成报告" --priority high
    python task_cli.py list
    python task_cli.py done 1
    python task_cli.py delete 1
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'add':
        if len(sys.argv) < 3:
            print("❌ 错误: 请提供任务标题")
            return
        
        title = sys.argv[2]
        priority = 'medium'
        
        # 解析 --priority 参数
        if '--priority' in sys.argv:
            idx = sys.argv.index('--priority')
            if idx + 1 < len(sys.argv):
                priority = sys.argv[idx + 1]
        
        add_task(title, priority)
    
    elif command == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status)
    
    elif command == 'done':
        if len(sys.argv) < 3:
            print("❌ 错误: 请提供任务ID")
            return
        done_task(sys.argv[2])
    
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("❌ 错误: 请提供任务ID")
            return
        delete_task(sys.argv[2])
    
    elif command == 'help':
        show_help()
    
    else:
        print(f"❌ 未知命令: {command}")
        show_help()

if __name__ == '__main__':
    main()
