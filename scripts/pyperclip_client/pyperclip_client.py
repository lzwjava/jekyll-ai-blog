import pyperclip
import argparse

MODEL_MAPPING = {
    "gpt-4o": "openai/gpt-4o",
    "gpt-4.1": "openai/gpt-4.1",
}


def call_pyperclip_api(prompt, model=None):
    messages = [{"role": "user", "content": prompt}]
    return call_clipboard_api_with_messages(messages, model)


def call_clipboard_api_with_messages(messages, model=None):
    user_message = None
    for message in messages:
        if message.get("role") == "user":
            user_message = message.get("content")
            break
    if not user_message:
        raise Exception("No user message found in messages")
    pyperclip.copy(user_message)
    input(
        f"Using model: {model}\nPress Enter after you've copied the answer from Copilot Chat..."
    )
    answer = pyperclip.paste()
    return answer if answer else None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy prompt to clipboard for Copilot Chat workflow."
    )
    parser.add_argument("prompt", nargs="+", help="Prompt to send to Copilot Chat")
    parser.add_argument(
        "--model",
        choices=MODEL_MAPPING.keys(),
        default="gpt-4.1",
        help="Model to use (default: gpt-4.1)",
    )
    args = parser.parse_args()
    prompt = " ".join(args.prompt)
    model = MODEL_MAPPING[args.model]
    response = call_pyperclip_api(prompt, model)
    print(response)
