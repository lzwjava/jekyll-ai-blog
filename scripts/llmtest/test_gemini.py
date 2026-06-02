import os
import requests
import json

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
headers = {"Content-Type": "application/json"}
data = {"contents": [{"parts": [{"text": "Explain how AI works"}]}]}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    response.raise_for_status()  # Raise an exception for bad status codes

    json_response = response.json()

    if "candidates" in json_response and json_response["candidates"]:
        first_candidate = json_response["candidates"][0]
        if "content" in first_candidate and "parts" in first_candidate["content"]:
            first_part = first_candidate["content"]["parts"][0]
            if "text" in first_part:
                print(first_part["text"])
            else:
                print("No text found in the response")
        else:
            print("Unexpected response format: content or parts missing")
    else:
        print("No candidates found in the response")

except requests.exceptions.RequestException as e:
    print(f"Error during API request: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
