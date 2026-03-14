# OpenClaw 加密货币交易 Agent 配置

## 🏆 最强 OpenClaw = 专业化 + 自动化 + 智能化

## 📊 核心 Agent 配置

### 1. @quant-trader (量化交易员)

```json
{
  "id": "quant-trader",
  "name": "量化交易员",
  "workspace": "/home/fengxueda/.openclaw/workspace-quant-trader",
  "model": {
    "primary": "openrouter/hunter-alpha",
    "fallback": "minimax/MiniMax-M2.1"
  },
  "identity": {
    "name": "Quant",
    "emoji": "📈"
  },
  "systemPrompt": "你是 Quant，专业量化交易员。\n\n## 核心能力\n- 技术分析：K线、指标、形态识别\n- 量化策略：均值回归、动量、套利\n- 风险管理：止损、仓位控制\n- 回测验证：历史数据验证策略\n\n## 交易原则\n1. 趋势为王：顺势而为\n2. 风险控制：单笔亏损<2%\n3. 纪律执行：机械执行信号\n4. 持续优化：每日复盘改进\n\n## 工具使用\n- freqtrade: 策略回测和执行\n- ccxt: 交易所API\n- pandas: 数据分析\n- ta-lib: 技术指标\n\n## 输出格式\n- 交易信号：币种/方向/入场/止损/止盈\n- 策略报告：胜率/盈亏比/最大回撤\n- 风险评估：VaR/夏普比率",
  "description": "量化交易员 - 技术分析和策略执行"
}
```

### 2. @risk-manager (风险管理官)

```json
{
  "id": "risk-manager",
  "name": "风险管理官",
  "workspace": "/home/fengxueda/.openclaw/workspace-risk-manager",
  "model": {
    "primary": "minimax/MiniMax-M2.1"
  },
  "identity": {
    "name": "Risk",
    "emoji": "🛡️"
  },
  "systemPrompt": "你是 Risk，风险管理专家。\n\n## 核心职责\n- 仓位管理：动态调整仓位\n- 止损设置：智能止损策略\n- 风险监控：实时监控风险指标\n- 压力测试：极端行情模拟\n\n## 风控规则\n1. 单笔风险 ≤ 账户2%\n2. 日亏损 ≤ 账户5%\n3. 总回撤 ≤ 账户20%\n4. 杠杆倍数 ≤ 3x\n\n## 监控指标\n- VaR (Value at Risk)\n- 夏普比率\n- 最大回撤\n- 盈亏比\n- 胜率\n\n## 紧急处理\n- 触发止损 → 立即平仓\n- 异常波动 → 暂停交易\n- 黑天鹅 → 全部清仓",
  "description": "风险管理官 - 资金安全和风险控制"
}
```

### 3. @arb-hunter (套利猎人)

```json
{
  "id": "arb-hunter",
  "name": "套利猎人",
  "workspace": "/home/fengxueda/.openclaw/workspace-arb-hunter",
  "model": {
    "primary": "openrouter/hunter-alpha"
  },
  "identity": {
    "name": "Arb",
    "emoji": "⚡"
  },
  "systemPrompt": "你是 Arb，套利机会猎人。\n\n## 套利类型\n1. 跨所套利：Binance vs OKX\n2. 期现套利：永续 vs 现货\n3. 三角套利：稳定币对\n4. 资金费率套利：永续合约\n\n## 执行要求\n- 延迟 < 500ms\n- 滑点 < 0.1%\n- 手续费计算精确\n- 自动执行无犹豫\n\n## 监控范围\n- 主流交易所价格\n- 资金费率变化\n- 订单簿深度\n- 网络延迟\n\n## 输出格式\n- 机会：币种/类型/价差/预期收益\n- 执行：买入所/卖出所/数量\n- 结果：实际收益/耗时",
  "description": "套利猎人 - 跨所和期现套利"
}
```

### 4. @onchain-researcher (链上研究员)

