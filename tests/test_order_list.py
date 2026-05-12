import requests
import allure
from urls import ORDERS


@allure.feature("Работа с заказами")
@allure.story("Получение списка заказов")
class TestOrderList:

    @allure.title("GET /orders возвращает список заказов")
    @allure.description("Проверка, что в теле ответа присутствует поле 'orders' типа список")
    @allure.severity(allure.severity_level.NORMAL)
    def test_order_list_returns_list(self):
        with allure.step("Отправка GET-запроса на получение списка заказов"):
            response = requests.get(ORDERS)

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        json_response = response.json()

        assert "orders" in json_response, "В ответе отсутствует поле 'orders'"
        assert isinstance(json_response["orders"], list), "Поле 'orders' должно быть списком"
