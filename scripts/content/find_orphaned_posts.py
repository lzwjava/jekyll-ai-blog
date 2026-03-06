#!/usr/bin/env python3
"""
Find Orphaned Posts Script

This script identifies blog posts that are missing translations in one or more languages.
It scans the _posts directory structure and cross-references with the original directory
to find incomplete translation sets.

Usage:
    python scripts/content/find_orphaned_posts.py
    python scripts/content/find_orphaned_posts.py --missing-lang en
    python scripts/content/find_orphaned_posts.py --show-complete --format list
"""

import os
import argparse
from collections import defaultdict

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


def scan_translated_posts():
    """
    Scan the _posts directory to catalog all translated posts by base name and language.

    Returns:
        dict: Dictionary mapping base names to sets of available languages
    """
    posts_by_base_name = defaultdict(set)

    for language in SUPPORTED_LANGUAGES:
        posts_directory = f"_posts/{language}"

        if not os.path.exists(posts_directory):
            print(f"Warning: Directory {posts_directory} does not exist")
            continue

        for filename in os.listdir(posts_directory):
            if not filename.endswith(".md"):
                continue

            base_name = extract_post_base_name(filename)
            detected_language = extract_language_from_filename(filename)

            # Verify the detected language matches the directory
            if detected_language == language:
                posts_by_base_name[base_name].add(language)

    return posts_by_base_name


def scan_original_posts():
    """
    Scan the original directory to find all source posts.

    Returns:
        set: Set of base names for posts that have original source files
    """
    original_post_names = set()
    original_directory = "original"

    if not os.path.exists(original_directory):
        print(f"Warning: Directory {original_directory} does not exist")
        return original_post_names

    for filename in os.listdir(original_directory):
        if not filename.endswith(".md"):
            continue

        base_name = extract_post_base_name(filename)
        original_post_names.add(base_name)

    return original_post_names


def analyze_post_completeness():
    """
    Analyze all posts to identify orphaned and complete posts.

    Returns:
        tuple: (orphaned_posts, complete_posts) where each is a list of dictionaries
    """
    all_supported_languages = set(SUPPORTED_LANGUAGES)
    translated_posts = scan_translated_posts()
    original_posts = scan_original_posts()

    orphaned_posts = []
    complete_posts = []

    # Analyze existing translated posts
    for base_name, available_languages in translated_posts.items():
        missing_languages = all_supported_languages - available_languages

        post_info = {
            "base_name": base_name,
            "available_languages": sorted(available_languages),
            "missing_languages": sorted(missing_languages),
            "has_original_source": base_name in original_posts,
        }

        if missing_languages:
            orphaned_posts.append(post_info)
        else:
            complete_posts.append(post_info)

    # Check for original posts with no translations at all
    for base_name in original_posts:
        if base_name not in translated_posts:
            orphaned_posts.append(
                {
                    "base_name": base_name,
                    "available_languages": [],
                    "missing_languages": sorted(all_supported_languages),
                    "has_original_source": True,
                }
            )

    return orphaned_posts, complete_posts


def filter_posts_by_missing_language(orphaned_posts, target_language):
    """
    Filter orphaned posts to only those missing a specific language.

    Args:
        orphaned_posts (list): List of orphaned post dictionaries
        target_language (str): Language code to filter by

    Returns:
        list: Filtered list of orphaned posts
    """
    return [
        post for post in orphaned_posts if target_language in post["missing_languages"]
    ]


def display_posts_table(posts, title):
    """
    Display posts in a formatted table.

    Args:
        posts (list): List of post dictionaries
        title (str): Title for the table section
    """
    print(f"\n{title}:")
    print("=" * 80)
    print(f"{'Base Name':<40} {'Available':<20} {'Missing':<30} {'Orig'}")
    print("-" * 100)

    for post in posts:
        available = ", ".join(post["available_languages"]) or "None"
        missing = ", ".join(post["missing_languages"])
        has_original = "Y" if post["has_original_source"] else "N"
        print(f"{post['base_name']:<40} {available:<20} {missing:<30} {has_original}")


