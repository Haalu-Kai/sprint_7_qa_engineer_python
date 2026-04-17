import pytest
from helpers import register_new_courier_and_return_login_password


@pytest.fixture
def new_courier():
    """Возвращает данные нового курьера (login, password, firstName)"""
    courier = register_new_courier_and_return_login_password()
    if not courier:
        pytest.fail("Не удалось создать курьера в фикстуре")
    return courier
