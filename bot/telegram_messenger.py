import json
import urllib.parse
import urllib.request
from typing import Any

from bot.messenger import Messenger

REQUEST_TIMEOUT = 40  # Больше, чем timeout=30 в getUpdates.


class TelegramMessenger(Messenger):
    def __init__(self, token: str, base_url: str) -> None:
        self._url = f"{base_url.rstrip('/')}/bot{token}"

    def _request(self, method: str, params: dict[str, object]) -> dict[str, Any]:
        # Сохраняем form-urlencoded из исходного эхо-бота.
        encoded_params = {
            key: json.dumps(value) if isinstance(value, (list, dict)) else value
            for key, value in params.items()
        }
        request = urllib.request.Request(
            f"{self._url}/{method}",
            data=urllib.parse.urlencode(encoded_params).encode(),
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            payload: dict[str, Any] = json.loads(response.read())
        if not payload["ok"]:
            raise RuntimeError(payload.get("description", "Telegram API error"))
        return payload

    def get_updates(self, **params: object) -> list[dict[str, Any]]:
        updates: list[dict[str, Any]] = self._request("getUpdates", params)["result"]
        return updates

    def send_message(self, **params: object) -> dict[str, Any]:
        return self._request("sendMessage", params)
