#!/bin/bash
# 自动发布两个账号的内容

set -euo pipefail

echo "🚀 自动发布两个账号"
echo "===================="
echo ""

BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"
cd "$BASE_DIR"

# 发布数码虾
echo "📱 发布数码虾内容..."
echo "--------------------"

export XHS_COOKIE=$(grep "^XHS_COOKIE=" .env.tech-geek | sed 's/XHS_COOKIE=//' | head -1)

if [ -z "$XHS_COOKIE" ]; then
    echo "❌ 数码虾Cookie未配置"
else
    echo "✅ 数码虾Cookie已加载"
    
    # 使用填充脚本
    echo "📝 填充数码虾内容..."
    
    # 创建发布命令
    cat > /tmp/publish_tech.sh << 'EOF'
#!/bin/bash
cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix/xiaohongshu-skills
python3 scripts/publish_pipeline.py \
    --title "实测30天，这3个AI工具让我效率提升10倍" \
    --content-file ../generated/tech-geek/ai_tech_viral_2026.md \
    --preview \
    --headless
EOF
    chmod +x /tmp/publish_tech.sh
    
    echo "💡 数码虾内容已准备"
    echo "   标题: 实测30天，这3个AI工具让我效率提升10倍"
    echo "   文件: generated/tech-geek/ai_tech_viral_2026.md"
    echo ""
fi

# 发布职场虾
echo "📱 发布职场虾内容..."
echo "--------------------"

export XHS_COOKIE=$(grep "^XHS_COOKIE=" .env.career-growth | sed 's/XHS_COOKIE=//' | head -1)

if [ -z "$XHS_COOKIE" ]; then
    echo "❌ 职场虾Cookie未配置"
else
    echo "✅ 职场虾Cookie已加载"
    
    # 创建发布命令
    cat > /tmp/publish_career.sh << 'EOF'
#!/bin/bash
cd /home/fengxueda/.openclaw/workspace/xiaohongshu-matrix/xiaohongshu-skills
python3 scripts/publish_pipeline.py \
    --title "工作3年，AI让我从月薪8k到年薪50万" \
    --content-file ../generated/career-growth/ai_career_viral_2026.md \
    --preview \
    --headless
EOF
    chmod +x /tmp/publish_career.sh
    
    echo "💡 职场虾内容已准备"
    echo "   标题: 工作3年，AI让我从月薪8k到年薪50万"
    echo "   文件: generated/career-growth/ai_career_viral_2026.md"
    echo ""
fi

echo "===================="
echo "✅ 内容准备完成！"
echo ""
echo "📋 发布命令:"
echo ""
echo "数码虾:"
echo "   /tmp/publish_tech.sh"
echo ""
echo "职场虾:"
echo "   /tmp/publish_career.sh"
echo ""
echo "💡 注意: 需要Chrome浏览器已启动并登录"
echo ""
echo "或者手动复制内容到小红书发布:"
echo "   1. 打开小红书创作者中心"
echo "   2. 复制标题和正文"
echo "   3. 上传图片"
echo "   4. 点击发布"
echo ""
