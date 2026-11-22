import json
import unittest
import urllib.parse
from typing import Self
from unittest.mock import Mock, patch

from bot.telegram_messenger import TelegramMessenger


class FakeResponse:
    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps({"ok": True, "result": []}).encode()


class TelegramMessengerTest(unittest.TestCase):
    @patch("bot.telegram_messenger.urllib.request.urlopen")
    def test_uses_configured_url_and_form_encoding(self, urlopen: Mock) -> None:
        urlopen.return_value = FakeResponse()

        messenger = TelegramMessenger(
            "abc",
            "https://example.test/",
        )

        result = messenger.get_updates(
            offset=5,
            timeout=30,
            allowed_updates=["message"],
        )

        self.assertEqual(result, [])

        request = urlopen.call_args.args[0]

        self.assertEqual(
            request.full_url,
            "https://example.test/botabc/getUpdates",
        )

        data = urllib.parse.parse_qs(request.data.decode())

        self.assertEqual(data["offset"], ["5"])
        self.assertEqual(data["allowed_updates"], ['["message"]'])
