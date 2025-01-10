import os

from typing import Any

import requests

from trader.types import T212Server


class _T212Client:
    _SESSION: requests.Session = requests.Session()

    def __init__(self, server: T212Server = T212Server.DEMO):
        self.server = server

        if (token := os.getenv("T212_API_TOKEN", "")) == "":
            raise ValueError("Could not retrieve T212 API token.")

        self._SESSION.headers = {"Authorization": token}

    def get(self, url: str, params: dict[str, Any] | None = None) -> requests.Response:
        return self._SESSION.get(self.server.value+url, params=params)

    def post(
        self, url: str, json: dict[str, Any],
        params: dict[str, Any] | None = None
    ) -> requests.Response:
        return self._SESSION.post(self.server.value+url, json=json, params=params)

    def delete(self, url: str, params: dict[str, Any]) -> requests.Response:
        return self._SESSION.delete(self.server.value+url, params=params)
