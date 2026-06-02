import unittest
from unittest.mock import Mock, patch
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../scripts"))


class MockResponse:
    """Utility class for creating mock HTTP responses"""

    def __init__(
        self, json_data=None, status_code=200, text="", raise_for_status_exception=None
    ):
        self.json_data = json_data
        self.status_code = status_code
        self.text = text
        self._raise_for_status_exception = raise_for_status_exception

    def json(self):
        if self.json_data is None:
            raise ValueError("No JSON object could be decoded")
        return self.json_data

    def raise_for_status(self):
        if self._raise_for_status_exception:
            raise self._raise_for_status_exception


class TestDataFixtures:
    """Common test data and fixtures for LLM client tests"""

    DEEPSEEK_SUCCESS_RESPONSE = {
        "choices": [
            {
                "message": {"content": "Hello! How can I help you?"},
                "finish_reason": "stop",
            }
        ]
    }

    GEMINI_SUCCESS_RESPONSE = {
        "candidates": [
            {"content": {"parts": [{"text": "Hello! How can I assist you today?"}]}}
        ]
    }

    MISTRAL_SUCCESS_RESPONSE = {
        "choices": [{"message": {"content": "Hello! I'm Mistral, how can I help you?"}}]
    }

    OPENROUTER_SUCCESS_RESPONSE = {
        "choices": [{"message": {"content": "Hello from OpenRouter!"}}]
    }

    EMPTY_RESPONSE = {}
    EMPTY_CHOICES_RESPONSE = {"choices": []}
    MALFORMED_RESPONSE = {"invalid": "structure"}

    SAMPLE_PROMPTS = [
        "Hello",
        "What is the capital of France?",
        "Write a Python function to calculate factorial",
        "Explain quantum computing in simple terms",
        "Generate a haiku about programming",
        "Translate 'Hello world' to Spanish",
        "",  # Empty prompt
        "A" * 1000,  # Long prompt
        "Prompt with émojis 🚀 and spëcial chars: @#$%^&*()",  # Special characters
        """Multiline
        prompt
        with breaks""",  # Multiline prompt
    ]

    SAMPLE_RESPONSES = [
        "Simple response",
        "",  # Empty response
        "Response with émojis 🚀 and spëcial chars: ñáéíóú",  # Unicode
        """Multiline response
        with code:

        def example():
            return 'Hello'""",  # Code response
        "A" * 2000,  # Long response
        json.dumps({"json": "response"}),  # JSON response
    ]


class LLMClientTestMixin:
    """Mixin class providing common test methods for LLM clients"""

    def assert_api_request_structure(
        self, mock_post, expected_url, expected_headers, expected_data_keys
    ):
        """Assert that the API request has the correct structure"""
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        self.assertEqual(args[0], expected_url)

        for header_key, header_value in expected_headers.items():
            self.assertIn(header_key, kwargs["headers"])
            if header_value:
                self.assertEqual(kwargs["headers"][header_key], header_value)

        for key in expected_data_keys:
            if "json" in kwargs:
                self.assertIn(key, kwargs["json"])
            elif "data" in kwargs:
                data = (
                    json.loads(kwargs["data"])
                    if isinstance(kwargs["data"], str)
                    else kwargs["data"]
                )
                self.assertIn(key, data)

    def create_mock_response(
        self, response_data, status_code=200, raise_exception=None
    ):
        """Create a mock response object"""
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = response_data
        mock_response.text = json.dumps(response_data) if response_data else ""

        if raise_exception:
            mock_response.raise_for_status.side_effect = raise_exception
        else:
            mock_response.raise_for_status.return_value = None

        return mock_response


class APIKeyTestMixin:
    """Mixin for testing API key handling"""

    def test_api_key_from_environment(self):
        """Test that API key is correctly read from environment"""
        with patch.dict(os.environ, {"TEST_API_KEY": "test_value"}):
            # Implementation depends on specific client
            pass

    def test_missing_api_key_handling(self):
        """Test behavior when API key is missing"""
        with patch.dict(os.environ, {}, clear=True):
            # Implementation depends on specific client
            pass


