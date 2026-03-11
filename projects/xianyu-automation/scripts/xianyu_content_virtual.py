#!/usr/bin/env python3
"""
闲鱼虚拟资料内容生成器
针对虚拟资料的特殊优化版本
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional

class VirtualContentGenerator:
    """虚拟资料内容生成器"""
    
    # 虚拟资料专用标签
    TAGS = [
        "【自用出】", "【闲置转让】", "【正品保证】",
        "【自动发货】", "【网盘秒发】", "【全套资料】",
        "【高清无水印】", "【包更新】", "【亲测有效】"
    ]
    
    # 品类关键词
    CATEGORY_KEYWORDS = {
        "学习资料": ["教程", "课程", "学习", "资料", "笔记", "题库", "视频课"],
        "设计素材": ["素材", "模板", "PSD", "矢量", "字体", "样机", "图标"],
        "考试资料": ["真题", "解析", "考点", "押题", "密卷", "冲刺", "上岸"],
        "软件工具": ["破解", "激活", "绿色版", "免安装", "插件", "教程"],
        "课程资源": ["运营", "干货", "方法论", "SOP", "攻略", "实战"]
    }
    
    def __init__(self):
        self.generated_count = 0
    
    def generate_title(self, item: Dict) -> str:
        """生成虚拟资料标题"""
        subcategory = item.get("subcategory", "虚拟资料")
        title_base = item.get("title", "")
        
        # 选择标签
        tag = random.choice(self.TAGS)
        
        # 构建标题
        components = [
            tag,
            title_base.replace("【自用出】", "").replace("【闲置转让】", "").replace("【正品保证】", "").strip()
        ]
        
        title = " ".join(filter(None, components))
        
        # 确保30字以内
        if len(title) > 30:
            title = title[:29] + "…"
        
        return title.strip()
    
    def generate_description(self, item: Dict) -> str:
        """生成虚拟资料描述"""
        sections = []
        
        # 第一段：资料介绍
        sections.append("【资料介绍】")
        sections.append(f"这套{item.get('subcategory', '资料')}是我{item.get('reason', '精心收集')}的，内容非常全面。")
        sections.append(f"格式：{item.get('format', '百度网盘')}")
        sections.append(f"大小：{item.get('size', '未知')}")
        sections.append("")
        
        # 第二段：包含内容
        sections.append("【包含内容】")
        includes = item.get("includes", [])
        for i, content in enumerate(includes, 1):
            sections.append(f"{i}. {content}")
        sections.append("")
        
        # 第三段：使用说明
        sections.append("【使用说明】")
        sections.append("✅ 拍下后自动发货（网盘链接）")
        sections.append("✅ 手机/电脑/平板均可查看")
        sections.append("✅ 可下载到本地永久保存")
        sections.append("✅ 内容高清无水印")
        sections.append("")
        
        # 第四段：售后说明
        sections.append("【售后说明】")
        sections.append("• 虚拟商品，发货后不支持退款")
        sections.append("• 链接失效可联系补发")
        sections.append("• 有问题随时咨询，看到必回")
        sections.append("")
        
        # 关键词优化
        keywords = self._generate_keywords(item)
        sections.append("【关键词】")
        sections.append(" ".join(keywords))
        
        return "\n".join(sections)
    
    def _generate_keywords(self, item: Dict) -> List[str]:
        """生成搜索关键词"""
        subcategory = item.get("subcategory", "")
        base_keywords = ["虚拟资料", "网盘", "自动发货", "全套"]
        
        # 添加品类关键词
        if subcategory in self.CATEGORY_KEYWORDS:
            base_keywords.extend(self.CATEGORY_KEYWORDS[subcategory][:3])
        
        # 添加标题中的关键词
        title = item.get("title", "")
        if "Python" in title:
            base_keywords.extend(["Python", "编程", "教程"])
        elif "考研" in title:
            base_keywords.extend(["考研", "英语", "真题"])
        elif "设计" in title:
            base_keywords.extend(["设计", "素材", "PS"])
        elif "Adobe" in title:
            base_keywords.extend(["Adobe", "PS", "PR"])
        elif "小红书" in title:
            base_keywords.extend(["小红书", "运营", "自媒体"])
        
        return list(set(base_keywords))[:8]
    
    def generate_full_content(self, item: Dict) -> Dict:
        """生成完整内容"""
        title = self.generate_title(item)
        description = self.generate_description(item)
        
        return {
            "title": title,
            "description": description,
            "price": item.get("price"),
            "generated_at": datetime.now().isoformat(),
            "word_count": len(description)
        }
    
    def batch_generate(self, items: List[Dict]) -> List[Dict]:
        """批量生成"""
        results = []
        for item in items:
            content = self.generate_full_content(item)
            results.append({
                "item_id": item.get("id"),
                "original": item,
                "generated": content
            })
        return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="虚拟资料内容生成器")
    parser.add_argument("--input", required=True, help="商品数据JSON文件")
    parser.add_argument("--output", help="输出文件")
    
    args = parser.parse_args()
    
    generator = VirtualContentGenerator()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 支持两种格式：直接列表或包含products的对象
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and "products" in data:
        items = data["products"]
    else:
        items = [data]
    
    results = generator.batch_generate(items)
    
    output = {
        "generated_at": datetime.now().isoformat(),
        "count": len(results),
        "results": results
    }
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"✅ 已生成 {len(results)} 个商品内容，保存到: {args.output}")
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))
