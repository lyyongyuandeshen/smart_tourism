"""
景点导览接口测试脚本
使用前请确保：
1. 数据库已创建相关表
2. 已配置环境变量
3. 应用已启动
"""

import requests
import json
from datetime import date, timedelta

# API基础URL
BASE_URL = "http://localhost:8090/api/v1/scenic"


def test_create_scenic_guide():
    """测试创建景点导览"""
    print("\n=== 测试创建景点导览 ===")
    
    guide_data = {
        "scenic_id": "scenic-test-001",
        "guide_title": "测试景点导览",
        "historical_background": "这是一个测试景点的历史背景介绍...",
        "cultural_value": "这是文化价值介绍...",
        "architectural_features": "这是建筑特色介绍...",
        "historical_stories": "这是历史故事...",
        "ecological_science": "这是生态科普...",
        "open_status": 1,
        "last_bus_time": "17:30",
        "evacuation_route_url": "https://example.com/evacuation/test.pdf"
    }
    
    url = f"{BASE_URL}/guides"
    response = requests.post(url, json=guide_data)
    
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(guide_data, indent=2, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.json()


def test_get_all_guides():
    """测试查询所有景点导览"""
    print("\n=== 测试查询所有景点导览 ===")
    
    url = f"{BASE_URL}/guides"
    response = requests.get(url)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.json()


def test_get_guide_by_scenic_id(scenic_id):
    """测试根据景点ID查询导览"""
    print(f"\n=== 测试根据景点ID查询导览 ===")
    
    url = f"{BASE_URL}/guides/scenic/{scenic_id}"
    response = requests.get(url)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.json()


def test_update_guide(guide_id):
    """测试更新景点导览"""
    print(f"\n=== 测试更新景点导览 ===")
    
    update_data = {
        "guide_title": "测试景点导览（已更新）",
        "open_status": 0,
        "last_bus_time": "18:00"
    }
    
    url = f"{BASE_URL}/guides/{guide_id}"
    response = requests.put(url, json=update_data)
    
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(update_data, indent=2, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.json()


def test_batch_create_time_slots(scenic_id):
    """测试批量创建时段"""
    print(f"\n=== 测试批量创建时段 ===")
    
    today = date.today()
    dates = [
        str(today + timedelta(days=1)),
        str(today + timedelta(days=2)),
        str(today + timedelta(days=3))
    ]
    
    batch_data = {
        "ticket_id": "ticket-test-001",
        "scenic_id": scenic_id,
        "reservation_dates": dates,
        "time_slots": [
            {"start_time": "09:00", "end_time": "11:00", "total_quota": 100},
            {"start_time": "11:00", "end_time": "13:00", "total_quota": 100},
            {"start_time": "14:00", "end_time": "16:00", "total_quota": 100},
            {"start_time": "16:00", "end_time": "18:00", "total_quota": 100}
        ]
    }
    
    url = f"{BASE_URL}/time-slots/batch"
    response = requests.post(url, json=batch_data)
    
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(batch_data, indent=2, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.json()


def test_get_time_slots(scenic_id):
    """测试查询景点时段"""
    print(f"\n=== 测试查询景点时段 ===")
    
    today = date.today()
    start_date = str(today + timedelta(days=1))
    end_date = str(today + timedelta(days=3))
    
    url = f"{BASE_URL}/time-slots/scenic/{scenic_id}?start_date={start_date}&end_date={end_date}"
    response = requests.get(url)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.json()


def test_update_time_slot(slot_id):
    """测试更新时段"""
    print(f"\n=== 测试更新时段 ===")
    
    update_data = {
        "total_quota": 150
    }
    
    url = f"{BASE_URL}/time-slots/{slot_id}"
    response = requests.put(url, json=update_data)
    
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(update_data, indent=2, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.json()


def test_delete_guide(guide_id):
    """测试删除景点导览"""
    print(f"\n=== 测试删除景点导览 ===")
    
    url = f"{BASE_URL}/guides/{guide_id}"
    response = requests.delete(url)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.json()


def main():
    """主测试函数"""
    print("开始测试景点导览接口...")
    
    try:
        # 1. 创建景点导览
        create_result = test_create_scenic_guide()
        if not create_result.get('success'):
            print("\n创建景点导览失败，停止测试")
            return
        
        guide_id = create_result['data']['id']
        scenic_id = "scenic-test-001"
        
        # 2. 查询所有景点导览
        test_get_all_guides()
        
        # 3. 根据景点ID查询导览
        test_get_guide_by_scenic_id(scenic_id)
        
        # 4. 更新景点导览
        test_update_guide(guide_id)
        
        # 5. 批量创建时段
        batch_result = test_batch_create_time_slots(scenic_id)
        
        # 6. 查询景点时段
        time_slots = test_get_time_slots(scenic_id)
        
        # 7. 如果有时段，测试更新时段
        if time_slots and len(time_slots) > 0:
            first_slot_id = time_slots[0]['id']
            test_update_time_slot(first_slot_id)
        
        # 8. 删除景点导览（清理测试数据）
        print("\n是否删除测试数据？(y/n): ", end='')
        choice = input().strip().lower()
        if choice == 'y':
            test_delete_guide(guide_id)
            print("\n测试数据已清理")
        else:
            print(f"\n测试数据保留，导览ID: {guide_id}")
            
    except requests.exceptions.ConnectionError:
        print("\n错误：无法连接到服务器，请确保应用已启动")
    except Exception as e:
        print(f"\n测试过程中出现错误: {str(e)}")


if __name__ == "__main__":
    main()
