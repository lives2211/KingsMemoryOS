# Twitter MCP 配置指南

## 获取Twitter API凭证

1. 访问 https://developer.twitter.com/
2. 创建App，获取以下凭证：
   - API Key
   - API Secret Key
   - Access Token
   - Access Token Secret

## 配置方式

### 方式A: 环境变量（推荐）

```bash
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

添加到 `~/.bashrc` 或 `~/.zshrc` 使其永久生效。

### 方式B: OpenClaw配置文件

编辑 `~/.openclaw/openclaw.json`，添加mcp部分：

```json
{
  "mcp": {
    "servers": [
      {
        "name": "twitter",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-twitter"],
        "env": {
          "TWITTER_API_KEY": "your_api_key",
          "TWITTER_API_SECRET": "your_api_secret",
          "TWITTER_ACCESS_TOKEN": "your_access_token",
          "TWITTER_ACCESS_TOKEN_SECRET": "your_access_token_secret"
        }
      }
    ]
  }
}
```

### 方式C: 使用 inference.sh Twitter工具

如果已有 inference.sh 账号：

```bash
infsh auth login
infsh tools use twitter
```

## 验证配置

配置完成后，测试推文发送：

```bash
# 使用 MCP 工具
echo '{"text": "Test tweet from AI Agent team 🤖"}' | openclaw mcp call twitter post_tweet
```

## 注意事项

1. Twitter API有速率限制（免费版通常15分钟/条）
2. 确保API密钥有写权限（Write permission）
3. 建议先测试再接入自动化流程