#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find Weird Posts Script

This script identifies blog posts with unusual translation length ratios compared to
their original versions. It checks if translations have reasonable content lengths
based on expected language characteristics.

Usage:
    python scripts/content/find_weird_posts.py
    python scripts/content/find_weird_posts.py --threshold 0.3
    python scripts/content/find_weird_posts.py --format list
"""

import os
import re
import argparse
from collections import defaultdict

# Supported languages for the blog
SUPPORTED_LANGUAGES = ["en", "zh", "ja", "es", "hi", "fr", "de", "ar", "hant"]

# Expected length ratios compared to English (baseline)
# These are approximate ratios based on typical language characteristics
LANGUAGE_RATIOS = {
    "en": 1.0,  # English baseline
    "zh": 0.5,  # Chinese is typically about 50% of English length
    "hant": 0.5,  # Traditional Chinese similar to simplified
    "ja": 0.6,  # Japanese slightly longer than Chinese due to hiragana/katakana
    "es": 1.1,  # Spanish slightly longer than English
    "fr": 1.1,  # French slightly longer than English
    "de": 0.9,  # German can be shorter due to compound words
    "hi": 1.2,  # Hindi often longer due to script characteristics
    "ar": 0.8,  # Arabic often shorter due to script density
}


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


def get_content_length(file_path):
    """
    Get the content length of a markdown file, excluding front matter.

    Args:
        file_path (str): Path to the markdown file

    Returns:
        int: Number of characters in the content (excluding front matter)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove front matter (content between --- markers)
        parts = content.split("---", 2)
        if len(parts) >= 3:
            # Content after the second ---
            content = parts[2].strip()

        # Remove markdown syntax for more accurate length measurement
        # Remove images: ![alt](url)
        content = re.sub(r"!\[.*?\]\([^)]+\)", "", content)
        # Remove links: [text](url) -> text
        content = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", content)
        # Remove headers: ## Header -> Header
        content = re.sub(r"^#+\s*", "", content, flags=re.MULTILINE)
        # Remove code blocks
        content = re.sub(r"```[^`]*```", "", content, flags=re.DOTALL)
        # Remove inline code
        content = re.sub(r"`[^`]+`", "", content)
        # Remove extra whitespace
        content = re.sub(r"\s+", " ", content).strip()

        return len(content)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0


def scan_posts_with_lengths():
    """
    Scan all posts and calculate their content lengths.

    Returns:
        dict: Dictionary mapping base names to language->length mappings
    """
    posts_by_base_name = defaultdict(dict)

    # Scan original directory
    original_directory = "original"
    if os.path.exists(original_directory):
        for filename in os.listdir(original_directory):
            if not filename.endswith(".md"):
                continue

            base_name = extract_post_base_name(filename)
            language = extract_language_from_filename(filename)

            if language:
                file_path = os.path.join(original_directory, filename)
                length = get_content_length(file_path)
                posts_by_base_name[base_name][language] = {
                    "length": length,
                    "path": file_path,
                }

    # Scan _posts directories
    for language in SUPPORTED_LANGUAGES:
        posts_directory = f"_posts/{language}"

        if not os.path.exists(posts_directory):
            continue

        for filename in os.listdir(posts_directory):
            if not filename.endswith(".md"):
                continue

            base_name = extract_post_base_name(filename)
            detected_language = extract_language_from_filename(filename)

            # Verify the detected language matches the directory
            if detected_language == language:
                file_path = os.path.join(posts_directory, filename)
                length = get_content_length(file_path)
                posts_by_base_name[base_name][language] = {
                    "length": length,
                    "path": file_path,
                }

    return posts_by_base_name


