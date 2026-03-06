#!/usr/bin/env python3
"""
Check if clipboard content already exists in the latest 200 notes.

This script reads content from the clipboard and compares it against the latest
200 notes in the notes directory using fast similarity checking.
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional

# Add repository root to sys.path for importing utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.create.create_note_utils import (
    get_clipboard_content,
    clean_grok_tags,
    clean_content,
)


def _repo_root() -> str:
    """Return the repository root derived from this file's location."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _extract_content_without_frontmatter(file_path):
    """Extract content without front matter from a note file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split on front matter
        sections = content.split("---", 2)
        if len(sections) >= 3:
            return sections[2].strip()

        # If no front matter, return content
        return content.strip()
    except Exception as e:
        print(f"[warn] Error reading {file_path}: {e}")
        return ""


def _are_notes_quick_similar(content1, content2):
    """Fast similarity check between two note contents"""
    if not content1 or not content2:
        return False

    # Quick length check within 5% tolerance
    len1 = len(content1)
    len2 = len(content2)
    if max(len1, len2) == 0:
        return False

    if abs(len1 - len2) / max(len1, len2) > 0.05:
        return False

    # Fast content check - first 500 chars
    first500_1 = content1[:500]
    first500_2 = content2[:500]

    # Exact match for first 250 chars, 90% match for 500 chars
    if len(first500_1) >= 250 and len(first500_2) >= 250:
        if first500_1[:250] != first500_2[:250]:
            return False

        # 90% similarity for 500 chars
        matches = sum(c1 == c2 for c1, c2 in zip(first500_1[:500], first500_2[:500]))
        return matches >= 450  # 90% of 500

    return content1.strip() == content2.strip()


def check_duplicate_notes() -> bool:
    """Check if clipboard content already exists in the latest 200 notes.

    Returns True if a duplicate is found, False otherwise.
    Prints information about potential duplicates found.
    """
    # Get clipboard content
    clipboard_content = get_clipboard_content()
    if not clipboard_content or not clipboard_content.strip():
        print("[info] No content in clipboard")
        return False

    # Clean the clipboard content like in create_note_from_clipboard
    clipboard_content = clean_grok_tags(clipboard_content)
    clipboard_content = clean_content(clipboard_content)

    # Find notes directory
    repo_root = _repo_root()
    notes_dir = Path(repo_root) / "notes"

    if not notes_dir.exists():
        print(f"[warn] Notes directory not found: {notes_dir}")
        return False

    # Get all markdown files in notes directory, sorted by modification time (latest first)
    note_files = list(notes_dir.glob("*.md"))
    if not note_files:
        print("[info] No notes found")
        return False

    # Sort by modification time (latest first) and take latest 200
    note_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    latest_notes = note_files[:-1]

    print(f"[info] Checking against latest {len(latest_notes)} notes...")

    for note_file in latest_notes:
        try:
            note_content = _extract_content_without_frontmatter(note_file)
            if _are_notes_quick_similar(clipboard_content, note_content):
                print(f"[warn] DUPLICATE FOUND: Content similar to {note_file.name}")
                return True
        except Exception as e:
            print(f"[warn] Error checking {note_file.name}: {e}")
            continue

    print("[info] No duplicates found")
    return False


if __name__ == "__main__":
    exit_code = 0 if check_duplicate_notes() else 1
    sys.exit(exit_code)
