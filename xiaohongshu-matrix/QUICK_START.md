# 🚀 小红书矩阵运营系统 - 快速上手指南

## 5分钟快速启动

### 第1步: 验证系统 (1分钟)
```bash
cd xiaohongshu-matrix
python3 verify.py
```

预期输出:
```
✅ 系统验证通过！所有组件就绪。
```

### 第2步: 配置Cookie (2分钟)

获取Cookie:
1. 浏览器打开小红书并登录
2. 按F12打开开发者工具
3. 切换到Network标签
4. 刷新页面，点击任意请求
5. 找到Request Headers中的Cookie
6. 复制整串Cookie

配置账号:
```bash
# 编辑第一个账号
nano .env.tech-geek
```

粘贴内容:
```
# 账号: tech-geek
XHS_COOKIE=你的Cookie字符串
```

重复以上步骤配置其他4个账号。

### 第3步: 生成计划 (1分钟)
```bash
./start.sh schedule
```

预期输出:
```
今日共计划发布 21 篇笔记:
[07:30] 职场虾 (career-growth)
[08:26] 数码虾 (tech-geek)
...
```

### 第4步: 测试发布 (1分钟)
```bash
./start.sh test
```

预期输出:
```
测试账号: tech-geek
标题: 先说结论：iPhone值得买吗？
渲染: ✅
```

## 启动运营

### 方式A: 手动模式
```bash
# 执行一次发布
./start.sh post

# 或启动守护进程
./start.sh daemon
```

### 方式B: 自动模式 (推荐)
```bash
# 设置定时任务
./start.sh cron

# 安装定时任务
crontab cron.txt

# 验证定时任务
crontab -l
```

定时任务会自动:
- 每天6:00生成新计划
- 每10分钟检查并发布
- 每天23:00生成报告
- 每周日备份数据

## 日常管理

### 查看状态
```bash
./start.sh status
```

### 查看报告
```bash
./start.sh report
```

### 研究热点
```bash
./start.sh research
```

### 导出数据
```bash
python3 analytics.py --export
```

## 常见问题

### Q: 发布失败怎么办?
**A:** Cookie可能过期，重新获取并更新.env文件

### Q: 如何暂停发布?
**A:** 
```bash
# 停止守护进程
Ctrl+C

# 或删除定时任务
crontab -r
```

### Q: 如何修改发布频率?
**A:** 编辑scheduler.py中的daily_posts参数

### Q: 如何更换账号定位?
**A:** 编辑personas/目录下的对应.md文件

### Q: 图片渲染失败?
**A:** 
```bash
# 重新安装Playwright
python3 -m playwright install chromium
```

## 监控面板

### 实时查看
```bash
# 查看今日计划
./start.sh schedule

# 查看系统状态
./start.sh status

# 查看数据报告
./start.sh report
```

### 日志监控
```bash
# 实时查看发布日志
tail -f logs/auto_post.log

# 查看调度日志
tail -f logs/scheduler.log

# 查看所有日志
ls -lh logs/
```

## 高级功能

### 爆款复刻
```bash
# 输入爆款笔记链接
python3 ops-skill/scripts/clone_viral.py <url>
```

### 自动回复
```bash
# 检查并回复评论
python3 ops-skill/scripts/auto_reply.py
```

### AI绘图
```bash
# 启动aitu服务
./start.sh aitu

# 访问 http://localhost:7200
```

### 多平台搜索
```bash
# 搜索小红书
python3 union-search/union_search_cli.py xiaohongshu "关键词"

# 搜索抖音
python3 union-search/union_search_cli.py douyin "关键词"

# 搜索B站
python3 union-search/union_search_cli.py bilibili "关键词"
```

## 性能优化

### 减少发布频率
编辑scheduler.py:
```python
"daily_posts": (2, 3)  # 改为每天2-3篇
```

### 调整发布时间
编辑scheduler.py中的posting_window:
```python
"posting_window": [
    (9, 0, 10, 0),   # 上午9-10点
    (14, 0, 15, 0),  # 下午2-3点
    (20, 0, 21, 0)   # 晚上8-9点
]
```

### 关闭辅助工具
如果不需要搜索和AI绘图功能，可以删除:
```bash
rm -rf union-search aitu
```

## 安全建议

1. **Cookie安全**
   - 不要提交到Git仓库
   - 定期更换(建议每月)
   - 使用专用小号测试

2. **发布频率**
   - 新号先养1-2周
   - 从每天1-2篇开始
   - 逐步增加到3-5篇

3. **内容审核**
   - 定期人工检查内容
   - 避免敏感话题
   - 保持账号人设一致性

4. **风控策略**
   - 错峰发布
   - 避免短时间内高频发布
   - 模拟真人操作习惯

## 故障排查

### 系统验证失败
```bash
# 重新初始化
./start.sh init

# 再次验证
python3 verify.py
```

### Python依赖缺失
```bash
pip3 install playwright markdown pyyaml requests lxml --break-system-packages
```

### Playwright浏览器问题
```bash
# 卸载重装
python3 -m playwright uninstall
python3 -m playwright install chromium
```

### 定时任务不执行
```bash
# 检查cron服务
sudo service cron status

# 查看系统日志
grep CRON /var/log/syslog | tail -20
```

## 升级更新

### 更新代码
```bash
# 进入项目目录
cd xiaohongshu-matrix

# 拉取最新代码
git pull

# 或重新克隆
cd ..
rm -rf xiaohongshu-matrix
git clone <仓库地址>
```

### 更新依赖
```bash
# Python依赖
pip3 install --upgrade playwright markdown pyyaml requests lxml --break-system-packages

# Node依赖
cd aitu && npm update
```

## 联系支持

### 相关仓库
- Auto-Redbook-Skills: https://github.com/comeonzhj/Auto-Redbook-Skills
- xiaohongshu-ops-skill: https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill
- union-search-skill: https://github.com/runningZ1/union-search-skill
- aitu: https://github.com/ljquan/aitu

### 查看文档
```bash
# 系统概览
cat SYSTEM_OVERVIEW.md

# 部署完成文档
cat DEPLOY_COMPLETE.md

# 快速上手指南
cat QUICK_START.md
```

---

🦞 **祝你运营顺利，早日成为小红书大V！**
