import os
import requests

MODEL_NAME = "deepseek-chat"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"


def call_deepseek_api(prompt):
    if not DEEPSEEK_API_KEY:
        print("Error: DEEPSEEK_API_KEY is not set in .env file.")
        return None
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        }
        data = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        if (
            not response_json
            or not response_json.get("choices")
            or not response_json["choices"][0]["message"]["content"]
        ):
            print("  Error: Translation response is empty or invalid:")
            print(response.content)
            return None
        if response_json["choices"][0].get("finish_reason") not in ("stop", "length"):
            print("  Error: Translation did not finish with 'stop' or 'length' reason:")
            print(response.content)
            return None
        print("Translation successful")
        translated_text = response_json["choices"][0]["message"]["content"]
        return translated_text
    except requests.exceptions.RequestException as e:
        print(f"  Translation failed with error: {e}")
        return None


if __name__ == "__main__":
    print(call_deepseek_api("hi"))
