from create_normal_log import create_normal_log
from create_note_utils import get_clipboard_content, generate_title


def is_sensitive_content(content):
    """Use AI to detect if content contains sensitive information like passwords or keys."""
    sensitivity_prompt = lambda c: (
        f"Does the following text contain sensitive information such as passwords, API keys, or personal data? Respond with 'yes' or 'no' only: {c}"
    )
    response = generate_title(content, 1, sensitivity_prompt).lower()
    return response == "yes"


def create_log():
    """Create a log entry based on clipboard content, checking for sensitivity and length."""
    # Get and validate clipboard content
    content = get_clipboard_content()

    # Check character limit
    if len(content) > 1048576:  # 1MB limit
        print("Error: Content exceeds 1MB. Please shorten the log and try again.")
        return

    # Detect if content is sensitive
    if is_sensitive_content(content):
        print(
            "Error: Sensitive content detected. Please remove passwords, keys, or personal data and try again."
        )
        return

    create_normal_log()


if __name__ == "__main__":
    create_log()
