# Auto Dispatch Tool

## 描述
自动识别 Discord 消息中的任务请求，并调用 Paperclip 派发

## 触发
- channel: discord
- channel_id: 1480388799589515446
- event: message

## 执行
当收到消息时：
1. 检查是否包含任务关键词
2. 解析预算和能力
3. 调用 paperclip_client.py 派发
4. 回复派发结果

## 用法
在总指挥频道直接输入任务描述

## 示例
输入: "帮我爬取数据，预算10美元"
输出: "🤖 任务已派发 → @yitai"
