#!/usr/bin/env python3
"""
闲鱼市场数据爬虫
抓取热门商品、销量、价格等数据
输出Excel表格
"""

import json
import time
import random
import logging
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/fengxueda/.openclaw/workspace/projects/xianyu-automation/logs/scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class XianyuScraper:
    """闲鱼市场数据爬虫"""
    
    def __init__(self):
        self.base_dir = Path("/home/fengxueda/.openclaw/workspace/projects/xianyu-automation")
        self.data_dir = self.base_dir / "data" / "market_data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 模拟浏览器请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        
        # 搜索关键词列表
        self.keywords = [
            "虚拟资料", "教程", "课程", "学习资料",
            "考研", "四六级", "公考", "教资",
            "Python", "编程", "AI", "ChatGPT",
            "小红书", "运营", "自媒体",
            "PPT模板", "设计素材", "简历模板",
            "Adobe", "软件", "工具"
        ]
    
    def _random_delay(self, min_sec=1, max_sec=3):
        """随机延迟，防止被封"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def _get_proxy(self) -> Optional[str]:
        """获取代理（可选）"""
        # 这里可以配置代理池
        return None
    
    def search_items(self, keyword: str, page: int = 1) -> List[Dict]:
        """
        搜索商品（模拟数据，实际需对接闲鱼API或爬虫）
        
        Args:
            keyword: 搜索关键词
            page: 页码
        
        Returns:
            商品列表
        """
        logger.info(f"🔍 搜索: {keyword}, 页码: {page}")
        
        # 模拟数据（实际使用时需要实现真实爬虫）
        # 这里生成模拟数据用于演示
        mock_items = []
        
        for i in range(10):
            item = {
                "item_id": f"mock_{keyword}_{page}_{i}",
                "title": f"【热销】{keyword}全套资料",
                "price": random.choice([9.9, 15, 19, 29, 39, 49]),
                "original_price": random.choice([99, 199, 299, 499]),
                "views": random.randint(50, 500),
                "wants": random.randint(5, 50),
                "sales": random.randint(1, 30),
                "seller": f"seller_{random.randint(1000, 9999)}",
                "location": random.choice(["北京", "上海", "广州", "深圳", "杭州", "成都"]),
                "post_time": (datetime.now() - timedelta(hours=random.randint(1, 72))).strftime("%Y-%m-%d %H:%M"),
                "category": keyword,
                "url": f"https://www.goofish.com/item?id=mock_{i}",
                "scraped_at": datetime.now().isoformat()
            }
            mock_items.append(item)
        
        self._random_delay()
        return mock_items
    
    def get_hot_items(self) -> List[Dict]:
        """获取热门商品"""
        logger.info("🔥 获取热门商品...")
        
        hot_items = []
        
        # 搜索多个关键词
        for keyword in self.keywords[:5]:  # 先搜前5个
            items = self.search_items(keyword, page=1)
            # 按想要数排序，取前3
            items.sort(key=lambda x: x['wants'], reverse=True)
            hot_items.extend(items[:3])
        
        # 去重并按销量排序
        seen = set()
        unique_items = []
        for item in hot_items:
            if item['title'] not in seen:
                seen.add(item['title'])
                unique_items.append(item)
        
        unique_items.sort(key=lambda x: x['sales'], reverse=True)
        
        return unique_items[:20]  # 返回前20
    
    def get_new_items(self, hours: int = 24) -> List[Dict]:
        """获取最新发布的商品"""
        logger.info(f"🆕 获取最近{hours}小时的新商品...")
        
        new_items = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for keyword in self.keywords[:3]:
            items = self.search_items(keyword, page=1)
            for item in items:
                item_time = datetime.strptime(item['post_time'], "%Y-%m-%d %H:%M")
                if item_time > cutoff_time:
                    new_items.append(item)
        
        # 按发布时间排序
        new_items.sort(key=lambda x: x['post_time'], reverse=True)
        
        return new_items[:30]  # 返回前30
    
    def get_price_trend(self, keyword: str) -> Dict:
        """获取价格趋势"""
        logger.info(f"📈 分析价格趋势: {keyword}")
        
        items = self.search_items(keyword, page=1)
        items.extend(self.search_items(keyword, page=2))
        
        prices = [item['price'] for item in items]
        
        return {
            "keyword": keyword,
            "sample_count": len(prices),
            "avg_price": round(sum(prices) / len(prices), 2) if prices else 0,
            "min_price": min(prices) if prices else 0,
            "max_price": max(prices) if prices else 0,
            "median_price": round(sorted(prices)[len(prices)//2], 2) if prices else 0,
            "recommended_price": round(sum(prices) / len(prices) * 0.9, 2) if prices else 0,
            "scraped_at": datetime.now().isoformat()
        }
    
    def analyze_market(self) -> Dict:
        """全面市场分析"""
        logger.info("📊 开始全面市场分析...")
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "hot_items": self.get_hot_items(),
            "new_items": self.get_new_items(hours=24),
            "price_trends": []
        }
        
        # 分析热门品类的价格趋势
        hot_categories = ["考研", "四六级", "ChatGPT", "小红书", "Python"]
        for category in hot_categories:
            trend = self.get_price_trend(category)
            analysis["price_trends"].append(trend)
        
        return analysis
    
    def save_to_excel(self, data: Dict, filename: Optional[str] = None):
        """
        保存数据到Excel
        
        Args:
            data: 市场分析数据
            filename: 文件名
        """
        if filename is None:
            filename = f"xianyu_market_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        
        filepath = self.data_dir / filename
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Sheet 1: 热门商品
            if data.get("hot_items"):
                df_hot = pd.DataFrame(data["hot_items"])
                df_hot = df_hot[["title", "price", "sales", "wants", "views", "category", "url", "post_time"]]
                df_hot.to_excel(writer, sheet_name='热门商品', index=False)
            
            # Sheet 2: 最新商品
            if data.get("new_items"):
                df_new = pd.DataFrame(data["new_items"])
                df_new = df_new[["title", "price", "wants", "category", "url", "post_time"]]
                df_new.to_excel(writer, sheet_name='最新发布', index=False)
            
            # Sheet 3: 价格趋势
            if data.get("price_trends"):
                df_trend = pd.DataFrame(data["price_trends"])
                df_trend = df_trend[["keyword", "avg_price", "min_price", "max_price", "recommended_price", "sample_count"]]
                df_trend.to_excel(writer, sheet_name='价格趋势', index=False)
            
            # Sheet 4: 数据摘要
            summary = {
                "采集时间": [data["timestamp"]],
                "热门商品数": [len(data.get("hot_items", []))],
                "最新商品数": [len(data.get("new_items", []))],
                "分析品类数": [len(data.get("price_trends", []))]
            }
            df_summary = pd.DataFrame(summary)
            df_summary.to_excel(writer, sheet_name='数据摘要', index=False)
        
        logger.info(f"✅ Excel已保存: {filepath}")
        return filepath
    
    def run(self, save_excel: bool = True) -> Dict:
        """运行完整爬虫流程"""
        logger.info("🚀 开始爬取闲鱼市场数据...")
        
        start_time = time.time()
        
        # 获取市场分析数据
        data = self.analyze_market()
        
        # 保存到Excel
        if save_excel:
            filepath = self.save_to_excel(data)
            data["excel_path"] = str(filepath)
        
        # 保存JSON备份
        json_path = self.data_dir / f"market_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        elapsed = time.time() - start_time
        logger.info(f"✅ 爬取完成！耗时: {elapsed:.1f}秒")
        logger.info(f"📊 热门商品: {len(data['hot_items'])} 个")
        logger.info(f"📊 最新商品: {len(data['new_items'])} 个")
        logger.info(f"📊 价格趋势: {len(data['price_trends'])} 个品类")
        
        return data


# CLI 接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="闲鱼市场数据爬虫")
    parser.add_argument("--keyword", help="搜索特定关键词")
    parser.add_argument("--no-excel", action="store_true", help="不生成Excel")
    parser.add_argument("--output", help="输出文件名")
    
    args = parser.parse_args()
    
    scraper = XianyuScraper()
    
    if args.keyword:
        # 搜索特定关键词
        items = scraper.search_items(args.keyword)
        print(json.dumps(items, ensure_ascii=False, indent=2))
    else:
        # 完整市场分析
        data = scraper.run(save_excel=not args.no_excel)
        print(f"\n✅ 数据已保存!")
        print(f"📁 Excel: {data.get('excel_path')}")
