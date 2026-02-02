import pytest

from api.auth_api import AuthApi
from api.ingredients_api import IngredientsApi
from api.orders_api import OrdersApi
from generators import generate_user


@pytest.fixture(scope="session")
def auth_api():
    return AuthApi()


@pytest.fixture(scope="session")
def ingredients_api():
    return IngredientsApi()


@pytest.fixture(scope="session")
def orders_api():
    return OrdersApi()


@pytest.fixture()
def registered_user(auth_api):
    user = generate_user()
    resp = auth_api.register_user(user)
    assert resp.status_code == 200, f"Registration failed: {resp.status_code} {resp.text}"

    body = resp.json()
    user["accessToken"] = body.get("accessToken")
    user["refreshToken"] = body.get("refreshToken")

    yield user

    token = user.get("accessToken")
    if token:
        resp_del = auth_api.delete_user(token)
        # Если начнёт флапать на окружении, можно заменить на: assert resp_del.status_code < 500
        assert resp_del.status_code in (200, 202, 204), f"Delete user failed: {resp_del.status_code} {resp_del.text}"


@pytest.fixture()
def access_token(registered_user):
    return registered_user["accessToken"]


@pytest.fixture(scope="session")
def ingredient_ids(ingredients_api):
    resp = ingredients_api.get_ingredients()
    assert resp.status_code == 200, f"Ingredients failed: {resp.status_code} {resp.text}"

    data = resp.json().get("data", [])
    ids = [item["_id"] for item in data if "_id" in item]
    assert ids, "Empty ingredients list"
    return ids
