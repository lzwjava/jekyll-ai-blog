# LLM Client Tests

This directory contains comprehensive tests for the LLM client modules in `scripts/llm/`.

## Test Structure

```
tests/llm/
├── __init__.py              # Package initialization
├── conftest.py              # Pytest configuration and fixtures
├── pytest.ini              # Pytest settings
├── requirements.txt         # Test dependencies
├── README.md               # This file
├── test_deepseek_client.py  # Tests for DeepSeek client
├── test_gemini_client.py    # Tests for Gemini client
├── test_mistral_client.py   # Tests for Mistral client
├── test_openrouter_client.py # Tests for OpenRouter client
├── test_integration.py      # Integration tests across clients
└── test_utils.py           # Test utilities and fixtures
```

## Test Types

### Unit Tests
- **File Pattern**: `test_*_client.py`
- **Description**: Test individual client functions in isolation using mocks
- **Dependencies**: None (uses mocks for API calls)
- **Run Command**: `python -m pytest tests/llm/test_*_client.py -v`

### Integration Tests
- **File**: `test_integration.py`
- **Description**: Test actual API calls with real services
- **Dependencies**: Requires valid API keys set as environment variables
- **Run Command**: `python -m pytest tests/llm/test_integration.py -v`

### Utility Tests
- **File**: `test_utils.py`
- **Description**: Test helper functions and test fixtures
- **Dependencies**: None
- **Run Command**: `python -m pytest tests/llm/test_utils.py -v`

## Setup

### Install Dependencies
```bash
cd tests/llm
pip install -r requirements.txt
```

### Environment Variables
For integration tests, set the following environment variables:
```bash
export DEEPSEEK_API_KEY="your_deepseek_key"
export GEMINI_API_KEY="your_gemini_key"
export MISTRAL_API_KEY="your_mistral_key"
export OPENROUTER_API_KEY="your_openrouter_key"
```

**Note**: Integration tests will be skipped if API keys are not set.

## Running Tests

### Run All Tests
```bash
python -m pytest tests/llm/ -v
```

### Run Only Unit Tests
```bash
python -m pytest tests/llm/ -m unit -v
```

### Run Only Integration Tests
```bash
python -m pytest tests/llm/ -m integration -v
```

### Run Tests with Coverage
```bash
python -m pytest tests/llm/ --cov=scripts.llm --cov-report=html -v
```

### Run Specific Client Tests
```bash
python -m pytest tests/llm/test_deepseek_client.py -v
python -m pytest tests/llm/test_gemini_client.py -v
python -m pytest tests/llm/test_mistral_client.py -v
python -m pytest tests/llm/test_openrouter_client.py -v
```

### Run Tests Excluding Slow Tests
```bash
python -m pytest tests/llm/ -v -m "not slow"
```

## Test Coverage

The tests cover the following scenarios:

### For Each Client
- ✅ Successful API calls
- ✅ Missing API keys
- ✅ Network errors and timeouts
- ✅ HTTP errors (4xx, 5xx)
- ✅ Malformed JSON responses
- ✅ Empty responses
- ✅ Invalid response structures
- ✅ Special characters and Unicode
- ✅ Edge cases (empty prompts, long prompts)

### Integration Tests
- ✅ Cross-client compatibility
- ✅ Performance comparison
- ✅ Error handling consistency
- ✅ Response format validation

### Utility Tests
- ✅ Mock response creation
- ✅ Test fixture availability
- ✅ Helper function validation

## Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests (no external dependencies)
- `@pytest.mark.integration` - Integration tests (require API keys)
- `@pytest.mark.slow` - Tests that may take longer to run
- `@pytest.mark.network` - Tests requiring network access

## Debugging Tests

### Verbose Output
```bash
python -m pytest tests/llm/ -v -s
```

### Stop on First Failure
```bash
python -m pytest tests/llm/ -v -x
```

### Run Specific Test Function
```bash
python -m pytest tests/llm/test_deepseek_client.py::TestDeepseekClient::test_successful_api_call -v
```

### Debug Mode
```bash
python -m pytest tests/llm/ --pdb
```

## Contributing

When adding new LLM clients:

1. Create a new test file: `test_new_client.py`
2. Follow the existing test patterns
3. Include all standard test scenarios
4. Add integration tests in `test_integration.py`
5. Update this README with the new client

### Test Template

```python
import unittest
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../scripts'))

from llm.new_client import call_new_api

class TestNewClient(unittest.TestCase):

    @patch.dict(os.environ, {'NEW_API_KEY': 'test_key'})
    @patch('llm.new_client.requests.post')
    def test_successful_api_call(self, mock_post):
        # Implementation here
        pass

    # Add more tests following existing patterns
```

## Continuous Integration

These tests are designed to work in CI/CD environments:

- Unit tests run without external dependencies
- Integration tests are skipped when API keys are not available
- All tests have reasonable timeouts
- Mock objects prevent actual API calls in unit tests

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `scripts` directory is in Python path
2. **API Key Errors**: Check environment variables are set correctly
3. **Network Timeouts**: Integration tests may fail with slow connections
4. **Rate Limits**: Some APIs have rate limits that may affect integration tests

### Getting Help

- Check test output for specific error messages
- Run with `-v` flag for verbose output
- Use `--tb=long` for detailed tracebacks
- Consult individual test files for specific test documentation
