from uuid import uuid4


def generate_user() -> dict:
    uid = uuid4().hex
    return {
        "email": f"test_{uid}@yandex.ru",
        "password": f"Pass_{uid}!",
        "name": f"User_{uid[:8]}",
    }
