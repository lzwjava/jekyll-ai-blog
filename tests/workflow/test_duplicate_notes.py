#!/usr/bin/env python3
"""
Fast duplicate detection for notes - group by date and compare within each date

Groups notes by date from filename (YYYY-MM-DD prefix) and checks for duplicates
within each date group using fast content comparison.

Usage:
    python test_duplicate_notes.py          # Test mode - reports duplicates
    python test_duplicate_notes.py --fix    # Fix mode - removes duplicates
"""

import argparse
import os
import re
from pathlib import Path
import unittest
import sys


class DuplicateNotesHandler:
    """Handler for finding and removing duplicate notes."""

    def __init__(self, notes_dir=None):
        self.notes_dir = notes_dir or Path(__file__).parent.parent.parent / "notes"
        self.note_files = []

        # Find all markdown files in notes directory
        if self.notes_dir.exists():
            self.note_files = list(self.notes_dir.glob("*.md"))

    def _extract_date_from_filename(self, filename):
        """Extract date from filename (format: YYYY-MM-DD-title)"""
        match = re.match(r"^(\d{4}-\d{2}-\d{2})-", filename)
        return match.group(1) if match else None

    def _extract_content_without_frontmatter(self, file_path):
        """Extract content without front matter"""
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
            print(f"Error reading {file_path}: {e}")
            return ""

    def _char_similarity(self, text1, text2):
        """Character-by-character similarity ratio between two strings."""
        if not text1 or not text2:
            return 0.0
        matches = sum(c1 == c2 for c1, c2 in zip(text1, text2))
        return matches / max(len(text1), len(text2))

    def _are_notes_quick_similar(self, content1, content2):
        """Fast similarity check between two note contents.

        Checks both the first N and last N characters.
        If either region matches, the notes are considered duplicates.
        """
        if not content1 or not content2:
            return False

        # Quick length check within 5% tolerance
        len1 = len(content1)
        len2 = len(content2)
        if max(len1, len2) == 0:
            return False

        if abs(len1 - len2) / max(len1, len2) > 0.05:
            return False

        # Short content: exact match
        if len1 < 100 or len2 < 100:
            return content1.strip() == content2.strip()

        # Check first 200 chars
        first_match = False
        first200_1 = content1[:200]
        first200_2 = content2[:200]
        if first200_1[:100] == first200_2[:100]:
            if self._char_similarity(first200_1, first200_2) >= 0.90:
                first_match = True

        # Check last 200 chars
        last_match = False
        last200_1 = content1[-200:]
        last200_2 = content2[-200:]
        if last200_1[-100:] == last200_2[-100:]:
            if self._char_similarity(last200_1, last200_2) >= 0.90:
                last_match = True

        return first_match or last_match

    def find_duplicates(self):
        """Find duplicate notes within each date group. Returns list of duplicate pairs."""
        if not self.note_files:
            return []

        # Group notes by date
        date_groups = {}
        for file_path in self.note_files:
            date = self._extract_date_from_filename(file_path.name)
            if date:
                if date not in date_groups:
                    date_groups[date] = []
                date_groups[date].append(file_path)
            else:
                # Files without date prefixes go to special group
                if "no_date" not in date_groups:
                    date_groups["no_date"] = []
                date_groups["no_date"].append(file_path)

        duplicates = []

        # Check for duplicates within each date group
        for date, files in date_groups.items():
            if len(files) <= 1:
                continue

            # Read all contents for this date
            contents = {}
            for file_path in files:
                content = self._extract_content_without_frontmatter(file_path)
                contents[file_path] = content

            # Check each pair only once
            file_paths = list(contents.keys())
            for i, path1 in enumerate(file_paths):
                for j, path2 in enumerate(file_paths[i + 1 :], i + 1):
                    if self._are_notes_quick_similar(contents[path1], contents[path2]):
                        duplicates.append((path1, path2))

        return duplicates

    def test_no_duplicate_notes(self):
        """Test that there are no duplicate notes within each date group."""
        duplicates = self.find_duplicates()

        if duplicates:
            print("✗ DUPLICATE NOTES DETECTED:")
            print("-" * 40)
            for path1, path2 in duplicates:
                print(f"  {path1.name} ~ {path2.name}")
            print(f"-" * 40)
            self.fail(f"Found {len(duplicates)} duplicate note pairs")
        else:
            total_files = len(self.note_files)
            print(f"✓ No duplicates found among {total_files} files")


def fix_duplicates():
    """Find and remove duplicate notes."""
    handler = DuplicateNotesHandler()
    duplicates = handler.find_duplicates()

    if not duplicates:
        print("✓ No duplicates found")
        return

    print(f"Found {len(duplicates)} duplicate pairs")
    removed_count = 0

    for path1, path2 in duplicates:
        # Keep the first file, remove the second
        to_remove = path2  # Remove the second file in pair
        print(f"Removing duplicate: {to_remove.name}")
        try:
            to_remove.unlink()
            removed_count += 1
            print(f"  ✓ Removed {to_remove.name}")
        except Exception as e:
            print(f"  ✗ Failed to remove {to_remove.name}: {e}")

    print(f"✓ Removed {removed_count} duplicate files")


class TestDuplicateNotes(unittest.TestCase):
    """Test case for detecting duplicate notes group by date."""

    def setUp(self):
        """Set up test by finding all note files."""
        self.handler = DuplicateNotesHandler()

    def test_no_duplicate_notes(self):
        """Test that there are no duplicate notes within each date group."""
        duplicates = self.handler.find_duplicates()

        if duplicates:
            print("✗ DUPLICATE NOTES DETECTED:")
            print("-" * 40)
            for path1, path2 in duplicates:
                print(f"  {path1.name} ~ {path2.name}")
            print(f"-" * 40)
            self.fail(f"Found {len(duplicates)} duplicate note pairs")
        else:
            total_files = len(self.handler.note_files)
            print(f"✓ No duplicates found among {total_files} files")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Detect and optionally remove duplicate notes"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Remove duplicates instead of just testing"
    )

    args = parser.parse_args()

    if args.fix:
        fix_duplicates()
    else:
        unittest.main()