def analyze_length_anomalies(posts_data, threshold=0.5):
    """
    Analyze posts for length anomalies based on expected language ratios.

    Args:
        posts_data (dict): Dictionary of posts with their lengths
        threshold (float): Threshold for detecting anomalies (0.5 = 50% deviation)

    Returns:
        list: List of posts with detected anomalies
    """
    anomalous_posts = []

    for base_name, languages in posts_data.items():
        if len(languages) < 2:
            continue  # Need at least 2 languages to compare

        # Find a reference language (preferably English)
        reference_lang = None
        reference_length = 0

        if "en" in languages:
            reference_lang = "en"
            reference_length = languages["en"]["length"]
        elif languages:
            # Use the first available language as reference
            reference_lang = list(languages.keys())[0]
            reference_length = languages[reference_lang]["length"]

        if reference_length == 0:
            continue  # Skip if reference is empty

        anomalies = []

        for lang, data in languages.items():
            if lang == reference_lang:
                continue

            actual_length = data["length"]
            if actual_length == 0:
                anomalies.append(
                    {
                        "language": lang,
                        "issue": "empty_content",
                        "actual_length": actual_length,
                        "expected_range": "N/A",
                        "path": data["path"],
                    }
                )
                continue

            # Calculate expected length based on language ratios
            if reference_lang in LANGUAGE_RATIOS and lang in LANGUAGE_RATIOS:
                ratio = LANGUAGE_RATIOS[lang] / LANGUAGE_RATIOS[reference_lang]
                expected_length = reference_length * ratio

                # Calculate acceptable range
                min_expected = expected_length * (1 - threshold)
                max_expected = expected_length * (1 + threshold)

                # Check if actual length is outside acceptable range
                if actual_length < min_expected or actual_length > max_expected:
                    deviation = abs(actual_length - expected_length) / expected_length
                    anomalies.append(
                        {
                            "language": lang,
                            "issue": "length_anomaly",
                            "actual_length": actual_length,
                            "expected_length": int(expected_length),
                            "expected_range": f"{int(min_expected)}-{int(max_expected)}",
                            "deviation": f"{deviation:.1%}",
                            "path": data["path"],
                        }
                    )

        if anomalies:
            anomalous_posts.append(
                {
                    "base_name": base_name,
                    "reference_language": reference_lang,
                    "reference_length": reference_length,
                    "anomalies": anomalies,
                    "total_languages": len(languages),
                }
            )

    return anomalous_posts


def display_anomalies_table(anomalous_posts):
    """
    Display anomalies in a formatted table.

    Args:
        anomalous_posts (list): List of posts with anomalies
    """
    print("\nWEIRD POSTS (Length Anomalies Detected):")
    print("=" * 120)
    print(
        f"{'Base Name':<35} {'Lang':<4} {'Issue':<12} {'Actual':<7} {'Expected':<12} {'Deviation':<10} {'Path':<30}"
    )
    print("-" * 120)

    for post in anomalous_posts:
        base_name = post["base_name"]
        ref_info = f"(ref: {post['reference_language']}={post['reference_length']})"

        for i, anomaly in enumerate(post["anomalies"]):
            display_name = base_name if i == 0 else ""
            if i == 0 and len(post["anomalies"]) > 1:
                display_name += f" {ref_info}"

            expected_str = str(
                anomaly.get("expected_length", anomaly["expected_range"])
            )
            deviation = anomaly.get("deviation", "N/A")

            print(
                f"{display_name:<35} {anomaly['language']:<4} {anomaly['issue']:<12} "
                f"{anomaly['actual_length']:<7} {expected_str:<12} {deviation:<10} "
                f"{os.path.basename(anomaly['path']):<30}"
            )


