import os
import sys
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ww.llm.openrouter_client import call_openrouter_api


def get_name_suggestions(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    original_name = os.path.basename(file_path)

    prompt = f"Suggest 5 concise and descriptive file names based on the following content and its original name '{original_name}'. Respond with only the names, one per line:\n\n{content}"

    response = call_openrouter_api(prompt, model="claude-sonnet")
    suggestions = response.strip().split("\n")
    return suggestions[:5]  # Ensure we only get 5 names


def is_text_file(file_path):
    try:
        with open(file_path, "r") as f:
            f.read(1024)
        return True
    except UnicodeDecodeError:
        return False


def rename_file(file_path):
    suggestions = get_name_suggestions(file_path)

    print(f"\nFile: {file_path}")
    print("Suggested names:")
    for i, name in enumerate(suggestions, 1):
        print(f"{i}. {name}")
    print("0. Skip/Cancel")

    while True:
        choice = input("\nEnter your choice (0-5): ")
        if choice.isdigit() and 0 <= int(choice) <= 5:
            break
        print("Invalid choice. Please enter a number between 0 and 5.")

    choice = int(choice)
    if choice == 0:
        print("Skipped.")
        return None

    new_name = suggestions[choice - 1]
    dir_path = os.path.dirname(file_path)
    new_path = os.path.join(dir_path, new_name)

    os.rename(file_path, new_path)
    return new_path


def process_directory(dir_path):
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_text_file(file_path):
                print(f"\n{'=' * 50}")
                new_path = rename_file(file_path)
                if new_path:
                    print(f"Renamed to: {new_path}")
                print(f"{'=' * 50}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename files based on their content.")
    parser.add_argument("path", type=str, help="Path to file or directory")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        process_directory(args.path)
    else:
        new_path = rename_file(args.path)
        if new_path:
            print(f"\nFile renamed to: {new_path}")
