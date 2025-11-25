"""
票务接口测试脚本
使用前请确保：
1. 数据库已创建相关表
2. 已配置环境变量
3. 应用已启动
"""

import requests
import json
from datetime import date, timedelta

# API基础URL
BASE_URL = "http://localhost:8090/api/v1/tickets"


def test_get_time_slots():
    """测试查询余票接口"""
    print("\n=== 测试查询余票接口 ===")
    scenic_id = "scenic-001"
    
    url = f"{BASE_URL}/time-slots/{scenic_id}"
    response = requests.get(url)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.json()


def test_purchase_ticket():
    """测试购票接口"""
    print("\n=== 测试购票接口 ===")
    
    # 购票请求数据
    purchase_data = {
        "scenic_id": "scenic-001",
        "scenic_name": "黄山风景区",
        "time_slot_id": "slot-001",  # 需要先从查询接口获取真实的时段ID
        "ticket_type": 1,  # 成人票
        "ticket_quantity": 2,
        "ticket_price": 190.00,
        "sales_channel": 1,  # 官网
        "channel_name": "官网",
        "valid_start_date": str(date.today() + timedelta(days=1)),
        "valid_end_date": str(date.today() + timedelta(days=1))
    }
    
    url = f"{BASE_URL}/purchase"
    response = requests.post(url, json=purchase_data)
    
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(purchase_data, indent=2, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.json()


def main():
    """主测试函数"""
    print("开始测试票务接口...")
    
    try:
        # 1. 测试查询余票
        time_slots = test_get_time_slots()
        
        # 2. 如果有可用时段，测试购票
        if time_slots and len(time_slots) > 0:
            print("\n找到可用时段，准备测试购票...")
            # 使用第一个时段进行测试
            first_slot = time_slots[0]
            
            purchase_data = {
                "scenic_id": first_slot["scenic_id"],
                "scenic_name": "黄山风景区",
                "time_slot_id": first_slot["id"],
                "ticket_type": 1,
                "ticket_quantity": 2,
                "ticket_price": 190.00,
                "sales_channel": 1,
                "channel_name": "官网",
                "valid_start_date": str(first_slot["reservation_date"]),
                "valid_end_date": str(first_slot["reservation_date"])
            }
            
            url = f"{BASE_URL}/purchase"
            response = requests.post(url, json=purchase_data)
            
            print(f"\n请求URL: {url}")
            print(f"请求数据: {json.dumps(purchase_data, indent=2, ensure_ascii=False)}")
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print("\n没有找到可用时段，跳过购票测试")
            
    except requests.exceptions.ConnectionError:
        print("\n错误：无法连接到服务器，请确保应用已启动")
    except Exception as e:
        print(f"\n测试过程中出现错误: {str(e)}")


if __name__ == "__main__":
    main()