def display_posts_list(posts, title):
    """
    Display posts in a detailed list format.

    Args:
        posts (list): List of post dictionaries
        title (str): Title for the list section
    """
    print(f"\n{title}:")
    print("=" * 80)

    for post in posts:
        print(f"\n📝 {post['base_name']}")
        print(f"   Available: {', '.join(post['available_languages']) or 'None'}")
        print(f"   Missing: {', '.join(post['missing_languages'])}")
        print(f"   Has Original: {'Yes' if post['has_original_source'] else 'No'}")


def display_posts_csv(posts):
    """
    Display posts in CSV format.

    Args:
        posts (list): List of post dictionaries
    """
    print("base_name,available_languages,missing_languages,has_original_source")
    for post in posts:
        available = ";".join(post["available_languages"])
        missing = ";".join(post["missing_languages"])
        print(
            f"{post['base_name']},{available},{missing},{post['has_original_source']}"
        )


def display_language_statistics(orphaned_posts):
    """
    Display statistics about missing translations by language.

    Args:
        orphaned_posts (list): List of orphaned post dictionaries
    """
    missing_language_counts = defaultdict(int)

    for post in orphaned_posts:
        for language in post["missing_languages"]:
            missing_language_counts[language] += 1

    print(f"\nMISSING TRANSLATIONS BY LANGUAGE:")
    for language, count in sorted(missing_language_counts.items()):
        print(f"   {language}: {count} posts missing")


def main():
    """Main function to run the orphaned posts finder."""
    parser = argparse.ArgumentParser(
        description="Find blog posts that are missing translations in one or more languages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Find all orphaned posts
  %(prog)s --missing-lang en            # Find posts missing English
  %(prog)s --show-complete              # Show complete posts too
  %(prog)s --format list                # Use detailed list format
  %(prog)s --format csv                 # Export in CSV format
        """,
    )

    parser.add_argument(
        "--show-complete",
        action="store_true",
        help="Also display posts that have all translations complete",
    )

    parser.add_argument(
        "--missing-lang",
        type=str,
        choices=SUPPORTED_LANGUAGES,
        help="Show only posts missing translations for a specific language",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["table", "list", "csv"],
        default="table",
        help="Output format for displaying results (default: table)",
    )

    args = parser.parse_args()

    # Analyze all posts
    orphaned_posts, complete_posts = analyze_post_completeness()

    # Filter by missing language if specified
    if args.missing_lang:
        orphaned_posts = filter_posts_by_missing_language(
            orphaned_posts, args.missing_lang
        )
        filter_info = f" missing '{args.missing_lang}'"
    else:
        filter_info = ""

    # Display summary
    print(f"Found {len(orphaned_posts)} orphaned posts{filter_info}")
    print(f"Found {len(complete_posts)} complete posts (all translations available)")
    print("=" * 80)

    # Display orphaned posts
    if orphaned_posts:
        if args.format == "table":
            display_posts_table(orphaned_posts, "ORPHANED POSTS (Missing Translations)")
        elif args.format == "list":
            display_posts_list(orphaned_posts, "ORPHANED POSTS (Missing Translations)")
        elif args.format == "csv":
            display_posts_csv(orphaned_posts)

    # Display complete posts if requested
    if args.show_complete and complete_posts:
        if args.format == "table":
            display_posts_table(
                complete_posts,
                f"COMPLETE POSTS ({len(complete_posts)} with all translations)",
            )
        elif args.format == "list":
            display_posts_list(
                complete_posts,
                f"COMPLETE POSTS ({len(complete_posts)} with all translations)",
            )
        elif args.format == "csv":
            display_posts_csv(complete_posts)

    # Display summary statistics
    print(f"\nSUMMARY:")
    print(f"   Total orphaned posts: {len(orphaned_posts)}")
    print(f"   Total complete posts: {len(complete_posts)}")

    # Display language-specific statistics for orphaned posts
    if orphaned_posts and args.format != "csv":
        display_language_statistics(orphaned_posts)


if __name__ == "__main__":
    main()
