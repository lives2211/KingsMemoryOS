#!/bin/bash
# 小红书矩阵运营系统启动脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

show_help() {
    echo "🦞 小红书矩阵运营系统"
    echo "====================="
    echo ""
    echo "用法: ./start.sh [命令]"
    echo ""
    echo "命令:"
    echo "  init          初始化系统（首次运行）"
    echo "  status        查看系统状态"
    echo "  schedule      生成今日发布计划"
    echo "  test          测试生成一篇内容"
    echo "  post          执行一次发布"
    echo "  daemon        启动守护进程（自动发布）"
    echo "  research      研究热门话题"
    echo "  aitu          启动AI绘图服务"
    echo "  report        查看数据报告"
    echo "  cron          设置定时任务"
    echo "  help          显示帮助"
    echo ""
}

cmd_init() {
    echo "🦞 初始化小红书矩阵运营系统..."
    echo ""
    
    # 检查目录
    echo "📁 检查目录结构..."
    mkdir -p generated/{tech-geek,life-aesthetics,career-growth,foodie,fashion}
    mkdir -p personas
    mkdir -p logs
    mkdir -p research
    echo "✅ 目录检查完成"
    
    # 初始化账号配置
    echo ""
    echo "⚙️ 初始化账号配置..."
    python3 auto_post.py --init 2>/dev/null || true
    
    # 创建空的cookie文件（模板）
    for account in tech-geek life-aesthetics career-growth foodie fashion; do
        env_file=".env.$account"
        if [ ! -f "$env_file" ]; then
            cat > "$env_file" << EOF
# 账号: $account
# 获取方式: 浏览器登录小红书 → F12 → Network → 任意请求的 Cookie
XHS_COOKIE=
EOF
        fi
    done
    echo "✅ 账号配置模板已创建"
    
    # 检查工具状态
    echo ""
    echo "🔧 检查辅助工具..."
    python3 assistant_tools.py
    
    echo ""
    echo "====================="
    echo "✅ 初始化完成！"
    echo ""
    echo "下一步:"
    echo "1. 配置Cookie: 编辑 .env.* 文件"
    echo "2. 生成计划: ./start.sh schedule"
    echo "3. 测试发布: ./start.sh test"
    echo "4. 启动守护: ./start.sh daemon"
}

cmd_status() {
    echo "🦞 系统状态"
    echo "=========="
    echo ""
    
    # 检查核心组件
    echo "核心组件:"
    [ -d "content-gen" ] && echo "  ✅ content-gen (内容生成)" || echo "  ❌ content-gen"
    [ -d "ops-skill" ] && echo "  ✅ ops-skill (运营互动)" || echo "  ❌ ops-skill"
    [ -d "union-search" ] && echo "  ✅ union-search (统一搜索)" || echo "  ❌ union-search"
    [ -d "aitu" ] && echo "  ✅ aitu (AI绘图)" || echo "  ❌ aitu"
    
    echo ""
    echo "配置文件:"
    for account in tech-geek life-aesthetics career-growth foodie fashion; do
        env_file=".env.$account"
        if [ -f "$env_file" ]; then
            if grep -q "XHS_COOKIE=.*[^[:space:]]" "$env_file" 2>/dev/null; then
                echo "  ✅ $account (已配置)"
            else
                echo "  ⚠️  $account (未配置Cookie)"
            fi
        else
            echo "  ❌ $account (文件不存在)"
        fi
    done
    
    echo ""
    echo "今日计划:"
    if [ -f "schedule.json" ]; then
        python3 -c "
import json
from datetime import datetime
try:
    with open('schedule.json') as f:
        data = json.load(f)
    today = datetime.now().date().isoformat()
    if today in data:
        posts = data[today]
        pending = len([p for p in posts if p['status'] == 'pending'])
        posted = len([p for p in posts if p['status'] == 'posted'])
        print(f'  总计: {len(posts)} 篇')
        print(f'  待发布: {pending} 篇')
        print(f'  已发布: {posted} 篇')
    else:
        print('  暂无今日计划')
except Exception as e:
    print(f'  读取失败: {e}')
"
    else
        echo "  暂无计划文件"
    fi
    
    echo ""
    echo "辅助工具:"
    python3 assistant_tools.py 2>/dev/null || echo "  辅助工具未就绪"
}

cmd_schedule() {
    echo "🦞 生成今日发布计划..."
    python3 scheduler.py
}

cmd_test() {
    echo "🦞 测试内容生成..."
    echo ""
    
    # 随机选择一个账号
    accounts=("tech-geek" "life-aesthetics" "career-growth" "foodie" "fashion")
    account=${accounts[$RANDOM % 5]}
    
    echo "测试账号: $account"
    echo ""
    
    # 生成内容
    python3 -c "
from content_generator import ContentGenerator
gen = ContentGenerator()
result = gen.generate_post('$account')
print(f'标题: {result[\"title\"]}')
print(f'渲染: {\"✅\" if result[\"rendered\"] else \"❌\"}')
print(f'')
print('内容预览:')
print(result['content'][:300] + '...')
"
}

cmd_post() {
    echo "🦞 执行一次发布..."
    python3 auto_post.py --once
}

cmd_daemon() {
    echo "🦞 启动守护进程..."
    echo "按 Ctrl+C 停止"
    echo ""
    python3 auto_post.py --daemon
}

cmd_research() {
    echo "🦞 研究热门话题..."
    echo ""
    
    # 研究各账号领域
    topics=(
        "tech-geek:手机评测"
        "life-aesthetics:家居布置"
        "career-growth:职场干货"
        "foodie:美食探店"
        "fashion:穿搭分享"
    )
    
    for item in "${topics[@]}"; do
        IFS=':' read -r account topic <<< "$item"
        echo "---"
        echo "研究: $account ($topic)"
        python3 -c "
from enhanced_content_generator import EnhancedContentGenerator
gen = EnhancedContentGenerator()
try:
    result = gen.research_and_generate('$account', '$topic')
    print(f'标题: {result[\"title\"][:50]}...')
    print(f'爆款模式: {result[\"viral_patterns\"]}')
except Exception as e:
    print(f'研究失败: {e}')
"
        echo ""
    done
}

cmd_aitu() {
    echo "🦞 启动AI绘图服务..."
    echo "访问: http://localhost:7200"
    echo ""
    
    if [ -d "aitu" ]; then
        cd aitu
        if [ -d "node_modules" ]; then
            npm start
        else
            echo "⚠️ 请先安装依赖: cd aitu && npm install"
        fi
    else
        echo "❌ aitu目录不存在"
    fi
}

cmd_report() {
    echo "🦞 生成数据报告..."
    python3 analytics.py --report
}

cmd_cron() {
    echo "🦞 设置定时任务..."
    python3 setup_cron.py
    echo ""
    echo "要安装定时任务，请运行:"
    echo "  crontab cron.txt"
}

# 主逻辑
case "${1:-help}" in
    init)
        cmd_init
        ;;
    status)
        cmd_status
        ;;
    schedule)
        cmd_schedule
        ;;
    test)
        cmd_test
        ;;
    post)
        cmd_post
        ;;
    daemon)
        cmd_daemon
        ;;
    research)
        cmd_research
        ;;
    aitu)
        cmd_aitu
        ;;
    report)
        cmd_report
        ;;
    cron)
        cmd_cron
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
