#!/usr/bin/env python3
"""
Script to move markdown files from pnotes/ to notes/ with random dates in last year
"""

import os
import shutil
import random
from datetime import datetime, timedelta
import glob


def generate_random_date():
    """Generate a random date within the last year"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    random_days = random.randint(0, 180)
    random_date = start_date + timedelta(days=random_days)

    return random_date.strftime("%Y-%m-%d")


def move_files_with_random_dates():
    """Move markdown files from pnotes to notes with random dates"""

    # Get absolute paths
    base_dir = "/Users/lzwjava/projects/lzwjava.github.io"
    pnotes_dir = os.path.join(base_dir, "pnotes")
    notes_dir = os.path.join(base_dir, "notes")

    # Ensure pnotes directory exists
    if not os.path.exists(pnotes_dir):
        print(f"Error: pnotes directory not found: {pnotes_dir}")
        return

    # Ensure notes directory exists
    os.makedirs(notes_dir, exist_ok=True)

    # Get all markdown files from pnotes
    pattern = os.path.join(pnotes_dir, "*.md")
    pnote_files = glob.glob(pattern)

    if not pnote_files:
        print("No markdown files found in pnotes directory")
        return

    print(f"Found {len(pnote_files)} files to move:")

    files_moved = 0
    for src_path in pnote_files:
        filename = os.path.basename(src_path)

        # Extract filename part (remove date)
        filename_parts = filename.split("-", 3)
        if len(filename_parts) >= 4:
            # Has date prefix, extract topic and suffix
            name_parts = filename_parts[3:]
            topic_name = "-".join(name_parts)
        else:
            # No date prefix, use filename as-is
            topic_name = filename

        # Generate random date
        random_date = generate_random_date()

        # Create new filename
        new_filename = f"{random_date}-{topic_name}"
        dest_path = os.path.join(notes_dir, new_filename)

        try:
            shutil.move(src_path, dest_path)
            print(f"Moved: {filename} -> {new_filename}")
            files_moved += 1
        except Exception as e:
            print(f"Error moving {filename}: {e}")

    print(f"\nSuccessfully moved {files_moved} files")

    # Check if pnotes is empty and remove if so
    remaining_files = glob.glob(os.path.join(pnotes_dir, "*"))
    if not remaining_files:
        try:
            os.rmdir(pnotes_dir)
            print("pnotes directory is now empty and removed")
        except OSError:
            print("Could not remove pnotes directory (may contain hidden files)")


if __name__ == "__main__":
    move_files_with_random_dates()
