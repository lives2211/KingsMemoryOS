#!/usr/bin/env python3
"""
Discord Webhook 配置工具
"""

import os
import sys
from pathlib import Path


def create_webhook_guide():
    """创建 Webhook 配置指南"""
    guide = """
╔══════════════════════════════════════════════════════════════════╗
║           Discord Webhook 配置指南                               ║
╚══════════════════════════════════════════════════════════════════╝

步骤 1: 在 Discord 中创建 Webhook
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 打开 Discord，进入你的服务器
2. 选择你想接收推送的频道
3. 点击频道名称右侧的 ⚙️ 设置图标（齿轮）
4. 选择「集成」→「Webhooks」
5. 点击「新建 Webhook」按钮
6. 设置：
   • 名称：Twitter新闻推送（或其他你喜欢的名字）
   • 频道：选择目标频道
7. 点击「复制 Webhook URL」

步骤 2: 获取 Webhook URL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Webhook URL 格式如下：
https://discord.com/api/webhooks/1234567890123456789/abcdefghijklmnopqrstuvwxyz

                 ↑ Webhook ID          ↑ Webhook Token

步骤 3: 配置到系统
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

将复制的 URL 粘贴到下面的输入框：
"""
    print(guide)


def save_webhook_config(webhook_url: str):
    """保存 Webhook 配置"""
    config_file = Path(__file__).parent / ".env.discord"
    
    config_content = f"""# Discord Webhook 配置
# 生成时间: {__import__('datetime').datetime.now().isoformat()}

DISCORD_WEBHOOK_URL={webhook_url}
DISCORD_CHANNEL_NAME=twitter-news
MAX_TWEETS_PER_MESSAGE=5
ENABLE_THREADING=true
"""
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    # 设置权限
    os.chmod(config_file, 0o600)
    
    return config_file


def test_webhook(webhook_url: str):
    """测试 Webhook"""
    import requests
    
    test_message = {
        "content": "🤖 **Twitter 新闻推送机器人已配置成功！**\n\n"
                   "✅ Webhook 连接正常\n"
                   "⏰ 每小时自动推送最新推文\n"
                   "📊 包含完整链接和详细内容\n\n"
                   "_配置时间: {}_".format(__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    }
    
    try:
        response = requests.post(webhook_url, json=test_message, timeout=10)
        if response.status_code == 204:
            return True, "测试消息发送成功！"
        else:
            return False, f"HTTP 错误: {response.status_code}"
    except Exception as e:
        return False, str(e)


def main():
    """主函数"""
    create_webhook_guide()
    
    webhook_url = input("请输入 Webhook URL: ").strip()
    
    if not webhook_url:
        print("❌ 错误: Webhook URL 不能为空")
        sys.exit(1)
    
    if not webhook_url.startswith("https://discord.com/api/webhooks/"):
        print("⚠️ 警告: URL 格式可能不正确，但将继续配置")
    
    print("\n💾 正在保存配置...")
    config_file = save_webhook_config(webhook_url)
    print(f"✅ 配置已保存到: {config_file}")
    
    print("\n🧪 正在测试 Webhook...")
    success, message = test_webhook(webhook_url)
    
    if success:
        print(f"✅ {message}")
        print("\n🎉 配置完成！现在可以运行新闻推送了：")
        print("   python3 twitter_news_full.py --once --max 5")
    else:
        print(f"❌ 测试失败: {message}")
        print("\n可能的原因：")
        print("  • Webhook URL 复制不完整")
        print("  • Webhook 已被删除")
        print("  • 网络连接问题")
        print("\n请检查 URL 后重试，或手动编辑 .env.discord 文件")


if __name__ == "__main__":
    main()
