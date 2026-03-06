#!/usr/bin/env python3

import os
import argparse
import frontmatter
import json


def scan_translated_notes():
    """Scan _posts directory for translated notes and record filenames with their languages."""

    translated_notes = {}
    posts_dir = "_posts"

    if not os.path.exists(posts_dir):
        print(f"Posts directory {posts_dir} does not exist")
        return translated_notes

    # Get all language directories
    languages = []
    for item in os.listdir(posts_dir):
        lang_path = os.path.join(posts_dir, item)
        if os.path.isdir(lang_path):
            languages.append(item)

    print(f"Found language directories: {languages}")

    for lang in languages:
        lang_dir = os.path.join(posts_dir, lang)
        print(f"Scanning {lang_dir}")

        for filename in os.listdir(lang_dir):
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(lang_dir, filename)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    post = frontmatter.load(f)

                # Check if this is a note by examining frontmatter
                if post.get("type") == "note":
                    # Extract base filename (without language suffix)
                    base_name = (
                        filename.rsplit("-", 1)[0] + ".md"
                        if "-" in filename
                        else filename
                    )

                    if base_name not in translated_notes:
                        translated_notes[base_name] = {}

                    translated_notes[base_name][lang] = filename

                    print(f"Found translated note: {base_name} -> {lang} ({filename})")

            except Exception as e:
                print(f"Error reading {filepath}: {e}")
                continue

    print(f"\nTotal unique notes found: {len(translated_notes)}")

    for note, translations in translated_notes.items():
        print(f"{note}: {list(translations.keys())}")

    return translated_notes


def main():
    parser = argparse.ArgumentParser(
        description="Scan _posts directory for already translated notes and record them in JSON format."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="translated_notes.json",
        help="Output JSON file name (default: translated_notes.json)",
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Perform a dry run without writing to file",
    )

    args = parser.parse_args()

    translated_notes = scan_translated_notes()

    if args.dry_run:
        print("\nDry run - no file written")
        return

    # Write to JSON file
    output_file = os.path.join(os.path.dirname(__file__), args.output)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(translated_notes, f, indent=2, ensure_ascii=False)

    print(f"\nWritten translation records to {output_file}")


if __name__ == "__main__":
    main()
