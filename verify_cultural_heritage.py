#!/usr/bin/env python
"""
文化遗产管理功能快速验证脚本
"""

import requests
import json

BASE_URL = "http://localhost:8090/api/v1/cultural-heritage"

def test_api():
    """测试API是否正常工作"""
    
    print("=" * 60)
    print("文化遗产管理功能验证")
    print("=" * 60)
    
    # 测试1: 全量查询
    print("\n【测试1】全量查询文化遗产")
    try:
        response = requests.get(f"{BASE_URL}/list", params={"page": 1, "page_size": 10})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功 - 共查询到 {result['total']} 条数据")
            print(f"   返回 {len(result['data'])} 条记录")
        else:
            print(f"❌ 失败 - 状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
    
    # 测试2: 查询非遗数据
    print("\n【测试2】查询所有非遗数据")
    try:
        response = requests.get(f"{BASE_URL}/list", params={"tag": "非遗"})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功 - 查询到 {result['total']} 条非遗数据")
            for item in result['data']:
                print(f"   - {item['file_name']} ({item['file_type']})")
        else:
            print(f"❌ 失败 - 状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
    
    # 测试3: 查询视频类型
    print("\n【测试3】查询所有视频资料")
    try:
        response = requests.get(f"{BASE_URL}/list", params={"file_type": "视频"})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功 - 查询到 {result['total']} 条视频数据")
            for item in result['data']:
                print(f"   - {item['file_name']} (标签: {item['tag']})")
        else:
            print(f"❌ 失败 - 状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
    
    # 测试4: 模糊查询
    print("\n【测试4】模糊查询包含'土楼'的文件")
    try:
        response = requests.get(f"{BASE_URL}/list", params={"file_name": "土楼"})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功 - 查询到 {result['total']} 条数据")
            for item in result['data']:
                print(f"   - {item['file_name']}")
        else:
            print(f"❌ 失败 - 状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
    
    # 测试5: 组合查询
    print("\n【测试5】组合查询（视频+非遗）")
    try:
        response = requests.get(f"{BASE_URL}/list", params={"file_type": "视频", "tag": "非遗"})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功 - 查询到 {result['total']} 条非遗视频数据")
            for item in result['data']:
                print(f"   - {item['file_name']}")
        else:
            print(f"❌ 失败 - 状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
    
    # 测试6: 查询详情
    print("\n【测试6】查询文件详情")
    try:
        response = requests.get(f"{BASE_URL}/CH_WJ_001")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功 - 查询到文件详情")
            print(f"   文件名: {result['file_name']}")
            print(f"   类型: {result['file_type']}")
            print(f"   标签: {result['tag']}")
            print(f"   URL: {result['url']}")
        else:
            print(f"❌ 失败 - 状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
    
    print("\n" + "=" * 60)
    print("验证完成")
    print("=" * 60)

if __name__ == "__main__":
    test_api()
