import unittest
from unittest.mock import patch, Mock
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../scripts"))

from llm.gemini_client import call_gemini_api, GEMINI_API_URL


class TestGeminiClient(unittest.TestCase):
    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_successful_api_call(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "Hello! How can I assist you today?"}]}}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_gemini_api("Hello")

        self.assertEqual(result, "Hello! How can I assist you today?")
        mock_post.assert_called_once()

        args, kwargs = mock_post.call_args
        expected_url = f"{GEMINI_API_URL}?key=test_key"
        self.assertEqual(args[0], expected_url)
        self.assertEqual(kwargs["headers"]["Content-Type"], "application/json")

        request_data = json.loads(kwargs["data"])
        expected_data = {"contents": [{"parts": [{"text": "Hello"}]}]}
        self.assertEqual(request_data, expected_data)

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key(self):
        result = call_gemini_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_request_exception(self, mock_post):
        mock_post.side_effect = Exception("Network error")

        result = call_gemini_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_http_error(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 401 Unauthorized")
        mock_post.return_value = mock_response

        result = call_gemini_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_empty_candidates(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"candidates": []}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_gemini_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_no_candidates_key(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_gemini_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_missing_content_key(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"candidates": [{}]}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_gemini_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_missing_parts_key(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"candidates": [{"content": {}}]}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_gemini_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_missing_text_key(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"candidates": [{"content": {"parts": [{}]}}]}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_gemini_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_json_decode_error(self, mock_post):
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_gemini_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_empty_parts_list(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"candidates": [{"content": {"parts": []}}]}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_gemini_api("Hello")
        self.assertIsNone(result)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_multiple_parts(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": "First part"}, {"text": "Second part"}]
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_gemini_api("Hello")
        self.assertEqual(result, "First part")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_multiline_response(self, mock_post):
        multiline_text = "This is a\nmultiline\nresponse."
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": multiline_text}]}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_gemini_api("Complex question")
        self.assertEqual(result, multiline_text)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("llm.gemini_client.requests.post")
    def test_special_characters_in_response(self, mock_post):
        special_text = "Response with émojis 🚀 and spëcial chars: @#$%^&*()"
        mock_response = Mock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": special_text}]}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = call_gemini_api("Test")
        self.assertEqual(result, special_text)

    def test_api_url_constant(self):
        expected_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        self.assertEqual(GEMINI_API_URL, expected_url)


if __name__ == "__main__":
    unittest.main()
