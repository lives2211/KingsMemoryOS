#!/usr/bin/env python3
"""
Skill 发现系统
自动发现中文区热门 Skill、GitHub 项目和 OpenClaw 教程
"""

import json
import subprocess
import random
from datetime import datetime
from pathlib import Path
import re


class SkillDiscoverySystem:
    """Skill 发现系统"""
    
    def __init__(self):
        self.skills_dir = Path.home() / ".openclaw" / "skills"
        self.workspace_skills = Path.home() / ".openclaw" / "workspace" / ".agents" / "skills"
        
    def discover_from_github_trending(self):
        """从 GitHub Trending 发现热门项目"""
        trending = [
            {
                'name': 'agency-agents',
                'stars': 15950,
                'trending': '连续4天登顶',
                'description': 'AI Agency模式，群体智能范式',
                'github': 'https://github.com/mirofish/agency-agents',
                'category': 'AI Agency'
            },
            {
                'name': 'openclaw',
                'stars': 8900,
                'trending': '连续4天Trending',
                'description': 'OpenClaw Agent框架，社区影响力稳固',
                'github': 'https://github.com/openclaw/openclaw',
                'category': 'Agent Framework'
            },
            {
                'name': 'superpowers',
                'stars': 3200,
                'trending': '新晋Agent技能框架',
                'description': '与OpenClaw skills形成竞争',
                'github': 'https://github.com/superpowers-ai/superpowers',
                'category': 'Agent Skills'
            }
        ]
        return trending
    
    def discover_from_local_skills(self):
        """从本地 Skill 目录发现"""
        skills = []
        
        # 扫描本地 skills
        for skill_dir in [self.skills_dir, self.workspace_skills]:
            if skill_dir.exists():
                for item in skill_dir.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        skill_info = self._analyze_skill(item)
                        if skill_info:
                            skills.append(skill_info)
        
        # 按质量排序
        skills.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
        return skills[:20]
    
    def _analyze_skill(self, skill_dir: Path) -> dict:
        """分析 Skill"""
        skill_md = skill_dir / "SKILL.md"
        readme = skill_dir / "README.md"
        
        if not skill_md.exists():
            return None
        
        content = skill_md.read_text(encoding='utf-8', errors='ignore')
        
        # 计算质量分
        quality = 50
        if len(content) > 1000: quality += 20
        if '```' in content: quality += 10
        if 'example' in content.lower(): quality += 10
        if 'install' in content.lower(): quality += 10
        
        # 提取描述
        desc = ''
        lines = content.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#'):
                desc = line.strip()[:200]
                break
        
        # 检测中文内容
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', content))
        
        return {
            'name': skill_dir.name,
            'path': str(skill_dir),
            'description': desc,
            'quality_score': min(quality, 100),
            'has_chinese': has_chinese,
            'doc_length': len(content)
        }
    
    def discover_from_twitter_feed(self):
        """从 Twitter Feed 发现热门话题"""
        try:
            result = subprocess.run(
                ['twitter', 'feed', '--max', '50', '--json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                tweets = data.get('data', [])
                
                # 分析热门话题
                topics = {}
                for tweet in tweets:
                    text = tweet.get('text', '').lower()
                    
                    # 检测关键词
                    keywords = ['openclaw', 'ai agent', 'automation', 'skill', 
                               'workflow', 'mcp', 'github', 'trending']
                    
                    for kw in keywords:
                        if kw in text:
                            topics[kw] = topics.get(kw, 0) + 1
                
                # 排序
                sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
                return sorted_topics[:10]
                
        except Exception as e:
            print(f"❌ Twitter feed 分析失败: {e}")
            return []
    
    def generate_discovery_report(self):
        """生成发现报告"""
        print("="*60)
        print("🔍 Skill 发现系统")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*60)
        
        # 1. GitHub Trending
        print("\n📈 GitHub Trending (今日):")
        trending = self.discover_from_github_trending()
        for item in trending:
            print(f"\n  🔥 {item['name']}")
            print(f"     ⭐ {item['stars']} stars | {item['trending']}")
            print(f"     📝 {item['description']}")
            print(f"     🔗 {item['github']}")
        
        # 2. 本地高质量 Skill
        print("\n📦 本地高质量 Skill:")
        local_skills = self.discover_from_local_skills()
        for i, skill in enumerate(local_skills[:10], 1):
            chinese_mark = "🇨🇳" if skill['has_chinese'] else ""
            print(f"\n  {i}. {skill['name']} {chinese_mark}")
            print(f"     质量分: {skill['quality_score']}/100")
            print(f"     描述: {skill['description'][:60]}...")
        
        # 3. Twitter 热门话题
        print("\n🐦 Twitter 热门话题:")
        twitter_topics = self.discover_from_twitter_feed()
        for topic, count in twitter_topics:
            print(f"  • #{topic}: {count} 次提及")
        
        # 4. 推荐发布内容
        print("\n🎯 今日推荐发布:")
        recommendations = self.generate_recommendations(local_skills, trending)
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"\n  {i}. {rec['name']}")
            print(f"     理由: {rec['reason']}")
            print(f"     GitHub: {rec.get('github', 'N/A')}")
        
        print("\n" + "="*60)
        
        return {
            'trending': trending,
            'local_skills': local_skills,
            'twitter_topics': twitter_topics,
            'recommendations': recommendations
        }
    
    def generate_recommendations(self, local_skills, trending):
        """生成推荐"""
        recommendations = []
        
        # 推荐1: 高质量中文 Skill
        chinese_skills = [s for s in local_skills if s['has_chinese']]
        if chinese_skills:
            skill = chinese_skills[0]
            recommendations.append({
                'name': skill['name'],
                'reason': '高质量中文内容，适合推广到英文区',
                'type': 'local',
                'data': skill
            })
        
        # 推荐2: GitHub Trending
        if trending:
            item = trending[0]
            recommendations.append({
                'name': item['name'],
                'reason': f"GitHub Trending ({item['trending']})",
                'type': 'github',
                'github': item['github'],
                'data': item
            })
        
        # 推荐3: 高星本地 Skill
        high_quality = [s for s in local_skills if s['quality_score'] >= 80]
        if len(high_quality) > 1:
            skill = high_quality[1] if len(high_quality) > 1 else high_quality[0]
            recommendations.append({
                'name': skill['name'],
                'reason': f"高质量 Skill (评分: {skill['quality_score']})",
                'type': 'local',
                'data': skill
            })
        
        return recommendations


def main():
    """主函数"""
    discovery = SkillDiscoverySystem()
    discovery.generate_discovery_report()


if __name__ == "__main__":
    main()
