#!/bin/bash
# 闲鱼自动化运营套件启动脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
LOGS_DIR="$SCRIPT_DIR/logs"

echo "🦞 闲鱼自动化运营套件"
echo "======================"
echo ""

# 显示菜单
show_menu() {
    echo "请选择功能:"
    echo "1) 生成商品内容 (xianyu_content)"
    echo "2) 批量擦亮商品 (xianyu_manage)"
    echo "3) 数据分析 (xianyu_metrics)"
    echo "4) 批量发布商品 (xianyu_publish)"
    echo "5) 完整工作流程"
    echo "6) 退出"
    echo ""
}

# 生成内容
run_content() {
    echo "📝 生成商品内容..."
    python3 "$SCRIPT_DIR/scripts/xianyu_content.py" \
        --brand "Apple" \
        --model "iPhone 14 Pro" \
        --condition "99新" \
        --price 5800 \
        --reason "升级15了，这台14Pro出掉" \
        --output "$DATA_DIR/generated_content.json"
    echo "✅ 内容生成完成"
    echo ""
}

# 擦亮商品
run_manage() {
    echo "✨ 批量擦亮商品..."
    python3 "$SCRIPT_DIR/scripts/xianyu_manage.py" \
        --config "$SCRIPT_DIR/config/config.json" \
        --items "$DATA_DIR/sample_items.json" \
        --dry-run
    echo "✅ 擦亮操作完成"
    echo ""
}

# 数据分析
run_metrics() {
    echo "📊 数据分析..."
    python3 "$SCRIPT_DIR/scripts/xianyu_metrics.py" \
        --items "$DATA_DIR/sample_items.json" \
        --full-report \
        --export-csv \
        --output "$DATA_DIR/metrics_report.json"
    echo "✅ 分析报告已生成"
    echo ""
}

# 发布商品
run_publish() {
    echo "🚀 批量发布商品..."
    python3 "$SCRIPT_DIR/scripts/xianyu_publish.py" \
        --items "$DATA_DIR/sample_items.json" \
        --dry-run \
        --max-per-hour 5
    echo "✅ 发布操作完成"
    echo ""
}

# 完整工作流程
run_full_workflow() {
    echo "🔄 执行完整工作流程..."
    echo ""
    
    echo "步骤1/4: 生成内容..."
    run_content
    
    echo "步骤2/4: 数据分析..."
    run_metrics
    
    echo "步骤3/4: 擦亮商品..."
    run_manage
    
    echo "步骤4/4: 发布商品..."
    run_publish
    
    echo ""
    echo "✨ 完整工作流程执行完毕!"
}

# 主循环
while true; do
    show_menu
    read -p "请输入选项 [1-6]: " choice
    
    case $choice in
        1)
            run_content
            ;;
        2)
            run_manage
            ;;
        3)
            run_metrics
            ;;
        4)
            run_publish
            ;;
        5)
            run_full_workflow
            ;;
        6)
            echo "👋 再见!"
            exit 0
            ;;
        *)
            echo "❌ 无效选项，请重新选择"
            ;;
    esac
    
    echo ""
    read -p "按回车键继续..."
    clear
done
