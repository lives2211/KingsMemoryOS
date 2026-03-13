#!/usr/bin/env python3
"""
共享技能管理器
所有 Agent 共享同一个技能仓库
"""

import json
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional


class SharedSkillManager:
    """
    共享技能管理器
    
    设计原则：
    1. 技能只安装一次，所有 Agent 共享
    2. 技能配置按 Agent 隔离
    3. 技能使用记录统一追踪
    """
    
    def __init__(self, skills_dir: str = "~/.openclaw/skills"):
        self.skills_dir = Path(skills_dir).expanduser()
        self.loaded_skills: Dict[str, any] = {}
        self.skill_usage: Dict[str, Dict] = {}
        
    def list_skills(self) -> List[Dict]:
        """列出所有可用技能"""
        skills = []
        
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_name = skill_dir.name
                skill_info = {
                    "name": skill_name,
                    "path": str(skill_dir),
                    "loaded": skill_name in self.loaded_skills
                }
                
                # 尝试读取 SKILL.md
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    with open(skill_md, 'r') as f:
                        content = f.read()
                        # 提取描述（简单处理）
                        lines = content.split('\n')
                        for line in lines:
                            if line.startswith('# ') or line.startswith('## '):
                                continue
                            if line.strip():
                                skill_info["description"] = line[:100]
                                break
                
                skills.append(skill_info)
        
        return sorted(skills, key=lambda x: x["name"])
    
    def load_skill(self, skill_name: str) -> Optional[any]:
        """加载技能（如果未加载）"""
        if skill_name in self.loaded_skills:
            return self.loaded_skills[skill_name]
        
        skill_path = self.skills_dir / skill_name
        if not skill_path.exists():
            print(f"❌ 技能不存在: {skill_name}")
            return None
        
        # 这里可以实现技能加载逻辑
        # 例如：读取 SKILL.md，加载 Python 模块等
        
        self.loaded_skills[skill_name] = {
            "name": skill_name,
            "path": str(skill_path),
            "loaded_at": "now"
        }
        
        print(f"✅ 技能已加载: {skill_name}")
        return self.loaded_skills[skill_name]
    
    def use_skill(self, skill_name: str, agent_id: str, task_id: str, 
                  params: Optional[Dict] = None) -> Dict:
        """
        使用技能
        
        记录哪个 Agent 在什么任务中使用了什么技能
        """
        # 确保技能已加载
        skill = self.load_skill(skill_name)
        if not skill:
            return {"success": False, "error": "技能未找到"}
        
        # 记录使用
        usage_key = f"{agent_id}:{task_id}:{skill_name}"
        self.skill_usage[usage_key] = {
            "agent_id": agent_id,
            "task_id": task_id,
            "skill_name": skill_name,
            "params": params,
            "used_at": "now"
        }
        
        return {
            "success": True,
            "skill": skill_name,
            "agent": agent_id,
            "task": task_id,
            "message": f"{agent_id} 使用 {skill_name} 完成任务 {task_id}"
        }
    
    def get_agent_skills(self, agent_id: str) -> List[str]:
        """获取 Agent 使用过的技能"""
        used_skills = set()
        for usage in self.skill_usage.values():
            if usage["agent_id"] == agent_id:
                used_skills.add(usage["skill_name"])
        return list(used_skills)
    
    def get_skill_stats(self) -> Dict:
        """获取技能使用统计"""
        stats = {}
        
        for usage in self.skill_usage.values():
            skill_name = usage["skill_name"]
            if skill_name not in stats:
                stats[skill_name] = {
                    "total_usage": 0,
                    "agents": set(),
                    "tasks": set()
                }
            
            stats[skill_name]["total_usage"] += 1
            stats[skill_name]["agents"].add(usage["agent_id"])
            stats[skill_name]["tasks"].add(usage["task_id"])
        
        # 转换 set 为 list（为了 JSON 序列化）
        for skill in stats.values():
            skill["agents"] = list(skill["agents"])
            skill["tasks"] = list(skill["tasks"])
        
        return stats
    
    def recommend_skills(self, agent_id: str, task_description: str) -> List[str]:
        """
        根据任务描述推荐技能
        
        简单实现：关键词匹配
        """
        keywords = {
            "图像": ["ai-image-generation", "ai-product-photography"],
            "视频": ["ai-video-generation", "ai-marketing-videos"],
            "音频": ["ai-podcast-creation", "ai-voice-cloning", "ai-music-generation"],
            "代码": ["dev-planner", "proactive-solvr"],
            "爬虫": ["agent-browser", "agent-reach"],
            "内容": ["ai-content-pipeline", "ai-social-media-content"],
            "SEO": ["audit", "audit-speed", "diagnose-seo"],
            "数据": ["data-visualization", "ai-rag-pipeline"]
        }
        
        recommended = []
        for keyword, skills in keywords.items():
            if keyword in task_description:
                recommended.extend(skills)
        
        return list(set(recommended))


# 全局共享实例
_shared_skill_manager = None

def get_skill_manager() -> SharedSkillManager:
    """获取全局共享技能管理器"""
    global _shared_skill_manager
    if _shared_skill_manager is None:
        _shared_skill_manager = SharedSkillManager()
    return _shared_skill_manager


# CLI 接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="共享技能管理器")
    parser.add_argument("--list", action="store_true", help="列出所有技能")
    parser.add_argument("--stats", action="store_true", help="技能使用统计")
    parser.add_argument("--recommend", nargs=2, metavar=("AGENT", "TASK"),
                       help="推荐技能")
    parser.add_argument("--use", nargs=4, metavar=("SKILL", "AGENT", "TASK", "PARAMS"),
                       help="使用技能")
    
    args = parser.parse_args()
    
    manager = get_skill_manager()
    
    if args.list:
        skills = manager.list_skills()
        print(f"\n📦 可用技能 ({len(skills)} 个):")
        print("-" * 60)
        for skill in skills:
            status = "✅" if skill["loaded"] else "⬜"
            desc = skill.get("description", "")[:50]
            print(f"{status} {skill['name']}")
            print(f"   {desc}...")
            print()
    
    elif args.stats:
        stats = manager.get_skill_stats()
        print("\n📊 技能使用统计:")
        print("-" * 60)
        for skill_name, stat in stats.items():
            print(f"{skill_name}:")
            print(f"  使用次数: {stat['total_usage']}")
            print(f"  使用 Agent: {', '.join(stat['agents'])}")
            print(f"  相关任务: {len(stat['tasks'])} 个")
            print()
    
    elif args.recommend:
        skills = manager.recommend_skills(args.recommend[0], args.recommend[1])
        print(f"\n💡 为 {args.recommend[0]} 推荐技能:")
        print(f"任务: {args.recommend[1]}")
        print("-" * 60)
        for skill in skills:
            print(f"  • {skill}")
    
    elif args.use:
        params = json.loads(args.use[3]) if args.use[3] else {}
        result = manager.use_skill(args.use[0], args.use[1], args.use[2], params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print("共享技能管理器")
        print("\n示例:")
        print("  python3 shared_skills.py --list")
        print("  python3 shared_skills.py --recommend yitai '编写爬虫'")
        print("  python3 shared_skills.py --stats")
