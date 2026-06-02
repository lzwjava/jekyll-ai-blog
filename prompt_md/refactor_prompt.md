# Refactor Prompt

## Instructions

Refactor the Python code below, focusing on:

- Improving readability
- Enhancing maintainability
- Following Python best practices
- Use if __name__ == "__main__" to do testing
- if there is missing param, use arg.parse

## Target File

`scripts/prompt/refactor_prompt.py`

## Code to Refactor

```python
import argparse
import os
import sys
from sample_code import sample_code  # Importing the sample code function

def generate_refactor_prompt(file_path):
    """Generate a refactor prompt for the given Python file with proper markdown formatting."""

    sample = sample_code()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        prompt = f"""# Refactor Prompt

## Instructions
Refactor the Python code below, focusing on:
- Improving readability
- Enhancing maintainability
- Following Python best practices
- Use if __name__ == "__main__" to do testing
- if there is missing param, use arg.parse

## Target File
`{file_path}`

## Code to Refactor
```python
{content}
```

## Sample Reference Code

```python
{sample}
```

"""
        return prompt
    except FileNotFoundError:
        return f"Error: The file {file_path} was not found."
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def save_prompt_to_md(prompt, original_path):
    """Save the generated prompt to a markdown file in scripts/prompt_md/ directory."""
    try:
        # Get the base filename without extension
        base_name = os.path.basename(original_path)
        file_name = os.path.splitext[base_name](0) + ".md"

        # Define the output directory
        output_dir = "scripts/prompt_md"
        os.makedirs(output_dir, exist_ok=True)

        # Define the full output path
        output_path = os.path.join(output_dir, file_name)

        # Save the prompt to the markdown file
        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(prompt)
        return f"Prompt saved to {output_path}"
    except Exception as e:
        return f"Error saving prompt to markdown file: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a refactor prompt for a Python file and save it as markdown.")
    parser.add_argument("file_path", help="Path to the Python file to refactor")

    # Add test mode flag
    parser.add_argument("--test", action="store_true", help="Run in test mode with sample input")

    args = parser.parse_args()

    if args.test:
        # Test mode - use the script itself as sample input
        test_file = os.path.abspath(__file__)
        prompt = generate_refactor_prompt(test_file)
        print("=== TEST MODE ===")
        print(prompt)
        print(save_prompt_to_md(prompt, test_file))
    elif not args.file_path:
        parser.print_help()
        print("\nError: file_path argument is required")
        sys.exit(1)
    else:
        # Normal mode
        prompt = generate_refactor_prompt(args.file_path)
        print(prompt)
        print(save_prompt_to_md(prompt, args.file_path))

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
