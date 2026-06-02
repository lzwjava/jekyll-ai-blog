#!/usr/bin/env python3
"""
Find Posts Missing Table of Contents

This script scans markdown post files (original/ and _posts/<lang>/)
and reports files that are missing a "### Table of Contents" section.

Usage:
    python scripts/content/find_missing_toc_posts.py
    python scripts/content/find_missing_toc_posts.py --show-with-toc
    python scripts/content/find_missing_toc_posts.py --format csv
    python scripts/content/find_missing_toc_posts.py --lang en
"""

import argparse
import re
from collections import defaultdict
from pathlib import Path

# Supported languages for the blog (kept for compatibility)
SUPPORTED_LANGUAGES = ["en", "zh", "ja", "es", "hi", "fr", "de", "ar", "hant"]


def extract_post_base_name(filename):
    """Return base name without language suffix and extension."""
    base_name = filename.replace(".md", "")
    for lang in SUPPORTED_LANGUAGES:
        suffix = f"-{lang}"
        if base_name.endswith(suffix):
            return base_name[: -len(suffix)]
    return base_name


def count_headers(content):
    """Count markdown headers (#, ##, ###) and return counts."""
    lines = content.splitlines()
    h1 = sum(1 for line in lines if re.match(r"^#\s+\S", line.strip()))
    h2 = sum(1 for line in lines if re.match(r"^##\s+\S", line.strip()))
    h3 = sum(1 for line in lines if re.match(r"^###\s+\S", line.strip()))
    total = h1 + h2 + h3
    return {"h1": h1, "h2": h2, "h3": h3, "total": total}


def detect_toc_in_content(content):
    """Return True if the content contains an explicit TOC marker."""
    return "### Table of Contents" in content


def should_have_toc_from_counts(counts, threshold=2, char_count=0, char_threshold=2000):
    """Decide if a post should have a TOC based on header counts and character count.

    Rules applied in priority order:
      1) If character count exceeds char_threshold, require TOC.
      2) Else apply header-based rules (as before) using `threshold` for header counts.
    """
    if char_threshold and char_count > char_threshold:
        return True

    h1 = counts.get("h1", 0)
    h2 = counts.get("h2", 0)
    h3 = counts.get("h3", 0)

    if h1 > threshold:
        return True
    if h1 == 0 and h2 > threshold:
        return True
    if h1 == 0 and h2 == 0 and h3 > threshold:
        return True
    return False


def scan_markdown_files(
    lang_filter=None, original_only=False, char_threshold=2000, header_threshold=2
):
    """Scan original/ and optionally _posts/* for markdown files and detect TOC presence.

    If original_only is True the function scans only the original/ directory.

    Returns a dict mapping base_name -> list of file records:
      { base_name: [ {path, language, is_original, has_toc, header_count, char_count, should_have_toc}, ... ] }
    """
    results = defaultdict(list)

    # Scan original directory
    original_dir = Path("original")
    if original_dir.exists():
        for p in original_dir.glob("*.md"):
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                text = ""
            base = extract_post_base_name(p.name)
            has_toc = detect_toc_in_content(text)
            counts = count_headers(text)
            char_count = len(text)
            should = should_have_toc_from_counts(
                counts,
                threshold=header_threshold,
                char_count=char_count,
                char_threshold=char_threshold,
            )
            results[base].append(
                {
                    "path": str(p),
                    "language": None,
                    "is_original": True,
                    "has_toc": has_toc,
                    "header_count": counts["total"],
                    "char_count": char_count,
                    "should_have_toc": should,
                }
            )

    # Scan _posts/<lang> directories unless original_only is requested
    posts_root = Path("_posts")
    if not original_only and posts_root.exists():
        for lang_dir in posts_root.iterdir():
            if not lang_dir.is_dir():
                continue
            lang = lang_dir.name
            if lang_filter and lang != lang_filter:
                continue
            for p in lang_dir.glob("*.md"):
                try:
                    text = p.read_text(encoding="utf-8")
                except Exception:
                    text = ""
                base = extract_post_base_name(p.name)
                has_toc = detect_toc_in_content(text)
                counts = count_headers(text)
                char_count = len(text)
                should = should_have_toc_from_counts(
                    counts,
                    threshold=header_threshold,
                    char_count=char_count,
                    char_threshold=char_threshold,
                )
                results[base].append(
                    {
                        "path": str(p),
                        "language": lang,
                        "is_original": False,
                        "has_toc": has_toc,
                        "header_count": counts["total"],
                        "char_count": char_count,
                        "should_have_toc": should,
                    }
                )

    return results


