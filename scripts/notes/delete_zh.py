#!/usr/bin/env python3
"""
Delete Chinese note files ending with -zh.md in the notes directory.
"""

import os
from pathlib import Path


def delete_chinese_notes():
    """Delete all Chinese note files ending with -zh.md"""
    notes_dir = Path(__file__).parent.parent.parent / "notes"
    pattern = "*-zh.md"

    # Find all Chinese note files
    chinese_files = list(notes_dir.glob(pattern))

    if not chinese_files:
        print("No Chinese note files found.")
        return

    print(f"Found {len(chinese_files)} Chinese note files:")
    for file in chinese_files:
        print(f"  - {file.name}")

    # Confirm deletion
    response = input("\nDo you want to delete these files? (y/N): ").strip().lower()
    if response != "y":
        print("Deletion cancelled.")
        return

    # Delete files
    deleted_count = 0
    for file in chinese_files:
        try:
            os.remove(file)
            print(f"Deleted: {file.name}")
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {file.name}: {e}")

    print(f"\nSuccessfully deleted {deleted_count} files.")


if __name__ == "__main__":
    delete_chinese_notes()
