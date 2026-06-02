import unittest
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../scripts"))

from llm.deepseek_client import call_deepseek_api, MODEL_NAME, DEEPSEEK_API_URL


class TestDeepseekClient(unittest.TestCase):
    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"})
    @patch("llm.deepseek_client.requests.post")
    def test_successful_api_call(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {"content": "Hello! How can I help you?"},
                    "finish_reason": "stop",
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_deepseek_api("Hello")

        self.assertEqual(result, "Hello! How can I help you?")
        mock_post.assert_called_once()

        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], DEEPSEEK_API_URL)
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_key")
        self.assertEqual(kwargs["json"]["model"], MODEL_NAME)
        self.assertEqual(
            kwargs["json"]["messages"], [{"role": "user", "content": "Hello"}]
        )

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key(self):
        result = call_deepseek_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"})
    @patch("llm.deepseek_client.requests.post")
    def test_request_exception(self, mock_post):
        mock_post.side_effect = Exception("Network error")

        result = call_deepseek_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"})
    @patch("llm.deepseek_client.requests.post")
    def test_empty_response(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_deepseek_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"})
    @patch("llm.deepseek_client.requests.post")
    def test_empty_choices(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"choices": []}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_deepseek_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"})
    @patch("llm.deepseek_client.requests.post")
    def test_empty_content(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": ""}, "finish_reason": "stop"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_deepseek_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"})
    @patch("llm.deepseek_client.requests.post")
    def test_invalid_finish_reason(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello!"}, "finish_reason": "error"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_deepseek_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"})
    @patch("llm.deepseek_client.requests.post")
    def test_finish_reason_length(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {"content": "Hello! This is a long response..."},
                    "finish_reason": "length",
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_deepseek_api("Hello")
        self.assertEqual(result, "Hello! This is a long response...")

    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"})
    @patch("llm.deepseek_client.requests.post")
    def test_http_error(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 401 Unauthorized")
        mock_post.return_value = mock_response

        result = call_deepseek_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"})
    @patch("llm.deepseek_client.requests.post")
    def test_malformed_json_response(self, mock_post):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_deepseek_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"})
    @patch("llm.deepseek_client.requests.post")
    def test_request_parameters(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Response"}, "finish_reason": "stop"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        call_deepseek_api("Test prompt")

        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["stream"], False)
        self.assertIn("Content-Type", kwargs["headers"])
        self.assertEqual(kwargs["headers"]["Content-Type"], "application/json")

    def test_constants(self):
        self.assertEqual(MODEL_NAME, "deepseek-chat")
        self.assertEqual(DEEPSEEK_API_URL, "https://api.deepseek.com/chat/completions")


if __name__ == "__main__":
    unittest.main()
