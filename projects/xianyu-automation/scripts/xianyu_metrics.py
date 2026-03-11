#!/usr/bin/env python3
"""
闲鱼数据分析 - xianyu_metrics
仪表盘、趋势分析、CSV导出
"""

import json
import csv
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class XianyuMetrics:
    """闲鱼数据分析器"""
    
    def __init__(self, data_dir: str = "/home/fengxueda/.openclaw/workspace/projects/xianyu-automation/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def load_items(self, items_file: Optional[str] = None) -> List[Dict]:
        """加载商品数据"""
        if items_file:
            with open(items_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认加载示例数据
        default_file = self.data_dir / "items.json"
        if default_file.exists():
            with open(default_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return []
    
    def calculate_dashboard(self, items: List[Dict]) -> Dict:
        """
        计算仪表盘数据
        
        Returns:
            仪表盘指标
        """
        total_items = len(items)
        total_views = sum(item.get("views", 0) for item in items)
        total_wants = sum(item.get("wants", 0) for item in items)
        total_revenue = sum(item.get("sold_price", 0) for item in items if item.get("status") == "sold")
        
        # 计算转化率
        conversion_rate = total_wants / total_views if total_views > 0 else 0
        
        # 在售商品
        active_items = [item for item in items if item.get("status") == "active"]
        
        # 平均数据
        avg_views = total_views / total_items if total_items > 0 else 0
        avg_wants = total_wants / total_items if total_items > 0 else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "overview": {
                "total_items": total_items,
                "active_items": len(active_items),
                "sold_items": len([i for i in items if i.get("status") == "sold"]),
                "total_views": total_views,
                "total_wants": total_wants,
                "total_revenue": total_revenue,
                "conversion_rate": round(conversion_rate * 100, 2)
            },
            "averages": {
                "avg_views_per_item": round(avg_views, 1),
                "avg_wants_per_item": round(avg_wants, 1),
                "avg_price": round(sum(i.get("price", 0) for i in items) / total_items, 2) if total_items > 0 else 0
            }
        }
    
    def analyze_trends(self, items: List[Dict], days: int = 7) -> Dict:
        """
        趋势分析
        
        Args:
            items: 商品列表
            days: 分析天数
        
        Returns:
            趋势数据
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 按日期分组统计
        daily_stats = defaultdict(lambda: {"views": 0, "wants": 0, "new_items": 0})
        
        for item in items:
            # 假设item有created_at字段
            created = item.get("created_at", "")
            if created:
                try:
                    item_date = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    if start_date <= item_date <= end_date:
                        date_key = item_date.strftime("%Y-%m-%d")
                        daily_stats[date_key]["new_items"] += 1
                except:
                    pass
            
            # 累加浏览和想要
            # 注意：这里简化处理，实际应该从历史记录中读取
        
        # 转换为列表并排序
        trend_data = []
        for date in sorted(daily_stats.keys()):
            trend_data.append({
                "date": date,
                **daily_stats[date]
            })
        
        return {
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "days": days,
            "trend": trend_data,
            "growth_rate": self._calculate_growth_rate(trend_data)
        }
    
    def _calculate_growth_rate(self, trend_data: List[Dict]) -> Dict:
        """计算增长率"""
        if len(trend_data) < 2:
            return {"views": 0, "wants": 0}
        
        first = trend_data[0]
        last = trend_data[-1]
        
        views_growth = ((last.get("views", 0) - first.get("views", 0)) / max(first.get("views", 1), 1)) * 100
        wants_growth = ((last.get("wants", 0) - first.get("wants", 0)) / max(first.get("wants", 1), 1)) * 100
        
        return {
            "views_growth": round(views_growth, 2),
            "wants_growth": round(wants_growth, 2)
        }
    
    def analyze_items(self, items: List[Dict]) -> List[Dict]:
        """
        单品分析
        
        Returns:
            每个商品的分析结果
        """
        analyzed = []
        
        for item in items:
            views = item.get("views", 0)
            wants = item.get("wants", 0)
            price = item.get("price", 0)
            
            conversion_rate = wants / views if views > 0 else 0
            
            # 性能评级
            if views > 100 and conversion_rate > 0.1:
                performance = "优秀"
                suggestion = "保持当前策略"
            elif views > 50 and conversion_rate > 0.05:
                performance = "良好"
                suggestion = "可适当优化标题"
            elif views > 20:
                performance = "一般"
                suggestion = "建议优化标题和价格"
            else:
                performance = "需优化"
                suggestion = "建议降价或重新拍摄图片"
            
            analyzed.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "views": views,
                "wants": wants,
                "price": price,
                "conversion_rate": round(conversion_rate * 100, 2),
                "performance": performance,
                "suggestion": suggestion
            })
        
        # 按浏览量排序
        analyzed.sort(key=lambda x: x["views"], reverse=True)
        
        return analyzed
    
    def export_csv(self, items: List[Dict], output_file: Optional[str] = None) -> str:
        """
        导出CSV
        
        Args:
            items: 商品列表
            output_file: 输出文件路径
        
        Returns:
            输出文件路径
        """
        if output_file is None:
            output_file = self.data_dir / f"xianyu_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        fieldnames = ["id", "title", "price", "views", "wants", "status", "created_at", "conversion_rate"]
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in items:
                views = item.get("views", 0)
                wants = item.get("wants", 0)
                conversion_rate = wants / views if views > 0 else 0
                
                row = {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "views": views,
                    "wants": wants,
                    "status": item.get("status"),
                    "created_at": item.get("created_at"),
                    "conversion_rate": f"{conversion_rate:.2%}"
                }
                writer.writerow(row)
        
        logger.info(f"✅ CSV导出完成: {output_file}")
        return str(output_file)
    
    def generate_report(self, items: List[Dict]) -> Dict:
        """
        生成完整报告
        
        Returns:
            完整分析报告
        """
        dashboard = self.calculate_dashboard(items)
        trends_7d = self.analyze_trends(items, days=7)
        trends_30d = self.analyze_trends(items, days=30)
        item_analysis = self.analyze_items(items)
        
        # 找出表现最好和最差的商品
        top_items = item_analysis[:5]
        bottom_items = item_analysis[-5:]
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "dashboard": dashboard,
            "trends": {
                "7_days": trends_7d,
                "30_days": trends_30d
            },
            "item_analysis": {
                "total": len(item_analysis),
                "top_performers": top_items,
                "needs_improvement": bottom_items
            },
            "recommendations": self._generate_recommendations(item_analysis)
        }
        
        return report
    
    def _generate_recommendations(self, analyzed_items: List[Dict]) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 整体转化率分析
        avg_conversion = sum(i["conversion_rate"] for i in analyzed_items) / len(analyzed_items) if analyzed_items else 0
        
        if avg_conversion < 5:
            recommendations.append(f"整体转化率较低({avg_conversion:.1f}%)，建议优化商品描述和价格策略")
        
        # 低浏览商品
        low_views = [i for i in analyzed_items if i["views"] < 20]
        if low_views:
            recommendations.append(f"有 {len(low_views)} 个商品浏览量过低，建议重新优化标题或降价")
        
        # 高浏览低转化
        high_views_low_conv = [i for i in analyzed_items if i["views"] > 100 and i["conversion_rate"] < 5]
        if high_views_low_conv:
            recommendations.append(f"有 {len(high_views_low_conv)} 个商品浏览高但转化低，建议检查价格竞争力")
        
        if not recommendations:
            recommendations.append("整体表现良好，继续保持当前运营策略")
        
        return recommendations


# CLI 接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="闲鱼数据分析")
    parser.add_argument("--items", required=True, help="商品数据JSON文件")
    parser.add_argument("--output", help="报告输出文件")
    parser.add_argument("--export-csv", action="store_true", help="导出CSV")
    parser.add_argument("--dashboard", action="store_true", help="显示仪表盘")
    parser.add_argument("--trends", type=int, help="趋势分析天数")
    parser.add_argument("--full-report", action="store_true", help="生成完整报告")
    
    args = parser.parse_args()
    
    metrics = XianyuMetrics()
    items = metrics.load_items(args.items)
    
    if not items:
        logger.error("❌ 没有找到商品数据")
        exit(1)
    
    logger.info(f"📊 加载了 {len(items)} 个商品")
    
    if args.dashboard:
        result = metrics.calculate_dashboard(items)
    elif args.trends:
        result = metrics.analyze_trends(items, days=args.trends)
    elif args.full_report:
        result = metrics.generate_report(items)
    else:
        result = metrics.calculate_dashboard(items)
    
    # 导出CSV
    if args.export_csv:
        csv_path = metrics.export_csv(items)
        result["csv_export"] = csv_path
    
    # 输出结果
    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        logger.info(f"✅ 报告已保存: {args.output}")
    else:
        print(output)
