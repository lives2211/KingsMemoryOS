#!/usr/bin/env python3
"""
调试小红书发布流程
"""

import json
import sys
sys.path.insert(0, '/media/fengxueda/D/openclaw-data/workspace/xiaohongshu-matrix/xiaohongshu-cli')

# 只测试数据构造，不导入客户端

# 测试数据
title = "测试标题"
desc = "测试正文内容"
image_file_ids = ["test_image_id_12345"]

try:
    # 尝试创建数据（不实际发送请求）
    print("=== 构造发布数据 ===")
    
    business_binds = {
        "version": 1,
        "noteId": 0,
        "noteOrderBind": {},
        "notePostTiming": {"postTime": None},
        "noteCollectionBind": {"id": ""},
    }
    
    images = [{"file_id": fid, "metadata": {"source": -1}} for fid in image_file_ids]
    
    data = {
        "common": {
            "type": "normal",
            "title": title,
            "note_id": "",
            "desc": desc,
            "source": '{"type":"web","ids":"","extraInfo":"{\\"subType\\":\\"official\\"}"}',
            "business_binds": json.dumps(business_binds),
            "ats": [],
            "hash_tag": [],
            "post_loc": {},
            "privacy_info": {"op_type": 1, "type": 0},
        },
        "image_info": {"images": images},
        "video_info": None,
    }
    
    json_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    
    print(f"数据大小: {len(json_str)} bytes")
    print(f"数据内容:\n{json_str[:1000]}...")
    
    print("\n=== 检查各字段 ===")
    print(f"title 长度: {len(title)} 字符, {len(title.encode('utf-8'))} bytes")
    print(f"desc 长度: {len(desc)} 字符, {len(desc.encode('utf-8'))} bytes")
    print(f"source 长度: {len(data['common']['source'])} 字符")
    print(f"business_binds 长度: {len(data['common']['business_binds'])} 字符")
    
    print("\n✅ 数据构造成功")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
