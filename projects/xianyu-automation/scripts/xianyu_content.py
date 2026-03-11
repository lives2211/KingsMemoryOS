#!/usr/bin/env python3
"""
闲鱼内容生成器 - xianyu_content
自动生成闲鱼标题和描述，优化关键词
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional

class XianyuContentGenerator:
    """闲鱼内容生成器"""
    
    # 吸睛标签库
    TAGS = [
        "【自用出】", "【9成新】", "【几乎全新】", "【闲置转让】",
        "【搬家出】", "【升级出】", "【正品保证】", "【急出】",
        "【不议价】", "【可小刀】", "【包邮】", "【送配件】"
    ]
    
    # 成色描述
    CONDITIONS = {
        "全新": "全新未拆封，原包装完好",
        "99新": "仅拆封检查，未使用，成色完美",
        "95新": "使用几次，几乎无痕迹，成色很新",
        "9成新": "正常使用，轻微痕迹，功能完好",
        "8成新": "有明显使用痕迹，功能正常"
    }
    
    def __init__(self):
        self.generated_count = 0
    
    def generate_title(self, brand: str, model: str, condition: str = "9成新", 
                      price: Optional[int] = None, tags: List[str] = None) -> str:
        """
        生成25字以内的闲鱼标题
        
        Args:
            brand: 品牌名
            model: 型号
            condition: 成色
            price: 价格（可选）
            tags: 自定义标签（可选）
        
        Returns:
            优化后的标题（25字以内）
        """
        # 选择标签
        if tags is None:
            tags = random.sample(self.TAGS, 2)
        
        # 构建标题组件
        components = [
            tags[0] if tags else "",
            f"{brand} {model}",
            condition,
            f"¥{price}" if price else ""
        ]
        
        # 组合标题
        title = " ".join(filter(None, components))
        
        # 确保25字以内
        if len(title) > 25:
            title = title[:24] + "…"
        
        self.generated_count += 1
        return title.strip()
    
    def generate_description(self, brand: str, model: str, condition: str,
                           reason: str, params: Dict[str, str], 
                           accessories: List[str], warranty: str) -> str:
        """
        生成三段式描述
        
        Args:
            brand: 品牌
            model: 型号
            condition: 成色
            reason: 出售原因
            params: 详细参数（字典）
            accessories: 配件列表
            warranty: 保修信息
        
        Returns:
            完整描述文本
        """
        # 第一段：出售原因
        section1 = f"【出售原因】\n{reason}\n"
        
        # 第二段：详细参数
        params_text = "\n".join([f"• {k}: {v}" for k, v in params.items()])
        section2 = f"【详细参数】\n{self.CONDITIONS.get(condition, condition)}\n{params_text}\n"
        
        # 第三段：配件和保修
        accessories_text = "、".join(accessories) if accessories else "无"
        section3 = f"【配件清单】\n{accessories_text}\n\n【保修信息】\n{warranty}\n"
        
        # 添加关键词优化
        keywords = self._extract_keywords(brand, model, params)
        keyword_section = f"\n【关键词】\n{' '.join(keywords)}\n"
        
        # 组合完整描述
        description = f"{section1}\n{section2}\n{section3}{keyword_section}"
        
        # 添加固定结尾
        description += "\n【交易说明】\n• 非偏远地区包邮\n• 签收前请验货\n• 二手商品不退不换\n"
        
        return description
    
    def _extract_keywords(self, brand: str, model: str, params: Dict[str, str]) -> List[str]:
        """提取5-8个关键词用于搜索优化"""
        keywords = [brand, model]
        
        # 从参数中提取关键词
        for key, value in params.items():
            if any(kw in key.lower() for kw in ["color", "颜色", "memory", "存储", "size", "尺寸"]):
                keywords.append(value)
        
        # 添加通用关键词
        keywords.extend(["二手", "闲置", "转让", "正品"])
        
        # 去重并限制数量
        keywords = list(set(keywords))[:8]
        
        return keywords
    
    def generate_product_content(self, product_info: Dict) -> Dict:
        """
        一键生成完整商品内容
        
        Args:
            product_info: 商品信息字典
        
        Returns:
            包含标题和描述的字典
        """
        title = self.generate_title(
            brand=product_info.get("brand", ""),
            model=product_info.get("model", ""),
            condition=product_info.get("condition", "9成新"),
            price=product_info.get("price")
        )
        
        description = self.generate_description(
            brand=product_info.get("brand", ""),
            model=product_info.get("model", ""),
            condition=product_info.get("condition", "9成新"),
            reason=product_info.get("reason", "闲置转让"),
            params=product_info.get("params", {}),
            accessories=product_info.get("accessories", []),
            warranty=product_info.get("warranty", "无保修")
        )
        
        return {
            "title": title,
            "description": description,
            "generated_at": datetime.now().isoformat(),
            "word_count": len(description)
        }
    
    def batch_generate(self, products: List[Dict]) -> List[Dict]:
        """批量生成商品内容"""
        results = []
        for product in products:
            content = self.generate_product_content(product)
            results.append({
                "product": product,
                "content": content
            })
        return results


# CLI 接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="闲鱼内容生成器")
    parser.add_argument("--brand", required=True, help="品牌名")
    parser.add_argument("--model", required=True, help="型号")
    parser.add_argument("--condition", default="9成新", help="成色")
    parser.add_argument("--price", type=int, help="价格")
    parser.add_argument("--reason", default="闲置转让", help="出售原因")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--batch", help="批量输入JSON文件")
    
    args = parser.parse_args()
    
    generator = XianyuContentGenerator()
    
    if args.batch:
        # 批量模式
        with open(args.batch, 'r', encoding='utf-8') as f:
            products = json.load(f)
        results = generator.batch_generate(products)
        output = {
            "generated_count": len(results),
            "results": results
        }
    else:
        # 单商品模式
        product_info = {
            "brand": args.brand,
            "model": args.model,
            "condition": args.condition,
            "price": args.price,
            "reason": args.reason,
            "params": {"颜色": "默认", "存储": "默认"},
            "accessories": [],
            "warranty": "无保修"
        }
        output = generator.generate_product_content(product_info)
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"✅ 内容已保存到: {args.output}")
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))
