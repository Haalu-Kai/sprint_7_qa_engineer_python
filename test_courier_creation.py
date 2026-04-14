import requests
import pytest
from helpers import register_new_courier_and_return_login_password
from data import BASE_URL


def test_create_courier_success(new_courier):
    """Курьера можно создать"""
    assert new_courier, "Курьер не был создан"


def test_cannot_create_duplicate_courier():
    """Нельзя создать двух одинаковых курьеров"""
    courier = register_new_courier_and_return_login_password()
    assert courier

    payload = {
        "login": courier[0],
        "password": courier[1],
        "firstName": courier[2]
    }

    response = requests.post(f"{BASE_URL}/courier", json=payload)
    assert response.status_code == 409
    assert "уже используется" in response.json().get("message", "")


@pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
def test_create_courier_missing_field(missing_field):
    """Если одного из обязательных полей нет — ошибка"""
    payload = {
        "login": "testlogin",
        "password": "testpass",
        "firstName": "Test"
    }
    del payload[missing_field]

    response = requests.post(f"{BASE_URL}/courier", json=payload)
    assert response.status_code == 400
    assert "Недостаточно данных" in response.json().get("message", "")


def test_create_courier_returns_ok_true():
    """Успешный запрос возвращает {"ok": true}"""
    courier = register_new_courier_and_return_login_password()
    payload = {
        "login": courier[0] + "extra",   
        "password": courier[1],
        "firstName": courier[2]
    }
    response = requests.post(f"{BASE_URL}/courier", json=payload)
    assert response.status_code == 201
    assert response.json() == {"ok": True}
