import json as json_lib
from typing import Any, Dict, Optional

import allure
import requests


class BaseApi:
    BASE_URL = "https://stellarburgers.education-services.ru"
    TIMEOUT_SECONDS = 10

    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.BASE_URL}{path}"

    @staticmethod
    def _auth_headers(token: Optional[str]) -> Dict[str, str]:
        return {"Authorization": token} if token else {}

    @staticmethod
    def _attach(name: str, data: str, attachment_type):
        allure.attach(data, name=name, attachment_type=attachment_type)

    def request(
        self,
        method: str,
        path: str,
        json: Any = None,
        headers: Optional[Dict[str, str]] = None,
        token: Optional[str] = None,
    ) -> requests.Response:
        url = self._url(path)

        hdrs: Dict[str, str] = {}
        if headers:
            hdrs.update(headers)
        hdrs.update(self._auth_headers(token))

        with allure.step(f"{method.upper()} {path}"):
            self._attach("url", url, allure.attachment_type.TEXT)

            if hdrs:
                self._attach(
                    "headers",
                    json_lib.dumps(hdrs, ensure_ascii=False, indent=2),
                    allure.attachment_type.JSON,
                )

            if json is not None:
                self._attach(
                    "request_body",
                    json_lib.dumps(json, ensure_ascii=False, indent=2),
                    allure.attachment_type.JSON,
                )

            resp = self.session.request(
                method=method.upper(),
                url=url,
                json=json,
                headers=hdrs,
                timeout=self.TIMEOUT_SECONDS,
            )

            self._attach("status_code", str(resp.status_code), allure.attachment_type.TEXT)

            try:
                parsed = resp.json()
                self._attach(
                    "response_body",
                    json_lib.dumps(parsed, ensure_ascii=False, indent=2),
                    allure.attachment_type.JSON,
                )
            except Exception:
                self._attach("response_body", resp.text, allure.attachment_type.TEXT)

            return resp
