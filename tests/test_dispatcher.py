import unittest
from unittest.mock import Mock

from bot.dispatcher import Dispatcher
from bot.handlers import get_handlers


class DispatcherTest(unittest.TestCase):
    def setUp(self) -> None:
        self.messenger = Mock()
        self.dispatcher = Dispatcher(self.messenger)
        self.dispatcher.add_handlers(*get_handlers())

    def test_text_is_sent(self) -> None:
        update = {"update_id": 1, "message": {"chat": {"id": 8}, "text": "abc"}}
        self.dispatcher.dispatch(update)
        self.messenger.send_message.assert_called_once_with(chat_id=8, text="abc")

    def test_sticker_is_ignored(self) -> None:
        update = {
            "update_id": 2,
            "message": {"chat": {"id": 8}, "sticker": {"file_id": "s"}},
        }
        self.dispatcher.dispatch(update)
        self.messenger.send_message.assert_not_called()

    def test_other_update_is_ignored(self) -> None:
        self.dispatcher.dispatch({"update_id": 3, "callback_query": {"id": "1"}})
        self.messenger.send_message.assert_not_called()
