import requests
import pytest
from data import BASE_URL, ORDER_PAYLOAD, COLORS


@pytest.mark.parametrize("color", COLORS)
def test_create_order_with_different_colors(color):
    """Проверка создания заказа с разными вариантами цвета:
    - один цвет (BLACK / GREY)
    - оба цвета
    - без цвета
    """
    payload = ORDER_PAYLOAD.copy()
    payload["color"] = color

    response = requests.post(f"{BASE_URL}/orders", json=payload)

    assert response.status_code == 201
    assert "track" in response.json()
    assert isinstance(response.json()["track"], int)
