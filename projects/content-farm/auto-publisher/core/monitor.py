"""
发布监控系统
记录发布历史、成功率、异常检测
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from loguru import logger


@dataclass
class PublishRecord:
    """发布记录"""
    id: str
    title: str
    account: str
    status: str  # success, failed, pending
    created_at: str
    published_at: Optional[str] = None
    error_message: Optional[str] = None
    image_count: int = 0
    hashtags_count: int = 0
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "PublishRecord":
        return cls(**data)


class PublishMonitor:
    """发布监控器"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.records_file = self.data_dir / "publish_records.json"
        self.records: List[PublishRecord] = []
        self._load_records()
    
    def _load_records(self):
        """加载历史记录"""
        if self.records_file.exists():
            try:
                with open(self.records_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.records = [PublishRecord.from_dict(r) for r in data]
                logger.info(f"加载 {len(self.records)} 条发布记录")
            except Exception as e:
                logger.error(f"加载记录失败: {e}")
    
    def _save_records(self):
        """保存记录"""
        try:
            data = [r.to_dict() for r in self.records]
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存记录失败: {e}")
    
    def add_record(self, record: PublishRecord):
        """添加记录"""
        self.records.append(record)
        self._save_records()
        logger.info(f"添加发布记录: {record.title}")
    
    def update_record(self, record_id: str, **kwargs):
        """更新记录"""
        for record in self.records:
            if record.id == record_id:
                for key, value in kwargs.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                self._save_records()
                return True
        return False
    
    def get_records(
        self,
        account: Optional[str] = None,
        status: Optional[str] = None,
        days: Optional[int] = None,
        limit: int = 100
    ) -> List[PublishRecord]:
        """查询记录"""
        records = self.records
        
        # 按账号筛选
        if account:
            records = [r for r in records if r.account == account]
        
        # 按状态筛选
        if status:
            records = [r for r in records if r.status == status]
        
        # 按日期筛选
        if days:
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()
            records = [r for r in records if r.created_at > cutoff]
        
        # 按时间倒序，限制数量
        records = sorted(records, key=lambda r: r.created_at, reverse=True)
        return records[:limit]
    
    def get_stats(self, days: int = 7) -> Dict:
        """获取统计信息"""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        recent_records = [r for r in self.records if r.created_at > cutoff]
        
        total = len(recent_records)
        success = len([r for r in recent_records if r.status == "success"])
        failed = len([r for r in recent_records if r.status == "failed"])
        
        success_rate = (success / total * 100) if total > 0 else 0
        
        # 按账号统计
        by_account = {}
        for r in recent_records:
            if r.account not in by_account:
                by_account[r.account] = {"total": 0, "success": 0}
            by_account[r.account]["total"] += 1
            if r.status == "success":
                by_account[r.account]["success"] += 1
        
        return {
            "period_days": days,
            "total": total,
            "success": success,
            "failed": failed,
            "success_rate": round(success_rate, 2),
            "by_account": by_account
        }
    
    def get_daily_stats(self, days: int = 7) -> List[Dict]:
        """获取每日统计"""
        stats = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            day_start = f"{date}T00:00:00"
            day_end = f"{date}T23:59:59"
            
            day_records = [
                r for r in self.records
                if day_start <= r.created_at <= day_end
            ]
            
            success = len([r for r in day_records if r.status == "success"])
            failed = len([r for r in day_records if r.status == "failed"])
            
            stats.append({
                "date": date,
                "total": len(day_records),
                "success": success,
                "failed": failed
            })
        
        return stats
    
    def detect_anomalies(self) -> List[Dict]:
        """检测异常"""
        anomalies = []
        
        # 检查连续失败
        recent = self.get_records(limit=10)
        failed_streak = 0
        for r in recent:
            if r.status == "failed":
                failed_streak += 1
            else:
                break
        
        if failed_streak >= 3:
            anomalies.append({
                "type": "failed_streak",
                "message": f"连续 {failed_streak} 次发布失败",
                "severity": "high"
            })
        
        # 检查成功率
        stats = self.get_stats(days=1)
        if stats["total"] > 0 and stats["success_rate"] < 50:
            anomalies.append({
                "type": "low_success_rate",
                "message": f"今日成功率仅 {stats['success_rate']}%",
                "severity": "medium"
            })
        
        return anomalies
    
    def export_report(self, output_file: str, days: int = 7):
        """导出报告"""
        stats = self.get_stats(days)
        daily = self.get_daily_stats(days)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "period_days": days,
            "summary": stats,
            "daily": daily,
            "recent_records": [
                r.to_dict() for r in self.get_records(limit=20)
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"报告已导出: {output_file}")


def main():
    """测试代码"""
    monitor = PublishMonitor()
    
    # 添加测试记录
    from uuid import uuid4
    record = PublishRecord(
        id=str(uuid4()),
        title="测试笔记",
        account="test_account",
        status="success",
        created_at=datetime.now().isoformat(),
        published_at=datetime.now().isoformat(),
        image_count=3,
        hashtags_count=5
    )
    monitor.add_record(record)
    
    # 查看统计
    stats = monitor.get_stats(days=7)
    print(f"\n发布统计:")
    print(f"  总计: {stats['total']}")
    print(f"  成功: {stats['success']}")
    print(f"  失败: {stats['failed']}")
    print(f"  成功率: {stats['success_rate']}%")
    
    # 检测异常
    anomalies = monitor.detect_anomalies()
    if anomalies:
        print(f"\n⚠️ 检测到 {len(anomalies)} 个异常:")
        for a in anomalies:
            print(f"  - [{a['severity']}] {a['message']}")


if __name__ == "__main__":
    main()
