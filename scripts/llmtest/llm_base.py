import requests
import json
import os
from openai import OpenAI
import time


# Initialize DeepSeek client if needed
def initialize_deepseek_client():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: DEEPSEEK_API_KEY environment variable not set.")
        exit()
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def call_deepseek_api():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: DEEPSEEK_API_KEY environment variable not set.")
        exit()
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    return client


def call_gemini_api(prompt, retries=3, backoff_factor=1):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        exit()
    base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    url = f"{base_url}"
    params = {"key": api_key}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    print(f"Input to Gemini API: {payload}")

    for attempt in range(retries):
        try:
            response = requests.post(url, json=payload, params=params)
            response.raise_for_status()
            response_json = response.json()
            print(response_json)
            return response_json
        except requests.exceptions.RequestException as e:
            response_json = e.response.json() if e.response else None
            print(f"Gemini API Error: {e} - {response_json}")
            if e.response and e.response.status_code == 429:
                time.sleep(backoff_factor * (2**attempt))  # Exponential backoff
            else:
                raise Exception(f"Gemini API Error: {e} - {response_json}")
    return None


def call_mistral_api(prompt, model="mistral-small-2501", process_response=True):
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("Error: MISTRAL_API_KEY environment variable not set.")
        exit()
    base_url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    url = base_url
    data = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    print(f"Input to Mistral API: {data}")
    print(f"Mistral API URL: {url}")
    print(f"Mistral API Headers: {headers}")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        print(response_json)
        # if response_json and response_json['choices']:
        #    content = response_json['choices'][0]['message']['content']
        #    return content
        # else:
        #    print(f"Mistral API Error: Invalid response format: {response_json}")
        return response_json
    except requests.exceptions.RequestException as e:
        print(f"Mistral API Error: {e}")
        stre = f"{e}"
        if "429" in stre:
            print("Too many requests, sleeping for 10 seconds and retrying")
            time.sleep(10)
            return call_mistral_api(prompt, model, process_response)

        raise e


def call_ollama_api(prompt, model):
    base_url = "http://localhost:11434/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    url = base_url
    data = {"messages": [{"role": "user", "content": prompt}], "model": model}
    print(f"Input to API: {data}")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ollama API Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None


def call_llama_api(prompt):
    base_url = "http://localhost:8080/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    url = base_url
    data = {"messages": [{"role": "user", "content": prompt}]}
    print(f"Input to API: {data}")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Llama API Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None


def call_grok_api(prompt):
    api_key = os.environ.get("GROK_API_KEY")
    if not api_key:
        print("Error: GROK_API_KEY environment variable not set.")
        return None
    base_url = "https://api.x.ai/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    url = base_url
    data = {"model": "grok-2-latest", "messages": [{"role": "user", "content": prompt}]}
    print(f"Input to Grok API: {data}")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        json_response = response.json()
        return json_response
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        if e.response:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None
