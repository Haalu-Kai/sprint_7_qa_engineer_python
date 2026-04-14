import requests
import pytest
from data import BASE_URL


def test_courier_can_login(authorized_courier):
    """Курьер может авторизоваться"""
    assert authorized_courier["id"] > 0


@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_login_missing_field(missing_field, new_courier):
    """Для авторизации нужно передать все обязательные поля"""
    login, password, _ = new_courier
    payload = {"login": login, "password": password}
    del payload[missing_field]

    response = requests.post(f"{BASE_URL}/courier/login", json=payload)
    assert response.status_code == 400
    assert "Недостаточно данных" in response.json().get("message", "")


def test_login_wrong_password(new_courier):
    """Ошибка при неправильном пароле"""
    login, _, _ = new_courier
    response = requests.post(
        f"{BASE_URL}/courier/login",
        json={"login": login, "password": "wrongpassword123"}
    )
    assert response.status_code == 404
    assert "Учетная запись не найдена" in response.json().get("message", "")


def test_login_nonexistent_user():
    """Авторизация под несуществующим пользователем"""
    response = requests.post(
        f"{BASE_URL}/courier/login",
        json={"login": "nonexistentuser12345", "password": "123456"}
    )
    assert response.status_code == 404
    assert "Учетная запись не найдена" in response.json().get("message", "")


def test_login_success_returns_id(authorized_courier):
    """Успешный запрос возвращает id курьера"""
    assert "id" in authorized_courier
