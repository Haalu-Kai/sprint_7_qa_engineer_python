import pytest
from helpers import register_new_courier_and_return_login_password


@pytest.fixture
def new_courier():
    """Фикстура создаёт нового курьера и возвращает [login, password, firstName].
    После теста можно добавить удаление, если захотим."""
    courier = register_new_courier_and_return_login_password()
    assert courier, "Не удалось создать курьера для теста"
    yield courier


@pytest.fixture
def authorized_courier(new_courier):
    """Возвращает id авторизованного курьера + его логин/пароль"""
    login, password, _ = new_courier
    response = requests.post(
        "https://qa-scooter.praktikum-services.ru/api/v1/courier/login",
        json={"login": login, "password": password}
    )
    assert response.status_code == 200
    courier_id = response.json()["id"]
    return {"id": courier_id, "login": login, "password": password}
