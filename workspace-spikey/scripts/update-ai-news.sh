#!/bin/bash
# AI News Aggregator 自动更新脚本

cd /tmp/ai-news-aggregator

# 运行数据抓取
echo "[$(date)] 开始抓取AI资讯..."
pnpm fetch

# 检查是否成功
if [ -f "data/latest-24h.json" ]; then
    echo "[$(date)] 抓取成功，共 $(cat data/latest-24h.json | grep -o '"total_items":[0-9]*' | cut -d: -f2) 条资讯"
    
    # 复制到workspace供Dwight读取
    cp data/latest-24h.json /media/fengxueda/D/openclaw-data/workspace/workspace-spikey/intel/ai-news-24h.json
    echo "[$(date)] 已同步到情报目录"
else
    echo "[$(date)] 抓取失败"
fi