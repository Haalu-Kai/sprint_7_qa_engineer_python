import requests
import allure
from data import BASE_URL


@allure.feature("Работа с заказами")
@allure.story("Получение списка заказов")
class TestOrderList:

    @allure.title("GET /orders возвращает список заказов")
    @allure.description("Проверка, что в теле ответа присутствует массив orders")
    @allure.severity(allure.severity_level.NORMAL)
    def test_order_list_returns_list(self):
        response = requests.get(f"{BASE_URL}/orders")

        assert response.status_code == 200
        json_response = response.json()

        assert "orders" in json_response
        assert isinstance(json_response["orders"], list)
