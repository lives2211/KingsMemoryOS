#!/usr/bin/env python3
"""
OpenClaw Content Farm - 自动化推文生成系统
自动生成基于 OpenClaw Skills 的英文长推文
"""

import os
import re
import json
import random
import requests
from datetime import datetime
from pathlib import Path

class OpenClawContentFarm:
    """OpenClaw 内容农场主类"""
    
    def __init__(self, config_path="config.yaml"):
        self.config = self._load_config(config_path)
        self.skills_data = {}
        self.generated_tweets = []
        
    def _load_config(self, config_path):
        """加载配置文件"""
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def fetch_skill_content(self, skill_name):
        """从 GitHub 获取 skill 内容"""
        url = f"https://raw.githubusercontent.com/openclaw/openclaw/main/skills/{skill_name}/SKILL.md"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.text
            return None
        except Exception as e:
            print(f"Error fetching {skill_name}: {e}")
            return None
    
    def analyze_skill(self, skill_content):
        """分析 skill 内容，提取关键信息"""
        if not skill_content:
            return None
        
        # 提取 YAML frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---', skill_content, re.DOTALL)
        frontmatter = {}
        if frontmatter_match:
            try:
                import yaml
                frontmatter = yaml.safe_load(frontmatter_match.group(1))
            except:
                pass
        
        # 提取主要内容
        main_content = re.sub(r'^---\n.*?\n---', '', skill_content, flags=re.DOTALL).strip()
        
        # 提取代码示例
        code_examples = re.findall(r'```(?:bash|shell)?\n(.*?)\n```', main_content, re.DOTALL)
        
        # 提取关键特性
        features = []
        for line in main_content.split('\n'):
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                features.append(line.strip()[2:])
        
        return {
            'name': frontmatter.get('name', 'Unknown'),
            'description': frontmatter.get('description', ''),
            'emoji': frontmatter.get('metadata', {}).get('openclaw', {}).get('emoji', '📦'),
            'content': main_content[:3000],  # 限制长度
            'code_examples': code_examples[:3],  # 前3个代码示例
            'features': features[:5],  # 前5个特性
            'github_url': f"https://github.com/openclaw/openclaw/tree/main/skills/{frontmatter.get('name', 'unknown')}"
        }
    
    def generate_tweet(self, skill_data, theme="skill_deep_dive"):
        """生成推文内容"""
        
        templates = {
            "skill_deep_dive": self._generate_deep_dive_tweet,
            "workflow_tutorial": self._generate_workflow_tweet,
            "use_case_study": self._generate_use_case_tweet,
            "tips_and_tricks": self._generate_tips_tweet,
        }
        
        generator = templates.get(theme, self._generate_deep_dive_tweet)
        return generator(skill_data)
    
    def _generate_deep_dive_tweet(self, skill_data):
        """生成深度分析推文"""
        name = skill_data['name']
        emoji = skill_data['emoji']
        description = skill_data['description']
        github_url = skill_data['github_url']
        
        # 提取关键特性
        features_text = "\n".join([f"• {f}" for f in skill_data['features'][:5]])
        
        # 提取代码示例
        code_example = ""
        if skill_data['code_examples']:
            code = skill_data['code_examples'][0][:500]
            code_example = f"\n```bash\n{code}\n```\n"
        
        tweet = f"""{emoji} OpenClaw {name.title()} Skill Deep Dive

After 24 hours working with the {name} skill, here's what makes it essential for your workflow.

## What It Does

{description}

## Key Features

{features_text}
{code_example}
## Why It Matters

This skill transforms how you work by automating the tedious parts and letting you focus on what matters.

## Get Started

GitHub: {github_url}
Documentation: https://docs.openclaw.ai

What's your favorite OpenClaw skill? Let me know below! 👇

#OpenClaw #AIAgents #{name.replace('-', '')}"""
        
        return tweet
    
    def _generate_workflow_tweet(self, skill_data):
        """生成工作流教程推文"""
        name = skill_data['name']
        emoji = skill_data['emoji']
        github_url = skill_data['github_url']
        
        tweet = f"""{emoji} OpenClaw Workflow: Mastering {name.title()}

Here's the complete workflow I use daily:

## Step 1: Setup
```bash
# Install the skill
openclaw skill install {name}
```

## Step 2: Basic Usage
{skill_data['features'][0] if skill_data['features'] else 'Configure the skill'}

## Step 3: Advanced Patterns
{skill_data['features'][1] if len(skill_data['features']) > 1 else 'Automate with scripts'}

## Real-World Example

{skill_data['features'][2] if len(skill_data['features']) > 2 else 'Integrate with other skills'}

## Results

✅ Save 2 hours/day
✅ Reduce errors by 80%
✅ Focus on high-value work

GitHub: {github_url}

#OpenClaw #Productivity #{name.replace('-', '')}"""
        
        return tweet
    
    def _generate_use_case_tweet(self, skill_data):
        """生成使用案例推文"""
        name = skill_data['name']
        emoji = skill_data['emoji']
        github_url = skill_data['github_url']
        
        tweet = f"""{emoji} How I Use OpenClaw {name.title()} (Real Case Study)

**The Problem:**
Managing {name} tasks was taking 3+ hours daily

**The Solution:**
OpenClaw {name} skill automation

**The Workflow:**
1. Morning: Check status
2. Afternoon: Batch process
3. Evening: Review & archive

**The Results:**
📊 Time saved: 2.5 hours/day
📊 Error rate: Down 75%
📊 Team satisfaction: Up 90%

**The Setup:**
{skill_data['features'][0] if skill_data['features'] else 'Simple configuration'}

**The Impact:**
This one skill changed how our entire team works.

GitHub: {github_url}

#OpenClaw #CaseStudy #{name.replace('-', '')}"""
        
        return tweet
    
    def _generate_tips_tweet(self, skill_data):
        """生成技巧分享推文"""
        name = skill_data['name']
        emoji = skill_data['emoji']
        github_url = skill_data['github_url']
        
        tips = skill_data['features'][:5] if skill_data['features'] else [
            "Use environment variables for secrets",
            "Set up aliases for common commands",
            "Combine with other skills for power workflows",
            "Use background mode for long tasks",
            "Monitor costs with session-logs"
        ]
        
        tips_text = "\n".join([f"{i+1}. {tip}" for i, tip in enumerate(tips)])
        
        tweet = f"""{emoji} 5 Pro Tips for OpenClaw {name.title()}

After 100+ hours using this skill:

{tips_text}

**Bonus Tip:**
Combine {name} with other skills for 10x productivity:
- coding-agent: Automate code generation
- github: Auto-create PRs
- notion: Log results automatically

**The Result:**
Work that used to take hours now takes minutes.

GitHub: {github_url}

What's your favorite OpenClaw tip? Share below! 👇

#OpenClaw #Tips #{name.replace('-', '')}"""
        
        return tweet
    
    def generate_daily_tweets(self, count=5):
        """生成一天的推文"""
        priority_skills = self.config['github']['priority_skills']
        themes = self.config['content_generation']['themes']
        
        tweets = []
        selected_skills = random.sample(priority_skills, min(count, len(priority_skills)))
        
        for i, skill_name in enumerate(selected_skills):
            print(f"Processing skill: {skill_name}")
            
            # 获取 skill 内容
            skill_content = self.fetch_skill_content(skill_name)
            if not skill_content:
                continue
            
            # 分析 skill
            skill_data = self.analyze_skill(skill_content)
            if not skill_data:
                continue
            
            # 选择主题
            theme = themes[i % len(themes)]
            
            # 生成推文
            tweet = self.generate_tweet(skill_data, theme)
            
            tweets.append({
                'skill': skill_name,
                'theme': theme,
                'content': tweet,
                'github_url': skill_data['github_url'],
                'generated_at': datetime.now().isoformat()
            })
        
        return tweets
    
    def save_tweets(self, tweets, date_str=None):
        """保存生成的推文"""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        output_dir = Path(self.config['output']['save_path'])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"tweets_{date_str}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tweets, f, ensure_ascii=False, indent=2)
        
        print(f"Saved {len(tweets)} tweets to {output_file}")
        return output_file
    
    def run(self):
        """运行内容农场"""
        print("🚀 OpenClaw Content Farm Starting...")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"🎯 Target: {self.config['content_generation']['tweets_per_day']} tweets")
        
        # 生成推文
        tweets = self.generate_daily_tweets(
            self.config['content_generation']['tweets_per_day']
        )
        
        # 保存推文
        output_file = self.save_tweets(tweets)
        
        print(f"✅ Generated {len(tweets)} tweets")
        print(f"📁 Saved to: {output_file}")
        
        return tweets


if __name__ == "__main__":
    farm = OpenClawContentFarm()
    tweets = farm.run()
    
    # 打印第一篇推文预览
    if tweets:
        print("\n" + "="*80)
        print("📄 First Tweet Preview:")
        print("="*80)
        print(tweets[0]['content'][:500] + "...")
