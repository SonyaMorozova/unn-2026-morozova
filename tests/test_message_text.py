import unittest
from unittest.mock import Mock

from bot.handlers.handler import HandlerStatus
from bot.handlers.message_text import MessageTextHandler


class MessageTextHandlerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = MessageTextHandler()
        self.messenger = Mock()

    def test_echo_text(self) -> None:
        update = {"message": {"chat": {"id": 42}, "text": "Привет!"}}
        self.assertTrue(self.handler.can_handle(update))
        status = self.handler.handle(update, self.messenger)
        self.assertEqual(status, HandlerStatus.STOP)
        self.messenger.send_message.assert_called_once_with(chat_id=42, text="Привет!")

    def test_non_text_ignored(self) -> None:
        for message in ({"sticker": {"file_id": "a"}}, {"photo": []}, {}):
            with self.subTest(message=message):
                self.assertFalse(self.handler.can_handle({"message": message}))
        self.assertFalse(self.handler.can_handle({"edited_message": {"text": "a"}}))
        self.messenger.send_message.assert_not_called()
