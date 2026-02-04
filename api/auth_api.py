from .base import BaseApi


class AuthApi(BaseApi):
    REGISTER = "/api/auth/register"
    LOGIN = "/api/auth/login"
    USER = "/api/auth/user"

    def register_user(self, payload: dict):
        return self.request("POST", self.REGISTER, json=payload)

    def login_user(self, payload: dict):
        return self.request("POST", self.LOGIN, json=payload)

    def delete_user(self, access_token: str):
        return self.request("DELETE", self.USER, token=access_token)
