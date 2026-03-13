# 小红书登录指南

## 问题原因

小红财出现 `HTTP 400: InternalError.Algo.InvalidParameter` 错误，**实际原因是未登录**，不是内容长度问题。

## 解决方案

### 方法一：二维码登录（推荐）

```bash
# 运行二维码登录
xhs login --qr

# 按照提示：
# 1. 终端会显示二维码
# 2. 用小红书 App 扫码
# 3. 确认登录
# 4. Cookie 会自动保存
```

### 方法二：浏览器 Cookie 登录

```bash
# 1. 先在浏览器中登录小红书
#    - 打开 Chrome/Firefox
#    - 访问 https://www.xiaohongshu.com/
#    - 扫码或密码登录

# 2. 然后运行
xhs login --cookie-source chrome
# 或
xhs login --cookie-source firefox
```

### 方法三：手动设置 Cookie

```bash
# 1. 在浏览器中登录小红书
# 2. F12 打开开发者工具
# 3. Network 标签页
# 4. 刷新页面，找到任意请求
# 5. 复制 Cookie 中的 a1 值

# 6. 创建 Cookie 文件
mkdir -p ~/.config/xhs-cli
echo 'xiaohongshu.com\tTRUE\t/\tTRUE\t0\ta1\tYOUR_A1_COOKIE_VALUE' > ~/.config/xhs-cli/cookies.txt
```

## 验证登录

```bash
# 检查登录状态
xhs status

# 应该显示：
# ok: true
# user_id: xxx
# nickname: xxx
```

## 测试发布

```bash
# 测试发布（使用测试图片）
cd ~/.openclaw/workspace/xiaohongshu-matrix
xhs post --title "测试标题" --body "测试内容" --images content-gen/card_1.png
```

## 自动发布配置

登录成功后，修改 `auto_post.py` 确保使用正确的登录状态：

```python
# 在发布前检查登录状态
import subprocess
result = subprocess.run(['xhs', 'status'], capture_output=True, text=True)
if 'ok: false' in result.stdout:
    print("❌ 未登录，请先运行: xhs login --qr")
    return False
```

## 常见问题

### Q: 登录后还是报错？
**A**: Cookie 可能过期，需要重新登录。小红书 Cookie 有效期通常为几天到几周。

### Q: 二维码不显示？
**A**: 尝试使用 `--cookie-source` 方式登录。

### Q: 浏览器登录后提取失败？
**A**: 确保浏览器完全关闭后再运行命令，或者尝试其他浏览器。

---

**重要**: 登录成功后，小红财的自动发布功能应该正常工作！
