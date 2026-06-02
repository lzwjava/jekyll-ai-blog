import pytest
import os
import sys
from unittest.mock import patch

# Add the scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../scripts"))


@pytest.fixture
def mock_env_no_keys():
    """Fixture that removes all API keys from environment"""
    with patch.dict(os.environ, {}, clear=True):
        yield


@pytest.fixture
def mock_env_with_keys():
    """Fixture that provides mock API keys"""
    with patch.dict(
        os.environ,
        {
            "DEEPSEEK_API_KEY": "test_deepseek_key",
            "GEMINI_API_KEY": "test_gemini_key",
            "MISTRAL_API_KEY": "test_mistral_key",
            "OPENROUTER_API_KEY": "test_openrouter_key",
        },
    ):
        yield


@pytest.fixture
def sample_prompts():
    """Fixture providing sample prompts for testing"""
    return [
        "Hello",
        "What is 2+2?",
        "Write a Python function",
        "",  # Empty prompt
        "Prompt with émojis 🚀",
        "A" * 100,  # Long prompt
    ]


@pytest.fixture
def sample_responses():
    """Fixture providing sample API responses for different clients"""
    return {
        "deepseek": {
            "choices": [
                {
                    "message": {"content": "Hello! How can I help you?"},
                    "finish_reason": "stop",
                }
            ]
        },
        "gemini": {
            "candidates": [
                {"content": {"parts": [{"text": "Hello! How can I assist you today?"}]}}
            ]
        },
        "mistral": {
            "choices": [
                {"message": {"content": "Hello! I'm Mistral, how can I help you?"}}
            ]
        },
        "openrouter": {"choices": [{"message": {"content": "Hello from OpenRouter!"}}]},
    }


@pytest.fixture
def error_responses():
    """Fixture providing error responses for testing"""
    return {
        "empty": {},
        "no_choices": {"choices": []},
        "no_candidates": {"candidates": []},
        "malformed": {"invalid": "structure"},
        "empty_content": {
            "choices": [{"message": {"content": ""}, "finish_reason": "stop"}]
        },
    }


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "network: mark test as requiring network access")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Mark integration tests
        if "test_integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.network)

        # Mark unit tests
        elif any(
            x in item.nodeid
            for x in ["test_deepseek", "test_gemini", "test_mistral", "test_openrouter"]
        ):
            item.add_marker(pytest.mark.unit)

        # Mark slow tests
        if any(x in item.name.lower() for x in ["performance", "stress", "load"]):
            item.add_marker(pytest.mark.slow)


@pytest.fixture(autouse=True)
def cleanup_environment():
    """Automatically cleanup environment after each test"""
    yield
    # Cleanup code runs after each test
    pass
