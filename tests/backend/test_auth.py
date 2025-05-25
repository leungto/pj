import requests
import pytest

def test_login_success():
    response = requests.post("http://localhost:3001/api/auth/login", json={"email": "user@example.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert response.json()["message"] == "success"
    assert response.json()["data"]["token"] is not None
    assert response.json()["data"]["user"] is not None

def test_login_wrong_password():
    response = requests.post("http://localhost:3001/api/auth/login", json={"email": "user@example.com", "password": "wrong_password"})
    assert response.status_code == 401
    assert response.json()["code"] == 401
    assert "密码错误" in response.json()["message"]

def test_login_nonexistent_user():
    response = requests.post("http://localhost:3001/api/auth/login", json={"email": "nonexistent@example.com", "password": "any_password"})
    assert response.status_code == 404
    assert response.json()["code"] == 404
    assert "用户不存在" in response.json()["message"]

def test_login_banned_user():
    # 首先创建一个被封禁的用户
    register_response = requests.post("http://localhost:3001/api/auth/register", json={
        "name": "banned_user",
        "email": "banned@example.com",
        "password": "password123",
        "confirmPassword": "password123"
    })
    assert register_response.status_code == 200
    
    # 更新用户状态为封禁
    user_id = register_response.json()["data"]["user"]["id"]
    update_response = requests.put(f"http://localhost:3001/api/users/{user_id}", json={
        "is_active": False
    })
    assert update_response.status_code == 200
    
    # 尝试登录被封禁的账号
    login_response = requests.post("http://localhost:3001/api/auth/login", json={
        "email": "banned@example.com",
        "password": "password123"
    })
    assert login_response.status_code == 403
    assert login_response.json()["code"] == 403
    assert "账号已被封禁" in login_response.json()["message"]

def test_login_empty_credentials():
    # 测试空邮箱
    response = requests.post("http://localhost:3001/api/auth/login", json={"email": "", "password": "any_password"})
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert "邮箱不能为空" in response.json()["message"]
    
    # 测试空密码
    response = requests.post("http://localhost:3001/api/auth/login", json={"email": "test@example.com", "password": ""})
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert "密码不能为空" in response.json()["message"]
    
    # 测试空邮箱和空密码
    response = requests.post("http://localhost:3001/api/auth/login", json={"email": "", "password": ""})
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert "邮箱和密码不能为空" in response.json()["message"]
