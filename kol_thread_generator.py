#!/usr/bin/env python3
"""
KOL 风格 Thread 生成器
- 模仿中文区 KOL 风格
- 标准账户 (280字符)
- 完整 Skill 介绍
"""

import json
from datetime import datetime


class KOLThreadGenerator:
    """KOL Thread 生成器"""
    
    def __init__(self):
        self.max_length = 260  # 留余量
    
    def generate_kol_thread(self, skill_name, skill_data):
        """生成 KOL 风格 Thread"""
        
        tweets = []
        
        # Tweet 1: Hook (钩子)
        tweet1 = self._create_hook(skill_name, skill_data)
        tweets.append(tweet1)
        
        # Tweet 2: Problem (痛点)
        tweet2 = self._create_problem(skill_data)
        tweets.append(tweet2)
        
        # Tweet 3: Solution Intro (方案介绍)
        tweet3 = self._create_solution_intro(skill_name, skill_data)
        tweets.append(tweet3)
        
        # Tweet 4: GitHub Info (GitHub信息)
        tweet4 = self._create_github_info(skill_name, skill_data)
        tweets.append(tweet4)
        
        # Tweet 5: Features (核心功能)
        tweet5 = self._create_features(skill_data)
        tweets.append(tweet5)
        
        # Tweet 6: Usage (使用方法)
        tweet6 = self._create_usage(skill_name)
        tweets.append(tweet6)
        
        # Tweet 7: Results Before (Before数据)
        tweet7 = self._create_results_before()
        tweets.append(tweet7)
        
        # Tweet 8: Results After (After数据)
        tweet8 = self._create_results_after(skill_data)
        tweets.append(tweet8)
        
        # Tweet 9: Comparison (对比)
        tweet9 = self._create_comparison()
        tweets.append(tweet9)
        
        # Tweet 10: Use Cases (使用场景)
        tweet10 = self._create_use_cases(skill_data)
        tweets.append(tweet10)
        
        # Tweet 11: Best Practices (最佳实践)
        tweet11 = self._create_best_practices()
        tweets.append(tweet11)
        
        # Tweet 12: CTA (行动号召)
        tweet12 = self._create_cta(skill_name, skill_data)
        tweets.append(tweet12)
        
        return tweets
    
    def _create_hook(self, skill_name, skill_data):
        """创建钩子推文"""
        return f"""🔥 刚发现这个 {skill_name}，用了一周直接省出 2 小时/天

解决 {skill_data.get('pain_point', '重复工作')} 的神器

👇 完整使用经验 🧵"""
    
    def _create_problem(self, skill_data):
        """创建问题推文"""
        return f"""❌ 以前的问题：

{skill_data.get('pain_point', '重复性工作')}

• 手动处理 2-3 小时/天
• 容易出错，经常返工
• 无法扩展，人停工作停

效率瓶颈明显"""
    
    def _create_solution_intro(self, skill_name, skill_data):
        """创建方案介绍"""
        return f"""✅ 解决方案：{skill_name}

{skill_data.get('description', '自动化工具')}

核心能力：
• 全自动处理
• 零人工干预
• 生产环境验证
• 开箱即用"""
    
    def _create_github_info(self, skill_name, skill_data):
        """创建 GitHub 信息"""
        github = skill_data.get('github', f'https://github.com/openclaw/{skill_name}')
        return f"""📊 项目数据：

GitHub: {github}
⭐ {skill_data.get('stars', '1000+')} stars
👥 {skill_data.get('users', '5000+')} users

社区活跃，持续更新"""
    
    def _create_features(self, skill_data):
        """创建功能推文"""
        features = skill_data.get('features', [
            '全自动处理',
            'OpenClaw原生集成',
            '支持自定义',
            '生产级可靠'
        ])
        
        feature_text = '\n'.join([f"• {f}" for f in features[:4]])
        return f"""🔧 核心功能：

{feature_text}

与 OpenClaw 生态无缝集成"""
    
    def _create_usage(self, skill_name):
        """创建使用方法"""
        return f"""🚀 使用方法：

1️⃣ 安装
openclaw skills install {skill_name}

2️⃣ 配置
cp config.example.yaml config.yaml

3️⃣ 运行
openclaw run {skill_name}

3步搞定"""
    
    def _create_results_before(self):
        """创建 Before 数据"""
        return f"""📉 Before：

⏱️ 手动处理：2.5 小时/天
❌ 错误率：15-20%
💰 成本：$2000/月
📉 效率：无法扩展"""
    
    def _create_results_after(self, skill_data):
        """创建 After 数据"""
        return f"""📈 After：

⏱️ 自动化：0.1 小时/天
✅ 错误率：2-3%
💰 成本：$0
📈 效率：{skill_data.get('result', '无限扩展')}

ROI: 立即回本"""
    
    def _create_comparison(self):
        """创建对比推文"""
        return f"""⚖️ 对比：

vs Zapier:
✅ 免费 vs $50-500/月
✅ 开源 vs 封闭
✅ 可定制 vs 受限

vs 自建:
✅ 70分钟 vs 2-6月
✅ 社区维护 vs 自己维护"""
    
    def _create_use_cases(self, skill_data):
        """创建使用场景"""
        return f"""🎯 适用场景：

✅ {skill_data.get('category', '内容创作')}
✅ 批量数据处理
✅ 自动化工作流
✅ 团队协作

不适合：喜欢手动操作的人"""
    
    def _create_best_practices(self):
        """创建最佳实践"""
        return f"""💡 最佳实践：

✅ 先测试再部署
✅ 从简单开始
✅ 监控日志
✅ 备份配置

❌ 不要跳过测试
❌ 不要硬编码密钥"""
    
    def _create_cta(self, skill_name, skill_data):
        """创建行动号召"""
        github = skill_data.get('github', f'https://github.com/openclaw/{skill_name}')
        return f"""📚 资源：

GitHub: {github}

💬 用过类似工具？
欢迎交流经验

⭐ 有用请 star 支持

#OpenClaw #{skill_name.replace('-', '')} #AI #开源"""
    
    def validate_and_generate(self, skill_name, skill_data):
        """验证并生成"""
        tweets = self.generate_kol_thread(skill_name, skill_data)
        
        print("="*60)
        print("📝 KOL 风格 Thread 生成")
        print("="*60)
        print(f"\nSkill: {skill_name}")
        print(f"推文数: {len(tweets)}")
        print(f"\n推文预览:\n")
        
        for i, tweet in enumerate(tweets, 1):
            print(f"推文 {i} ({len(tweet)} 字符):")
            print(tweet)
            print()
            
            # 验证长度
            if len(tweet) > 280:
                print(f"⚠️ 警告: 推文 {i} 超出 280 字符限制!")
        
        # 保存
        data = {
            'skill_name': skill_name,
            'skill_data': skill_data,
            'tweets': tweets,
            'count': len(tweets),
            'generated_at': datetime.now().isoformat()
        }
        
        filename = f"kol_thread_{skill_name}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 已保存: {filename}")
        
        return tweets


def main():
    """主函数"""
    generator = KOLThreadGenerator()
    
    # 示例数据
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
    
    generator.validate_and_generate('ai-content-pipeline', skill_data)


if __name__ == "__main__":
    main()
