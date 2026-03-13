#!/usr/bin/env python3
"""
OpenClaw Multi-Agent CLI
命令行工具，用于管理任务和 Agents
"""

import argparse
import json
import requests
import sys
from datetime import datetime
from typing import Optional

API_URL = "http://localhost:3100"

def print_table(headers, rows):
    """打印表格"""
    # 计算列宽
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # 打印表头
    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(header_line)
    print("-" * len(header_line))
    
    # 打印行
    for row in rows:
        print(" | ".join(str(cell).ljust(w) for cell, w in zip(row, widths)))

def cmd_status(args):
    """查看系统状态"""
    try:
        resp = requests.get(f"{API_URL}/health", timeout=5)
        data = resp.json()
        
        print("🦞 OpenClaw Multi-Agent System")
        print(f"   状态: {'✅ 运行中' if data['status'] == 'ok' else '❌ 异常'}")
        print(f"   版本: {data['version']}")
        print(f"   Agents: {data['agents_count']}")
        print(f"   心跳调度: {'✅' if data['scheduler_running'] else '❌'}")
        
        # 获取任务统计
        tasks_resp = requests.get(f"{API_URL}/api/tasks", timeout=5)
        tasks = tasks_resp.json()
        
        print(f"\n📋 任务统计:")
        print(f"   总数: {len(tasks)}")
        
        status_counts = {}
        for t in tasks:
            status_counts[t['status']] = status_counts.get(t['status'], 0) + 1
        
        for status, count in status_counts.items():
            print(f"   {status}: {count}")
            
    except Exception as e:
        print(f"❌ 连接失败: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_list(args):
    """列出任务"""
    try:
        resp = requests.get(f"{API_URL}/api/tasks", timeout=5)
        tasks = resp.json()
        
        if not tasks:
            print("暂无任务")
            return
        
        if args.json:
            print(json.dumps(tasks, indent=2, ensure_ascii=False))
            return
        
        headers = ["ID", "标题", "Agent", "状态", "预算", "剩余"]
        rows = []
        
        for t in tasks[:20]:  # 最多显示20个
            rows.append([
                t['id'][:15],
                t['title'][:30],
                t['agent_name'][:10],
                t['status'],
                f"${t['budget']['total']}",
                f"${t['budget']['remaining']:.1f}"
            ])
        
        print_table(headers, rows)
        
        if len(tasks) > 20:
            print(f"\n... 还有 {len(tasks) - 20} 个任务")
            
    except Exception as e:
        print(f"❌ 获取失败: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_create(args):
    """创建任务"""
    try:
        data = {
            "title": args.title or args.description[:50],
            "description": args.description,
            "budget": args.budget,
            "priority": args.priority,
            "requester": args.requester or "cli"
        }
        
        resp = requests.post(
            f"{API_URL}/api/tasks",
            json=data,
            timeout=10
        )
        
        result = resp.json()
        
        if resp.status_code == 201:
            print(f"✅ 任务已创建")
            print(f"   ID: {result['id']}")
            print(f"   标题: {result['title']}")
            print(f"   指派给: @{result['agent_name']} ({result['agent_role']})")
            print(f"   预算: ${result['budget']['total']}")
            print(f"   状态: {result['status']}")
        else:
            print(f"❌ 创建失败: {result.get('error', '未知错误')}", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_show(args):
    """查看任务详情"""
    try:
        resp = requests.get(f"{API_URL}/api/tasks/{args.task_id}", timeout=5)
        
        if resp.status_code == 404:
            print(f"❌ 任务不存在: {args.task_id}", file=sys.stderr)
            sys.exit(1)
        
        task = resp.json()
        
        if args.json:
            print(json.dumps(task, indent=2, ensure_ascii=False))
            return
        
        print(f"📋 任务详情")
        print(f"   ID: {task['id']}")
        print(f"   标题: {task['title']}")
        print(f"   描述: {task['description']}")
        print(f"   状态: {task['status']}")
        print(f"   优先级: {task['priority']}")
        print(f"   指派给: @{task['agent_name']}")
        print(f"\n💰 预算:")
        print(f"   总额: ${task['budget']['total']}")
        print(f"   已花费: ${task['budget']['spent']}")
        print(f"   剩余: ${task['budget']['remaining']}")
        print(f"   使用率: {task['budget']['utilization'] * 100:.1f}%")
        print(f"\n📅 时间:")
        print(f"   创建: {task['created_at']}")
        if task['assigned_at']:
            print(f"   指派: {task['assigned_at']}")
        if task['started_at']:
            print(f"   开始: {task['started_at']}")
        if task['completed_at']:
            print(f"   完成: {task['completed_at']}")
        
        if task['audit_log']:
            print(f"\n📝 审计日志 (最近5条):")
            for log in task['audit_log'][-5:]:
                print(f"   [{log['timestamp']}] {log['event']} by {log['actor']}")
                
    except Exception as e:
        print(f"❌ 获取失败: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_agents(args):
    """列出 Agents"""
    try:
        resp = requests.get(f"{API_URL}/api/agents", timeout=5)
        agents = resp.json()
        
        if args.json:
            print(json.dumps(agents, indent=2, ensure_ascii=False))
            return
        
        print("🤖 Agents:")
        for id, data in agents.items():
            state = data.get('state', {})
            status = state.get('status', 'unknown')
            emoji = {
                'idle': '🟢',
                'busy': '🟡',
                'offline': '⚫'
            }.get(status, '⚪')
            
            print(f"\n   {emoji} @{data['config']['name']}")
            print(f"      角色: {data['config']['role']}")
            print(f"      状态: {status}")
            print(f"      技能: {', '.join(data['config']['skills'][:5])}")
            
            if state.get('current_task'):
                print(f"      当前任务: {state['current_task']}")
                
    except Exception as e:
        print(f"❌ 获取失败: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_match(args):
    """匹配 Agent"""
    try:
        resp = requests.post(
            f"{API_URL}/api/match",
            json={"description": args.description},
            timeout=5
        )
        
        result = resp.json()
        
        print(f"🔍 任务: {args.description}")
        print(f"   最佳匹配: @{result['agent']['name']}")
        print(f"   角色: {result['agent']['role']}")
        print(f"   置信度: {result['confidence']}")
        print(f"   技能: {', '.join(result['agent']['skills'])}")
        
    except Exception as e:
        print(f"❌ 匹配失败: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_complete(args):
    """完成任务"""
    try:
        data = {"result": {"message": args.message or "任务已完成"}}
        
        resp = requests.post(
            f"{API_URL}/api/tasks/{args.task_id}/complete",
            json=data,
            timeout=5
        )
        
        if resp.status_code == 200:
            print(f"✅ 任务 {args.task_id} 已完成")
        else:
            result = resp.json()
            print(f"❌ 失败: {result.get('error', '未知错误')}", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Multi-Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s status                    # 查看系统状态
  %(prog)s list                      # 列出任务
  %(prog)s create "爬取数据" -b 20    # 创建任务
  %(prog)s show TASK-xxx             # 查看任务详情
  %(prog)s agents                    # 列出 Agents
  %(prog)s match "设计Logo"          # 匹配 Agent
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # status
    subparsers.add_parser('status', help='查看系统状态')
    
    # list
    list_parser = subparsers.add_parser('list', help='列出任务')
    list_parser.add_argument('--json', action='store_true', help='JSON 输出')
    
    # create
    create_parser = subparsers.add_parser('create', help='创建任务')
    create_parser.add_argument('description', help='任务描述')
    create_parser.add_argument('-t', '--title', help='任务标题')
    create_parser.add_argument('-b', '--budget', type=float, default=0, help='预算')
    create_parser.add_argument('-p', '--priority', default='normal', 
                               choices=['low', 'normal', 'high', 'urgent'],
                               help='优先级')
    create_parser.add_argument('-r', '--requester', default='cli', help='请求者')
    
    # show
    show_parser = subparsers.add_parser('show', help='查看任务详情')
    show_parser.add_argument('task_id', help='任务ID')
    show_parser.add_argument('--json', action='store_true', help='JSON 输出')
    
    # agents
    agents_parser = subparsers.add_parser('agents', help='列出 Agents')
    agents_parser.add_argument('--json', action='store_true', help='JSON 输出')
    
    # match
    match_parser = subparsers.add_parser('match', help='匹配 Agent')
    match_parser.add_argument('description', help='任务描述')
    
    # complete
    complete_parser = subparsers.add_parser('complete', help='完成任务')
    complete_parser.add_argument('task_id', help='任务ID')
    complete_parser.add_argument('-m', '--message', help='完成消息')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 执行命令
    commands = {
        'status': cmd_status,
        'list': cmd_list,
        'create': cmd_create,
        'show': cmd_show,
        'agents': cmd_agents,
        'match': cmd_match,
        'complete': cmd_complete
    }
    
    commands[args.command](args)

if __name__ == '__main__':
    main()
