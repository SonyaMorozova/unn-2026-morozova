import unittest
from unittest.mock import Mock

from bot.long_polling import poll_once


class PollOnceTest(unittest.TestCase):
    def test_poll_once_routes_and_updates_offset(self) -> None:
        messenger = Mock()
        dispatcher = Mock()
        update = {"update_id": 100, "message": {"chat": {"id": 1}, "text": "Hi"}}
        messenger.get_updates.return_value = [update]
        offset = poll_once(dispatcher, messenger, 0)
        self.assertEqual(offset, 101)
        messenger.get_updates.assert_called_once_with(
            offset=0, limit=10, timeout=30, allowed_updates=["message"]
        )
        dispatcher.dispatch.assert_called_once_with(update)

    def test_empty_batch(self) -> None:
        messenger = Mock()
        dispatcher = Mock()
        messenger.get_updates.return_value = []
        self.assertEqual(poll_once(dispatcher, messenger, 6), 6)
        dispatcher.dispatch.assert_not_called()

    def test_offset_does_not_go_backwards(self) -> None:
        messenger = Mock()
        dispatcher = Mock()
        messenger.get_updates.return_value = [{"update_id": 100}, {"update_id": 50}]
        self.assertEqual(poll_once(dispatcher, messenger, 0), 101)
