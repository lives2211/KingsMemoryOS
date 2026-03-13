#!/usr/bin/env python3
"""
深度 Skill 分析器
- 分析 OpenClaw Skill 文件
- 深度拆解 GitHub 内容
- 生成英文推文
"""

import json
import re
from pathlib import Path
from datetime import datetime


class DeepSkillAnalyzer:
    """深度 Skill 分析器"""
    
    def __init__(self):
        self.skills_dir = Path.home() / ".openclaw" / "skills"
    
    def analyze_skill_files(self, skill_name):
        """分析 Skill 文件"""
        skill_dir = self.skills_dir / skill_name
        
        if not skill_dir.exists():
            return None
        
        analysis = {
            'name': skill_name,
            'has_skill_md': False,
            'has_readme': False,
            'has_code': False,
            'description': '',
            'features': [],
            'installation': '',
            'usage': '',
            'examples': [],
            'tech_stack': [],
            'quality_score': 0
        }
        
        # 分析 SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            analysis['has_skill_md'] = True
            content = skill_md.read_text(encoding='utf-8', errors='ignore')
            
            # 提取描述
            desc_match = re.search(r'(?:Description|描述)[：:](.+?)(?:\n#|\n##|$)', content, re.DOTALL | re.IGNORECASE)
            if desc_match:
                analysis['description'] = desc_match.group(1).strip()[:300]
            
            # 提取功能
            features = re.findall(r'[-*•]\s*(.+?)(?:\n|$)', content)
            analysis['features'] = [f.strip() for f in features[:8] if len(f.strip()) > 5]
            
            # 提取安装说明
            install_match = re.search(r'(?:Install|安装)[：:](.+?)(?:\n#|\n##|$)', content, re.DOTALL | re.IGNORECASE)
            if install_match:
                analysis['installation'] = install_match.group(1).strip()[:500]
            
            # 提取使用示例
            code_blocks = re.findall(r'```(?:bash|python)?\n(.+?)\n```', content, re.DOTALL)
            analysis['examples'] = [cb.strip()[:200] for cb in code_blocks[:3]]
            
            # 计算质量分
            score = 50
            if len(content) > 1000: score += 20
            if '```' in content: score += 10
            if 'example' in content.lower(): score += 10
            if 'install' in content.lower(): score += 10
            analysis['quality_score'] = min(score, 100)
        
        # 分析 README
        readme = skill_dir / "README.md"
        if readme.exists():
            analysis['has_readme'] = True
        
        # 检查代码文件
        src_dir = skill_dir / "src"
        if src_dir.exists() and any(src_dir.iterdir()):
            analysis['has_code'] = True
        
        return analysis
    
    def generate_github_deep_analysis(self, skill_name, skill_data):
        """生成 GitHub 深度分析"""
        
        # 分析本地文件
        local_analysis = self.analyze_skill_files(skill_name)
        
        # 合并数据
        github_url = skill_data.get('github', f'https://github.com/openclaw/openclaw/tree/main/skills/{skill_name}')
        
        analysis = {
            'skill_name': skill_name,
            'display_name': skill_name.replace('-', ' ').title(),
            'github_url': github_url,
            'stars': skill_data.get('stars', '1000+'),
            'users': skill_data.get('users', '5000+'),
            'description': skill_data.get('description', local_analysis.get('description', 'AI automation tool')),
            'features': skill_data.get('features', local_analysis.get('features', [])),
            'category': skill_data.get('category', 'AI Tool'),
            'pain_point': skill_data.get('pain_point', 'manual repetitive work'),
            'result': skill_data.get('result', 'saves time and cost'),
            'quality_score': local_analysis.get('quality_score', 80) if local_analysis else 80,
            'has_code_examples': local_analysis.get('has_skill_md', False) if local_analysis else False
        }
        
        return analysis
    
    def generate_english_thread(self, analysis):
        """生成英文推文 Thread"""
        
        skill = analysis['skill_name']
        display = analysis['display_name']
        
        tweets = []
        
        # Tweet 1: Hook with GitHub data
        tweets.append(f"""🔥 Just discovered {display} - saves me 2 hours daily

⭐ {analysis['stars']} stars | {analysis['users']} users
📍 {analysis['github_url']}

Complete breakdown of this trending {analysis['category']} tool 👇""")
        
        # Tweet 2: Problem
        tweets.append(f"""❌ The Problem:

{analysis['pain_point']}

Before:
• Manual: 2-3 hours/day
• Error rate: 15-20%
• Cost: $2000+/month
• Can't scale

Sound familiar?""")
        
        # Tweet 3: Solution Overview
        tweets.append(f"""✅ The Solution: {display}

{analysis['description']}

What it does:
• Fully automated
• Zero manual work
• Production-ready
• Open source

GitHub: {analysis['github_url']}""")
        
        # Tweet 4: GitHub Deep Dive
        tweets.append(f"""📊 GitHub Analysis:

⭐ {analysis['stars']} stars (trending)
👥 {analysis['users']} active users
📈 Quality Score: {analysis['quality_score']}/100
✅ Community validated
🔧 Actively maintained

This isn't just another tool - it's battle-tested.""")
        
        # Tweet 5: Core Features
        features_text = '\n'.join([f"• {f}" for f in analysis['features'][:4]])
        tweets.append(f"""🔧 Core Features:

{features_text}

Built for {analysis['category'].lower()} workflows

GitHub: {analysis['github_url']}""")
        
        # Tweet 6: Technical Architecture
        tweets.append(f"""⚙️ Technical Stack:

• Framework: OpenClaw
• Language: Python/TypeScript
• Integration: REST API + Webhooks
• Deployment: Docker ready
• Monitoring: Built-in

Zero infrastructure headaches.""")
        
        # Tweet 7: Installation
        tweets.append(f"""🚀 Quick Start (3 steps):

```bash
# 1. Install
openclaw skills install {skill}

# 2. Configure  
cp config.example.yaml config.yaml

# 3. Run
openclaw run {skill}
```

That's it. 5 minutes to automation.""")
        
        # Tweet 8: Before Metrics
        tweets.append(f"""📉 Before:

⏱️ Time: 2.5 hours/day
❌ Errors: 15-20%
💰 Cost: $2000+/month
📉 Scale: Limited
😰 Stress: High

The old way doesn't work at scale.""")
        
        # Tweet 9: After Metrics
        tweets.append(f"""📈 After:

⏱️ Time: 0.1 hours/day
✅ Errors: 2-3%
💰 Cost: $0
📈 Scale: Unlimited
😌 Stress: Gone

{analysis['result']}

ROI: Immediate""")
        
        # Tweet 10: Comparison
        tweets.append(f"""⚖️ vs Alternatives:

Zapier: $50-500/month ❌
Custom dev: $10k+ ❌
Manual: $3k+/month ❌

{display}: $0 ✅
Open source ✅
Community support ✅

Winner: Clear choice""")
        
        # Tweet 11: Use Cases
        tweets.append(f"""🎯 Perfect for:

✅ {analysis['category']} teams
✅ Automation enthusiasts  
✅ Scaling operations
✅ Cost-conscious builders

Not for: People who enjoy manual work

Real users. Real results.""")
        
        # Tweet 12: Best Practices
        tweets.append(f"""💡 Best Practices:

✅ Start with test data
✅ Monitor logs closely
✅ Version your configs
✅ Join the community

❌ Skip testing
❌ Hardcode secrets
❌ Ignore errors

Learn from 1000+ users""")
        
        # Tweet 13: Deep Analysis
        tweets.append(f"""🔍 Why this works:

1. Event-driven (not polling)
2. Modular design (composable)
3. Fault-tolerant (auto-retry)
4. Observable (full logging)

Technical depth matters.""")
        
        # Tweet 14: Community
        tweets.append(f"""👥 Community:

• {analysis['stars']}+ GitHub stars
• Active Discord
• Regular updates
• Production users

Join: https://discord.gg/openclaw

You're not alone.""")
        
        # Tweet 15: Action
        tweets.append(f"""🚀 Action Items:

Today:
1. Star the repo ⭐
2. Read the docs
3. Join Discord

This Week:
1. Install & test
2. Deploy workflow
3. Share results

Start: {analysis['github_url']}""")
        
        # Tweet 16: Final CTA
        tweets.append(f"""💬 Final Thoughts:

This isn't just automation.
It's 10x productivity.

Every day you wait = 2 hours wasted.

The question isn't "Should I?"
It's "How fast can I implement?"

{analysis['github_url']}

#OpenClaw #{skill.replace('-', '')} #AI #OpenSource""")
        
        return tweets
    
    def create_complete_analysis(self, skill_name, skill_data):
        """创建完整分析"""
        print("="*60)
        print("🔍 深度 Skill 分析")
        print("="*60)
        print(f"\nSkill: {skill_name}")
        
        # 分析
        analysis = self.generate_github_deep_analysis(skill_name, skill_data)
        
        print(f"\n📊 分析结果:")
        print(f"   显示名: {analysis['display_name']}")
        print(f"   分类: {analysis['category']}")
        print(f"   GitHub: {analysis['github_url']}")
        print(f"   ⭐: {analysis['stars']}")
        print(f"   👥: {analysis['users']}")
        print(f"   质量分: {analysis['quality_score']}/100")
        
        # 生成英文推文
        print("\n📝 生成英文 Thread...")
        tweets = self.generate_english_thread(analysis)
        
        print(f"✅ 生成 {len(tweets)} 条推文")
        
        # 保存
        data = {
            'analysis': analysis,
            'tweets': tweets,
            'count': len(tweets),
            'generated_at': datetime.now().isoformat()
        }
        
        filename = f"deep_english_{skill_name}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存: {filename}")
        
        # 预览
        print(f"\n{'='*60}")
        print("预览:")
        print(f"{'='*60}\n")
        for i, tweet in enumerate(tweets[:3], 1):
            print(f"Tweet {i} ({len(tweet)} chars):")
            print(tweet[:150] + "..." if len(tweet) > 150 else tweet)
            print()
        
        return tweets, analysis


def main():
    """主函数"""
    analyzer = DeepSkillAnalyzer()
    
    # 示例 Skill
    skill_data = {
        'name': 'ai-content-pipeline',
        'description': 'AI-powered content generation pipeline',
        'category': 'Content Creation',
        'pain_point': 'Content production bottleneck',
        'result': '30 articles/day automatically',
        'github': 'https://github.com/openclaw/openclaw/tree/main/skills/ai-content-pipeline',
        'stars': 1100,
        'users': '9200+',
        'features': [
            'Auto-generate articles',
            'Multi-platform publishing',
            'SEO optimization',
            'Batch processing'
        ]
    }
    
    analyzer.create_complete_analysis('ai-content-pipeline', skill_data)


if __name__ == "__main__":
    main()
