import requests
import os

# Get the API key from environment variable or replace with your key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise Exception("OPENROUTER_API_KEY environment variable is not set or is empty")


MODEL_MAPPING = {
    "claude-opus": "anthropic/claude-opus-4.1",
    "claude-sonnet": "anthropic/claude-4.5-sonnet",
    "claude-haiku": "anthropic/claude-4.5-haiku",
    "gemini-flash": "google/gemini-3-flash-preview",
    "gemini-pro": "google/gemini-3-pro-preview",
    "kimi": "moonshotai/kimi-k2",
    "deepseek": "deepseek/deepseek-v3.2",
    "mistral": "mistralai/mistral-medium-3.1",
    "qwen":"qwen/qwen3-coder",
    "gpt": "openai/gpt-5.2",
    "grok-code": "x-ai/grok-code-fast-1",
    "grok-fast": "x-ai/grok-4.1-fast",
    "glm": "z-ai/glm-4.7",
    "minimax": "minimax/minimax-m2",
    "kimi-thinking": "moonshotai/kimi-k2-thinking"
}

DEFAULT_TOKENS = {
    "claude-opus": 8192,
    "claude-sonnet": 8192,
    "gemini-flash": 400000,
    "gemini-pro": 8192,
    "kimi": 32768,
    "deepseek": 32768,
    "mistral": 32768,
    "qwen": 32768,
    "gpt": 8192,
    "grok-code": 62144,
    "grok-fast": 61072,
    "glm": 32768,
    "minimax": 32768,
    "kimi-thinking": 32768    
}


def call_openrouter_api_with_messages(messages, model="mistral", max_tokens=None, debug=False):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    # Check if the model exists in the mapping
    if model not in MODEL_MAPPING:
        raise Exception(f"Model '{model}' not found in MODEL_MAPPING")

    # Use provided max_tokens or default for this model
    if max_tokens is None:
        max_tokens = DEFAULT_TOKENS.get(model, 4096)

    data = {"model": MODEL_MAPPING[model], "messages": messages, "max_tokens": max_tokens}

    if debug:
        print(f"Request URL: {url}")
        print(f"Request Data: {data}")

    try:
        response = requests.post(url, headers=headers, json=data)
        if debug:
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


def call_openrouter_api(prompt, model="mistral", max_tokens=None, debug=False):
    messages = [{"role": "user", "content": prompt}]
    return call_openrouter_api_with_messages(messages, model, max_tokens, debug)


if __name__ == "__main__":
    import sys
    import subprocess

    # Read from stdin if piped, else try macOS clipboard via pbpaste, else use default prompt
    if not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        try:
            content = subprocess.check_output(["pbpaste"], text=True)
        except Exception:
            content = "Hello, 9.11 or 9.9, which one is bigger? "

    if not content or not content.strip():
        content = "Hello, 9.11 or 9.9, which one is bigger? "

    model = os.getenv("OPENROUTER_MODEL", "mistral-medium")

    try:
        result = call_openrouter_api(content, model, debug=True)
        print(result)
    except Exception as e:
        print(f"Error: {e}")