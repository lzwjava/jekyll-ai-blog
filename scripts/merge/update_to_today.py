#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime
from rename_post import rename_post

# Supported languages for the blog
SUPPORTED_LANGUAGES = ["en", "zh", "ja", "es", "hi", "fr", "de", "ar", "hant"]


def extract_post_base_name(filename):
    """
    Extract the base name from a blog post filename.

    Args:
        filename (str): Post filename like '2025-08-16-myopia-zh.md'

    Returns:
        str: Base name like '2025-08-16-myopia'
    """
    # Remove .md extension
    base_name = filename.replace(".md", "")

    # Remove language suffix (-en, -zh, -ja, etc.)
    for lang in SUPPORTED_LANGUAGES:
        suffix = f"-{lang}"
        if base_name.endswith(suffix):
            return base_name[: -len(suffix)]

    return base_name


def extract_language_from_filename(filename):
    """
    Extract the language code from a blog post filename.

    Args:
        filename (str): Post filename like '2025-08-16-myopia-zh.md'

    Returns:
        str or None: Language code like 'zh' or None if not found
    """
    base_name = filename.replace(".md", "")

    for lang in SUPPORTED_LANGUAGES:
        if base_name.endswith(f"-{lang}"):
            return lang

    return None


def find_all_language_variants(input_filename):
    """
    Find all language variants of a post across all language directories.

    Args:
        input_filename (str): Any post filename like '2025-08-16-myopia-zh.md'

    Returns:
        list: List of tuples (language_dir, filename) for all found variants
    """
    base_name = extract_post_base_name(input_filename)
    found_variants = []

    for language in SUPPORTED_LANGUAGES:
        posts_directory = f"_posts/{language}"

        if not os.path.exists(posts_directory):
            continue

        # Look for files with this base name and language

        # Search through all files in the language directory
        for filename in os.listdir(posts_directory):
            if not filename.endswith(".md"):
                continue

            file_base_name = extract_post_base_name(filename)
            file_language = extract_language_from_filename(filename)

            # Check if this file matches our base name and is in the correct language directory
            if file_base_name == base_name and file_language == language:
                found_variants.append((language, filename))
                break

    return found_variants


def update_post_to_today(input_filename):
    """Update all language variants of a post's date to today by renaming the files"""

    # Extract just the filename from the path
    if os.path.dirname(input_filename):
        input_filename = os.path.basename(input_filename)

    # Parse the input filename to extract the base name
    if not input_filename.endswith(".md"):
        print(f"Error: {input_filename} is not a markdown file")
        return False

    base_name = extract_post_base_name(input_filename)
    input_language = extract_language_from_filename(input_filename)

    if not input_language:
        print(
            f"Error: Could not determine language from {input_filename}. Supported languages: {SUPPORTED_LANGUAGES}"
        )
        return False

    print(f"Looking for all language variants of post: {base_name}")

    # Find all language variants
    variants = find_all_language_variants(input_filename)

    if not variants:
        print(f"No language variants found for {base_name}")
        return False

    print(f"Found {len(variants)} language variant(s):")
    for lang, filename in variants:
        print(f"  {lang}: {filename}")

    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # Extract the title part (everything after the original date)
    parts = base_name.split("-")
    if len(parts) < 4:
        print(
            f"Error: {base_name} doesn't follow the expected format (YYYY-MM-DD-title)"
        )
        return False

    title = "-".join(parts[3:])  # Everything after YYYY-MM-DD

    success_count = 0

    # Update each variant
    for language, old_filename in variants:
        new_filename = f"{today}-{title}-{language}.md"

        print(f"\nUpdating {language}: {old_filename} -> {new_filename}")

        try:
            # Use the rename_post function
            rename_post(old_filename, new_filename)
            success_count += 1
        except Exception as e:
            print(f"Error updating {old_filename}: {e}")

    print(f"\nSuccessfully updated {success_count}/{len(variants)} files")
    return success_count > 0


def main():
    parser = argparse.ArgumentParser(
        description="Update all language variants of a post's date to today",
        epilog="""
Examples:
  python update_to_today.py 2023-01-01-myopia-en.md    # Updates all language variants of myopia post
  python update_to_today.py 2023-01-01-myopia-zh.md    # Same result - finds all variants
        """,
    )
    parser.add_argument(
        "filename",
        help="Any language variant of the post to update (e.g., 2023-01-01-title-en.md). All language variants will be updated.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be updated without making changes",
    )

    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN MODE - No files will be modified")
        # For dry run, just show what would be found and updated
        input_filename = os.path.basename(args.filename)
        base_name = extract_post_base_name(input_filename)
        variants = find_all_language_variants(input_filename)

        if variants:
            today = datetime.now().strftime("%Y-%m-%d")
            parts = base_name.split("-")
            title = "-".join(parts[3:])

            print(f"\nWould update {len(variants)} files:")
            for language, old_filename in variants:
                new_filename = f"{today}-{title}-{language}.md"
                print(f"  {language}: {old_filename} -> {new_filename}")
        else:
            print(f"No language variants found for {base_name}")
    else:
        if not update_post_to_today(args.filename):
            sys.exit(1)

        print("\nAll language variants updated successfully!")


if __name__ == "__main__":
    main()
