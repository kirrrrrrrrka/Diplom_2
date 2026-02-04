import allure
import pytest


@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Вход под существующим пользователем — успешно")
    def test_login_existing_user_success(self, auth_api, registered_user):
        payload = {"email": registered_user["email"], "password": registered_user["password"]}

        resp = auth_api.login_user(payload)
        assert resp.status_code == 200

        body = resp.json()
        assert body.get("success") is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body.get("user", {}).get("email") == registered_user["email"]

    @allure.title("Вход с неверным логином/паролем — ошибка")
    @pytest.mark.parametrize(
        "email,password",
        [
            ("no_such_user@yandex.ru", "some_password"),
            ("", "some_password"),
            ("test_login@yandex.ru", ""),
            ("test_login@yandex.ru", "wrong_password"),
        ],
    )
    def test_login_with_wrong_credentials_fails(self, auth_api, email, password):
        resp = auth_api.login_user({"email": email, "password": password})
        assert resp.status_code == 401

        body = resp.json()
        assert body.get("success") is False
        assert body.get("message") == "email or password are incorrect"
