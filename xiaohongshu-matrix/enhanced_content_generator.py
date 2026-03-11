#!/usr/bin/env python3
"""
增强版内容生成器
- 集成union-search进行热点研究
- 集成aitu生成创意素材
- 基于爆款分析生成内容
"""

import os
import sys
import random
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from content_generator import ContentGenerator, CONTENT_TEMPLATES
from assistant_tools import AssistantToolsManager

class EnhancedContentGenerator(ContentGenerator):
    """增强版内容生成器"""
    
    def __init__(self, base_path="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"):
        super().__init__(base_path)
        self.tools = AssistantToolsManager()
        self.research_cache = {}
        
    def research_and_generate(self, account_type: str, topic: str = None) -> Dict:
        """研究话题并生成内容"""
        print(f"\n🔍 开始研究: {account_type}")
        
        # 1. 确定话题
        if not topic:
            topic = self._select_topic(account_type)
        
        print(f"📌 选定话题: {topic}")
        
        # 2. 多平台研究
        research = self.tools.research_topic(topic, account_type)
        
        # 3. 分析爆款
        viral_titles = [v.get("title", "") for v in research.get("viral_content", [])]
        viral_patterns = self._analyze_viral_patterns(viral_titles)
        
        print(f"📊 发现 {len(viral_titles)} 条相关爆款")
        print(f"💡 爆款特征: {viral_patterns[:3]}")
        
        # 4. 生成标题（参考爆款模式）
        title = self._generate_optimized_title(account_type, topic, viral_patterns)
        print(f"📝 生成标题: {title}")
        
        # 5. 生成内容
        content = self._generate_optimized_content(account_type, title, research)
        
        # 6. 保存研究数据
        self._save_research_data(account_type, topic, research)
        
        return {
            "title": title,
            "content": content,
            "topic": topic,
            "research": research,
            "viral_patterns": viral_patterns
        }
    
    def _select_topic(self, account_type: str) -> str:
        """选择话题"""
        topics = CONTENT_TEMPLATES[account_type]["topics"]
        return random.choice(topics)
    
    def _analyze_viral_patterns(self, titles: List[str]) -> List[str]:
        """分析爆款标题模式"""
        patterns = []
        
        # 常见爆款模式
        pattern_keywords = {
            "数字型": ["X个", "X款", "X天", "X元"],
            "疑问型": ["如何", "为什么", "怎么办", "值得吗"],
            "对比型": ["vs", "对比", "区别", "哪个"],
            "情绪型": ["震惊", "绝了", "救命", "必看"],
            "干货型": ["攻略", "指南", "教程", "干货"],
            "揭秘型": ["真相", "秘密", "内幕", "没人告诉你"]
        }
        
        for title in titles:
            for pattern, keywords in pattern_keywords.items():
                if any(kw in title for kw in keywords):
                    patterns.append(pattern)
        
        # 返回最常见的模式
        from collections import Counter
        if patterns:
            return [p for p, _ in Counter(patterns).most_common(3)]
        return ["数字型", "干货型"]
    
    def _generate_optimized_title(self, account_type: str, topic: str, viral_patterns: List[str]) -> str:
        """生成优化标题"""
        # 根据爆款模式选择模板
        templates = CONTENT_TEMPLATES[account_type]["titles"]
        
        # 优先选择符合爆款模式的模板
        if "数字型" in viral_patterns:
            candidates = [t for t in templates if "{X}" in t or "{Y}" in t or "{price}" in t]
        elif "疑问型" in viral_patterns:
            candidates = [t for t in templates if "?" in t or "吗" in t]
        elif "干货型" in viral_patterns:
            candidates = [t for t in templates if "干货" in t or "攻略" in t or "技巧" in t]
        else:
            candidates = templates
        
        if not candidates:
            candidates = templates
        
        template = random.choice(candidates)
        
        # 替换变量
        variables = {
            "{X}": str(random.randint(2, 10)),
            "{Y}": str(random.randint(2, 5)),
            "{price}": str(random.choice([29, 49, 99, 199, 299, 499, 999])),
            "{product}": random.choice(["iPhone", "AirPods", "机械键盘", "显示器", "耳机", "平板"]),
            "{style}": random.choice(["ins风", "原木风", "极简风", "复古风", "奶油风"]),
            "{level}": random.choice(["专员", "主管", "经理", "小白"]),
            "{target}": random.choice(["总监", "VP", "专家", "高手"]),
            "{dish}": random.choice(["红烧肉", "提拉米苏", "韩式拌饭", "奶茶", "火锅"]),
            "{season}": random.choice(["春日", "夏日", "秋日", "冬日"])
        }
        
        title = template
        for var, value in variables.items():
            title = title.replace(var, value)
        
        return title
    
    def _generate_optimized_content(self, account_type: str, title: str, research: Dict) -> str:
        """生成优化内容"""
        # 基于研究结果调整内容
        viral_content = research.get("viral_content", [])
        
        # 提取爆款内容的共同点
        common_elements = self._extract_common_elements(viral_content)
        
        # 生成基础内容
        base_content = self.generate_content(account_type, title)
        
        # 根据研究优化内容
        optimized = self._optimize_with_research(base_content, common_elements)
        
        return optimized
    
    def _extract_common_elements(self, viral_content: List[Dict]) -> Dict:
        """提取爆款内容的共同元素"""
        elements = {
            "has_numbers": False,
            "has_emojis": False,
            "has_cta": False,  # Call to action
            "avg_length": 0,
            "common_words": []
        }
        
        if not viral_content:
            return elements
        
        # 分析内容特征
        all_text = " ".join([v.get("content", "") for v in viral_content])
        
        # 检查是否有数字
        elements["has_numbers"] = any(c.isdigit() for c in all_text)
        
        # 检查是否有表情
        # 简化处理
        
        # 检查是否有互动引导
        cta_words = ["评论", "点赞", "收藏", "关注", "私信", "告诉我"]
        elements["has_cta"] = any(word in all_text for word in cta_words)
        
        return elements
    
    def _optimize_with_research(self, content: str, elements: Dict) -> str:
        """根据研究优化内容"""
        optimized = content
        
        # 如果没有互动引导，添加一个
        if not elements.get("has_cta"):
            ctas = [
                "\n\n💬 你觉得呢？评论区聊聊",
                "\n\n👆 有用的话记得收藏",
                "\n\n❤️ 喜欢就点个赞吧",
                "\n\n📝 有问题评论区留言，看到都会回"
            ]
            optimized += random.choice(ctas)
        
        return optimized
    
    def _save_research_data(self, account_type: str, topic: str, research: Dict):
        """保存研究数据"""
        research_dir = self.base_path / "research"
        research_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{account_type}_{topic}_{timestamp}.json"
        filepath = research_dir / filename
        
        # 简化保存
        simplified = {
            "account_type": account_type,
            "topic": topic,
            "timestamp": timestamp,
            "viral_count": len(research.get("viral_content", [])),
            "suggestions": research.get("suggestions", [])
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(simplified, f, ensure_ascii=False, indent=2)
        
        print(f"💾 研究数据已保存: {filepath}")
    
    def batch_generate_with_research(self, account_type: str, count: int = 5) -> List[Dict]:
        """批量生成（带研究）"""
        results = []
        
        # 先研究热门话题
        topics = CONTENT_TEMPLATES[account_type]["topics"]
        researched_topics = []
        
        for topic in topics[:3]:  # 研究前3个话题
            print(f"\n{'='*50}")
            print(f"研究话题: {topic}")
            result = self.research_and_generate(account_type, topic)
            results.append(result)
            researched_topics.append(topic)
        
        # 剩余数量用随机话题
        remaining = count - len(results)
        for i in range(remaining):
            topic = random.choice(topics)
            print(f"\n{'='*50}")
            print(f"生成内容 {len(results)+1}/{count}: {topic}")
            result = self.research_and_generate(account_type, topic)
            results.append(result)
        
        return results

if __name__ == "__main__":
    generator = EnhancedContentGenerator()
    
    # 测试增强生成
    print("🦞 增强版内容生成器测试\n")
    
    # 显示工具状态
    status = generator.tools.get_status()
    for tool, info in status.items():
        icon = "✅" if info["available"] else "❌"
        print(f"{icon} {tool}: {', '.join(info['features'][:2])}...")
    
    print("\n" + "="*50)
    print("测试生成: 数码虾")
    
    result = generator.research_and_generate("tech-geek", "手机评测")
    
    print(f"\n✅ 生成完成!")
    print(f"标题: {result['title']}")
    print(f"话题: {result['topic']}")
    print(f"爆款模式: {result['viral_patterns']}")
    print(f"\n内容预览:")
    print(result['content'][:200] + "...")
