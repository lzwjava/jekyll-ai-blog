import unittest
import os
from unittest.mock import patch, MagicMock
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.bot.habit_bot import send_telegram_message


class TestHabitBot(unittest.TestCase):
    @patch("scripts.bot.habit_bot.requests.post")
    def test_send_telegram_message_success(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Test the function
        result = send_telegram_message("test_token", "test_chat_id", "test_message")

        # Verify the request was made correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://api.telegram.org/bottest_token/sendMessage")
        self.assertEqual(kwargs["params"]["chat_id"], "test_chat_id")
        self.assertEqual(kwargs["params"]["text"], "test_message")
        self.assertEqual(kwargs["params"]["parse_mode"], "Markdown")
        self.assertTrue(result)

    @patch("scripts.bot.habit_bot.requests.post")
    def test_send_telegram_message_with_markdown_removal(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Test with message containing asterisks and URLs
        message_with_markdown = "This is *bold* text with https://example.com link"
        send_telegram_message("test_token", "test_chat_id", message_with_markdown)

        # Verify asterisks and URLs are removed
        args, kwargs = mock_post.call_args
        sent_text = kwargs["params"]["text"]
        self.assertNotIn("*", sent_text)
        self.assertNotIn("https://example.com", sent_text)
        self.assertIn("This is bold text with  link", sent_text)

    @patch("scripts.bot.habit_bot.requests.post")
    def test_send_telegram_message_long_message(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Create a long message that exceeds TELEGRAM_MAX_LENGTH (4096)
        long_message = "A" * 5000
        send_telegram_message("test_token", "test_chat_id", long_message)

        # Verify multiple POST requests were made (message was split)
        self.assertGreater(mock_post.call_count, 1)

    @patch("scripts.bot.habit_bot.requests.post")
    def test_send_telegram_message_error(self, mock_post):
        # Mock error response
        mock_post.side_effect = Exception("Network error")

        # Test the function
        with patch("builtins.print") as mock_print:
            result = send_telegram_message("test_token", "test_chat_id", "test_message")
            self.assertFalse(result)
            mock_print.assert_called()

    def test_send_telegram_message_missing_credentials(self):
        # Test with missing bot token
        with patch("builtins.print") as mock_print:
            result = send_telegram_message(None, "test_chat_id", "test_message")
            self.assertFalse(result)
            mock_print.assert_called_with(
                "Error: TELEGRAM_HABIT_BOT_API_KEY or TELEGRAM_CHAT_ID not set."
            )

        # Test with missing chat ID
        with patch("builtins.print") as mock_print:
            result = send_telegram_message("test_token", None, "test_message")
            self.assertFalse(result)
            mock_print.assert_called_with(
                "Error: TELEGRAM_HABIT_BOT_API_KEY or TELEGRAM_CHAT_ID not set."
            )

    @patch("scripts.bot.habit_bot.requests.post")
    def test_send_telegram_message_with_newlines(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Create a message with newlines that would be split properly
        message_with_newlines = (
            "Line 1\nLine 2\nLine 3\n" * 200
        )  # Make it long enough to split
        send_telegram_message("test_token", "test_chat_id", message_with_newlines)

        # If message was split, verify multiple calls were made
        if mock_post.call_count > 1:
            # Check that splits occurred at newlines when possible
            for call in mock_post.call_args_list:
                sent_text = call[1]["params"]["text"]
                self.assertLessEqual(len(sent_text), 4096)


if __name__ == "__main__":
    unittest.main()
