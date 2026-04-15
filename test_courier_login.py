import requests
import pytest
import allure
from helpers import register_new_courier_and_return_login_password
from data import BASE_URL


@allure.feature("Авторизация курьера")
@allure.story("Логин в систему")
class TestCourierLogin:

    @allure.title("Курьер может успешно авторизоваться")
    @allure.description("Проверка успешной авторизации существующего курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_courier_can_login(self, authorized_courier):
        assert authorized_courier["id"] > 0

    @allure.title("Авторизация без обязательного поля")
    @allure.description("Проверка ошибки при отсутствии логина или пароля")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, missing_field):
        courier = register_new_courier_and_return_login_password()
        assert courier, "Не удалось создать курьера для теста"

        login, password, _ = courier
        payload = {"login": login, "password": password}

        if missing_field in payload:
            del payload[missing_field]

        response = requests.post(f"{BASE_URL}/courier/login", json=payload)

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json().get("message", "")

    @allure.title("Ошибка при неверном пароле")
    @allure.description("Проверка возврата 404 при неправильном пароле")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_password(self, new_courier):
        login, _, _ = new_courier
        response = requests.post(
            f"{BASE_URL}/courier/login",
            json={"login": login, "password": "wrongpassword123"}
        )
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")

    @allure.title("Авторизация несуществующего пользователя")
    @allure.description("Проверка ошибки при попытке залогиниться под несуществующим логином")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_nonexistent_user(self):
        response = requests.post(
            f"{BASE_URL}/courier/login",
            json={"login": "nonexistentuser12345", "password": "123456"}
        )
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")

    @allure.title("Успешная авторизация возвращает id")
    @allure.description("Проверка, что в ответе приходит идентификатор курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success_returns_id(self, authorized_courier):
        assert "id" in authorized_courier
