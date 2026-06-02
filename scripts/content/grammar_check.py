import os
from dotenv import load_dotenv
import argparse
import requests
from datetime import datetime

load_dotenv()


def call_mistral_api(prompt):
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("Error: MISTRAL_API_KEY environment variable not set.")
        return None

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        response_json = response.json()
        if response_json and response_json["choices"]:
            content = response_json["choices"][0]["message"]["content"]
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


def main():
    parser = argparse.ArgumentParser(
        description="English grammar 'compiler' for Markdown files using Mistral API. Reports one error at a time."
    )
    parser.add_argument("file", help="The Markdown file to check for grammar errors.")
    parser.add_argument(
        "--skip-lines",
        nargs="+",
        type=int,
        default=[],
        help="Line numbers to skip checking for errors.",
    )
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.")
        return

    with open(args.file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Prepare numbered lines for the prompt
    numbered_lines = [f"Line {i + 1}: {line.rstrip()}" for i, line in enumerate(lines)]
    content = "\n".join(numbered_lines)

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_text = f"Today's date and time is {current_datetime}.\n"

    skip_text = ""
    if args.skip_lines:
        skip_text = f"Ignore any errors in the following lines: {', '.join(map(str, args.skip_lines))}.\n"

    prompt = f"""You are a lenient English grammar checker suitable for daily writing. Analyze the provided text (which is from a Markdown file) for significant grammar errors only. Ignore minor issues, Markdown syntax, formatting, style, or any non-grammar issues. Focus solely on English grammar in the text content.

{date_text}{skip_text}Scan the text line by line in order. Report ONLY the very first grammar error you encounter. Do not report multiple errors or any other information.

If there are no grammar errors at all, respond with exactly this: 'No grammar errors found.'

If you find an error, respond in this exact format (no additional text):
Error at line <line_number>: <quote the original problematic text snippet>
Description: <brief description of the grammar error>
Suggestion: <suggested correction for the snippet>

Text to check:
{content}
"""

    response = call_mistral_api(prompt)
    if response:
        response = response.strip()
        if response == "No grammar errors found.":
            print(response)
        else:
            lines = response.split("\n")
            if len(lines) == 3:
                processed_lines = []
                for line in lines:
                    if ":" in line:
                        left, right = line.split(":", 1)
                        left = left.strip()
                        right = right.strip()
                        processed_lines.append(f"{left.ljust(30)}:{right}")
                print("\n".join(processed_lines))
            else:
                print(response)
    else:
        print("Failed to get a response from the Mistral API.")


if __name__ == "__main__":
    main()
