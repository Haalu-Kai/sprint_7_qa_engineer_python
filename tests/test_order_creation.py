import requests
import pytest
import allure
from data import BASE_URL, ORDER_PAYLOAD, COLORS


@allure.feature("Работа с заказами")
@allure.story("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с разными цветами: {color}")
    @allure.description("Проверка создания заказа при разных вариантах поля color (один цвет, два цвета, без цвета)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("color", COLORS)
    def test_create_order_with_different_colors(self, color):
        payload = ORDER_PAYLOAD.copy()
        payload["color"] = color

        response = requests.post(f"{BASE_URL}/orders", json=payload)

        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
