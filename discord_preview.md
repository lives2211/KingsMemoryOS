# Discord 推送效果预览

## 🔔 Twitter 新闻推送

⏰ **时间**: 2026-03-11 11:36  
📊 **数量**: 5 条推文  

---

### [1] 🐦 继 twitter-cli 和 tg-cli 之后，小红书 CLI 也来了！

🔗 **完整链接**: https://x.com/jakevin7/status/2031411127532343318

👤 **作者**: 卡比卡比 ✅ (@jakevin7)  
🕐 **时间**: Tue Mar 10 16:45:29 +0000 2026

**内容**:
继 twitter-cli 和 tg-cli 之后，小红书 CLI 也来了！

逆向了小红书 Web 端的接口，终端里就能搜笔记、看评论、点赞收藏、发帖子。 Cookie 自动提取，不需要配 API Key。

同样做了不少反风控：Chrome UA/指纹伪装、请求间隔随机化、Referrer 链路模拟等。

https://t.co/gEHsnRw16q

📊 **互动数据**: ❤️ 512 | 🔁 83 | 💬 24 | 👁️ 27222 | 🔖 648

🔗 **外部链接**: 
- [链接 1](https://github.com/jackwener/xiaohongshu-cli)

---

### [2] 🐦 如果把 OpenClaw 当作一位员工，那我们可以把它招进 Paperclip 这家公司。

🔗 **完整链接**: https://x.com/GitHub_Daily/status/2031520484261577173

👤 **作者**: GitHubDaily (@GitHub_Daily)  
🕐 **时间**: Wed Mar 11 00:00:01 +0000 2026

**内容**:
如果把 OpenClaw 当作一位员工，那我们可以把它招进 Paperclip 这家公司。

Paperclip 是一个专为 Agent 打造的开源 AI 公司，仅仅开源几天，暴涨了 15000+ Star！

我们可以把 OpenClaw、Claude、Cursor 各种 Agent 全部招入麾下，并借助 Paperclip 进行企业化管理。

核心亮点：
- 可接入任意...

📊 **互动数据**: ❤️ 87 | 🔁 12 | 💬 4 | 👁️ 9527 | 🔖 140

🖼️ **媒体** (1 个):
- [视频](https://video.twimg.com/amplify_video/2031383817341259776/vid/avc1/1280x800/lB9zKnTs5JJd5lqb.mp4?tag=21)

---

### [3] 🐦 如果你想给自己的 AI 小龙虾配备一个后端工程师，InsForge 就是最佳选择。

🔗 **完整链接**: https://x.com/Jimmy_JingLv/status/2031492830636683708

👤 **作者**: 吕立青_JimmyLv 2𐃏26 ✅ (@Jimmy_JingLv)  
🕐 **时间**: Tue Mar 10 22:10:08 +0000 2026

**内容**:
如果你想给自己的 AI 小龙虾配备一个后端工程师，InsForge 就是最佳选择。

OpenClaw 负责聊天和任务调度，但它不会建数据库、不会部署网站、不会管认证——直到遇见 InsForge。

InsForge 是开源的 AI-native Supabase 替代品，专为 AI 编码 Agent

📊 **互动数据**: ❤️ 86 | 🔁 11 | 💬 1 | 👁️ 5706 | 🔖 128

---

## 📋 推送格式说明

每条推文包含：

1. **🐦 标题** - 推文前100字符作为题目
2. **🔗 完整链接** - 点击可直接跳转到推文
3. **👤 作者信息** - 名称、用户名、认证状态
4. **🕐 发布时间** - 完整时间戳
5. **📝 完整内容** - 推文全文（最多2000字符）
6. **📊 互动数据** - 点赞、转发、回复、浏览、收藏
7. **🖼️ 媒体链接** - 图片/视频直链（如有）
8. **🔗 外部链接** - 推文中的 URL（如有）
9. **📎 引用推文** - 引用的原文（如有）

---

## 🎨 Discord Embed 样式

推送使用 Discord Embed 格式，包含：
- 蓝色边框（Twitter 品牌色）
- 作者头像
- 可点击的标题链接
- 结构化的字段布局
- 时间戳

---

## 🚀 配置步骤

1. **运行配置脚本**:
   ```bash
   ./setup_discord_and_run.sh
   ```

2. **输入 Webhook URL**:
   - 在 Discord 频道设置中创建 Webhook
   - 复制 Webhook URL
   - 粘贴到脚本中

3. **测试推送**:
   - 脚本会自动发送测试消息
   - 确认在 Discord 收到消息

4. **运行抓取**:
   - 脚本会自动抓取推文并推送
   - 或手动运行: `python3 twitter_news_full.py --once --max 10`

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `setup_discord_and_run.sh` | 一键配置脚本 |
| `discord_webhook_setup.py` | Python 配置工具 |
| `twitter_discord_pusher.py` | Discord 推送器 |
| `.env.discord` | 配置文件 |
| `twitter_news_full.py` | 主程序 |
