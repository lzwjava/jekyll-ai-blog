import unittest
import os
import datetime
import argparse
from unittest.mock import patch, MagicMock
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.bot.punch_bot import (
    send_telegram_message,
    send_reminder,
    send_confirmation,
    parse_time,
)


class TestPunchBot(unittest.TestCase):
    @patch("scripts.bot.punch_bot.requests.post")
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
        self.assertEqual(kwargs["params"]["parse_mode"], "Markdown")

    @patch("scripts.bot.punch_bot.requests.post")
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

    @patch("scripts.bot.punch_bot.send_telegram_message")
    def test_send_reminder(self, mock_send):
        # Test punch_in reminder
        send_reminder("punch_in")
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        self.assertIn("punch in", args[2])
        self.assertIn("punch_in", args[2])

        # Reset mock and test punch_out reminder
        mock_send.reset_mock()
        send_reminder("punch_out")
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        self.assertIn("punch out", args[2])
        self.assertIn("punch_out", args[2])

    @patch("scripts.bot.punch_bot.send_telegram_message")
    def test_send_confirmation(self, mock_send):
        # Test punch_in confirmation
        send_confirmation("punch_in")
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        self.assertIn("punch in", args[2])
        self.assertIn("already", args[2])

        # Reset mock and test punch_out confirmation
        mock_send.reset_mock()
        send_confirmation("punch_out")
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        self.assertIn("punch out", args[2])
        self.assertIn("already", args[2])

    def test_parse_time_valid(self):
        # Test valid hours
        time_obj = parse_time("09")
        self.assertEqual(time_obj, datetime.time(9, 0))

        time_obj = parse_time("0")
        self.assertEqual(time_obj, datetime.time(0, 0))

        time_obj = parse_time("23")
        self.assertEqual(time_obj, datetime.time(23, 0))

    def test_parse_time_invalid(self):
        # Test invalid hours
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_time("24")

        with self.assertRaises(argparse.ArgumentTypeError):
            parse_time("-1")

        with self.assertRaises(argparse.ArgumentTypeError):
            parse_time("abc")

        with self.assertRaises(argparse.ArgumentTypeError):
            parse_time("12.5")


if __name__ == "__main__":
    unittest.main()
