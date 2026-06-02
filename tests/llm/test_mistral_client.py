import unittest
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../scripts"))

from llm.mistral_client import call_mistral_api, MISTRAL_API_URL


class TestMistralClient(unittest.TestCase):
    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_successful_api_call(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [
                {"message": {"content": "Hello! I'm Mistral, how can I help you?"}}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_mistral_api("Hello")

        self.assertEqual(result, "Hello! I'm Mistral, how can I help you?")
        mock_post.assert_called_once()

        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], MISTRAL_API_URL)
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_key")
        self.assertEqual(kwargs["headers"]["Content-Type"], "application/json")
        self.assertEqual(kwargs["headers"]["Accept"], "application/json")
        self.assertEqual(kwargs["json"]["model"], "mistral-small-latest")
        self.assertEqual(
            kwargs["json"]["messages"], [{"role": "user", "content": "Hello"}]
        )

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key(self):
        result = call_mistral_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_request_exception(self, mock_post):
        mock_post.side_effect = Exception("Network error")

        result = call_mistral_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_http_error_with_response(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 401 Unauthorized")
        mock_response.status_code = 401
        mock_response.text = "Unauthorized access"

        exception = Exception("HTTP error")
        exception.response = mock_response
        mock_post.side_effect = exception

        result = call_mistral_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_http_error_without_response(self, mock_post):
        exception = Exception("Network error")
        exception.response = None
        mock_post.side_effect = exception

        result = call_mistral_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_empty_response(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = None
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_mistral_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_empty_choices(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"choices": []}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_mistral_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_no_choices_key(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_mistral_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_malformed_response_structure(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"choices": [{"invalid": "structure"}]}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        with self.assertRaises(KeyError):
            call_mistral_api("Hello")

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_complex_prompt(self, mock_post):
        complex_prompt = """
        Write a function that calculates the factorial of a number.
        Include error handling and documentation.
        """
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Here's a factorial function..."}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_mistral_api(complex_prompt)

        self.assertEqual(result, "Here's a factorial function...")
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["messages"][0]["content"], complex_prompt)

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_multiline_response(self, mock_post):
        multiline_response = """def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)"""

        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": multiline_response}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_mistral_api("Write a factorial function")
        self.assertEqual(result, multiline_response)

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_unicode_content(self, mock_post):
        unicode_response = "Response with émojis 🚀 and spëcial chars: ñáéíóú"
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": unicode_response}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_mistral_api("Test unicode")
        self.assertEqual(result, unicode_response)

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_json_decode_error(self, mock_post):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_mistral_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"MISTRAL_API_KEY": "test_key"})
    @patch("llm.mistral_client.requests.post")
    def test_multiple_choices(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [
                {"message": {"content": "First response"}},
                {"message": {"content": "Second response"}},
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_mistral_api("Hello")
        self.assertEqual(result, "First response")

    def test_api_url_constant(self):
        expected_url = "https://api.mistral.ai/v1/chat/completions"
        self.assertEqual(MISTRAL_API_URL, expected_url)


if __name__ == "__main__":
    unittest.main()
