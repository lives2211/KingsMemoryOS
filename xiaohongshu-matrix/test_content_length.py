#!/usr/bin/env python3
"""
测试小红书内容长度限制
"""

import json

# 模拟 xhs_cli 的数据结构
def create_test_data(title, desc, image_file_ids=None):
    """创建测试数据"""
    if image_file_ids is None:
        image_file_ids = ["test_image_id_12345"]
    
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
    
    return data


def check_data_size(title, desc):
    """检查数据大小"""
    data = create_test_data(title, desc)
    json_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    
    title_bytes = title.encode('utf-8')
    desc_bytes = desc.encode('utf-8')
    total_bytes = len(json_str)
    
    print(f"标题长度: {len(title)} 字符, {len(title_bytes)} bytes")
    print(f"正文长度: {len(desc)} 字符, {len(desc_bytes)} bytes")
    print(f"JSON 总长度: {total_bytes} bytes")
    print(f"限制: 260096 bytes")
    
    if total_bytes > 260096:
        print(f"⚠️  超过限制 {total_bytes - 260096} bytes")
        return False
    else:
        print(f"✅ 符合限制 (剩余 {260096 - total_bytes} bytes)")
        return True


if __name__ == "__main__":
    print("=== 测试 1: 正常长度 ===")
    check_data_size("测试标题", "测试正文内容")
    
    print("\n=== 测试 2: 长标题 ===")
    check_data_size("测试标题" * 100, "测试正文")
    
    print("\n=== 测试 3: 长正文 ===")
    check_data_size("测试标题", "测试正文" * 10000)
    
    print("\n=== 测试 4: 超长正文 (接近限制) ===")
    # 计算能容纳的最大正文长度
    base_title = "测试标题"
    base_data = create_test_data(base_title, "")
    base_json = json.dumps(base_data, separators=(",", ":"), ensure_ascii=False)
    base_size = len(base_json)
    
    max_desc_bytes = 260096 - base_size - 100  # 留 100 bytes 余量
    max_desc = "测" * (max_desc_bytes // 3)  # 中文约 3 bytes/字符
    
    print(f"基础数据大小: {base_size} bytes")
    print(f"最大正文长度: {max_desc_bytes} bytes, 约 {len(max_desc)} 个汉字")
    check_data_size(base_title, max_desc)
    
    print("\n=== 测试 5: 超过限制 ===")
    overflow_desc = max_desc + " overflow"
    check_data_size(base_title, overflow_desc)
