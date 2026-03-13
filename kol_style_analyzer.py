#!/usr/bin/env python3
"""
中文区 KOL 推文风格分析器
分析优秀 KOL 的发文特点，生成高质量推文
"""

import json
from datetime import datetime


class KOLStyleAnalyzer:
    """KOL 风格分析器"""
    
    def __init__(self):
        # 分析优秀中文 KOL 的推文特点
        self.kol_examples = {
            'AlchainHust': {
                'style': '知识型干货',
                'characteristics': [
                    '开门见山，直接给价值',
                    '结构化内容，用数字分点',
                    '配高质量配图或截图',
                    '有明确的行动号召',
                    '个人经验背书'
                ],
                'example': {
                    'hook': '花98小时整理的OpenClaw橙皮书，完整学习路径',
                    'structure': '问题→方案→步骤→结果',
                    'cta': '回复"橙皮书"获取完整版',
                    'engagement': '2482 likes, 614 retweets'
                }
            },
            'wangray': {
                'style': '实战经验型',
                'characteristics': [
                    '真实案例开场',
                    '详细数据支撑',
                    '可复制的方法论',
                    '避坑指南',
                    '长期价值导向'
                ],
                'example': {
                    'hook': '30天真实运行，5个Agent团队的经验总结',
                    'structure': '背景→实践→数据→教训→建议',
                    'cta': '完整SOP已整理，需要自取',
                    'engagement': '543 likes, 154 retweets'
                }
            },
            'Jimmy_JingLv': {
                'style': '工具推荐型',
                'characteristics': [
                    '痛点场景引入',
                    '工具核心功能介绍',
                    '与其他工具对比',
                    '使用场景举例',
                    'GitHub链接'
                ],
                'example': {
                    'hook': 'InsForge = AI-native Supabase，专为Agent设计',
                    'structure': '痛点→工具→功能→对比→链接',
                    'cta': 'GitHub: github.com/xxx',
                    'engagement': '86 likes, 11 retweets'
                }
            },
            'servasyy_ai': {
                'style': '资源分享型',
                'characteristics': [
                    '直接给出资源',
                    '列出核心功能',
                    '使用体验分享',
                    '适用人群说明',
                    'GitHub stars数据'
                ],
                'example': {
                    'hook': 'MediaCrawler 45K+ stars，支持小红书抖音B站',
                    'structure': '工具→功能→体验→适用→链接',
                    'cta': 'GitHub: github.com/xxx',
                    'engagement': '143 likes, 29 retweets'
                }
            }
        }
    
    def analyze_style(self, kol_name):
        """分析特定 KOL 风格"""
        if kol_name not in self.kol_examples:
            return None
        
        return self.kol_examples[kol_name]
    
    def generate_kol_style_tweet(self, skill_name, skill_data, style='AlchainHust'):
        """生成 KOL 风格推文"""
        
        # 获取风格模板
        style_template = self.kol_examples.get(style, self.kol_examples['AlchainHust'])
        
        # 构建推文
        tweet_parts = []
        
        # 1. Hook (钩子) - 开门见山
        hook = self._generate_hook(skill_name, skill_data)
        tweet_parts.append(hook)
        
        # 2. Problem (问题) - 痛点场景
        problem = self._generate_problem(skill_data)
        tweet_parts.append(problem)
        
        # 3. Solution (方案) - Skill介绍
        solution = self._generate_solution(skill_name, skill_data)
        tweet_parts.append(solution)
        
        # 4. Features (功能) - 核心功能
        features = self._generate_features(skill_data)
        tweet_parts.append(features)
        
        # 5. Usage (使用) - 使用方法
        usage = self._generate_usage(skill_name)
        tweet_parts.append(usage)
        
        # 6. Results (结果) - 效果数据
        results = self._generate_results(skill_data)
        tweet_parts.append(results)
        
        # 7. CTA (行动号召) - GitHub链接
        cta = self._generate_cta(skill_name, skill_data)
        tweet_parts.append(cta)
        
        # 8. Tags (标签)
        tags = self._generate_tags(skill_name)
        tweet_parts.append(tags)
        
        return '\n\n'.join(tweet_parts)
    
    def _generate_hook(self, skill_name, skill_data):
        """生成钩子"""
        hooks = [
            f"🔥 刚发现这个 {skill_name}，用了一周直接省出 2 小时/天",
            f"💡 很多人问我 {skill_data.get('category', 'AI')}  workflow，今天分享我的配置",
            f"⚡ 这个 {skill_name} 在中文区火了，实测确实好用",
            f"🎯 解决 {skill_data.get('pain_point', '重复工作')} 的神器，不用写代码"
        ]
        return hooks[0]
    
    def _generate_problem(self, skill_data):
        """生成问题描述"""
        pain = skill_data.get('pain_point', '重复性工作')
        return f"""❌ 问题：
{pain}

以前我的做法：
• 手动处理，每天 2-3 小时
• 容易出错，经常返工
• 无法扩展，人停工作停"""
    
    def _generate_solution(self, skill_name, skill_data):
        """生成方案"""
        github = skill_data.get('github', f'https://github.com/openclaw/{skill_name}')
        return f"""✅ 解决方案：{skill_name}

GitHub: {github}
⭐ {skill_data.get('stars', '1000+')} stars
👥 {skill_data.get('users', '5000+')} 用户

核心能力：
{skill_data.get('description', '自动化处理')}"""
    
    def _generate_features(self, skill_data):
        """生成功能列表"""
        features = skill_data.get('features', [
            '全自动处理，零人工干预',
            '与 OpenClaw 原生集成',
            '支持自定义配置',
            '生产环境验证'
        ])
        
        feature_text = '\n'.join([f"• {f}" for f in features])
        return f"""🔧 核心功能：

{feature_text}"""
    
    def _generate_usage(self, skill_name):
        """生成使用方法"""
        return f"""🚀 使用方法：

```bash
# 1. 安装
openclaw skills install {skill_name}

# 2. 配置
cp config.example.yaml config.yaml
# 编辑 config.yaml

# 3. 运行
openclaw run {skill_name}
```

3 步搞定，5 分钟上手。"""
    
    def _generate_results(self, skill_data):
        """生成结果数据"""
        result = skill_data.get('result', '节省大量时间')
        return f"""📊 实测结果：

Before:
• 手动处理：2.5 小时/天
• 错误率：15-20%
• 成本：$2000/月

After:
• 自动化：0.1 小时/天
• 错误率：2-3%
• 成本：$0

{result}"""
    
    def _generate_cta(self, skill_name, skill_data):
        """生成行动号召"""
        github = skill_data.get('github', f'https://github.com/openclaw/{skill_name}')
        return f"""📚 资源：

GitHub: {github}
文档: https://docs.openclaw.ai/skills/{skill_name}

💬 用过类似工具的朋友欢迎交流
⭐ 觉得有用请 star 支持"""
    
    def _generate_tags(self, skill_name):
        """生成标签"""
        return f"#OpenClaw #{skill_name.replace('-', '')} #AI #Automation #开源 #效率工具"
    
    def generate_complete_thread(self, skill_name, skill_data):
        """生成完整 Thread"""
        
        print("="*60)
        print("📝 KOL 风格推文生成")
        print("="*60)
        print(f"\nSkill: {skill_name}")
        print(f"风格: AlchainHust (知识型干货)")
        print(f"\n推文预览:\n")
        
        tweet = self.generate_kol_style_tweet(skill_name, skill_data)
        print(tweet)
        
        # 统计
        char_count = len(tweet)
        word_count = len(tweet.split())
        
        print(f"\n{'='*60}")
        print(f"📊 统计:")
        print(f"   字符数: {char_count}")
        print(f"   单词数: {word_count}")
        print(f"   预估阅读时间: {word_count//200} 分钟")
        print(f"{'='*60}")
        
        return tweet


def main():
    """主函数"""
    analyzer = KOLStyleAnalyzer()
    
    # 示例 Skill 数据
    skill_data = {
        'name': 'ai-content-pipeline',
        'description': 'AI内容流水线，自动生成文章',
        'category': '内容创作',
        'pain_point': '内容生产瓶颈，无法规模化',
        'result': '日产30篇高质量文章',
        'github': 'https://github.com/openclaw/openclaw/tree/main/skills/ai-content-pipeline',
        'stars': 1100,
        'users': '9200+',
        'features': [
            '全自动内容生成',
            '支持多平台发布',
            'SEO优化内置',
            '批量处理能力'
        ]
    }
    
    analyzer.generate_complete_thread('ai-content-pipeline', skill_data)


if __name__ == "__main__":
    main()
