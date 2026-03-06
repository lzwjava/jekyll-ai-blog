import os
import requests
import base64
import argparse

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def encode_image_to_base64(image_path):
    """Encode image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def mistral_ocr(image_path, api_key):
    """
    Extract text from image using Mistral's vision model
    """
    # Encode image
    base64_image = encode_image_to_base64(image_path)

    # API endpoint
    url = "https://api.mistral.ai/v1/chat/completions"

    # Headers
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    # Payload
    payload = {
        "model": "pixtral-12b-2409",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all text from this image. Return only the text content without any additional formatting or explanation.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 1000,
    }

    # Make request
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract text from image using Mistral OCR"
    )
    parser.add_argument("image_path", help="Path to the image file")
    args = parser.parse_args()

    # Use environment variable
    if not MISTRAL_API_KEY:
        print("Error: MISTRAL_API_KEY environment variable not set")
        exit(1)

    try:
        extracted_text = mistral_ocr(args.image_path, MISTRAL_API_KEY)
        print("Extracted text:")
        print(extracted_text)
    except Exception as e:
        print(f"Error: {e}")