def summarize_missing_toc(results, show_with_toc=False):
    """Return two lists: missing_toc_entries, with_toc_entries.

    Each entry is a dict: {base_name, files: [record,...], total_files, toc_count, needs_toc}
    """
    missing = []
    present = []

    for base, records in sorted(results.items()):
        toc_count = sum(1 for r in records if r["has_toc"])
        total = len(records)
        # Decide if this base should have a TOC: if any variant has.should_have_toc
        needs_toc = any(r.get("should_have_toc") for r in records)
        entry = {
            "base_name": base,
            "files": records,
            "total_files": total,
            "toc_count": toc_count,
            "needs_toc": needs_toc,
        }
        # Missing only if it needs a TOC and none of the variants have one
        if needs_toc and toc_count == 0:
            missing.append(entry)
        else:
            present.append(entry)

    if show_with_toc:
        return missing, present
    return missing, []


def display_table(entries, title):
    print(f"\n{title}:")
    print("=" * 80)
    print(f"{'Base Name':<40} {'Files':<6} {'With TOC':<8} {'Example Path'}")
    print("-" * 100)
    for e in entries:
        example = e["files"][0]["path"] if e["files"] else ""
        print(
            f"{e['base_name']:<40} {e['total_files']:<6} {e['toc_count']:<8} {example}"
        )


def display_list(entries, title):
    print(f"\n{title}:")
    print("=" * 80)
    for e in entries:
        print(
            f"\n📝 {e['base_name']}  (files: {e['total_files']}, with_toc: {e['toc_count']})"
        )
        for f in e["files"]:
            tag = "ORIG" if f["is_original"] else (f"{f['language']}")
            print(f"   - [{tag}] {f['path']}  -> has_toc: {f['has_toc']}")


def display_csv(entries):
    print("base_name,total_files,toc_count,example_path")
    for e in entries:
        example = e["files"][0]["path"] if e["files"] else ""
        print(f"{e['base_name']},{e['total_files']},{e['toc_count']},{example}")


def main():
    parser = argparse.ArgumentParser(
        description='Find posts missing "### Table of Contents"'
    )
    parser.add_argument(
        "--show-with-toc",
        action="store_true",
        help="Also show posts that already have a TOC",
    )
    parser.add_argument(
        "--format",
        choices=["table", "list", "csv"],
        default="table",
        help="Output format",
    )
    parser.add_argument(
        "--lang",
        type=str,
        choices=SUPPORTED_LANGUAGES,
        help="When provided, only scan the original/ directory (useful for checking source files)",
    )
    parser.add_argument(
        "--char-threshold",
        type=int,
        default=2000,
        help="Character count threshold to require a TOC (default: 2000)",
    )
    parser.add_argument(
        "--header-threshold",
        type=int,
        default=2,
        help="Header count threshold for #/##/### (default: 2)",
    )

    args = parser.parse_args()

    # If --lang is provided, per user request only check original/ directory
    original_only = bool(args.lang)
    results = scan_markdown_files(
        lang_filter=args.lang,
        original_only=original_only,
        char_threshold=args.char_threshold,
        header_threshold=args.header_threshold,
    )
    missing, present = summarize_missing_toc(results, show_with_toc=args.show_with_toc)

    print(f"Found {len(missing)} base posts missing TOC")
    if args.show_with_toc:
        print(f"Found {len(present)} base posts with TOC")

    if args.format == "table":
        if missing:
            display_table(missing, "POSTS MISSING TOC")
        if args.show_with_toc and present:
            display_table(present, "POSTS WITH TOC")
    elif args.format == "list":
        if missing:
            display_list(missing, "POSTS MISSING TOC")
        if args.show_with_toc and present:
            display_list(present, "POSTS WITH TOC")
    elif args.format == "csv":
        if missing:
            display_csv(missing)
        if args.show_with_toc and present:
            display_csv(present)


if __name__ == "__main__":
    main()
