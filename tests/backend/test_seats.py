import requests
import pytest
from datetime import datetime

# 测试数据
TEST_SEAT = {
    "seat_number": "A1",
    "room_id": 1,
    "is_available": 1,
}

def test_get_all_seats():
    # 测试获取所有座位
    response = requests.get("http://localhost:3001/api/seats/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_available_seats():
    # 测试获取可用座位
    response = requests.get("http://localhost:3001/api/seats/available?date=2024-03-20")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all(seat["is_available"] for seat in response.json())
    
    # 测试带时间段的可用座位查询
    response = requests.get("http://localhost:3001/api/seats/available?date=2024-03-20&timeSlotId=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_seat_by_id():
    # 测试获取存在的座位
    response = requests.get("http://localhost:3001/api/seats/1")
    assert response.status_code == 200
    assert response.json()["id"] == "1"
    
    # 测试获取不存在的座位
    response = requests.get("http://localhost:3001/api/seats/999")
    assert response.status_code == 404

def test_create_seat():
    # 测试创建新座位
    response = requests.post("http://localhost:3001/api/seats/", json=TEST_SEAT)
    assert response.status_code == 201
    assert response.json()["seat_number"] == TEST_SEAT["seat_number"]
    assert response.json()["room_id"] == TEST_SEAT["room_id"]
    
    # 测试创建重复座位号
    response = requests.post("http://localhost:3001/api/seats/", json=TEST_SEAT)
    assert response.status_code == 409
    
    # 测试创建不存在的房间的座位
    invalid_seat = TEST_SEAT.copy()
    invalid_seat["room_id"] = 999
    response = requests.post("http://localhost:3001/api/seats/", json=invalid_seat)
    assert response.status_code == 404

def test_update_seat():
    # 测试更新座位信息
    update_data = {
        "seat_number": "B1",
        "is_available": False
    }
    response = requests.put("http://localhost:3001/api/seats/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["seat_number"] == update_data["seat_number"]
    assert response.json()["is_available"] == update_data["is_available"]
    
    # 测试更新不存在的座位
    response = requests.put("http://localhost:3001/api/seats/999", json=update_data)
    assert response.status_code == 404

def test_delete_seat():
    # 测试删除存在的座位
    response = requests.delete("http://localhost:3001/api/seats/1")
    assert response.status_code == 200
    
    # 测试删除不存在的座位
    response = requests.delete("http://localhost:3001/api/seats/999")
    assert response.status_code == 404

def test_seat_validation():
    # 测试空座位号
    invalid_seat = TEST_SEAT.copy()
    invalid_seat["seat_number"] = ""
    response = requests.post("http://localhost:3001/api/seats/", json=invalid_seat)
    assert response.status_code == 400
    
    # 测试无效的房间ID
    invalid_seat = TEST_SEAT.copy()
    invalid_seat["room_id"] = -1
    response = requests.post("http://localhost:3001/api/seats/", json=invalid_seat)
    assert response.status_code == 400

def test_seat_availability():
    # 测试座位可用性状态更新
    status_data = {"is_available": 0}
    response = requests.put("http://localhost:3001/api/seats/1/availability", json=status_data)
    assert response.status_code == 200
    assert response.json()["is_available"] == 0
    
    # 测试重新设置座位为可用
    status_data = {"is_available": 1}
    response = requests.put("http://localhost:3001/api/seats/1/availability", json=status_data)
    assert response.status_code == 200
    assert response.json()["is_available"] == 1
