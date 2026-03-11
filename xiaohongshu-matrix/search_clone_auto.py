#!/usr/bin/env python3
"""
搜索+复刻一体化工具
自动搜索爆款 → 选择最爆款 → 复刻生成
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class SearchCloneAuto:
    """搜索复刻自动化"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"):
        self.base_path = Path(base_path)
        self.output_dir = self.base_path / "generated" / "viral_clones"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def search_by_cli(self, keyword, sort="popular", page=1):
        """使用CLI搜索"""
        print(f"🔍 搜索: {keyword}")
        
        cmd = [
            "xhs", "search", keyword,
            "--sort", sort,
            "--page", str(page),
            "--yaml"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                if "not_authenticated" in result.stderr:
                    print("❌ 未登录，请先运行: xhs login --qrcode")
                    return None
                print(f"❌ 搜索失败: {result.stderr}")
                return None
            
            return result.stdout
            
        except Exception as e:
            print(f"❌ 异常: {e}")
            return None
    
    def parse_search_result(self, yaml_output):
        """解析搜索结果"""
        # 简化解析，提取笔记信息
        notes = []
        
        lines = yaml_output.split('\n')
        current_note = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith("- id:"):
                if current_note:
                    notes.append(current_note)
                current_note = {"id": line.split(":")[1].strip()}
            elif line.startswith("title:") and current_note:
                current_note["title"] = line.split(":", 1)[1].strip()
            elif line.startswith("likes:") and current_note:
                current_note["likes"] = int(line.split(":")[1].strip())
            elif line.startswith("url:") and current_note:
                current_note["url"] = line.split(":", 1)[1].strip()
        
        if current_note:
            notes.append(current_note)
        
        return notes
    
    def select_best_viral(self, notes):
        """选择最爆款"""
        if not notes:
            return None
        
        # 按点赞数排序
        sorted_notes = sorted(notes, key=lambda x: x.get("likes", 0), reverse=True)
        return sorted_notes[0]
    
    def clone_note(self, note_url, account):
        """复刻笔记"""
        print(f"🎨 复刻: {note_url}")
        
        clone_script = self.base_path / "clone_viral.py"
        
        cmd = [
            "python3", str(clone_script),
            note_url,
            "--account", account
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            print(result.stdout)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ 复刻异常: {e}")
            return False
    
    def run(self, account, keyword):
        """运行完整流程"""
        print("=" * 50)
        print(f"🚀 搜索+复刻: {account} | {keyword}")
        print("=" * 50)
        print()
        
        # 1. 搜索
        search_result = self.search_by_cli(keyword)
        if not search_result:
            return False
        
        # 2. 解析结果
        notes = self.parse_search_result(search_result)
        if not notes:
            print("❌ 未找到笔记")
            return False
        
        print(f"✅ 找到 {len(notes)} 篇笔记:")
        for i, note in enumerate(notes[:5], 1):
            title = note.get("title", "N/A")[:40]
            likes = note.get("likes", 0)
            print(f"   {i}. {title}... (👍 {likes})")
        print()
        
        # 3. 选择最爆款
        best = self.select_best_viral(notes)
        if not best:
            print("❌ 无法选择爆款")
            return False
        
        print(f"🎯 最爆款: {best.get('title', 'N/A')[:50]}...")
        print(f"   点赞: {best.get('likes', 0)}")
        print(f"   URL: {best.get('url', 'N/A')}")
        print()
        
        # 4. 复刻
        success = self.clone_note(best.get("url", ""), account)
        
        if success:
            print("✅ 搜索+复刻完成！")
        else:
            print("❌ 复刻失败")
        
        return success

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="搜索+复刻一体化")
    parser.add_argument("account", help="账号类型")
    parser.add_argument("keyword", help="搜索关键词")
    
    args = parser.parse_args()
    
    tool = SearchCloneAuto()
    success = tool.run(args.account, args.keyword)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
