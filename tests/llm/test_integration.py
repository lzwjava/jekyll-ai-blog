import unittest
from unittest.mock import patch
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../scripts"))

from llm.deepseek_client import call_deepseek_api
from llm.gemini_client import call_gemini_api
from llm.mistral_client import call_mistral_api
from llm.openrouter_client import call_openrouter_api


class TestLLMIntegration(unittest.TestCase):
    """Integration tests for LLM clients

    These tests are designed to run against actual APIs when API keys are available.
    They are skipped if API keys are not set to avoid failures in CI/CD.
    """

    def setUp(self):
        """Set up integration test environment"""
        self.test_prompt = "Say hello in one word."
        self.timeout = 30  # seconds

        # Check which API keys are available
        self.deepseek_available = bool(os.getenv("DEEPSEEK_API_KEY"))
        self.gemini_available = bool(os.getenv("GEMINI_API_KEY"))
        self.mistral_available = bool(os.getenv("MISTRAL_API_KEY"))
        self.openrouter_available = bool(os.getenv("OPENROUTER_API_KEY"))

    @unittest.skipUnless(os.getenv("DEEPSEEK_API_KEY"), "DEEPSEEK_API_KEY not set")
    def test_deepseek_integration(self):
        """Test actual DeepSeek API integration"""
        start_time = time.time()
        result = call_deepseek_api(self.test_prompt)
        end_time = time.time()

        self.assertIsNotNone(result, "DeepSeek API should return a response")
        self.assertIsInstance(result, str, "Response should be a string")
        self.assertTrue(len(result) > 0, "Response should not be empty")
        self.assertLess(
            end_time - start_time,
            self.timeout,
            f"API call should complete within {self.timeout} seconds",
        )

    @unittest.skipUnless(os.getenv("GEMINI_API_KEY"), "GEMINI_API_KEY not set")
    def test_gemini_integration(self):
        """Test actual Gemini API integration"""
        start_time = time.time()
        result = call_gemini_api(self.test_prompt)
        end_time = time.time()

        self.assertIsNotNone(result, "Gemini API should return a response")
        self.assertIsInstance(result, str, "Response should be a string")
        self.assertTrue(len(result) > 0, "Response should not be empty")
        self.assertLess(
            end_time - start_time,
            self.timeout,
            f"API call should complete within {self.timeout} seconds",
        )

    @unittest.skipUnless(os.getenv("MISTRAL_API_KEY"), "MISTRAL_API_KEY not set")
    def test_mistral_integration(self):
        """Test actual Mistral API integration"""
        start_time = time.time()
        result = call_mistral_api(self.test_prompt)
        end_time = time.time()

        self.assertIsNotNone(result, "Mistral API should return a response")
        self.assertIsInstance(result, str, "Response should be a string")
        self.assertTrue(len(result) > 0, "Response should not be empty")
        self.assertLess(
            end_time - start_time,
            self.timeout,
            f"API call should complete within {self.timeout} seconds",
        )

    @unittest.skipUnless(os.getenv("OPENROUTER_API_KEY"), "OPENROUTER_API_KEY not set")
    def test_openrouter_integration(self):
        """Test actual OpenRouter API integration"""
        start_time = time.time()
        result = call_openrouter_api(self.test_prompt, "mistral-medium")
        end_time = time.time()

        self.assertIsNotNone(result, "OpenRouter API should return a response")
        self.assertIsInstance(result, str, "Response should be a string")
        self.assertTrue(len(result) > 0, "Response should not be empty")
        self.assertLess(
            end_time - start_time,
            self.timeout,
            f"API call should complete within {self.timeout} seconds",
        )

    def test_api_availability_summary(self):
        """Print summary of available APIs for testing"""
        summary = []
        if self.deepseek_available:
            summary.append("DeepSeek")
        if self.gemini_available:
            summary.append("Gemini")
        if self.mistral_available:
            summary.append("Mistral")
        if self.openrouter_available:
            summary.append("OpenRouter")

        print(
            f"\nAvailable APIs for integration testing: {', '.join(summary) if summary else 'None'}"
        )
        print("Set API keys as environment variables to enable integration tests")

        # This test always passes, it's just for information
        self.assertTrue(True)


