import pytest
import requests
from helpers import register_new_courier_and_return_login_password


@pytest.fixture
def new_courier():
    """Создаёт нового курьера для тестов"""
    courier = register_new_courier_and_return_login_password()
    assert courier, "Не удалось создать курьера"
    yield courier


@pytest.fixture
def authorized_courier(new_courier):
    """Авторизует курьера и возвращает его id + данные"""
    login, password, _ = new_courier
    response = requests.post(
        "https://qa-scooter.praktikum-services.ru/api/v1/courier/login",
        json={"login": login, "password": password}
    )
    assert response.status_code == 200
    return {"id": response.json()["id"], "login": login, "password": password}
