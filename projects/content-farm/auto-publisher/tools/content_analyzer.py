#!/usr/bin/env python3
"""
内容分析工具
分析小红书热门内容，提取爆款特征
"""

import sys
from pathlib import Path
from typing import List, Dict, Counter
from collections import Counter
import re

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from api_publisher import XHSAPIPublisher
from loguru import logger


class ContentAnalyzer:
    """内容分析器"""
    
    def __init__(self):
        self.publisher = XHSAPIPublisher()
    
    def analyze_hot_notes(
        self,
        category: str = "food",
        limit: int = 50
    ) -> Dict:
        """
        分析热门笔记
        
        Returns:
            分析报告
        """
        logger.info(f"分析 {category} 分类热门笔记...")
        
        notes = self.publisher.get_hot(category, limit=limit)
        
        if not notes:
            return {}
        
        # 提取特征
        titles = []
        hashtags = []
        interactions = {
            "likes": [],
            "collects": [],
            "comments": []
        }
        
        for note in notes:
            # 标题
            title = note.get('title', '')
            if title:
                titles.append(title)
            
            # 标签
            tags = note.get('tags', [])
            hashtags.extend(tags)
            
            # 互动数据
            interactions["likes"].append(note.get('likes', 0))
            interactions["collects"].append(note.get('collects', 0))
            interactions["comments"].append(note.get('comments', 0))
        
        # 分析标题特征
        title_patterns = self._analyze_titles(titles)
        
        # 热门标签
        top_hashtags = Counter(hashtags).most_common(20)
        
        # 互动统计
        avg_likes = sum(interactions["likes"]) / len(interactions["likes"]) if interactions["likes"] else 0
        avg_collects = sum(interactions["collects"]) / len(interactions["collects"]) if interactions["collects"] else 0
        avg_comments = sum(interactions["comments"]) / len(interactions["comments"]) if interactions["comments"] else 0
        
        return {
            "category": category,
            "sample_size": len(notes),
            "title_patterns": title_patterns,
            "top_hashtags": top_hashtags,
            "avg_interactions": {
                "likes": round(avg_likes, 2),
                "collects": round(avg_collects, 2),
                "comments": round(avg_comments, 2)
            },
            "high_performers": self._get_high_performers(notes, top_n=5)
        }
    
    def _analyze_titles(self, titles: List[str]) -> Dict:
        """分析标题特征"""
        patterns = {
            "has_emoji": 0,
            "has_numbers": 0,
            "has_question": 0,
            "has_exclamation": 0,
            "starts_with_emoji": 0,
            "length_distribution": Counter()
        }
        
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]')
        
        for title in titles:
            # 检查emoji
            if emoji_pattern.search(title):
                patterns["has_emoji"] += 1
                if title[0] in emoji_pattern.pattern:
                    patterns["starts_with_emoji"] += 1
            
            # 检查数字
            if re.search(r'\d', title):
                patterns["has_numbers"] += 1
            
            # 检查问号
            if '?' in title or '？' in title:
                patterns["has_question"] += 1
            
            # 检查感叹号
            if '!' in title or '！' in title:
                patterns["has_exclamation"] += 1
            
            # 长度分布
            length = len(title)
            if length <= 10:
                patterns["length_distribution"]["short"] += 1
            elif length <= 20:
                patterns["length_distribution"]["medium"] += 1
            else:
                patterns["length_distribution"]["long"] += 1
        
        # 计算比例
        total = len(titles)
        if total > 0:
            for key in ["has_emoji", "has_numbers", "has_question", "has_exclamation", "starts_with_emoji"]:
                patterns[key] = {
                    "count": patterns[key],
                    "ratio": round(patterns[key] / total * 100, 2)
                }
        
        return patterns
    
    def _get_high_performers(self, notes: List[Dict], top_n: int = 5) -> List[Dict]:
        """获取高表现笔记"""
        # 按总互动排序
        for note in notes:
            note["total_interactions"] = (
                note.get('likes', 0) +
                note.get('collects', 0) +
                note.get('comments', 0)
            )
        
        sorted_notes = sorted(
            notes,
            key=lambda x: x["total_interactions"],
            reverse=True
        )
        
        return [
            {
                "title": n.get('title', ''),
                "likes": n.get('likes', 0),
                "collects": n.get('collects', 0),
                "comments": n.get('comments', 0),
                "total": n["total_interactions"]
            }
            for n in sorted_notes[:top_n]
        ]
    
    def generate_content_suggestions(self, analysis: Dict) -> List[str]:
        """生成内容建议"""
        suggestions = []
        
        # 基于标题特征
        patterns = analysis.get("title_patterns", {})
        
        if patterns.get("has_emoji", {}).get("ratio", 0) > 60:
            suggestions.append("✅ 标题使用emoji效果显著，建议继续使用")
        
        if patterns.get("has_numbers", {}).get("ratio", 0) > 40:
            suggestions.append("✅ 数字类标题表现良好，尝试使用具体数字")
        
        if patterns.get("has_question", {}).get("ratio", 0) > 20:
            suggestions.append("✅ 疑问式标题能引发互动，可适当使用")
        
        # 基于标签
        top_tags = analysis.get("top_hashtags", [])
        if top_tags:
            tag_names = [f"#{t[0]}" for t in top_tags[:5]]
            suggestions.append(f"🔥 热门标签: {', '.join(tag_names)}")
        
        # 基于互动数据
        avg = analysis.get("avg_interactions", {})
        suggestions.append(
            f"📊 平均互动: 👍{avg.get('likes', 0)} ⭐{avg.get('collects', 0)} 💬{avg.get('comments', 0)}"
        )
        
        return suggestions


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书内容分析工具")
    parser.add_argument("--category", default="food", help="内容分类")
    parser.add_argument("--limit", type=int, default=50, help="分析数量")
    
    args = parser.parse_args()
    
    analyzer = ContentAnalyzer()
    
    # 分析
    analysis = analyzer.analyze_hot_notes(
        category=args.category,
        limit=args.limit
    )
    
    if not analysis:
        print("分析失败")
        return
    
    # 输出报告
    print(f"\n📊 {args.category} 分类分析报告")
    print("=" * 50)
    
    print(f"\n样本数量: {analysis['sample_size']}")
    
    print("\n📝 标题特征:")
    patterns = analysis['title_patterns']
    for key, value in patterns.items():
        if isinstance(value, dict):
            print(f"  - {key}: {value['count']} ({value['ratio']}%)")
    
    print("\n🏷️ 热门标签 TOP 10:")
    for tag, count in analysis['top_hashtags'][:10]:
        print(f"  #{tag}: {count}")
    
    print("\n📈 平均互动:")
    avg = analysis['avg_interactions']
    print(f"  👍 点赞: {avg['likes']}")
    print(f"  ⭐ 收藏: {avg['collects']}")
    print(f"  💬 评论: {avg['comments']}")
    
    print("\n🔥 高表现笔记 TOP 5:")
    for i, note in enumerate(analysis['high_performers'], 1):
        print(f"  {i}. {note['title'][:30]}...")
        print(f"     👍{note['likes']} ⭐{note['collects']} 💬{note['comments']} 总计:{note['total']}")
    
    print("\n💡 内容建议:")
    suggestions = analyzer.generate_content_suggestions(analysis)
    for suggestion in suggestions:
        print(f"  {suggestion}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()