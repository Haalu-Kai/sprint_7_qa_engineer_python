import requests
from data import BASE_URL


def test_order_list_returns_list():
    """Проверка, что GET /orders возвращает список заказов (поле orders)"""
    response = requests.get(f"{BASE_URL}/orders")

    assert response.status_code == 200
    json_response = response.json()

    assert "orders" in json_response
    assert isinstance(json_response["orders"], list)
    
