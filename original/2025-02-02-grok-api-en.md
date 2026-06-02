---
audio: false
generated: false
image: false
lang: en
layout: post
title: Testing Grok API
translated: false
type: post
---

- It is ok to use China-issued Visa card.

- [https://console.x.ai](https://console.x.ai)

- `grok-2-latest` model: Input 2 USD per million tokens, Output 10 USD per million tokens.

Code:

```python
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.environ.get("GROK_API_KEY")
if not GROK_API_KEY:
    raise ValueError("GROK_API_KEY environment variable not set")

url = "https://api.x.ai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GROK_API_KEY}"
}
data = {
    "model": "grok-2-latest",
    "messages": [
        {
            "role": "user",
            "content": "Explain how AI works"
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    json_response = response.json()
    if 'choices' in json_response and json_response['choices']:
        first_choice = json_response['choices'][0]
        if 'message' in first_choice and 'content' in first_choice['message']:
            print(first_choice['message']['content'])
        else:
            print("Unexpected response format: message or content missing")
    else:
        print("No choices found in the response")
except requests.exceptions.RequestException as e:
    print(f"Error during API request: {e}")
    if e.response:
        print(f"Response status code: {e.response.status_code}")
        print(f"Response content: {e.response.text}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")

```
