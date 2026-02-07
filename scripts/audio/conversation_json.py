import argparse
import json
import os
import sys
from typing import Any, List


DEFAULT_OUTPUT_DIRECTORY = os.path.join("scripts", "conversation")


def read_conversation_input() -> str:
    print("Paste the conversation JSON. Enter 'q' on a new line to finish.")
    lines: List[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().lower() == "q":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def ensure_json_extension(filename: str) -> str:
    return filename if filename.endswith(".json") else f"{filename}.json"


def validate_conversation(data: Any) -> None:
    if not isinstance(data, list):
        raise ValueError("Conversation JSON must be a list.")
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Item {index} must be an object.")
        if "speaker" not in item or "line" not in item:
            raise ValueError(f"Item {index} must include 'speaker' and 'line'.")


def resolve_output_path(filename: str) -> str:
    filename = ensure_json_extension(filename)
    if os.path.dirname(filename):
        return filename
    return os.path.join(DEFAULT_OUTPUT_DIRECTORY, filename)


def write_conversation(filename: str, data: Any) -> str:
    output_path = resolve_output_path(filename)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file_handle:
        json.dump(data, file_handle, ensure_ascii=False, indent=2)
        file_handle.write("\n")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture conversation JSON and save it under scripts/conversation."
    )
    parser.add_argument("filename", help="Output filename for the conversation JSON.")
    args = parser.parse_args()

    raw_input = read_conversation_input()
    if not raw_input:
        print("No conversation content provided.", file=sys.stderr)
        return 1

    try:
        conversation = json.loads(raw_input)
        validate_conversation(conversation)
    except Exception as exc:
        print(f"Invalid conversation JSON: {exc}", file=sys.stderr)
        return 1

    output_path = write_conversation(args.filename, conversation)
    print(f"Conversation saved to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