class NetworkErrorTestMixin:
    """Mixin for testing network error scenarios"""

    def test_connection_timeout(self):
        """Test handling of connection timeouts"""
        pass

    def test_ssl_error(self):
        """Test handling of SSL errors"""
        pass

    def test_dns_resolution_error(self):
        """Test handling of DNS resolution errors"""
        pass


class ResponseValidationTestMixin:
    """Mixin for testing response validation"""

    def test_json_decode_error(self):
        """Test handling of malformed JSON responses"""
        pass

    def test_unexpected_response_structure(self):
        """Test handling of unexpected response structure"""
        pass

    def test_empty_response_handling(self):
        """Test handling of empty responses"""
        pass


class BaseTestCase(
    unittest.TestCase,
    LLMClientTestMixin,
    APIKeyTestMixin,
    NetworkErrorTestMixin,
    ResponseValidationTestMixin,
):
    """Base test case that combines all mixins"""

    def setUp(self):
        """Set up common test fixtures"""
        self.fixtures = TestDataFixtures()
        self.maxDiff = None  # Show full diff for long strings

    def tearDown(self):
        """Clean up after tests"""
        pass


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions and fixtures"""

    def test_mock_response_creation(self):
        """Test MockResponse utility class"""
        # Test successful response
        response = MockResponse({"test": "data"}, 200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"test": "data"})
        response.raise_for_status()  # Should not raise

        # Test error response
        error_response = MockResponse(None, 500, "Internal Server Error")
        self.assertEqual(error_response.status_code, 500)
        self.assertEqual(error_response.text, "Internal Server Error")

        with self.assertRaises(ValueError):
            error_response.json()

        # Test response with exception
        exception_response = MockResponse(
            {"error": "unauthorized"},
            401,
            raise_for_status_exception=Exception("Unauthorized"),
        )

        with self.assertRaises(Exception):
            exception_response.raise_for_status()

    def test_fixtures_availability(self):
        """Test that test fixtures are available and valid"""
        fixtures = TestDataFixtures()

        # Test response fixtures
        self.assertIn("choices", fixtures.DEEPSEEK_SUCCESS_RESPONSE)
        self.assertIn("candidates", fixtures.GEMINI_SUCCESS_RESPONSE)
        self.assertIn("choices", fixtures.MISTRAL_SUCCESS_RESPONSE)
        self.assertIn("choices", fixtures.OPENROUTER_SUCCESS_RESPONSE)

        # Test prompt fixtures
        self.assertIsInstance(fixtures.SAMPLE_PROMPTS, list)
        self.assertTrue(len(fixtures.SAMPLE_PROMPTS) > 0)

        # Test response fixtures
        self.assertIsInstance(fixtures.SAMPLE_RESPONSES, list)
        self.assertTrue(len(fixtures.SAMPLE_RESPONSES) > 0)

    def test_edge_case_prompts(self):
        """Test edge case prompts are included in fixtures"""
        fixtures = TestDataFixtures()

        # Check for empty prompt
        self.assertIn("", fixtures.SAMPLE_PROMPTS)

        # Check for long prompt
        long_prompts = [p for p in fixtures.SAMPLE_PROMPTS if len(p) > 500]
        self.assertTrue(len(long_prompts) > 0)

        # Check for special character prompt
        special_char_prompts = [
            p for p in fixtures.SAMPLE_PROMPTS if any(ord(c) > 127 for c in p)
        ]
        self.assertTrue(len(special_char_prompts) > 0)

        # Check for multiline prompt
        multiline_prompts = [p for p in fixtures.SAMPLE_PROMPTS if "\n" in p]
        self.assertTrue(len(multiline_prompts) > 0)


if __name__ == "__main__":
    unittest.main()
