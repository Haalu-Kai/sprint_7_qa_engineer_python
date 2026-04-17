import requests
import pytest
import allure
from data import ORDER_PAYLOAD, COLORS
from urls import ORDERS


@allure.feature("Работа с заказами")
@allure.story("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с разными вариантами цвета: {color}")
    @allure.description("Проверка создания заказа при передаче разных значений поля color: "
                       "один цвет (BLACK/GREY), оба цвета, без цвета")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("color", COLORS)
    def test_create_order_with_different_colors(self, color):
        payload = ORDER_PAYLOAD.copy()
        payload["color"] = color

        with allure.step(f"Отправка запроса на создание заказа с color = {color}"):
            response = requests.post(ORDERS, json=payload)

        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "track" in response.json(), "В ответе отсутствует поле 'track'"
        assert isinstance(response.json()["track"], int), "Поле 'track' должно быть числом"
