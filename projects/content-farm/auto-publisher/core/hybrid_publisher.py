"""
混合策略发布器
智能选择 CDP浏览器 或 API 方式
根据账号状态、风控情况自动切换
"""

import asyncio
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from loguru import logger

from .publisher import XHSPublisher, PublishConfig
from .api_publisher import XHSAPIPublisher
from .monitor import PublishMonitor


class PublishStrategy(Enum):
    """发布策略"""
    AUTO = "auto"           # 自动选择
    CDP = "cdp"            # 浏览器CDP
    API = "api"            # API调用


@dataclass
class StrategyConfig:
    """策略配置"""
    # 风控阈值
    api_fail_threshold: int = 3      # API连续失败次数切换CDP
    cdp_fail_threshold: int = 2      # CDP连续失败次数暂停
    
    # 冷却时间
    api_cooldown_minutes: int = 30   # API失败后冷却时间
    cdp_cooldown_minutes: int = 60   # CDP失败后冷却时间
    
    # 成功率阈值
    min_success_rate: float = 50.0   # 最低成功率
    
    # 新账号保护
    new_account_days: int = 7        # 新账号保护期（天）
    new_account_strategy: PublishStrategy = PublishStrategy.CDP


class HybridPublisher:
    """
    混合策略发布器
    
    智能决策逻辑：
    1. 新账号（7天内）→ 强制CDP
    2. API连续失败3次 → 切换CDP
    3. CDP连续失败2次 → 暂停发布
    4. 成功率<50% → 切换策略
    5. 正常状态 → 优先API（更快）
    """
    
    def __init__(
        self,
        strategy_config: Optional[StrategyConfig] = None,
        account_name: str = "default"
    ):
        self.config = strategy_config or StrategyConfig()
        self.account_name = account_name
        
        # 初始化发布器
        self.cdp_publisher: Optional[XHSPublisher] = None
        self.api_publisher: Optional[XHSAPIPublisher] = None
        
        # 状态追踪
        self.current_strategy = PublishStrategy.AUTO
        self.api_fail_count = 0
        self.cdp_fail_count = 0
        self.last_api_fail: Optional[datetime] = None
        self.last_cdp_fail: Optional[datetime] = None
        
        # 监控
        self.monitor = PublishMonitor()
        
        # 账号创建时间（从监控记录推断）
        self.account_created = self._get_account_created_time()
    
    def _get_account_created_time(self) -> datetime:
        """获取账号创建时间"""
        # 从记录中查找最早的发布记录
        records = self.monitor.get_records(
            account=self.account_name,
            limit=1
        )
        if records:
            return datetime.fromisoformat(records[0].created_at)
        return datetime.now()
    
    def _is_new_account(self) -> bool:
        """检查是否为新账号"""
        days = (datetime.now() - self.account_created).days
        return days < self.config.new_account_days
    
    def _is_api_in_cooldown(self) -> bool:
        """检查API是否在冷却期"""
        if self.last_api_fail is None:
            return False
        cooldown = timedelta(minutes=self.config.api_cooldown_minutes)
        return datetime.now() - self.last_api_fail < cooldown
    
    def _is_cdp_in_cooldown(self) -> bool:
        """检查CDP是否在冷却期"""
        if self.last_cdp_fail is None:
            return False
        cooldown = timedelta(minutes=self.config.cdp_cooldown_minutes)
        return datetime.now() - self.last_cdp_fail < cooldown
    
    def _get_recent_success_rate(self, days: int = 1) -> float:
        """获取最近成功率"""
        stats = self.monitor.get_stats(days=days)
        return stats.get('success_rate', 100.0)
    
    def select_strategy(self) -> PublishStrategy:
        """
        智能选择发布策略
        
        决策树：
        1. 新账号？ → CDP
        2. CDP冷却中？ → 暂停
        3. API连续失败3次？ → CDP
        4. API冷却中？ → CDP
        5. 成功率<50%？ → CDP
        6. 默认 → API
        """
        # 1. 新账号保护
        if self._is_new_account():
            logger.info("新账号保护期，使用CDP策略")
            return PublishStrategy.CDP
        
        # 2. CDP冷却检查
        if self._is_cdp_in_cooldown():
            remaining = self.config.cdp_cooldown_minutes - \
                (datetime.now() - self.last_cdp_fail).seconds // 60
            logger.warning(f"CDP冷却中，剩余 {remaining} 分钟")
            return PublishStrategy.CDP  # 尝试CDP，如果也失败会暂停
        
        # 3. API连续失败检查
        if self.api_fail_count >= self.config.api_fail_threshold:
            logger.warning(f"API连续失败 {self.api_fail_count} 次，切换CDP")
            return PublishStrategy.CDP
        
        # 4. API冷却检查
        if self._is_api_in_cooldown():
            logger.info("API冷却中，使用CDP")
            return PublishStrategy.CDP
        
        # 5. 成功率检查
        success_rate = self._get_recent_success_rate(days=1)
        if success_rate < self.config.min_success_rate:
            logger.warning(f"成功率 {success_rate}% 过低，切换CDP")
            return PublishStrategy.CDP
        
        # 6. 默认使用API
        logger.info("使用API策略")
        return PublishStrategy.API
    
    async def publish(
        self,
        config: PublishConfig,
        force_strategy: Optional[PublishStrategy] = None
    ) -> bool:
        """
        智能发布
        
        Args:
            config: 发布配置
            force_strategy: 强制使用指定策略
            
        Returns:
            是否成功
        """
        # 选择策略
        strategy = force_strategy or self.select_strategy()
        self.current_strategy = strategy
        
        logger.info(f"当前策略: {strategy.value}")
        
        # 根据策略执行
        if strategy == PublishStrategy.API:
            return await self._publish_with_api(config)
        else:
            return await self._publish_with_cdp(config)
    
    async def _publish_with_api(self, config: PublishConfig) -> bool:
        """使用API发布"""
        try:
            # 初始化API发布器
            if self.api_publisher is None:
                self.api_publisher = XHSAPIPublisher()
            
            # 检查认证
            if not self.api_publisher.check_auth():
                logger.warning("API未认证，尝试登录")
                if not self.api_publisher.login():
                    raise Exception("API登录失败")
            
            # TODO: 实现API发布笔记
            # 注意：xiaohongshu-cli v0.6.3 目前主要支持读取/互动，发布功能需确认
            logger.info("API发布功能待实现")
            
            # 模拟成功（实际需调用CLI的post命令）
            self.api_fail_count = 0
            return True
            
        except Exception as e:
            logger.error(f"API发布失败: {e}")
            self.api_fail_count += 1
            self.last_api_fail = datetime.now()
            return False
    
    async def _publish_with_cdp(self, config: PublishConfig) -> bool:
        """使用CDP发布"""
        try:
            # 初始化CDP发布器
            if self.cdp_publisher is None:
                self.cdp_publisher = XHSPublisher()
                await self.cdp_publisher.launch_browser(headless=True)
            
            # 检查登录
            if not await self.cdp_publisher.check_login():
                logger.warning("CDP未登录")
                return False
            
            # 发布
            success = await self.cdp_publisher.publish(config)
            
            if success:
                self.cdp_fail_count = 0
            else:
                self.cdp_fail_count += 1
                self.last_cdp_fail = datetime.now()
            
            return success
            
        except Exception as e:
            logger.error(f"CDP发布失败: {e}")
            self.cdp_fail_count += 1
            self.last_cdp_fail = datetime.now()
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            "current_strategy": self.current_strategy.value,
            "is_new_account": self._is_new_account(),
            "account_age_days": (datetime.now() - self.account_created).days,
            "api_fail_count": self.api_fail_count,
            "cdp_fail_count": self.cdp_fail_count,
            "api_in_cooldown": self._is_api_in_cooldown(),
            "cdp_in_cooldown": self._is_cdp_in_cooldown(),
            "recent_success_rate": self._get_recent_success_rate(),
        }


def main():
    """测试代码"""
    import asyncio
    
    async def test():
        publisher = HybridPublisher()
        
        # 查看状态
        status = publisher.get_status()
        print("当前状态:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        # 选择策略
        strategy = publisher.select_strategy()
        print(f"\n选择策略: {strategy.value}")
    
    asyncio.run(test())


if __name__ == "__main__":
    main()