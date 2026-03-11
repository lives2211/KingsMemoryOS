#!/usr/bin/env python3
"""
小红书搜索API接入
使用xiaohongshu-cli或直接调用API
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class XHSSearchAPI:
    """小红书搜索API"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"):
        self.base_path = Path(base_path)
        self.cookie = self.load_cookie()
    
    def load_cookie(self, account="tech-geek"):
        """加载Cookie"""
        env_file = self.base_path / f".env.{account}"
        
        if not env_file.exists():
            return None
        
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith("XHS_COOKIE="):
                    return line.replace("XHS_COOKIE=", "").strip()
        
        return None
    
    def search_by_cli(self, keyword, sort="popular", note_type="all", page=1):
        """
        使用xiaohongshu-cli搜索
        
        Args:
            keyword: 搜索关键词
            sort: 排序方式 (general|popular|latest)
            note_type: 笔记类型 (all|video|image)
            page: 页码
        
        Returns:
            搜索结果列表
        """
        print(f"🔍 使用CLI搜索: {keyword}")
        
        cmd = [
            "xhs", "search", keyword,
            "--sort", sort,
            "--type", note_type,
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
                print(f"❌ 搜索失败: {result.stderr}")
                return None
            
            # 解析YAML输出
            print("✅ 搜索成功")
            print("\n原始结果:")
            print(result.stdout[:1000])  # 只显示前1000字符
            
            return result.stdout
            
        except Exception as e:
            print(f"❌ 异常: {e}")
            return None
    
    def search_hot(self, category="food"):
        """
        获取热门笔记
        
        Args:
            category: 分类 (fashion|food|cosmetics|movie|career|love|home|gaming|travel|fitness)
        """
        print(f"🔥 获取热门: {category}")
        
        cmd = ["xhs", "hot", "-c", category, "--yaml"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"❌ 获取失败: {result.stderr}")
                return None
            
            print("✅ 获取成功")
            return result.stdout
            
        except Exception as e:
            print(f"❌ 异常: {e}")
            return None
    
    def get_feed(self):
        """获取推荐流"""
        print("📱 获取推荐流...")
        
        cmd = ["xhs", "feed", "--yaml"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"❌ 获取失败: {result.stderr}")
                return None
            
            print("✅ 获取成功")
            return result.stdout
            
        except Exception as e:
            print(f"❌ 异常: {e}")
            return None
    
    def parse_notes(self, yaml_output):
        """解析笔记列表"""
        # 简化解析，实际需要完整YAML解析
        notes = []
        
        # 这里应该使用PyYAML解析
        # 暂时返回原始数据
        
        return notes

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书搜索API")
    parser.add_argument("keyword", nargs="?", help="搜索关键词")
    parser.add_argument("--hot", action="store_true", help="获取热门")
    parser.add_argument("--category", default="food", help="热门分类")
    parser.add_argument("--feed", action="store_true", help="获取推荐流")
    
    args = parser.parse_args()
    
    api = XHSSearchAPI()
    
    if args.feed:
        result = api.get_feed()
    elif args.hot:
        result = api.search_hot(args.category)
    elif args.keyword:
        result = api.search_by_cli(args.keyword)
    else:
        parser.print_help()
        return 1
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())
