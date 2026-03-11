#!/bin/bash
# 小红书矩阵运营系统安装脚本

set -euo pipefail

echo "🦞 小红书矩阵运营系统安装"
echo "=========================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要安装 Python3"
    exit 1
fi

echo "✅ Python3 已安装"

# 安装依赖
echo ""
echo "📦 安装依赖..."

# content-gen依赖
cd content-gen
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install markdown PyYAML playwright xhs==0.2.13 --break-system-packages

# 安装Playwright浏览器
python3 -m playwright install chromium

cd ..

echo "✅ 依赖安装完成"

# 创建目录
echo ""
echo "📁 创建目录结构..."
mkdir -p generated/{tech-geek,life-aesthetics,career-growth,foodie,fashion}
mkdir -p personas
mkdir -p logs

echo "✅ 目录创建完成"

# 初始化账号配置
echo ""
echo "⚙️ 初始化账号配置..."
python3 auto_post.py --init

echo ""
echo "=========================="
echo "✅ 安装完成！"
echo ""
echo "下一步:"
echo "1. 配置小红书Cookie:"
echo "   - 编辑 .env.* 文件，填入各账号的Cookie"
echo "   - 获取方式: 浏览器登录小红书 → F12 → Network → 复制Cookie"
echo ""
echo "2. 生成今日发布计划:"
echo "   python3 scheduler.py"
echo ""
echo "3. 启动自动发布(测试模式):"
echo "   python3 auto_post.py --once"
echo ""
echo "4. 启动守护进程:"
echo "   python3 auto_post.py --daemon"
echo ""
echo "🦞 祝运营顺利！"
