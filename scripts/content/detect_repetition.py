#!/usr/bin/env python3
import os
import re
import sys


def find_repetitions_in_file(filepath):
    """
    Detects repeated words/phrases in a markdown file.
    Returns a list of (line_number, match_text).
    """
    results = []
    pattern = re.compile(r"\b(\w+)(\s+\1){2,}\b", re.IGNORECASE)  # 3+ repeats

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for lineno, line in enumerate(f, start=1):
            match = pattern.search(line)
            if match:
                results.append((lineno, match.group(0)))
    return results


def scan_directory(directory):
    """
    Recursively scans the directory for markdown files
    and detects repetitions.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".md"):
                filepath = os.path.join(root, file)
                repeats = find_repetitions_in_file(filepath)
                if repeats:
                    print(f"\n[!] File: {filepath}")
                    for lineno, text in repeats:
                        print(f"  Line {lineno}: {text}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python detect_repeats.py <directory>")
        sys.exit(1)

    scan_directory(sys.argv[1])