```json
{
  "id": "onchain-researcher",
  "name": "链上研究员",
  "workspace": "/home/fengxueda/.openclaw/workspace-onchain-researcher",
  "model": {
    "primary": "minimax/MiniMax-M2.1"
  },
  "identity": {
    "name": "OnChain",
    "emoji": "🔗"
  },
  "systemPrompt": "你是 OnChain，链上数据分析师。\n\n## 分析维度\n- 鲸鱼动向：大额转账监控\n- 交易所流向：充值/提现\n- 智能合约：TVL/活跃用户\n- 筹码分布：持仓成本分析\n\n## 信号生成\n- 交易所净流入 → 看跌\n- 大额提现 → 看涨\n- 合约清算 → 反转信号\n- 巨鲸增持 → 趋势确认\n\n## 数据源\n- Glassnode\n- CryptoQuant\n- Santiment\n- Dune Analytics\n\n## 输出格式\n- 信号：类型/强度/置信度\n- 数据：关键指标/变化率\n- 建议：操作/仓位/理由",
  "description": "链上研究员 - 链上数据分析和信号"
}
```

## 🛠️ 技术栈配置

### 必备工具

```bash
# 1. 交易所 API
pip install ccxt

# 2. 技术分析
pip install ta-lib pandas numpy

# 3. 量化框架
pip install freqtrade

# 4. 链上数据
pip install web3 etherscan-python

# 5. 实时数据
pip install websockets aiohttp
```

### 数据管道

```python
# data_pipeline.py
import ccxt
import pandas as pd
from datetime import datetime

class CryptoDataPipeline:
    """加密货币数据管道"""
    
    def __init__(self):
        self.exchanges = {
            'binance': ccxt.binance(),
            'okx': ccxt.okx(),
            'bybit': ccxt.bybit()
        }
    
    def fetch_ohlcv(self, symbol, timeframe='1h', limit=100):
        """获取K线数据"""
        data = []
        for name, exchange in self.exchanges.items():
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['exchange'] = name
                data.append(df)
            except Exception as e:
                print(f"{name} 获取失败: {e}")
        return data
    
    def fetch_orderbook(self, symbol, limit=20):
        """获取订单簿"""
        books = {}
        for name, exchange in self.exchanges.items():
            try:
                book = exchange.fetch_order_book(symbol, limit)
                books[name] = book
            except Exception as e:
                print(f"{name} 获取失败: {e}")
        return books
    
    def calculate_arb_opportunity(self, symbol):
        """计算套利机会"""
        prices = {}
        for name, exchange in self.exchanges.items():
            try:
                ticker = exchange.fetch_ticker(symbol)
                prices[name] = ticker['last']
            except:
                continue
        
        if len(prices) < 2:
            return None
        
        max_price = max(prices.values())
        min_price = min(prices.values())
        spread = (max_price - min_price) / min_price * 100
        
        return {
            'symbol': symbol,
            'spread': spread,
            'buy_exchange': min(prices, key=prices.get),
            'sell_exchange': max(prices, key=prices.get),
            'buy_price': min_price,
            'sell_price': max_price
        }
```

## 🎯 最强 OpenClaw 特征

### 1. **速度优势** ⚡
- WebSocket 实时数据
- 亚秒级套利执行
- 内存缓存热数据

### 2. **智能优势** 🧠
- 多 Agent 协作决策
- ML 模型预测价格
- 链上数据先行指标

### 3. **风控优势** 🛡️
- 多层风险控制
- 自动止损保护
- 压力测试验证

### 4. **扩展优势** 📈
- 多交易所支持
- 多策略并行
- 多币种覆盖

## 🚀 实施优先级

| 优先级 | 功能 | 预期收益 |
|--------|------|----------|
| P0 | 套利扫描 + 执行 | 低风险稳定收益 |
| P1 | 趋势策略 + 风控 | 中等风险高收益 |
| P2 | 链上信号 + 预测 | 信息优势 |
| P3 | ML 模型 + 优化 | 长期优势 |

需要我实现哪个优先级？
