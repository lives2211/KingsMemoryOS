"""
交易所 API 配置模板
用户需要填写自己的 API Key
"""

import os
from typing import Dict

# 交易所配置模板
EXCHANGE_CONFIGS = {
    'binance': {
        'apiKey': os.getenv('BINANCE_API_KEY', 'YOUR_API_KEY_HERE'),
        'secret': os.getenv('BINANCE_SECRET', 'YOUR_SECRET_HERE'),
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',  # spot, future, margin
        }
    },
    'okx': {
        'apiKey': os.getenv('OKX_API_KEY', 'YOUR_API_KEY_HERE'),
        'secret': os.getenv('OKX_SECRET', 'YOUR_SECRET_HERE'),
        'password': os.getenv('OKX_PASSWORD', 'YOUR_PASSWORD_HERE'),
        'enableRateLimit': True,
    },
    'bybit': {
        'apiKey': os.getenv('BYBIT_API_KEY', 'YOUR_API_KEY_HERE'),
        'secret': os.getenv('BYBIT_SECRET', 'YOUR_SECRET_HERE'),
        'enableRateLimit': True,
    }
}

def get_exchange_config(exchange: str) -> Dict:
    """获取交易所配置"""
    return EXCHANGE_CONFIGS.get(exchange, {})

def validate_config(exchange: str) -> bool:
    """验证配置是否有效"""
    config = get_exchange_config(exchange)
    api_key = config.get('apiKey', '')
    
    if not api_key or 'YOUR_' in api_key:
        print(f"❌ {exchange} API Key 未配置")
        return False
    
    print(f"✅ {exchange} 配置有效")
    return True

# 使用说明
USAGE = """
交易所 API 配置说明
==================

1. 设置环境变量 (推荐):
   export BINANCE_API_KEY="your_api_key"
   export BINANCE_SECRET="your_secret"
   export OKX_API_KEY="your_api_key"
   export OKX_SECRET="your_secret"
   export OKX_PASSWORD="your_password"

2. 或修改本文件:
   将 'YOUR_API_KEY_HERE' 替换为真实 API Key

3. 获取 API Key:
   - Binance: https://www.binance.com/en/my/settings/api-management
   - OKX: https://www.okx.com/account/my-api
   - Bybit: https://www.bybit.com/user/settings/api

4. 安全提醒:
   - 永远不要提交 API Key 到 Git
   - 使用 IP 白名单
   - 只开启必要的权限 (读取 + 交易)
   - 使用测试网先验证

5. 测试网:
   - Binance: https://testnet.binance.vision/
   - OKX: 模拟交易模式
"""

if __name__ == "__main__":
    print(USAGE)
    print("\n验证配置:")
    for exchange in EXCHANGE_CONFIGS.keys():
        validate_config(exchange)
