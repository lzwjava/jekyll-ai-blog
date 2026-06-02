import unittest
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../scripts"))

from llm.openrouter_client import (
    call_openrouter_api,
    call_openrouter_api_with_messages,
    MODEL_MAPPING,
)


class TestOpenrouterClient(unittest.TestCase):
    def setUp(self):
        self.test_api_key = "test_openrouter_key"
        self.test_messages = [{"role": "user", "content": "Hello"}]

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_successful_api_call_with_messages(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello! How can I help you?"}}]
        }
        mock_post.return_value = mock_response

        result = call_openrouter_api_with_messages(self.test_messages, "mistral-medium")

        self.assertEqual(result, "Hello! How can I help you?")
        mock_post.assert_called_once()

        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://openrouter.ai/api/v1/chat/completions")
        self.assertEqual(
            kwargs["headers"]["Authorization"], f"Bearer {self.test_api_key}"
        )
        self.assertEqual(kwargs["headers"]["Content-Type"], "application/json")
        self.assertEqual(kwargs["json"]["model"], MODEL_MAPPING["mistral-medium"])
        self.assertEqual(kwargs["json"]["messages"], self.test_messages)

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_successful_api_call(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello from OpenRouter!"}}]
        }
        mock_post.return_value = mock_response

        result = call_openrouter_api("Hello", "claude-sonnet")

        self.assertEqual(result, "Hello from OpenRouter!")
        args, kwargs = mock_post.call_args
        expected_messages = [{"role": "user", "content": "Hello"}]
        self.assertEqual(kwargs["json"]["messages"], expected_messages)
        self.assertEqual(kwargs["json"]["model"], MODEL_MAPPING["claude-sonnet"])

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key_raises_exception(self):
        with self.assertRaises(Exception) as context:
            call_openrouter_api("Hello")
        self.assertIn(
            "OPENROUTER_API_KEY environment variable is not set", str(context.exception)
        )

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    def test_invalid_model_raises_exception(self):
        with self.assertRaises(Exception) as context:
            call_openrouter_api_with_messages(self.test_messages, "invalid-model")
        self.assertIn(
            "Model 'invalid-model' not found in MODEL_MAPPING", str(context.exception)
        )

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_http_error_response(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            call_openrouter_api_with_messages(self.test_messages)
        self.assertIn("Error: 401 - Unauthorized", str(context.exception))

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_request_exception(self, mock_post):
        mock_post.side_effect = Exception("Network error")

        with self.assertRaises(Exception) as context:
            call_openrouter_api_with_messages(self.test_messages)
        self.assertIn("An error occurred: Network error", str(context.exception))

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_debug_mode(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"choices": [{"message": {"content": "Debug response"}}]}'
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Debug response"}}]
        }
        mock_post.return_value = mock_response

        result = call_openrouter_api_with_messages(self.test_messages, debug=True)
        self.assertEqual(result, "Debug response")

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_all_models_in_mapping(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_post.return_value = mock_response

        for model_name in MODEL_MAPPING.keys():
            result = call_openrouter_api("Test", model_name)
            self.assertEqual(result, "Test response")

            args, kwargs = mock_post.call_args
            self.assertEqual(kwargs["json"]["model"], MODEL_MAPPING[model_name])

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_complex_messages(self, mock_post):
        complex_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "assistant", "content": "The capital of France is Paris."},
            {"role": "user", "content": "What about Germany?"},
        ]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "The capital of Germany is Berlin."}}]
        }
        mock_post.return_value = mock_response

        result = call_openrouter_api_with_messages(complex_messages, "gemini-flash")
        self.assertEqual(result, "The capital of Germany is Berlin.")

        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["messages"], complex_messages)

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_malformed_json_response(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            call_openrouter_api_with_messages(self.test_messages)

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_missing_choices_in_response(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            call_openrouter_api_with_messages(self.test_messages)

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_multiline_response(self, mock_post):
        multiline_response = """Here's a Python function:

def greet(name):
    return f"Hello, {name}!"

This function takes a name parameter and returns a greeting."""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": multiline_response}}]
        }
        mock_post.return_value = mock_response

        result = call_openrouter_api("Write a greeting function")
        self.assertEqual(result, multiline_response)

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_special_characters_prompt(self, mock_post):
        special_prompt = "Explain émojis 🚀 and special chars: @#$%^&*()"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {"message": {"content": "Émojis and special characters explained..."}}
            ]
        }
        mock_post.return_value = mock_response

        result = call_openrouter_api(special_prompt, "deepseek-v3.2")
        self.assertEqual(result, "Émojis and special characters explained...")

    def test_model_mapping_completeness(self):
        expected_models = [
            "claude-opus",
            "claude-sonnet",
            "gemini-flash",
            "deepseek-v3.2",
            "gemini-pro",
            "kimi-k2",
            "mistral-medium",
            "qwen-coder",
            "gpt-oss",
            "gpt-5",
        ]

        for model in expected_models:
            self.assertIn(model, MODEL_MAPPING)
            self.assertIsInstance(MODEL_MAPPING[model], str)
            self.assertTrue(len(MODEL_MAPPING[model]) > 0)

    def test_model_mapping_values(self):
        self.assertEqual(MODEL_MAPPING["claude-opus"], "anthropic/claude-opus-4")
        self.assertEqual(MODEL_MAPPING["claude-sonnet"], "anthropic/claude-sonnet-4")
        self.assertEqual(MODEL_MAPPING["gemini-flash"], "google/gemini-2.5-flash")
        self.assertEqual(
            MODEL_MAPPING["mistral-medium"], "mistralai/mistral-medium-3.1"
        )

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_openrouter_key"})
    @patch("llm.openrouter_client.requests.post")
    def test_empty_response_content(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"choices": [{"message": {"content": ""}}]}
        mock_post.return_value = mock_response

        result = call_openrouter_api("Hello")
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
