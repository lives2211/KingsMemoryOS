#!/usr/bin/env python3
"""
内容截断工具 - 防止 MiniMax 输入长度超限
"""
import sys

MAX_CHARS = 150000  # 安全阈值（MiniMax 限制 260096）

def truncate_content(content: str, max_chars: int = MAX_CHARS) -> str:
    """截断内容到安全长度"""
    if len(content) <= max_chars:
        return content
    
    # 保留开头和结尾，中间用省略号
    head_len = max_chars // 2
    tail_len = max_chars // 2 - 20
    
    truncated = content[:head_len] + "\n\n... [内容过长，已截断] ...\n\n" + content[-tail_len:]
    return truncated

def truncate_messages(messages: list, max_total: int = MAX_CHARS) -> list:
    """截断消息列表"""
    total_chars = sum(len(str(m)) for m in messages)
    
    if total_chars <= max_total:
        return messages
    
    # 保留最近的对话
    truncated = []
    current_chars = 0
    
    for msg in reversed(messages):
        msg_chars = len(str(msg))
        if current_chars + msg_chars > max_total and len(truncated) > 0:
            break
        truncated.insert(0, msg)
        current_chars += msg_chars
    
    return truncated

if __name__ == "__main__":
    # 测试
    test_content = "A" * 300000
    result = truncate_content(test_content)
    print(f"原始长度: {len(test_content)}")
    print(f"截断后: {len(result)}")
