import os
import requests
import json

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def call_gemini_api(prompt):
    api_key = GEMINI_API_KEY
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None

    url = f"{GEMINI_API_URL}?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(data), timeout=30
        )
        response.raise_for_status()
        json_response = response.json()
        if "candidates" in json_response and json_response["candidates"]:
            first_candidate = json_response["candidates"][0]
            if "content" in first_candidate and "parts" in first_candidate["content"]:
                first_part = first_candidate["content"]["parts"][0]
                if "text" in first_part:
                    return first_part["text"]
                else:
                    print("No text found in the response")
                    return None
            else:
                print("Unexpected response format: content or parts missing")
                return None
        else:
            print("No candidates found in the response")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during Gemini API request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None


if __name__ == "__main__":
    print(call_gemini_api("hi"))
