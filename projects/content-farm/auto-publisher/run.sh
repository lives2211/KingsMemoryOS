#!/bin/bash
# 小红书自动发布系统 - 运行脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 帮助信息
show_help() {
    echo "小红书自动发布系统"
    echo ""
    echo "用法: ./run.sh [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  status      查看系统状态"
    echo "  preview     预览发布计划"
    echo "  login       扫码登录"
    echo "  publish     发布单篇笔记"
    echo "  batch       批量发布笔记"
    echo "  test        运行测试"
    echo "  help        显示帮助"
    echo ""
    echo "选项:"
    echo "  --date DATE     指定日期 (YYYY-MM-DD)"
    echo "  --limit N       最大发布数量 (默认: 3)"
    echo "  --headless      无头模式运行"
    echo "  --dry-run       仅预览，不实际发布"
    echo ""
    echo "示例:"
    echo "  ./run.sh status"
    echo "  ./run.sh login"
    echo "  ./run.sh batch --limit 2"
    echo "  ./run.sh batch --headless"
}

# 检查依赖
check_deps() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}错误: 未找到 python3${NC}"
        exit 1
    fi
    
    if ! python3 -c "import playwright" 2>/dev/null; then
        echo -e "${YELLOW}警告: 未安装 playwright，正在安装...${NC}"
        pip3 install -r requirements.txt
        playwright install chromium
    fi
}

# 主逻辑
case "${1:-help}" in
    status)
        check_deps
        python3 main.py status
        ;;
    
    preview)
        check_deps
        LIMIT="${2:-5}"
        python3 main.py preview --limit "$LIMIT"
        ;;
    
    login)
        check_deps
        echo -e "${YELLOW}请在小红书页面扫码登录...${NC}"
        python3 main.py login
        ;;
    
    publish)
        check_deps
        shift
        python3 main.py publish "$@"
        ;;
    
    batch)
        check_deps
        shift
        echo -e "${GREEN}开始批量发布...${NC}"
        python3 main.py batch "$@"
        ;;
    
    test)
        check_deps
        echo -e "${GREEN}运行测试...${NC}"
        
        echo -e "\n${YELLOW}1. 测试卡片生成${NC}"
        python3 test_card.py || echo -e "${RED}卡片测试失败${NC}"
        
        echo -e "\n${YELLOW}2. 测试内容加载${NC}"
        python3 test_content.py || echo -e "${RED}内容测试失败${NC}"
        
        echo -e "\n${YELLOW}3. 测试调度器${NC}"
        python3 test_scheduler.py || echo -e "${RED}调度器测试失败${NC}"
        
        echo -e "\n${GREEN}测试完成${NC}"
        ;;
    
    help|--help|-h)
        show_help
        ;;
    
    *)
        echo -e "${RED}未知命令: $1${NC}"
        show_help
        exit 1
        ;;
esac
