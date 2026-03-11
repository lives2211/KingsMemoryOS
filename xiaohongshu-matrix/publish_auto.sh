#!/bin/bash
# 全自动发布脚本

set -euo pipefail

echo "🚀 小红书全自动发布"
echo "===================="
echo ""

# 检查参数
if [ $# -lt 1 ]; then
    echo "用法: ./publish_auto.sh <账号> [选项]"
    echo ""
    echo "选项:"
    echo "  --setup          配置账号Cookie"
    echo "  --file <路径>    从markdown文件发布"
    echo ""
    echo "示例:"
    echo "  ./publish_auto.sh tech-geek --setup"
    echo "  ./publish_auto.sh tech-geek --file generated/tech-geek/high_quality/xxx.md"
    exit 1
fi

ACCOUNT=$1
shift

BASE_DIR="/home/fengxueda/.openclaw/workspace/xiaohongshu-matrix"

cd "$BASE_DIR"

# 检查是否有参数
if [ $# -eq 0 ]; then
    # 默认：查找最新内容自动发布
    echo "🔍 查找最新内容..."

    CONTENT_DIR="$BASE_DIR/generated/$ACCOUNT/high_quality"
    if [ ! -d "$CONTENT_DIR" ]; then
        echo "❌ 内容目录不存在"
        exit 1
    fi

    # 获取最新的markdown文件
    LATEST_MD=$(ls -t "$CONTENT_DIR"/*.md 2>/dev/null | head -1)
    if [ -z "$LATEST_MD" ]; then
        echo "❌ 未找到内容文件"
        exit 1
    fi

    echo "📄 发布文件: $(basename $LATEST_MD)"
    echo ""

    # 发布
    python3 auto_publish_v2.py "$ACCOUNT" --file "$LATEST_MD"

    echo ""
    echo "===================="
    if [ $? -eq 0 ]; then
        echo "✅ 发布完成！"
    else
        echo "❌ 发布失败"
    fi
    exit 0
fi

# 配置模式
if [ "$1" == "--setup" ]; then
    echo "🔧 配置账号: $ACCOUNT"
    
    # 加载Cookie
    ENV_FILE="$BASE_DIR/.env.$ACCOUNT"
    if [ ! -f "$ENV_FILE" ]; then
        echo "❌ 配置文件不存在: $ENV_FILE"
        exit 1
    fi
    
    export XHS_COOKIE=$(grep "^XHS_COOKIE=" "$ENV_FILE" | sed 's/XHS_COOKIE=//')
    
    if [ -z "$XHS_COOKIE" ]; then
        echo "❌ Cookie未配置"
        exit 1
    fi
    
    echo "✅ Cookie已加载"
    
    # 配置到XiaohongshuSkills
    python3 auto_publish_v2.py "$ACCOUNT" --setup
    
    echo ""
    echo "✅ 账号配置完成"
    exit 0
fi

# 发布模式
if [ "$1" == "--file" ] && [ -n "$2" ]; then
    FILE="$2"
    echo "📄 从文件发布: $(basename $FILE)"
    
    python3 auto_publish_v2.py "$ACCOUNT" --file "$FILE"
    exit $?
fi

# 默认：查找最新内容自动发布
echo "🔍 查找最新内容..."

CONTENT_DIR="$BASE_DIR/generated/$ACCOUNT/high_quality"
if [ ! -d "$CONTENT_DIR" ]; then
    echo "❌ 内容目录不存在"
    exit 1
fi

# 获取最新的markdown文件
LATEST_MD=$(ls -t "$CONTENT_DIR"/*.md 2>/dev/null | head -1)
if [ -z "$LATEST_MD" ]; then
    echo "❌ 未找到内容文件"
    exit 1
fi

echo "📄 发布文件: $(basename $LATEST_MD)"
echo ""

# 发布
python3 auto_publish_v2.py "$ACCOUNT" --file "$LATEST_MD"

echo ""
echo "===================="
if [ $? -eq 0 ]; then
    echo "✅ 发布完成！"
else
    echo "❌ 发布失败"
fi
