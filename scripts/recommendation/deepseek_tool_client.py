import os
import requests
from types import SimpleNamespace

MODEL_NAME = "deepseek-chat"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"


def parse_to_namespace(data):
    if isinstance(data, dict):
        return SimpleNamespace(**{k: parse_to_namespace(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [parse_to_namespace(item) for item in data]
    else:
        return data


def call_deepseek_api(messages, tools=None):
    if not DEEPSEEK_API_KEY:
        print("Error: DEEPSEEK_API_KEY is not set in .env file.")
        return None
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        }
        data = {"model": MODEL_NAME, "messages": messages, "stream": False}
        if tools:
            data["tools"] = tools
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        if (
            not response_json
            or not response_json.get("choices")
            or not response_json["choices"][0].get("message")
        ):
            print("  Error: Response is empty or invalid:")
            print(response.content)
            return None
        choice = response_json["choices"][0]
        if choice.get("finish_reason") not in ("stop", "length", "tool_calls"):
            print(
                "  Error: Did not finish with 'stop', 'length', or 'tool_calls' reason:"
            )
            print(response.content)
            return None
        print("API call successful")
        # Return the raw message dictionary instead of converting to SimpleNamespace
        return choice["message"]
    except requests.exceptions.RequestException as e:
        print(f"  API call failed with error: {e}")
        return None


if __name__ == "__main__":
    messages = [
        {
            "role": "user",
            "content": "Can you tell me the current weather in San Francisco, CA?",
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]
    print(call_deepseek_api(messages=messages, tools=tools))
