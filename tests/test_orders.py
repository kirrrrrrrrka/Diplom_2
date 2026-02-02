import allure


@allure.feature("Создание заказа")
class TestOrders:

    @allure.title("Создать заказ с авторизацией — успешно")
    def test_create_order_with_authorization_success(self, orders_api, ingredient_ids, access_token):
        resp = orders_api.create_order(ingredient_ids[:2], token=access_token)
        assert resp.status_code == 200

        body = resp.json()
        assert body.get("success") is True
        assert isinstance(body.get("order"), dict)
        assert isinstance(body["order"].get("number"), int)
        assert "name" in body

    @allure.title("Создать заказ без авторизации — успешно")
    def test_create_order_without_authorization_success(self, orders_api, ingredient_ids):
        resp = orders_api.create_order(ingredient_ids[:2])
        assert resp.status_code == 200

        body = resp.json()
        assert body.get("success") is True
        assert isinstance(body.get("order"), dict)
        assert isinstance(body["order"].get("number"), int)
        assert "name" in body

    @allure.title("Создать заказ с ингредиентами — успешно")
    def test_create_order_with_ingredients_success(self, orders_api, ingredient_ids):
        resp = orders_api.create_order([ingredient_ids[0]])
        assert resp.status_code == 200

        body = resp.json()
        assert body.get("success") is True
        assert isinstance(body.get("order"), dict)
        assert isinstance(body["order"].get("number"), int)
        assert "name" in body

    @allure.title("Создать заказ без ингредиентов — ошибка")
    def test_create_order_without_ingredients_fails(self, orders_api):
        resp = orders_api.create_order([])
        assert resp.status_code == 400

        body = resp.json()
        assert body.get("success") is False
        assert body.get("message") == "Ingredient ids must be provided"

    @allure.title("Создать заказ с неверным хешем ингредиентов — 500")
    def test_create_order_with_invalid_ingredient_hash_returns_500(self, orders_api):
        resp = orders_api.create_order(["invalid_ingredient_hash"])
        assert resp.status_code == 500
