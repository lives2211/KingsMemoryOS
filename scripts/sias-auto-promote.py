#!/usr/bin/env python3
"""SIAS Auto-Promote - 自动检测并升级 critical 学习"""

import os
import re
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
LEARNINGS_DIR = os.path.join(WORKSPACE, ".learnings")
MEMORY_FILE = os.path.join(WORKSPACE, "MEMORY.md")

def parse_entry(content):
    """解析学习条目"""
    lines = content.strip().split('\n')
    if not lines:
        return None
    
    # 提取 ID 和标题
    header = lines[0]
    match = re.match(r'## \[(.+?)\] (.+)', header)
    if not match:
        return None
    
    entry_id = match.group(1)
    title = match.group(2)
    
    # 提取字段
    data = {'id': entry_id, 'title': title}
    for line in lines[1:]:
        if '**Area**:' in line:
            data['area'] = line.split(':')[1].strip()
        elif '**Priority**:' in line:
            data['priority'] = line.split(':')[1].strip()
        elif '**Status**:' in line:
            data['status'] = line.split(':')[1].strip()
    
    return data

def find_entries(filepath):
    """查找所有条目"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 分割条目
    entries = re.split(r'\n(?=## \[)', content)
    results = []
    
    for entry in entries:
        if entry.startswith('## ['):
            parsed = parse_entry(entry)
            if parsed:
                results.append((entry, parsed))
    
    return results

def should_promote(entry_data):
    """检查是否应该升级"""
    # 条件1: Priority = critical
    if entry_data.get('priority') == 'critical':
        return True
    
    # 条件2: Status = active 且重复3次（简化版）
    # 实际应该检查整个文件中的重复
    
    return False

def promote_to_memory(entry_data, source_file):
    """升级到 MEMORY.md"""
    date = datetime.now().strftime('%Y-%m-%d')
    
    # 检查是否已存在
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            if entry_data['id'] in f.read():
                print(f"  -> Already in MEMORY.md")
                return False
    
    # 添加到 MEMORY.md
    with open(MEMORY_FILE, 'a') as f:
        f.write(f"\n## [{entry_data['id']}] {entry_data['title']}\n")
        f.write(f"- **Priority**: {entry_data.get('priority', 'medium')}\n")
        f.write(f"- **Promoted**: {date}\n")
        f.write(f"- **Source**: {source_file}\n")
    
    return True

def mark_archived(filepath, entry_id):
    """标记为 archived"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 替换 Status: active -> Status: archived
    pattern = rf'(## \[{re.escape(entry_id)}\].*?Status:) active'
    content = re.sub(pattern, r'\1 archived', content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(content)

def main():
    print(f"=== SIAS Auto-Promote ({datetime.now().strftime('%Y-%m-%d')}) ===\n")
    
    promoted = 0
    
    for filename in os.listdir(LEARNINGS_DIR):
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(LEARNINGS_DIR, filename)
        print(f"Checking: {filename}")
        
        entries = find_entries(filepath)
        
        for entry_text, entry_data in entries:
            if entry_data.get('status') == 'active' and should_promote(entry_data):
                print(f"  Found CRITICAL: {entry_data['id']}")
                
                if promote_to_memory(entry_data, filename):
                    print(f"  -> Promoted to MEMORY.md")
                    mark_archived(filepath, entry_data['id'])
                    promoted += 1
    
    print(f"\n=== Result ===")
    if promoted > 0:
        print(f"✅ Promoted {promoted} entries")
    else:
        print("ℹ️  No critical entries to promote")

if __name__ == "__main__":
    main()
