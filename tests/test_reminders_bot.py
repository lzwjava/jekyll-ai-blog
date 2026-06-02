import unittest
import os
from unittest.mock import patch, MagicMock
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.bot.reminders_bot import send_telegram_message, get_chat_id, send_reminder


class TestRemindersBot(unittest.TestCase):
    @patch("scripts.bot.reminders_bot.requests.post")
    def test_send_telegram_message_success(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Test the function
        send_telegram_message("test_token", "test_chat_id", "test_message")

        # Verify the request was made correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://api.telegram.org/bottest_token/sendMessage")
        self.assertEqual(kwargs["params"]["chat_id"], "test_chat_id")
        self.assertEqual(kwargs["params"]["text"], "test_message")

    @patch("scripts.bot.reminders_bot.requests.post")
    def test_send_telegram_message_error(self, mock_post):
        # Mock error response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        # Test the function
        with patch("builtins.print") as mock_print:
            send_telegram_message("test_token", "test_chat_id", "test_message")
            mock_print.assert_called_once()
            self.assertIn("Error sending Telegram message", mock_print.call_args[0][0])

    @patch("scripts.bot.reminders_bot.requests.get")
    def test_get_chat_id_success(self, mock_get):
        # Mock successful response with updates
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": [{"message": {"chat": {"id": "123456789"}}}]
        }
        mock_get.return_value = mock_response

        # Test the function
        with patch("builtins.print"):  # Suppress JSON print output
            chat_id = get_chat_id("test_token")

        # Verify the result
        self.assertEqual(chat_id, "123456789")
        mock_get.assert_called_once_with(
            "https://api.telegram.org/bottest_token/getUpdates"
        )

    @patch("scripts.bot.reminders_bot.requests.get")
    def test_get_chat_id_no_updates(self, mock_get):
        # Mock response with no updates
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": []}
        mock_get.return_value = mock_response

        # Test the function
        with patch("builtins.print"):  # Suppress JSON print output
            chat_id = get_chat_id("test_token")

        # Should return None when no updates
        self.assertIsNone(chat_id)

    @patch("scripts.bot.reminders_bot.requests.get")
    def test_get_chat_id_error(self, mock_get):
        # Mock error response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        # Test the function
        chat_id = get_chat_id("test_token")

        # Should return None on error
        self.assertIsNone(chat_id)

    @patch("scripts.bot.reminders_bot.send_telegram_message")
    def test_send_reminder_with_credentials(self, mock_send):
        # Mock environment variables
        with patch.dict(os.environ, {"TELEGRAM_BOT2_API_KEY": "test_key"}):
            with patch("scripts.bot.reminders_bot.TELEGRAM_BOT2_API_KEY", "test_key"):
                with patch("scripts.bot.reminders_bot.TELEGRAM_CHAT_ID", "test_chat"):
                    send_reminder("Test reminder message")
                    mock_send.assert_called_once_with(
                        "test_key", "test_chat", "Test reminder message"
                    )

    @patch("scripts.bot.reminders_bot.send_telegram_message")
    def test_send_reminder_missing_credentials(self, mock_send):
        # Test with missing credentials
        with patch("scripts.bot.reminders_bot.TELEGRAM_BOT2_API_KEY", None):
            with patch("builtins.print") as mock_print:
                send_reminder("Test reminder message")
                mock_send.assert_not_called()
                mock_print.assert_called_with(
                    "TELEGRAM_BOT2_API_KEY and TELEGRAM_CHAT_ID are not set."
                )


if __name__ == "__main__":
    unittest.main()
