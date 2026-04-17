import requests
import pytest
import allure
from helpers import register_new_courier_and_return_login_password
from urls import COURIER_LOGIN


@allure.feature("Авторизация курьера")
@allure.story("Логин в систему")
class TestCourierLogin:

    @allure.title("Курьер может успешно авторизоваться")
    @allure.description("Проверка успешной авторизации существующего курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_courier_can_login(self):
        """Основной позитивный сценарий авторизации"""
        courier = register_new_courier_and_return_login_password()
        assert courier, "Не удалось создать курьера для теста"

        login, password, _ = courier

        with allure.step("Отправка POST-запроса на авторизацию курьера"):
            response = requests.post(
                COURIER_LOGIN,
                json={"login": login, "password": password}
            )

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        assert "id" in response.json(), "В ответе отсутствует поле 'id'"

    @allure.title("Авторизация без логина возвращает ошибку 400")
    @allure.description("Проверка, что авторизация без поля login невозможна")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_without_login(self):
        courier = register_new_courier_and_return_login_password()
        assert courier

        _, password, _ = courier

        with allure.step("Отправка POST-запроса на авторизацию без логина"):
            response = requests.post(
                COURIER_LOGIN,
                json={"password": password}
            )

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json().get("message", "")

    @allure.title("Авторизация без пароля возвращает ошибку 400")
    @allure.description("Проверка, что авторизация без поля password невозможна")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_without_password(self):
        courier = register_new_courier_and_return_login_password()
        assert courier

        login, _, _ = courier

        with allure.step("Отправка POST-запроса на авторизацию без пароля"):
            response = requests.post(
                COURIER_LOGIN,
                json={"login": login}
            )

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json().get("message", "")

    @allure.title("Ошибка при неверном пароле")
    @allure.description("При указании неверного пароля должен возвращаться статус 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_password(self):
        courier = register_new_courier_and_return_login_password()
        assert courier

        login, _, _ = courier

        with allure.step("Отправка POST-запроса с неверным паролем"):
            response = requests.post(
                COURIER_LOGIN,
                json={"login": login, "password": "wrongpassword123"}
            )

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")

    @allure.title("Авторизация несуществующего пользователя")
    @allure.description("При попытке авторизации под несуществующим пользователем должен возвращаться 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_nonexistent_user(self):
        with allure.step("Отправка POST-запроса с несуществующими данными"):
            response = requests.post(
                COURIER_LOGIN,
                json={"login": "nonexistentuser12345", "password": "123456"}
            )

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")
