#!/usr/bin/env python3

import os
import requests


def main():
    api_key = os.environ.get("PINCC_API_KEY")
    if not api_key:
        raise ValueError("PINCC_API_KEY environment variable not set")

    response = requests.post(
        "https://v2-as.pincc.ai/v1/messages",
        headers={
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "claude-code/2.1.76 (external)",
            "anthropic-beta": "claude-code-20250219",
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Hello!"}],
        },
    )

    print(response.json())


if __name__ == "__main__":
    main()
