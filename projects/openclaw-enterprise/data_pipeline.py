"""
加密货币数据管道
实时市场数据获取和处理
"""

import ccxt
import asyncio
import websockets
import json
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MarketData:
    """市场数据结构"""
    symbol: str
    exchange: str
    timestamp: datetime
    price: float
    volume: float
    bid: float
    ask: float
    spread: float

class CryptoDataPipeline:
    """加密货币数据管道"""
    
    def __init__(self):
        self.exchanges = {}
        self.data_cache = {}
        self.ws_connections = {}
        
        # 初始化交易所
        self._init_exchanges()
    
    def _init_exchanges(self):
        """初始化交易所连接"""
        exchange_configs = {
            'binance': {
                'apiKey': '',  # 从环境变量读取
                'secret': '',
                'enableRateLimit': True,
            },
            'okx': {
                'apiKey': '',
                'secret': '',
                'enableRateLimit': True,
            }
        }
        
        for name, config in exchange_configs.items():
            try:
                exchange_class = getattr(ccxt, name)
                self.exchanges[name] = exchange_class(config)
                print(f"✅ {name} 初始化成功")
            except Exception as e:
                print(f"❌ {name} 初始化失败: {e}")
    
    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> pd.DataFrame:
        """获取K线数据"""
        data = []
        
        for name, exchange in self.exchanges.items():
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                df = pd.DataFrame(
                    ohlcv, 
                    columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
                )
                df['exchange'] = name
                df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
                data.append(df)
            except Exception as e:
                print(f"{name} 获取 {symbol} 失败: {e}")
        
        if data:
            return pd.concat(data, ignore_index=True)
        return pd.DataFrame()
    
    def fetch_orderbook(self, symbol: str, limit: int = 20) -> Dict:
        """获取订单簿"""
        books = {}
        
        for name, exchange in self.exchanges.items():
            try:
                book = exchange.fetch_order_book(symbol, limit)
                books[name] = {
                    'bids': book['bids'][:limit],
                    'asks': book['asks'][:limit],
                    'timestamp': book['timestamp']
                }
            except Exception as e:
                print(f"{name} 获取订单簿失败: {e}")
        
        return books
    
    def calculate_arbitrage(self, symbol: str) -> Optional[Dict]:
        """计算套利机会"""
        prices = {}
        
        for name, exchange in self.exchanges.items():
            try:
                ticker = exchange.fetch_ticker(symbol)
                prices[name] = {
                    'bid': ticker['bid'],
                    'ask': ticker['ask'],
                    'last': ticker['last']
                }
            except:
                continue
        
        if len(prices) < 2:
            return None
        
        # 计算价差
        best_bid = max(prices.items(), key=lambda x: x[1]['bid'])
        best_ask = min(prices.items(), key=lambda x: x[1]['ask'])
        
        spread = (best_bid[1]['bid'] - best_ask[1]['ask']) / best_ask[1]['ask'] * 100
        
        return {
            'symbol': symbol,
            'spread_percent': spread,
            'buy_exchange': best_ask[0],
            'sell_exchange': best_bid[0],
            'buy_price': best_ask[1]['ask'],
            'sell_price': best_bid[1]['bid'],
            'profit_per_unit': best_bid[1]['bid'] - best_ask[1]['ask'],
            'timestamp': datetime.now().isoformat()
        }
    
    async def websocket_ticker(self, exchange: str, symbols: List[str]):
        """WebSocket 实时 ticker"""
        # 这里实现 WebSocket 连接
        # 不同交易所的 WebSocket 地址不同
        ws_urls = {
            'binance': 'wss://stream.binance.com:9443/ws',
            'okx': 'wss://ws.okex.com:8443/ws/v5/public'
        }
        
        uri = ws_urls.get(exchange)
        if not uri:
            return
        
        try:
            async with websockets.connect(uri) as ws:
                # 订阅 ticker
                subscribe_msg = {
                    'method': 'SUBSCRIBE',
                    'params': [f'{s.lower()}@ticker' for s in symbols],
                    'id': 1
                }
                await ws.send(json.dumps(subscribe_msg))
                
                while True:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    # 处理数据
                    self._process_ws_data(exchange, data)
                    
        except Exception as e:
            print(f"WebSocket 错误: {e}")
    
    def _process_ws_data(self, exchange: str, data: Dict):
        """处理 WebSocket 数据"""
        # 存储到缓存
        symbol = data.get('s', '')
        if symbol:
            self.data_cache[f"{exchange}:{symbol}"] = {
                'data': data,
                'timestamp': datetime.now()
            }
    
    def get_cached_data(self, exchange: str, symbol: str) -> Optional[Dict]:
        """获取缓存数据"""
        key = f"{exchange}:{symbol}"
        return self.data_cache.get(key)


# 测试
if __name__ == "__main__":
    pipeline = CryptoDataPipeline()
    
    print("🧪 数据管道测试:")
    print('=' * 60)
    
    # 测试获取 K 线
    print("\n1. 获取 BTC/USDT K线数据:")
    df = pipeline.fetch_ohlcv('BTC/USDT', '1h', 10)
    if not df.empty:
        print(f"   ✅ 获取成功: {len(df)} 条数据")
        print(f"   交易所: {df['exchange'].unique()}")
        print(f"   最新价格: {df['close'].iloc[-1]}")
    
    # 测试套利计算
    print("\n2. 计算套利机会:")
    arb = pipeline.calculate_arbitrage('BTC/USDT')
    if arb:
        print(f"   ✅ 发现套利机会!")
        print(f"   价差: {arb['spread_percent']:.2f}%")
        print(f"   买入: {arb['buy_exchange']} @ {arb['buy_price']}")
        print(f"   卖出: {arb['sell_exchange']} @ {arb['sell_price']}")
    else:
        print("   ℹ️ 暂无套利机会")
    
    print('\n' + '=' * 60)
    print('✅ 数据管道测试完成')
