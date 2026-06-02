import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_groq_api(prompt: str):
    api_key = GROQ_API_KEY
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set.")
        return None

    url = GROQ_API_URL
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        response_json = response.json()
        if response_json and response_json.get("choices"):
            return response_json["choices"][0]["message"]["content"]
        else:
            print(f"Groq API Error: Invalid response format: {response_json}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Groq API Error: {e}")
        if getattr(e, "response", None):
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return None


if __name__ == "__main__":
    print(call_groq_api("Explain the importance of fast language models"))
