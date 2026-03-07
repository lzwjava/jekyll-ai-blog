from create_note_utils import get_clipboard_content, generate_title
import os
from gpa import gpa

# Create file path in logs directory
logs_dir = "../logs"


def create_sensitive_log():
    # Get and validate clipboard content
    content = get_clipboard_content()

    # Generate AI-suggested filename
    filename_prompt = lambda c: (
        f"Generate a short filename (maximum 4 words, all lowercase, use only letters, numbers, or hyphens, no spaces or special characters, suitable for a log file) for the following text and respond with only the filename: {c}"
    )
    ai_filename = generate_title(content, 4, filename_prompt).lower()

    filename = f"{ai_filename}"

    os.makedirs(logs_dir, exist_ok=True)
    file_path = os.path.join(logs_dir, f"{filename}.log")

    # Write to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Log created: {file_path}")

    os.chdir(logs_dir)
    gpa()
    print(f"Changed working directory to: {os.getcwd()}")


if __name__ == "__main__":
    create_sensitive_log()
