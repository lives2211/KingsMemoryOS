#!/bin/bash
# 增强版小红书矩阵运营系统安装脚本

set -euo pipefail

echo "🦞 小红书矩阵运营系统 - 增强版安装"
echo "===================================="
echo ""

# 基础安装
echo "📦 步骤1: 基础环境安装..."
if [ -f "install.sh" ]; then
    ./install.sh
else
    echo "❌ 基础安装脚本不存在"
    exit 1
fi

echo ""
echo "📦 步骤2: 安装辅助工具..."

# 安装union-search依赖
echo "   - 安装统一搜索工具..."
cd union-search
pip3 install requests python-dotenv lxml -q 2>/dev/null || true

# 复制环境变量模板
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "   ✅ 创建union-search配置模板"
fi

cd ..

# 安装aitu依赖（可选）
echo "   - 安装AI绘图工具..."
if [ -d "aitu" ]; then
    cd aitu
    if command -v npm &> /dev/null; then
        echo "   正在安装Node依赖（可能需要几分钟）..."
        npm install --silent 2>/dev/null || echo "   ⚠️ npm install 失败，可手动运行"
    else
        echo "   ⚠️ 未安装Node.js，aitu功能不可用"
    fi
    cd ..
fi

echo ""
echo "📦 步骤3: 配置辅助工具..."

# 创建union-search配置文件
cat > union_search_config.json << 'EOF'
{
  "enabled_platforms": [
    "xiaohongshu",
    "douyin",
    "bilibili",
    "weibo"
  ],
  "search_limit": 10,
  "cache_enabled": true,
  "cache_duration": 3600
}
EOF

echo "   ✅ 创建union-search配置"

# 创建aitu启动脚本
cat > start_aitu.sh << 'EOF'
#!/bin/bash
cd aitu
npm start
EOF
chmod +x start_aitu.sh

echo "   ✅ 创建aitu启动脚本"

echo ""
echo "===================================="
echo "✅ 增强版安装完成！"
echo ""
echo "新增功能:"
echo "  🔍 统一搜索 - 支持30+平台内容研究"
echo "  📊 爆款分析 - 自动分析热门内容模式"
echo "  🎨 AI绘图 - 生成创意封面和素材"
echo "  🧠 智能优化 - 基于研究数据优化内容"
echo ""
echo "使用方式:"
echo "  1. 基础发布: python3 auto_post.py --once"
echo "  2. 增强生成: python3 enhanced_content_generator.py"
echo "  3. 启动aitu: ./start_aitu.sh (访问 http://localhost:7200)"
echo "  4. 工具状态: python3 assistant_tools.py"
echo ""
echo "配置说明:"
echo "  - union-search: 编辑 union-search/.env 添加API密钥"
echo "  - aitu: 访问 http://localhost:7200 使用Web界面"
echo ""
echo "🦞 矩阵运营，现在开始！"
