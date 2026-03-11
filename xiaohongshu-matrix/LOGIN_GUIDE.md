# 🔐 小红书登录指南

## 首次登录流程

### 步骤1: 启动浏览器并扫码登录

```bash
cd xiaohongshu-matrix/xiaohongshu-skills

# 启动Chrome（有窗口模式，用于扫码）
python3 scripts/chrome_launcher.py

# 检查登录状态（会弹出二维码）
python3 scripts/cdp_publish.py check-login
```

**操作**:
1. 会弹出Chrome浏览器窗口
2. 显示小红书登录二维码
3. 用手机小红书APP扫码登录
4. 登录成功后，关闭浏览器

### 步骤2: 验证登录状态

```bash
# 再次检查登录状态
python3 scripts/cdp_publish.py check-login

# 如果显示"已登录"，说明成功
```

### 步骤3: 使用无头模式发布

登录成功后，就可以使用无头模式（后台运行）发布了：

```bash
cd xiaohongshu-matrix

# 发布数码虾内容
python3 publish_xhs.py tech-geek

# 发布职场虾内容
python3 publish_xhs.py career-growth
```

---

## 登录状态保持

- 登录状态会保存在Chrome配置文件中
- 默认保持12小时
- 超过12小时需要重新扫码

---

## 自动化流程

### 完整发布流程

```bash
# 1. 确保已登录（如果未登录会提示扫码）
cd xiaohongshu-matrix/xiaohongshu-skills
python3 scripts/cdp_publish.py check-login

# 2. 发布内容
cd ..
python3 publish_xhs.py tech-geek
```

### 定时自动发布

登录成功后，可以设置定时任务自动发布：

```bash
# 编辑定时任务
crontab -e

# 添加以下行（每2小时检查发布一次）
0 */2 * * * cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix && python3 publish_xhs.py tech-geek >> logs/publish.log 2>&1
```

---

## 常见问题

### Q: 二维码不显示？
**A**: 确保Chrome已安装，使用有窗口模式启动

### Q: 扫码后还是显示未登录？
**A**: 等待10秒再检查，或刷新页面

### Q: 登录状态能保持多久？
**A**: 默认12小时，可以修改配置延长

### Q: 如何退出登录？
**A**: 删除Chrome配置文件：
```bash
rm -rf ~/Google/Chrome/XiaohongshuProfiles/default
```

---

## 安全建议

1. **首次登录后，保持浏览器运行**
2. **定期检查登录状态**
3. **不要在公共环境保存登录状态**
4. **Cookie过期后及时更新**

---

## 下一步

1. ✅ 启动Chrome并扫码登录
2. ✅ 验证登录状态
3. ✅ 运行发布脚本
4. ✅ 设置定时任务（可选）

现在就可以开始扫码登录了！
