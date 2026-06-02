# Refactor Prompt

## Instructions
Refactor the Python code below, focusing on:
- Improving readability
- Enhancing maintainability
- Following Python best practices
- Added if __name__ == "__main__": to ensure that the script can be both imported as a module and run as a standalone script.
- Do not use main() function, use other meaningful function names to let it import from other scripts.
- Used argparse to allow for flexible input of the params.
- Do not need docstring in each function.
- The code is divided into smaller, reusable functions, each with a single responsibility.
- Improved variable names and overall structure for better readability.
- Although not explicitly added, the structure now makes it easier to add error handling where necessary.
- Only output the refactored code without any additional comments or explanations.

## Target File
`scripts/prompt/add_prompt.py`

## Code to Refactor
```python
import os
import pyperclip

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the scripts/prompt_md/ directory
prompt_dir = os.path.join(os.path.dirname(script_dir), 'prompt_md')

# Create the directory if it doesn't exist
os.makedirs(prompt_dir, exist_ok=True)

# Path to the prompt.md file
prompt_file = os.path.join(prompt_dir, 'prompt.md')

# Get the prompt from clipboard
new_prompt = pyperclip.paste().strip()

# Check if the file exists and has content
if os.path.exists(prompt_file) and os.path.getsize(prompt_file) > 0:
    separator = '\n---\n'
else:
    separator = ''

# Append the new prompt
with open(prompt_file, 'a') as f:
    f.write(separator + new_prompt)
```

## Sample Reference Code
```python
import os
import requests

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def call_mistral_api(prompt):
    api_key = MISTRAL_API_KEY
    if not api_key:
        print("Error: MISTRAL_API_KEY environment variable not set.")
        return None

    url = MISTRAL_API_URL
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        if response_json and response_json['choices']:
            content = response_json['choices'][0]['message']['content']
            return content
        else:
            print(f"Mistral API Error: Invalid response format: {response_json}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Mistral API Error: {e}")
        if e.response:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    print(call_mistral_api('hi'))
```
