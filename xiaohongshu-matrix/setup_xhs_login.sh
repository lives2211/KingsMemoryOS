#!/bin/bash
# 小红书自动登录配置脚本

echo "=== 小红书登录配置 ==="
echo ""
echo "步骤 1: 在浏览器中登录小红书"
echo "  1. 打开 Chrome/Firefox/Edge"
echo "  2. 访问 https://www.xiaohongshu.com/"
echo "  3. 扫码或密码登录"
echo ""

# 检测已安装的浏览器
BROWSERS=""
for browser in chrome chromium firefox edge; do
    if which $browser &>/dev/null || which google-$browser &>/dev/null; then
        BROWSERS="$BROWSERS $browser"
    fi
done

echo "检测到的浏览器: $BROWSERS"
echo ""

# 尝试自动登录
echo "步骤 2: 尝试自动提取 Cookie..."

for browser in chrome chromium firefox edge; do
    echo "尝试从 $browser 提取 Cookie..."
    xhs login --cookie-source $browser 2>&1 && {
        echo "✅ 登录成功！"
        exit 0
    } || echo "❌ $browser 失败"
done

echo ""
echo "自动登录失败，请手动操作："
echo "  1. 确保浏览器已登录小红书"
echo "  2. 运行: xhs login --cookie-source <浏览器名称>"
echo ""
echo "或者使用二维码登录："
echo "  xhs login --qr"
