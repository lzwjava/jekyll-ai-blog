import subprocess
import os
import argparse
import requests

from dotenv import load_dotenv

load_dotenv()


# OpenRouter API client code (self-contained)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL_MAPPING = {
    "claude-opus": "anthropic/claude-opus-4.1",
    "claude-sonnet": "anthropic/claude-4.5-sonnet",
    "gemini-flash": "google/gemini-3-flash-preview",
    "gemini-pro": "google/gemini-3-pro-preview",
    "kimi": "moonshotai/kimi-k2",
    "deepseek": "deepseek/deepseek-v3.2",
    "mistral": "mistralai/mistral-medium-3.1",
    "qwen": "qwen/qwen3-coder",
    "gpt": "openai/gpt-5.1",
    "grok-code": "x-ai/grok-code-fast-1",
    "grok-fast": "x-ai/grok-4.1-fast",
    "glm": "z-ai/glm-4.7",
    "minimax": "minimax/minimax-m2",
    "kimi-thinking": "moonshotai/kimi-k2-thinking",
}


def call_openrouter_api(prompt, model="gemini-flash", debug=False):
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY environment variable not set.")
        return None

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    # Check if the model exists in the mapping
    if model not in MODEL_MAPPING:
        print(f"Error: Model '{model}' not found in MODEL_MAPPING")
        return None

    messages = [{"role": "user", "content": prompt}]
    data = {"model": MODEL_MAPPING[model], "messages": messages}

    if debug:
        print(f"Request URL: {url}")
        print(f"Request Data: {data}")

    try:
        response = requests.post(url, headers=headers, json=data)
        if debug:
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")

        if response.status_code == 200:
            response_json = response.json()
            if (
                response_json
                and "choices" in response_json
                and response_json["choices"]
            ):
                content = response_json["choices"][0]["message"]["content"]
                return content.strip()
            else:
                print(f"OpenRouter API Error: Invalid response format: {response_json}")
                return None
        else:
            print(f"OpenRouter API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"OpenRouter API Error: {str(e)}")
        return None


def gitmessageai(
    push=True,
    only_message=False,
    model="gemini-flash",
    allow_pull_push=False,
    type="file",
):
    # Stage all changes
    subprocess.run(["git", "add", "-A"], check=True)

    # Get a detailed summary of the changes
    diff_process = subprocess.run(
        ["git", "diff", "--staged", "--unified=0"],
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
        errors="replace",
    )
    diff_output = diff_process.stdout

    if not diff_output:
        print("No changes to commit.")
        return

    file_changes = []
    if type == "file":
        current_file = None
        lines = diff_output.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("diff --git"):
                parts = line.split(" ")
                if len(parts) >= 4:
                    file_a = parts[2][2:]
                    file_b = parts[3][2:]
                    if file_a == file_b:
                        if i + 1 < len(lines) and "deleted file mode" in lines[i + 1]:
                            file_changes.append(f"Deleted file {file_a}")
                            i += 1
                        elif i + 1 < len(lines) and "new file mode" in lines[i + 1]:
                            file_changes.append(f"Added file {file_a}")
                            i += 1
                        elif i + 1 < len(lines):
                            file_changes.append(f"Updated file {file_a}")
                            i += 1
                    else:
                        if i + 1 < len(lines) and "similarity index" in lines[i + 1]:
                            file_changes.append(f"Renamed file {file_a} to {file_b}")
                            i += 1
            i += 1

        for change in file_changes:
            print(change)

        if not file_changes:
            print("No changes to commit.")
            return

        # Prepare the prompt for the AI
        prompt = f"""
Generate a concise commit message in Conventional Commits format for the following code changes.
Use one of the following types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, or revert.
If applicable, include a scope in parentheses to describe the part of the codebase affected.
The commit message should not exceed 70 characters. Just give the commit message, without any leading or trailing notes.

Changed files:
{", ".join(file_changes[:20])}

"""
    elif type == "content":
        # Get a detailed summary of the changes
        diff_process = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
            errors="replace",
        )
        diff_output = diff_process.stdout

        if not diff_output:
            print("No changes to commit.")
            return

        # Limit the diff_output to 2000 characters
        diff_output = diff_output[:2000]

        # Prepare the prompt for the AI
        prompt = f"""
Generate a concise commit message in Conventional Commits format for the following code changes.
Use one of the following types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, or revert.
If applicable, include a scope in parentheses to describe the part of the codebase affected.
The commit message should not exceed 70 characters. Just give the commit message, without any leading or trailing notes.

Code changes:
{diff_output}

"""
    else:
        print(f"Error: Invalid type specified: {type}")
        return

    # Call OpenRouter API
    commit_message = call_openrouter_api(prompt, model=model)
    if not commit_message:
        print("Error: No response from OpenRouter API.")
        return

    # Clean up the commit message
    if commit_message and "```" in commit_message:
        commit_message = commit_message.replace("```", "")

    # Check if the commit message is empty
    if not commit_message:
        print("Error: Empty commit message generated. Aborting commit.")
        return

    if only_message:
        print(f"Suggested commit message: {commit_message}")
        return

    # Commit with the generated message
    subprocess.run(["git", "commit", "-m", commit_message], check=True)

    # Push the changes
    if push:
        try:
            subprocess.run(["git", "push"], check=True)
        except subprocess.CalledProcessError as e:
            if allow_pull_push:
                print("Push failed, attempting pull and push...")
                subprocess.run(["git", "pull", "--rebase"], check=True)
                subprocess.run(["git", "push"], check=True)
            else:
                print("Push failed.")
                raise e
    else:
        print("Changes committed locally, but not pushed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate commit message with AI and commit changes."
    )
    parser.add_argument(
        "--no-push",
        dest="push",
        action="store_false",
        help="Commit changes locally without pushing.",
    )
    parser.add_argument(
        "--only-message",
        dest="only_message",
        action="store_true",
        help="Only print the AI generated commit message.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="grok-fast",
        choices=list(MODEL_MAPPING.keys()),
        help="Model to use for commit message generation via OpenRouter.",
    )
    parser.add_argument(
        "--allow-pull-push",
        dest="allow_pull_push",
        action="store_true",
        help="Allow git pull and push if git push failed.",
    )
    parser.add_argument(
        "--type",
        type=str,
        default="content",
        choices=["file", "content"],
        help="Type of diff to use for commit message generation (file, content).",
    )

    args = parser.parse_args()
    gitmessageai(
        push=args.push,
        only_message=args.only_message,
        model=args.model,
        allow_pull_push=args.allow_pull_push,
        type=args.type,
    )