def display_anomalies_list(anomalous_posts):
    """
    Display anomalies in a detailed list format.

    Args:
        anomalous_posts (list): List of posts with anomalies
    """
    print("\nWEIRD POSTS (Length Anomalies Detected):")
    print("=" * 80)

    for post in anomalous_posts:
        print(f"\n[POST] {post['base_name']}")
        print(
            f"   Reference: {post['reference_language']} ({post['reference_length']} chars)"
        )
        print(f"   Total languages: {post['total_languages']}")

        for anomaly in post["anomalies"]:
            print(
                f"\n   [WARN]  {anomaly['language'].upper()} - {anomaly['issue'].replace('_', ' ').title()}"
            )
            print(f"      Actual length: {anomaly['actual_length']} chars")
            if "expected_length" in anomaly:
                print(f"      Expected length: {anomaly['expected_length']} chars")
                print(f"      Deviation: {anomaly['deviation']}")
            print(f"      File: {anomaly['path']}")


def display_anomalies_csv(anomalous_posts):
    """
    Display anomalies in CSV format.

    Args:
        anomalous_posts (list): List of posts with anomalies
    """
    print("base_name,language,issue,actual_length,expected_length,deviation,file_path")
    for post in anomalous_posts:
        for anomaly in post["anomalies"]:
            expected = anomaly.get("expected_length", "")
            deviation = anomaly.get("deviation", "")
            print(
                f"{post['base_name']},{anomaly['language']},{anomaly['issue']},"
                f"{anomaly['actual_length']},{expected},{deviation},{anomaly['path']}"
            )


def display_statistics(anomalous_posts):
    """
    Display statistics about the anomalies found.

    Args:
        anomalous_posts (list): List of posts with anomalies
    """
    issue_counts = defaultdict(int)
    language_counts = defaultdict(int)

    for post in anomalous_posts:
        for anomaly in post["anomalies"]:
            issue_counts[anomaly["issue"]] += 1
            language_counts[anomaly["language"]] += 1

    print("\nANOMALY STATISTICS:")
    print("   Issue types:")
    for issue, count in sorted(issue_counts.items()):
        print(f"      {issue.replace('_', ' ').title()}: {count}")

    print("\n   Languages with anomalies:")
    for language, count in sorted(language_counts.items()):
        print(f"      {language}: {count}")


def main():
    """Main function to run the weird posts finder."""
    parser = argparse.ArgumentParser(
        description="Find blog posts with unusual translation length ratios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Find all posts with length anomalies
  %(prog)s --threshold 0.3              # Use 30% threshold for anomaly detection
  %(prog)s --format list                # Use detailed list format
  %(prog)s --format csv                 # Export in CSV format
        """,
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Threshold for detecting length anomalies (default: 0.5 = 50%% deviation)",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["table", "list", "csv"],
        default="table",
        help="Output format for displaying results (default: table)",
    )

    args = parser.parse_args()

    # Validate threshold
    if args.threshold <= 0 or args.threshold >= 1:
        print("Error: Threshold must be between 0 and 1")
        return

    # Scan all posts and analyze lengths
    print("Scanning posts and analyzing content lengths...")
    posts_data = scan_posts_with_lengths()

    print(f"Analyzing {len(posts_data)} post groups for length anomalies...")
    anomalous_posts = analyze_length_anomalies(posts_data, args.threshold)

    # Display results
    print(f"Found {len(anomalous_posts)} posts with length anomalies")
    print(f"Using threshold: {args.threshold:.0%} deviation")
    print("=" * 80)

    if anomalous_posts:
        if args.format == "table":
            display_anomalies_table(anomalous_posts)
        elif args.format == "list":
            display_anomalies_list(anomalous_posts)
        elif args.format == "csv":
            display_anomalies_csv(anomalous_posts)

        # Display statistics (except for CSV format)
        if args.format != "csv":
            display_statistics(anomalous_posts)
    else:
        print(
            "\nNo length anomalies detected! All translations have reasonable lengths."
        )

    # Display summary
    total_anomalies = sum(len(post["anomalies"]) for post in anomalous_posts)
    print("\nSUMMARY:")
    print(f"   Posts with anomalies: {len(anomalous_posts)}")
    print(f"   Total anomalies found: {total_anomalies}")
    print(f"   Detection threshold: {args.threshold:.0%}")


if __name__ == "__main__":
    main()
