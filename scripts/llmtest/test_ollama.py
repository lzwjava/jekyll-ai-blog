import requests
import json


def _call_ollama_api(prompt, model):
    url = "http://192.168.1.3:11434/v1/chat/completions"
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": model,
        "stream": True,  # Enable streaming
    }
    headers = {"Content-Type": "application/json"}
    print(f"Input to API: {data}")
    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(data), stream=True, timeout=30
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        # Process the streaming response
        full_response = ""
        for chunk in response.iter_lines():
            if chunk:
                decoded_chunk = chunk.decode("utf-8")
                # Remove 'data: ' prefix and parse JSON
                if decoded_chunk.startswith("data: "):
                    json_string = decoded_chunk[5:]  # Remove 'data: ' prefix
                    if json_string.strip() == "[DONE]":
                        break  # End of stream

                    try:
                        json_data = json.loads(json_string)
                        if (
                            "choices" in json_data
                            and len(json_data["choices"]) > 0
                            and "delta" in json_data["choices"][0]
                            and "content" in json_data["choices"][0]["delta"]
                        ):
                            content = json_data["choices"][0]["delta"]["content"]
                            full_response += content
                            print(
                                content, end="", flush=True
                            )  # Print chunk incrementally
                    except json.JSONDecodeError as e:
                        print(f"JSONDecodeError: {e}")
                        print(f"Problematic chunk: {decoded_chunk}")
                        continue  # Skip to the next chunk
        print()  # newline after stream
        return full_response

    except requests.exceptions.RequestException as e:
        print(f"Ollama API Error: {e}")
        return ""


if __name__ == "__main__":
    # Example usage:
    prompt = input("Enter your prompt: ")
    model = "deepseek-r1:14b"

    response = _call_ollama_api(prompt, model)
    print(f"Ollama API Response: {response}")
