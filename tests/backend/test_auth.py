import requests

def test_login_success():
    response = requests.post("http://localhost:3001/api/auth/login", json={"email": "zeocax@zeocax.com", "password": "zeocax"})
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert response.json()["message"] == "success"
    assert response.json()["data"]["token"] is not None
    assert response.json()["data"]["user"] is not None

# TODO(@backend): 你们写吧