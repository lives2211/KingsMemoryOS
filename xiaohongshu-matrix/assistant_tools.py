#!/usr/bin/env python3
"""
辅助运营工具集成
- aitu: AI绘图创作视频
- union-search: 多平台搜索
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

class AITUTool:
    """AI绘图创作视频工具"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix/aitu"):
        self.base_path = Path(base_path)
        
    def is_available(self) -> bool:
        """检查是否可用"""
        return self.base_path.exists()
    
    def generate_image(self, prompt: str, model: str = "gemini-2.5-flash-image") -> Dict:
        """生成图片"""
        # aitu需要通过API调用或Web界面使用
        # 这里提供封装接口
        return {
            "tool": "aitu",
            "action": "generate_image",
            "prompt": prompt,
            "model": model,
            "note": "请访问 http://localhost:7200 或使用API调用"
        }
    
    def generate_video(self, prompt: str, model: str = "veo3") -> Dict:
        """生成视频"""
        return {
            "tool": "aitu",
            "action": "generate_video",
            "prompt": prompt,
            "model": model,
            "note": "请访问 http://localhost:7200 或使用API调用"
        }
    
    def create_mindmap(self, content: str) -> Dict:
        """创建思维导图"""
        return {
            "tool": "aitu",
            "action": "create_mindmap",
            "content": content,
            "note": "支持Markdown转思维导图"
        }
    
    def start_server(self) -> bool:
        """启动aitu服务"""
        try:
            os.chdir(self.base_path)
            # 检查是否已安装依赖
            if not (self.base_path / "node_modules").exists():
                subprocess.run(["npm", "install"], check=True)
            # 启动服务
            subprocess.Popen(["npm", "start"], 
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            print(f"启动aitu失败: {e}")
            return False

class UnionSearchTool:
    """统一搜索工具"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix/union-search"):
        self.base_path = Path(base_path)
        self.cli_path = self.base_path / "union_search_cli.py"
        
    def is_available(self) -> bool:
        """检查是否可用"""
        return self.cli_path.exists()
    
    def search_xiaohongshu(self, keyword: str, limit: int = 10) -> List[Dict]:
        """搜索小红书"""
        try:
            cmd = [
                "python3", str(self.cli_path),
                "xiaohongshu", keyword,
                "--limit", str(limit)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.base_path)
            if result.returncode == 0:
                # 解析结果
                return self._parse_results(result.stdout)
            else:
                print(f"搜索失败: {result.stderr}")
                return []
        except Exception as e:
            print(f"搜索异常: {e}")
            return []
    
    def search_douyin(self, keyword: str, limit: int = 10) -> List[Dict]:
        """搜索抖音"""
        try:
            cmd = [
                "python3", str(self.cli_path),
                "douyin", keyword,
                "--limit", str(limit)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.base_path)
            if result.returncode == 0:
                return self._parse_results(result.stdout)
            return []
        except Exception as e:
            print(f"搜索异常: {e}")
            return []
    
    def search_bilibili(self, keyword: str, limit: int = 10) -> List[Dict]:
        """搜索B站"""
        try:
            cmd = [
                "python3", str(self.cli_path),
                "bilibili", keyword,
                "--limit", str(limit)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.base_path)
            if result.returncode == 0:
                return self._parse_results(result.stdout)
            return []
        except Exception as e:
            print(f"搜索异常: {e}")
            return []
    
    def search_trends(self, keyword: str, platforms: List[str] = None) -> Dict:
        """多平台趋势搜索"""
        if platforms is None:
            platforms = ["xiaohongshu", "douyin", "bilibili", "weibo"]
        
        results = {}
        for platform in platforms:
            try:
                method = getattr(self, f"search_{platform}", None)
                if method:
                    results[platform] = method(keyword, limit=5)
            except Exception as e:
                results[platform] = {"error": str(e)}
        
        return results
    
    def find_viral_content(self, account_type: str, days: int = 7) -> List[Dict]:
        """查找爆款内容"""
        # 根据账号类型确定搜索关键词
        keywords_map = {
            "tech-geek": ["数码评测", "手机推荐", "科技好物"],
            "life-aesthetics": ["家居布置", "生活美学", "氛围感"],
            "career-growth": ["职场干货", "面试技巧", "升职加薪"],
            "foodie": ["美食探店", "隐藏小店", "网红餐厅"],
            "fashion": ["穿搭分享", "平价好物", "OOTD"]
        }
        
        keywords = keywords_map.get(account_type, ["热门"])
        all_results = []
        
        for keyword in keywords:
            # 搜索小红书
            results = self.search_xiaohongshu(keyword, limit=5)
            for r in results:
                r["keyword"] = keyword
                r["source"] = "xiaohongshu"
            all_results.extend(results)
            
            # 搜索抖音
            results = self.search_douyin(keyword, limit=3)
            for r in results:
                r["keyword"] = keyword
                r["source"] = "douyin"
            all_results.extend(results)
        
        # 按互动量排序（假设有互动数据）
        return sorted(all_results, key=lambda x: x.get("likes", 0), reverse=True)[:10]
    
    def _parse_results(self, output: str) -> List[Dict]:
        """解析搜索结果"""
        results = []
        try:
            # 尝试解析JSON
            lines = output.strip().split('\n')
            for line in lines:
                if line.strip() and line.startswith('{'):
                    try:
                        data = json.loads(line)
                        results.append(data)
                    except:
                        pass
        except Exception as e:
            print(f"解析结果失败: {e}")
        return results

class AssistantToolsManager:
    """辅助工具管理器"""
    
    def __init__(self):
        self.aitu = AITUTool()
        self.union_search = UnionSearchTool()
        
    def get_status(self) -> Dict:
        """获取工具状态"""
        return {
            "aitu": {
                "available": self.aitu.is_available(),
                "path": str(self.aitu.base_path),
                "features": ["AI生图", "AI生视频", "思维导图", "流程图"]
            },
            "union_search": {
                "available": self.union_search.is_available(),
                "path": str(self.union_search.base_path),
                "features": ["小红书搜索", "抖音搜索", "B站搜索", "多平台趋势"]
            }
        }
    
    def research_topic(self, topic: str, account_type: str = None) -> Dict:
        """研究话题"""
        print(f"🔍 研究话题: {topic}")
        
        # 多平台搜索
        trends = self.union_search.search_trends(topic)
        
        # 查找相关爆款
        viral = []
        if account_type:
            viral = self.union_search.find_viral_content(account_type)
        
        return {
            "topic": topic,
            "trends": trends,
            "viral_content": viral,
            "suggestions": self._generate_suggestions(topic, trends, viral)
        }
    
    def _generate_suggestions(self, topic: str, trends: Dict, viral: List) -> List[str]:
        """生成内容建议"""
        suggestions = []
        
        # 分析趋势
        total_results = sum(len(v) for v in trends.values() if isinstance(v, list))
        if total_results > 0:
            suggestions.append(f"话题'{topic}'在多平台共有{total_results}条相关内容")
        
        # 分析爆款
        if viral:
            suggestions.append(f"找到{len(viral)}条相关爆款内容可供参考")
            suggestions.append("建议：分析爆款标题结构和内容角度")
        
        suggestions.extend([
            "建议：结合当前热点创作内容",
            "建议：参考爆款但保持原创性",
            "建议：添加个人独特视角"
        ])
        
        return suggestions
    
    def generate_creative_assets(self, content_type: str, params: Dict) -> Dict:
        """生成创意素材"""
        if content_type == "image":
            return self.aitu.generate_image(
                prompt=params.get("prompt", ""),
                model=params.get("model", "gemini-2.5-flash-image")
            )
        elif content_type == "video":
            return self.aitu.generate_video(
                prompt=params.get("prompt", ""),
                model=params.get("model", "veo3")
            )
        elif content_type == "mindmap":
            return self.aitu.create_mindmap(params.get("content", ""))
        else:
            return {"error": f"不支持的内容类型: {content_type}"}

if __name__ == "__main__":
    manager = AssistantToolsManager()
    
    # 显示状态
    print("🦞 辅助运营工具状态\n")
    status = manager.get_status()
    
    for tool, info in status.items():
        icon = "✅" if info["available"] else "❌"
        print(f"{icon} {tool}")
        print(f"   路径: {info['path']}")
        print(f"   功能: {', '.join(info['features'])}")
        print()
    
    # 测试搜索
    if status["union_search"]["available"]:
        print("\n🔍 测试搜索: 数码评测")
        results = manager.union_search.search_xiaohongshu("数码评测", limit=3)
        print(f"找到 {len(results)} 条结果")
        for r in results[:3]:
            print(f"  - {r.get('title', 'N/A')[:40]}...")