class TestCrossClientCompatibility(unittest.TestCase):
    """Test compatibility and consistency across different LLM clients"""

    def setUp(self):
        """Set up cross-client compatibility tests"""
        self.simple_prompt = "What is 2+2?"
        self.math_prompt = "Calculate the square root of 16"
        self.creative_prompt = "Write one word that rhymes with 'cat'"

    def test_all_clients_handle_simple_math(self):
        """Test that all available clients can handle simple math questions"""
        clients_to_test = []

        if os.getenv("DEEPSEEK_API_KEY"):
            clients_to_test.append(("DeepSeek", lambda p: call_deepseek_api(p)))
        if os.getenv("GEMINI_API_KEY"):
            clients_to_test.append(("Gemini", lambda p: call_gemini_api(p)))
        if os.getenv("MISTRAL_API_KEY"):
            clients_to_test.append(("Mistral", lambda p: call_mistral_api(p)))
        if os.getenv("OPENROUTER_API_KEY"):
            clients_to_test.append(
                ("OpenRouter", lambda p: call_openrouter_api(p, "mistral-medium"))
            )

        if not clients_to_test:
            self.skipTest("No API keys available for cross-client testing")

        results = {}
        for client_name, client_func in clients_to_test:
            try:
                result = client_func(self.simple_prompt)
                results[client_name] = result
                self.assertIsNotNone(result, f"{client_name} should return a response")
                self.assertIsInstance(
                    result, str, f"{client_name} response should be a string"
                )
            except Exception as e:
                self.fail(f"{client_name} failed with error: {e}")

        # Print results for manual verification
        print(f"\nCross-client results for '{self.simple_prompt}':")
        for client_name, result in results.items():
            print(f"{client_name}: {result[:100]}{'...' if len(result) > 100 else ''}")

    def test_response_consistency(self):
        """Test that responses are consistent in format across clients"""
        if not any(
            [
                os.getenv("DEEPSEEK_API_KEY"),
                os.getenv("GEMINI_API_KEY"),
                os.getenv("MISTRAL_API_KEY"),
                os.getenv("OPENROUTER_API_KEY"),
            ]
        ):
            self.skipTest("No API keys available for consistency testing")

        # Test with a prompt that should have a definitive answer
        definitive_prompt = "What is the capital of Japan?"

        responses = []

        if os.getenv("DEEPSEEK_API_KEY"):
            try:
                response = call_deepseek_api(definitive_prompt)
                if response:
                    responses.append(("DeepSeek", response))
            except Exception:
                pass

        if os.getenv("GEMINI_API_KEY"):
            try:
                response = call_gemini_api(definitive_prompt)
                if response:
                    responses.append(("Gemini", response))
            except Exception:
                pass

        if os.getenv("MISTRAL_API_KEY"):
            try:
                response = call_mistral_api(definitive_prompt)
                if response:
                    responses.append(("Mistral", response))
            except Exception:
                pass

        if os.getenv("OPENROUTER_API_KEY"):
            try:
                response = call_openrouter_api(definitive_prompt, "mistral-medium")
                if response:
                    responses.append(("OpenRouter", response))
            except Exception:
                pass

        # All responses should contain "Tokyo" (case insensitive)
        for client_name, response in responses:
            self.assertIn(
                "Tokyo",
                response,
                f"{client_name} should mention Tokyo in response to capital of Japan",
            )

        print(f"\nConsistency test results for '{definitive_prompt}':")
        for client_name, response in responses:
            print(
                f"{client_name}: {response[:150]}{'...' if len(response) > 150 else ''}"
            )


