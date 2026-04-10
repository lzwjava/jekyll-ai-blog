from __future__ import annotations

import os
import pyperclip


def derive_script_paths() -> tuple[str, str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_dir = os.path.join(os.path.dirname(script_dir), "prompt_md")
    prompt_file = os.path.join(prompt_dir, "prompt.md")
    return prompt_dir, prompt_file


def create_directory(target_dir: str) -> None:
    os.makedirs(target_dir, exist_ok=True)


def read_clipboard() -> str:
    return pyperclip.paste().strip()


def determine_file_separator(prompt_file: str) -> str:
    if os.path.exists(prompt_file) and os.path.getsize(prompt_file) > 0:
        return "\n---\n"
    return ""


def append_prompt_to_file(prompt_file: str, content: str, separator: str) -> None:
    with open(prompt_file, "a", encoding="utf-8") as f:
        f.write(separator + content)


def save_clipboard_prompt() -> None:
    prompt_dir, prompt_file = derive_script_paths()
    create_directory(prompt_dir)
    new_prompt = read_clipboard()
    separator = determine_file_separator(prompt_file)
    append_prompt_to_file(prompt_file, new_prompt, separator)


if __name__ == "__main__":
    save_clipboard_prompt()
