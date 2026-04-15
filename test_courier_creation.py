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
        """Курьера можно создать"""
        assert new_courier, "Курьер не был создан"

    @allure.title("Нельзя создать дубликат курьера")
    @allure.description("Проверка, что при повторной регистрации с тем же логином возвращается ошибка 409")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cannot_create_duplicate_courier(self):
        """Нельзя создать двух курьеров с одинаковым логином"""
        courier = register_new_courier_and_return_login_password()
        assert courier, "Не удалось создать первого курьера"

        payload = {
            "login": courier[0],
            "password": courier[1],
            "firstName": courier[2]
        }

        response = requests.post(f"{BASE_URL}/courier", json=payload)

        assert response.status_code == 409
        assert "уже используется" in response.json().get("message", "")

    @allure.title("Создание курьера без обязательного поля")
    @allure.description("Проверка ошибки 400 при отсутствии одного из обязательных полей")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, missing_field):
        """Если одного из обязательных полей нет — возвращается ошибка"""
        payload = {
            "login": "testlogin123",
            "password": "testpass123",
            "firstName": "TestName"
        }
        del payload[missing_field]

        response = requests.post(f"{BASE_URL}/courier", json=payload)

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json().get("message", "")

    @allure.title("Успешная регистрация возвращает ok: true")
    @allure.description("Проверка, что при успешном создании курьера тело ответа содержит {'ok': true}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_returns_ok_true(self):
        """Успешный запрос возвращает {"ok": true}"""
        courier_data = register_new_courier_and_return_login_password()
        payload = {
            "login": courier_data[0] + "x",
            "password": courier_data[1],
            "firstName": courier_data[2]
        }

        response = requests.post(f"{BASE_URL}/courier", json=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}