class TestErrorHandlingIntegration(unittest.TestCase):
    """Test error handling in real-world scenarios"""

    def test_invalid_api_keys(self):
        """Test behavior with invalid API keys"""
        # Test with obviously invalid API keys
        with patch.dict(
            os.environ,
            {
                "DEEPSEEK_API_KEY": "invalid_key_12345",
                "GEMINI_API_KEY": "invalid_key_12345",
                "MISTRAL_API_KEY": "invalid_key_12345",
                "OPENROUTER_API_KEY": "invalid_key_12345",
            },
        ):
            # All should handle invalid keys gracefully
            self.assertIsNone(call_deepseek_api("test"))
            self.assertIsNone(call_gemini_api("test"))
            self.assertIsNone(call_mistral_api("test"))

            # OpenRouter raises exception for invalid keys
            with self.assertRaises(Exception):
                call_openrouter_api("test")

    def test_extreme_inputs(self):
        """Test clients with extreme inputs"""
        if not any(
            [
                os.getenv("DEEPSEEK_API_KEY"),
                os.getenv("GEMINI_API_KEY"),
                os.getenv("MISTRAL_API_KEY"),
                os.getenv("OPENROUTER_API_KEY"),
            ]
        ):
            self.skipTest("No API keys available for extreme input testing")

        # Test very long prompt (but not so long as to exceed API limits)
        long_prompt = "Explain this: " + "x" * 1000

        test_cases = [
            ("empty", ""),
            ("single_char", "a"),
            ("special_chars", "!@#$%^&*()"),
            ("unicode", "Hello 世界 🌍"),
            ("long", long_prompt[:500]),  # Truncate to avoid API limits
        ]

        for test_name, prompt in test_cases:
            print(
                f"\nTesting extreme input '{test_name}': {prompt[:50]}{'...' if len(prompt) > 50 else ''}"
            )

            if os.getenv("DEEPSEEK_API_KEY"):
                try:
                    result = call_deepseek_api(prompt)
                    print(
                        f"DeepSeek handled '{test_name}': {'Success' if result else 'Empty response'}"
                    )
                except Exception as e:
                    print(f"DeepSeek failed on '{test_name}': {str(e)[:100]}")

            if os.getenv("GEMINI_API_KEY"):
                try:
                    result = call_gemini_api(prompt)
                    print(
                        f"Gemini handled '{test_name}': {'Success' if result else 'Empty response'}"
                    )
                except Exception as e:
                    print(f"Gemini failed on '{test_name}': {str(e)[:100]}")


class TestPerformanceIntegration(unittest.TestCase):
    """Test performance characteristics of LLM clients"""

    @unittest.skipUnless(
        any(
            [
                os.getenv("DEEPSEEK_API_KEY"),
                os.getenv("GEMINI_API_KEY"),
                os.getenv("MISTRAL_API_KEY"),
                os.getenv("OPENROUTER_API_KEY"),
            ]
        ),
        "No API keys available for performance testing",
    )
    def test_response_times(self):
        """Test and compare response times across clients"""
        test_prompt = "Count from 1 to 5"
        performance_results = {}

        clients = []
        if os.getenv("DEEPSEEK_API_KEY"):
            clients.append(("DeepSeek", call_deepseek_api))
        if os.getenv("GEMINI_API_KEY"):
            clients.append(("Gemini", call_gemini_api))
        if os.getenv("MISTRAL_API_KEY"):
            clients.append(("Mistral", call_mistral_api))
        if os.getenv("OPENROUTER_API_KEY"):
            clients.append(
                ("OpenRouter", lambda p: call_openrouter_api(p, "mistral-medium"))
            )

        for client_name, client_func in clients:
            start_time = time.time()
            try:
                result = client_func(test_prompt)
                end_time = time.time()

                if result:
                    performance_results[client_name] = {
                        "time": end_time - start_time,
                        "success": True,
                        "response_length": len(result),
                    }
                else:
                    performance_results[client_name] = {
                        "time": end_time - start_time,
                        "success": False,
                        "response_length": 0,
                    }
            except Exception as e:
                end_time = time.time()
                performance_results[client_name] = {
                    "time": end_time - start_time,
                    "success": False,
                    "error": str(e)[:100],
                }

        # Print performance summary
        print(f"\nPerformance results for '{test_prompt}':")
        for client_name, result in performance_results.items():
            status = "✓" if result["success"] else "✗"
            time_ms = result["time"] * 1000
            print(f"{client_name}: {status} {time_ms:.0f}ms", end="")
            if result["success"]:
                print(f" ({result['response_length']} chars)")
            elif "error" in result:
                print(f" - {result['error']}")
            else:
                print(" - No response")

        # Assert that at least one client succeeded
        successful_clients = [
            name for name, result in performance_results.items() if result["success"]
        ]
        self.assertTrue(
            len(successful_clients) > 0, "At least one client should succeed"
        )


if __name__ == "__main__":
    # Run with verbose output to see the integration test results
    unittest.main(verbosity=2)
