import allure
import pytest

from generators import generate_user


@allure.feature("Создание пользователя")
class TestUserCreate:

    @allure.title("Создать уникального пользователя — успешно")
    def test_create_unique_user_success(self, auth_api):
        payload = generate_user()

        resp = auth_api.register_user(payload)
        assert resp.status_code == 200

        body = resp.json()
        assert body.get("success") is True
        assert body.get("user", {}).get("email") == payload["email"]
        assert "accessToken" in body
        assert "refreshToken" in body

        auth_api.delete_user(body["accessToken"])

    @allure.title("Создать пользователя, который уже зарегистрирован — ошибка")
    def test_create_existing_user_fails(self, auth_api, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"],
        }

        resp = auth_api.register_user(payload)
        assert resp.status_code == 403

        body = resp.json()
        assert body.get("success") is False
        assert body.get("message") == "User already exists"

    @allure.title("Создать пользователя без обязательного поля — ошибка")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field_fails(self, auth_api, missing_field):
        payload = generate_user()
        payload.pop(missing_field)

        resp = auth_api.register_user(payload)
        assert resp.status_code == 403

        body = resp.json()
        assert body.get("success") is False
        assert body.get("message") == "Email, password and name are required fields"
