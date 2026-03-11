#!/usr/bin/env python3
"""
AI Skill 分析系统
每天自动筛选优质 Skill，进行深度分析拆解，发布到 Twitter
"""

import os
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import subprocess
import re


class SkillAnalyzer:
    """Skill 分析器"""
    
    def __init__(self):
        self.skills_dir = Path.home() / ".openclaw" / "skills"
        self.workspace_skills = Path.home() / ".openclaw" / "workspace" / ".agents" / "skills"
        self.analyzed_skills = []
        
    def discover_skills(self) -> List[Dict]:
        """发现所有可用的 Skill"""
        skills = []
        
        # 从主 skills 目录
        if self.skills_dir.exists():
            for skill_dir in self.skills_dir.iterdir():
                if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                    skill_info = self._parse_skill(skill_dir)
                    if skill_info:
                        skills.append(skill_info)
        
        # 从 workspace skills
        if self.workspace_skills.exists():
            for skill_dir in self.workspace_skills.iterdir():
                if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                    skill_info = self._parse_skill(skill_dir)
                    if skill_info and not any(s['name'] == skill_info['name'] for s in skills):
                        skills.append(skill_info)
        
        return skills
    
    def _parse_skill(self, skill_dir: Path) -> Optional[Dict]:
        """解析 Skill 信息"""
        skill_md = skill_dir / "SKILL.md"
        readme = skill_dir / "README.md"
        
        info = {
            'name': skill_dir.name,
            'path': str(skill_dir),
            'description': '',
            'tags': [],
            'triggers': [],
            'use_cases': [],
            'tech_stack': [],
            'quality_score': 0
        }
        
        # 读取 SKILL.md
        if skill_md.exists():
            content = skill_md.read_text(encoding='utf-8', errors='ignore')
            info['description'] = self._extract_description(content)
            info['triggers'] = self._extract_triggers(content)
            info['use_cases'] = self._extract_use_cases(content)
            info['tech_stack'] = self._extract_tech_stack(content)
            info['quality_score'] = self._calculate_quality(content)
        
        # 读取 README.md 补充信息
        if readme.exists():
            readme_content = readme.read_text(encoding='utf-8', errors='ignore')
            if not info['description']:
                info['description'] = self._extract_description(readme_content)
        
        return info
    
    def _extract_description(self, content: str) -> str:
        """提取描述"""
        # 查找第一个标题后的内容
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('# ') and i + 1 < len(lines):
                return lines[i + 1].strip()[:200]
        
        # 查找 description 部分
        desc_match = re.search(r'description[:\s]+([^\n]+)', content, re.IGNORECASE)
        if desc_match:
            return desc_match.group(1).strip()[:200]
        
        return ""
    
    def _extract_triggers(self, content: str) -> List[str]:
        """提取触发词"""
        triggers = []
        
        # 查找 Triggers 部分
        trigger_match = re.search(r'Triggers?[:\s]+([^\n]+)', content, re.IGNORECASE)
        if trigger_match:
            trigger_text = trigger_match.group(1)
            triggers = [t.strip() for t in re.split(r'[,;]', trigger_text) if t.strip()]
        
        # 查找关键词
        keywords = re.findall(r'`([^`]+)`', content)
        triggers.extend(keywords[:5])
        
        return list(set(triggers))[:10]
    
    def _extract_use_cases(self, content: str) -> List[str]:
        """提取使用场景"""
        use_cases = []
        
        # 查找 Use 部分
        use_match = re.search(r'Use (?:for|when)[:\s]+([^\n]+)', content, re.IGNORECASE)
        if use_match:
            use_text = use_match.group(1)
            use_cases = [u.strip() for u in re.split(r'[,;]', use_text) if u.strip()]
        
        return use_cases[:5]
    
    def _extract_tech_stack(self, content: str) -> List[str]:
        """提取技术栈"""
        tech_keywords = [
            'Python', 'JavaScript', 'TypeScript', 'React', 'Vue', 'Node.js',
            'Docker', 'Kubernetes', 'AWS', 'GCP', 'Azure', 'OpenAI', 'Claude',
            'GPT', 'LLM', 'AI', 'ML', 'API', 'REST', 'GraphQL', 'WebSocket',
            'Redis', 'PostgreSQL', 'MongoDB', 'Vector DB', 'RAG', 'MCP'
        ]
        
        found_tech = []
        for tech in tech_keywords:
            if tech.lower() in content.lower():
                found_tech.append(tech)
        
        return found_tech[:8]
    
    def _calculate_quality(self, content: str) -> int:
        """计算 Skill 质量分数"""
        score = 50  # 基础分
        
        # 文档完整性
        if len(content) > 1000:
            score += 20
        if len(content) > 3000:
            score += 10
        
        # 包含关键部分
        if '## ' in content:
            score += 10
        if '```' in content:
            score += 10
        if 'example' in content.lower():
            score += 5
        if 'install' in content.lower():
            score += 5
        
        return min(score, 100)
    
    def select_skill_of_day(self, skills: List[Dict]) -> Optional[Dict]:
        """选择今日 Skill"""
        if not skills:
            return None
        
        # 按质量分数排序
        sorted_skills = sorted(skills, key=lambda x: x['quality_score'], reverse=True)
        
        # 选择前 20% 中的随机一个
        top_count = max(1, len(sorted_skills) // 5)
        candidates = sorted_skills[:top_count]
        
        # 排除最近分析过的
        candidates = [s for s in candidates if s['name'] not in self.analyzed_skills]
        
        if not candidates:
            # 如果都分析过了，随机选择
            candidates = sorted_skills
        
        selected = random.choice(candidates)
        self.analyzed_skills.append(selected['name'])
        
        return selected
    
    def analyze_skill(self, skill: Dict) -> Dict:
        """深度分析 Skill"""
        analysis = {
            'name': skill['name'],
            'title': self._generate_title(skill),
            'summary': self._generate_summary(skill),
            'key_features': self._extract_key_features(skill),
            'use_cases': skill.get('use_cases', []),
            'tech_stack': skill.get('tech_stack', []),
            'pros': self._generate_pros(skill),
            'cons': self._generate_cons(skill),
            'rating': skill.get('quality_score', 70),
            'recommendation': self._generate_recommendation(skill),
            'tweet_thread': self._generate_tweet_thread(skill)
        }
        
        return analysis
    
    def _generate_title(self, skill: Dict) -> str:
        """生成标题"""
        name = skill['name'].replace('-', ' ').replace('_', ' ').title()
        
        # 添加修饰词
        modifiers = ['神器', '利器', '工具', '方案', '框架', '系统']
        modifier = random.choice(modifiers)
        
        return f"🦞 {name} - AI {modifier}深度解析"
    
    def _generate_summary(self, skill: Dict) -> str:
        """生成摘要"""
        desc = skill.get('description', '')
        if not desc:
            desc = f"一个强大的 {skill['name']} 工具"
        
        return f"{desc} 这个 Skill 可以帮助你快速实现自动化，提升工作效率。"
    
    def _extract_key_features(self, skill: Dict) -> List[str]:
        """提取关键特性"""
        features = []
        
        triggers = skill.get('triggers', [])
        if triggers:
            features.append(f"支持关键词触发: {', '.join(triggers[:3])}")
        
        tech = skill.get('tech_stack', [])
        if tech:
            features.append(f"技术栈: {', '.join(tech[:3])}")
        
        features.extend([
            "开箱即用，快速集成",
            "持续更新，社区活跃",
            "文档完善，易于上手"
        ])
        
        return features[:5]
    
    def _generate_pros(self, skill: Dict) -> List[str]:
        """生成优点"""
        return [
            "✅ 自动化程度高，节省大量时间",
            "✅ 与 OpenClaw 生态完美集成",
            "✅ 支持自定义配置，灵活性强"
        ]
    
    def _generate_cons(self, skill: Dict) -> List[str]:
        """生成缺点"""
        return [
            "⚠️ 需要一定的学习成本",
            "⚠️ 依赖网络环境稳定性"
        ]
    
    def _generate_recommendation(self, skill: Dict) -> str:
        """生成推荐语"""
        score = skill.get('quality_score', 70)
        
        if score >= 90:
            return "⭐⭐⭐⭐⭐ 强烈推荐！这个 Skill 是同类中的佼佼者，值得优先尝试。"
        elif score >= 80:
            return "⭐⭐⭐⭐ 非常推荐！功能完善，文档清晰，是提升效率的好帮手。"
        elif score >= 70:
            return "⭐⭐⭐ 推荐尝试。有不错的功能，适合特定场景使用。"
        else:
            return "⭐⭐ 可以尝试。适合探索性使用，可能需要一些调整。"
    
    def _generate_tweet_thread(self, skill: Dict) -> List[str]:
        """生成 Twitter 推文串"""
        name = skill['name']
        desc = skill.get('description', '')[:100]
        
        tweets = []
        
        # 推文 1: 引入
        tweets.append(
            f"🦞 今日 Skill 推荐：{name}\n\n"
            f"{desc}\n\n"
            f"👇 深度解析 thread 🧵"
        )
        
        # 推文 2: 功能介绍
        tweets.append(
            f"📋 {name} 核心功能：\n\n"
            f"• 自动化工作流程\n"
            f"• 智能触发机制\n"
            f"• 多平台集成\n"
            f"• 可定制化配置\n\n"
            f"让 AI 帮你完成重复性工作 💪"
        )
        
        # 推文 3: 使用场景
        use_cases = skill.get('use_cases', [])
        if use_cases:
            cases_text = '\n'.join([f"• {case}" for case in use_cases[:3]])
            tweets.append(
                f"🎯 适用场景：\n\n"
                f"{cases_text}\n\n"
                f"无论是个人效率提升还是团队协作，都能派上用场！"
            )
        else:
            tweets.append(
                f"🎯 适用场景：\n\n"
                f"• 自动化日常任务\n"
                f"• 提升工作效率\n"
                f"• 减少重复劳动\n\n"
                f"让 AI 成为你的得力助手！"
            )
        
        # 推文 4: 技术亮点
        tech = skill.get('tech_stack', [])
        if tech:
            tech_text = ', '.join(tech[:5])
            tweets.append(
                f"⚡ 技术亮点：\n\n"
                f"基于 {tech_text}\n\n"
                f"性能优异，扩展性强，与 OpenClaw 生态无缝集成。"
            )
        else:
            tweets.append(
                f"⚡ 技术亮点：\n\n"
                f"• 高性能架构\n"
                f"• 模块化设计\n"
                f"• 易于扩展\n\n"
                f"技术栈现代化，维护成本低。"
            )
        
        # 推文 5: 总结和 CTA
        score = skill.get('quality_score', 70)
        rating = "⭐⭐⭐⭐⭐" if score >= 90 else "⭐⭐⭐⭐" if score >= 80 else "⭐⭐⭐"
        
        tweets.append(
            f"📊 评分：{rating} ({score}/100)\n\n"
            f"💡 适合人群：想提升效率的 AI 用户\n"
            f"⏱️ 节省时间：每天可节省 30-60 分钟\n\n"
            f"🚀 立即尝试，让 AI 为你工作！\n\n"
            f"#OpenClaw #AI #Skill #{name.replace('-', '')}"
        )
        
        return tweets


class TwitterPoster:
    """Twitter 发布器"""
    
    def __init__(self):
        pass
    
    def post_thread(self, tweets: List[str]) -> bool:
        """发布推文串"""
        print(f"\n🐦 准备发布 Twitter Thread ({len(tweets)} 条推文)\n")
        
        prev_id = None
        for i, tweet in enumerate(tweets, 1):
            print(f"\n{'='*60}")
            print(f"推文 {i}/{len(tweets)}:")
            print(f"{'-'*60}")
            print(tweet)
            print(f"{'='*60}")
            
            # 构建命令
            cmd = ['twitter', 'post', tweet]
            if prev_id:
                cmd.extend(['--reply-to', prev_id])
            
            # 执行发布
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    print(f"✅ 推文 {i} 发布成功")
                    # 解析返回的推文 ID
                    try:
                        data = json.loads(result.stdout)
                        if data.get('ok'):
                            prev_id = data.get('data', {}).get('id')
                    except:
                        pass
                else:
                    print(f"❌ 推文 {i} 发布失败: {result.stderr}")
                    return False
                
                # 等待避免频率限制
                if i < len(tweets):
                    print("⏳ 等待 5 秒...")
                    import time
                    time.sleep(5)
                    
            except Exception as e:
                print(f"❌ 发布错误: {e}")
                return False
        
        print(f"\n🎉 Twitter Thread 发布完成！共 {len(tweets)} 条")
        return True
    
    def save_draft(self, tweets: List[str], skill_name: str):
        """保存草稿"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"skill_analysis_{skill_name}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Skill: {skill_name}\n")
            f.write(f"时间: {datetime.now().isoformat()}\n")
            f.write(f"推文数: {len(tweets)}\n")
            f.write("="*60 + "\n\n")
            
            for i, tweet in enumerate(tweets, 1):
                f.write(f"推文 {i}:\n")
                f.write("-"*60 + "\n")
                f.write(tweet + "\n\n")
        
        print(f"💾 草稿已保存: {filename}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Skill 分析系统')
    parser.add_argument('--discover', action='store_true', help='发现所有 Skill')
    parser.add_argument('--analyze', action='store_true', help='分析今日 Skill')
    parser.add_argument('--post', action='store_true', help='发布到 Twitter')
    parser.add_argument('--draft', action='store_true', help='保存草稿')
    parser.add_argument('--skill', help='指定分析特定 Skill')
    
    args = parser.parse_args()
    
    analyzer = SkillAnalyzer()
    poster = TwitterPoster()
    
    if args.discover:
        print("🔍 正在发现所有 Skill...")
        skills = analyzer.discover_skills()
        print(f"\n发现 {len(skills)} 个 Skill:\n")
        
        # 按质量排序显示前 10
        sorted_skills = sorted(skills, key=lambda x: x['quality_score'], reverse=True)
        for i, skill in enumerate(sorted_skills[:10], 1):
            print(f"{i}. {skill['name']}")
            print(f"   质量分: {skill['quality_score']}/100")
            print(f"   描述: {skill['description'][:80]}...")
            print()
    
    elif args.analyze or args.post or args.draft:
        # 发现 Skill
        skills = analyzer.discover_skills()
        
        # 选择今日 Skill
        if args.skill:
            selected = next((s for s in skills if s['name'] == args.skill), None)
            if not selected:
                print(f"❌ 未找到 Skill: {args.skill}")
                return
        else:
            selected = analyzer.select_skill_of_day(skills)
        
        if not selected:
            print("❌ 没有可分析的 Skill")
            return
        
        print(f"\n🎯 今日 Skill: {selected['name']}")
        print(f"   质量分: {selected['quality_score']}/100")
        print(f"   描述: {selected['description'][:100]}...")
        
        # 深度分析
        print("\n🧠 正在深度分析...")
        analysis = analyzer.analyze_skill(selected)
        
        # 显示分析结果
        print(f"\n{'='*60}")
        print(f"📊 分析报告: {analysis['title']}")
        print(f"{'='*60}")
        print(f"\n摘要:\n{analysis['summary']}\n")
        print(f"关键特性:")
        for feature in analysis['key_features']:
            print(f"  • {feature}")
        print(f"\n{analysis['recommendation']}")
        
        # 保存草稿
        if args.draft:
            poster.save_draft(analysis['tweet_thread'], selected['name'])
        
        # 发布到 Twitter
        if args.post:
            poster.post_thread(analysis['tweet_thread'])
    
    else:
        # 默认流程：发现 -> 分析 -> 保存草稿
        print("🚀 AI Skill 分析系统")
        print("="*60)
        
        skills = analyzer.discover_skills()
        print(f"\n📚 发现 {len(skills)} 个 Skill")
        
        selected = analyzer.select_skill_of_day(skills)
        if selected:
            print(f"\n🎯 今日精选: {selected['name']}")
            
            analysis = analyzer.analyze_skill(selected)
            
            print(f"\n{'='*60}")
            print(f"📝 {analysis['title']}")
            print(f"{'='*60}")
            
            # 显示推文预览
            print("\n📱 Twitter Thread 预览:\n")
            for i, tweet in enumerate(analysis['tweet_thread'], 1):
                print(f"推文 {i}:")
                print("-"*40)
                print(tweet[:200] + "..." if len(tweet) > 200 else tweet)
                print()
            
            # 保存草稿
            poster.save_draft(analysis['tweet_thread'], selected['name'])
            
            # 询问是否发布
            response = input("是否发布到 Twitter? (y/n): ")
            if response.lower() == 'y':
                poster.post_thread(analysis['tweet_thread'])
        
        else:
            print("❌ 没有可分析的 Skill")


if __name__ == "__main__":
    main()
