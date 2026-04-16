import pytest
import requests
from helpers import register_new_courier_and_return_login_password


@pytest.fixture
def new_courier():
    """Создаёт нового уникального курьера для тестов"""
    courier = register_new_courier_and_return_login_password()
    assert courier, "Не удалось создать курьера для теста"
    yield courier


@pytest.fixture
def authorized_courier(new_courier):
    """Авторизует курьера и возвращает его данные + id"""
    login, password, _ = new_courier
    response = requests.post(
        "https://qa-scooter.praktikum-services.ru/api/v1/courier/login",
        json={"login": login, "password": password}
    )
    assert response.status_code == 200, f"Авторизация не удалась. Статус: {response.status_code}"
    return {"id": response.json()["id"], "login": login, "password": password}
