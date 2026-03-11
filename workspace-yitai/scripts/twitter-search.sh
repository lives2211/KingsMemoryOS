#!/bin/bash
# Twitter/X 搜索脚本 - 使用Nitter RSS（无需API）

QUERY="$1"
LIMIT="${2:-10}"

# Nitter镜像列表（自动选择可用的）
NITTER_HOSTS=(
    "nitter.privacydev.net"
    "nitter.net"
    "nitter.it"
)

search_twitter() {
    local query="$1"
    local limit="$2"
    
    # URL编码查询词
    encoded_query=$(echo "$query" | sed 's/ /%20/g')
    
    for host in "${NITTER_HOSTS[@]}"; do
        echo "尝试: $host..." >&2
        
        # 获取RSS feed
        rss_url="https://${host}/search?f=tweets&q=${encoded_query}&e-nativeretweets=on&e-replies=on"
        
        # 使用curl获取并解析
        result=$(curl -s --max-time 10 "$rss_url" 2>/dev/null | \
            grep -oP '(?<=<title>)[^<]+' | \
            tail -n +2 | \
            head -n "$limit")
        
        if [ -n "$result" ]; then
            echo "✅ 成功从 $host 获取结果" >&2
            echo "$result"
            return 0
        fi
    done
    
    echo "❌ 所有Nitter镜像都不可用" >&2
    return 1
}

# 执行搜索
if [ -z "$QUERY" ]; then
    echo "用法: $0 <搜索关键词> [结果数量]"
    echo "示例: $0 'Bitcoin' 5"
    exit 1
fi

echo "🔍 搜索Twitter: $QUERY (前$LIMIT条)"
echo "---"
search_twitter "$QUERY" "$LIMIT"