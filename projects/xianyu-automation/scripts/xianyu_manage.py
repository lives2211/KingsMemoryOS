#!/usr/bin/env python3
"""
闲鱼商品管理 - xianyu_manage
自动擦亮商品、批量管理
"""

import json
import time
import random
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/fengxueda/.openclaw/workspace/projects/xianyu-automation/logs/xianyu_manage.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class XianyuManager:
    """闲鱼商品管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.polished_today = set()
        self.last_polish_time = None
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置"""
        default_config = {
            "max_items_per_day": 50,
            "delay_min": 1,
            "delay_max": 3,
            "peak_hours": ["07:00-09:00", "19:00-21:00"],
            "auto_price_adjust": True,
            "price_adjust_threshold": {
                "views_high_wants_low": 0.3,  # 浏览高但想要低，降价30%
                "views_low": 0.1  # 浏览低，降价10%
            }
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def _random_delay(self):
        """随机延迟，模拟真人操作"""
        delay = random.uniform(self.config["delay_min"], self.config["delay_max"])
        logger.info(f"⏱️  延迟 {delay:.1f} 秒...")
        time.sleep(delay)
    
    def is_peak_hour(self) -> bool:
        """检查当前是否为流量高峰期"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        for peak_range in self.config["peak_hours"]:
            start, end = peak_range.split("-")
            if start <= current_time <= end:
                return True
        return False
    
    def can_polish(self, item_id: str) -> bool:
        """检查商品是否可以擦亮"""
        # 每天每个商品只能擦亮一次
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"{today}:{item_id}"
        return key not in self.polished_today
    
    def polish_item(self, item_id: str, item_info: Dict) -> Dict:
        """
        擦亮单个商品
        
        Args:
            item_id: 商品ID
            item_info: 商品信息
        
        Returns:
            操作结果
        """
        if not self.can_polish(item_id):
            logger.warning(f"⚠️  商品 {item_id} 今天已擦亮过")
            return {"success": False, "reason": "already_polished_today"}
        
        # 模拟擦亮操作
        self._random_delay()
        
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"{today}:{item_id}"
        self.polished_today.add(key)
        self.last_polish_time = datetime.now()
        
        logger.info(f"✅ 商品 {item_id} 擦亮成功")
        
        return {
            "success": True,
            "item_id": item_id,
            "polished_at": datetime.now().isoformat(),
            "next_polish": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        }
    
    def polish_all(self, items: List[Dict]) -> List[Dict]:
        """
        批量擦亮商品
        
        Args:
            items: 商品列表
        
        Returns:
            操作结果列表
        """
        results = []
        max_items = self.config["max_items_per_day"]
        
        logger.info(f"🚀 开始批量擦亮，共 {len(items)} 个商品，上限 {max_items}")
        
        for i, item in enumerate(items[:max_items], 1):
            logger.info(f"[{i}/{min(len(items), max_items)}] 处理商品: {item.get('title', item.get('id', 'Unknown'))}")
            
            result = self.polish_item(item.get("id"), item)
            results.append(result)
            
            if i < len(items[:max_items]):
                self._random_delay()
        
        # 保存操作记录
        self._save_polish_log(results)
        
        success_count = sum(1 for r in results if r.get("success"))
        logger.info(f"✨ 批量擦亮完成: {success_count}/{len(results)} 成功")
        
        return results
    
    def _save_polish_log(self, results: List[Dict]):
        """保存擦亮记录"""
        log_file = Path("/home/fengxueda/.openclaw/workspace/projects/xianyu-automation/data/polish_log.json")
        
        log_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().isoformat(),
            "results": results
        }
        
        logs = []
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def suggest_price_adjustment(self, item: Dict) -> Optional[Dict]:
        """
        智能调价建议
        
        Args:
            item: 商品数据（需包含views, wants, price）
        
        Returns:
            调价建议
        """
        views = item.get("views", 0)
        wants = item.get("wants", 0)
        price = item.get("price", 0)
        
        if views == 0 or price == 0:
            return None
        
        conversion_rate = wants / views if views > 0 else 0
        
        # 浏览高但转化率低 → 降价
        if views > 100 and conversion_rate < 0.05:
            new_price = int(price * (1 - self.config["price_adjust_threshold"]["views_high_wants_low"]))
            return {
                "action": "decrease",
                "current_price": price,
                "suggested_price": new_price,
                "reason": f"浏览量高({views})但转化率低({conversion_rate:.1%})，建议降价",
                "expected_increase": "30-50%"
            }
        
        # 浏览量低 → 小幅降价
        if views < 50:
            new_price = int(price * (1 - self.config["price_adjust_threshold"]["views_low"]))
            return {
                "action": "decrease",
                "current_price": price,
                "suggested_price": new_price,
                "reason": f"浏览量低({views})，建议小幅降价增加曝光",
                "expected_increase": "10-20%"
            }
        
        return {"action": "keep", "reason": "数据正常，建议保持价格"}
    
    def get_daily_summary(self) -> Dict:
        """获取每日操作摘要"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        return {
            "date": today,
            "polished_count": len([k for k in self.polished_today if k.startswith(today)]),
            "max_items": self.config["max_items_per_day"],
            "is_peak_hour": self.is_peak_hour(),
            "last_polish_time": self.last_polish_time.isoformat() if self.last_polish_time else None
        }


# CLI 接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="闲鱼商品管理器")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--items", required=True, help="商品列表JSON文件")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行，不实际执行")
    parser.add_argument("--check-peak", action="store_true", help="检查当前是否为高峰期")
    
    args = parser.parse_args()
    
    manager = XianyuManager(args.config)
    
    if args.check_peak:
        is_peak = manager.is_peak_hour()
        print(f"当前{'是' if is_peak else '不是'}流量高峰期")
        exit(0)
    
    # 加载商品列表
    with open(args.items, 'r', encoding='utf-8') as f:
        items = json.load(f)
    
    if args.dry_run:
        logger.info("🔍 模拟运行模式，不会实际擦亮")
    
    # 执行擦亮
    results = manager.polish_all(items)
    
    # 输出结果
    print(json.dumps({
        "summary": manager.get_daily_summary(),
        "results": results
    }, ensure_ascii=False, indent=2))
