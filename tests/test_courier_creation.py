import requests
import pytest
import allure
from helpers import register_new_courier_and_return_login_password
from data import BASE_URL


@allure.feature("Создание курьера")
@allure.story("Регистрация нового курьера")
class TestCourierCreation:

    @allure.title("Успешное создание курьера")
    @allure.description("Проверка, что курьера можно создать с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self, new_courier):
        assert new_courier, "Курьер не был создан"

    @allure.title("Нельзя создать дубликат курьера")
    @allure.description("При регистрации курьера с уже существующим логином должен возвращаться 409")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cannot_create_duplicate_courier(self):
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

    @allure.title("Создание курьера без обязательного поля → ошибка 400")
    @allure.description("Если отсутствует login, password или firstName — должна быть ошибка 400")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, missing_field):
        payload = {
            "login": "testlogin123",
            "password": "testpass123",
            "firstName": "TestName"
        }
        del payload[missing_field]

        response = requests.post(f"{BASE_URL}/courier", json=payload)

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json().get("message", "")

    @allure.title("Успешная регистрация возвращает {'ok': true}")
    @allure.description("При успешном создании курьера тело ответа должно быть {'ok': true}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_returns_ok_true(self):
        courier_data = register_new_courier_and_return_login_password()

        payload = {
            "login": courier_data[0] + "unique",
            "password": courier_data[1],
            "firstName": courier_data[2]
        }

        response = requests.post(f"{BASE_URL}/courier", json=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}
