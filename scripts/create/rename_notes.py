#!/usr/bin/env python3
"""
Script to rename the last N notes to random dates within the past year
"""

import os
import argparse
import random
from datetime import datetime, timedelta
from typing import List, Tuple
import glob


def generate_random_date() -> str:
    """Generate a random date within the past year"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    random_days = random.randint(0, 180)
    random_date = start_date + timedelta(days=random_days)

    return random_date.strftime("%Y-%m-%d")


def parse_filename_date(filename: str) -> datetime:
    """Extract date from filename in YYYY-MM-DD format"""
    parts = filename.split("-", 3)
    if len(parts) < 3:
        return datetime.min
    date_str = "-".join(parts[:3])
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return datetime.min


def get_notes_files_sorted_by_date(notes_dir: str) -> List[Tuple[str, datetime]]:
    """Get all markdown files from notes directory, sorted by date descending"""
    pattern = os.path.join(notes_dir, "*.md")
    note_files = glob.glob(pattern)

    files_with_dates = []
    for filepath in note_files:
        filename = os.path.basename(filepath)
        file_date = parse_filename_date(filename)
        files_with_dates.append((filepath, file_date))

    # Sort by date descending (newest first)
    files_with_dates.sort(key=lambda x: x[1], reverse=True)

    return files_with_dates


def rename_notes_with_random_dates(notes_dir: str, num_notes: int) -> None:
    """Rename the last N notes to random dates within past year"""

    # Get all notes sorted by date (newest first)
    sorted_files = get_notes_files_sorted_by_date(notes_dir)

    if not sorted_files:
        print("No markdown files found in notes directory")
        return

    # Select the last N files (these are the oldest ones since we sort by date desc)
    # "last notes" means the most recent by date, so we take the first N from sorted list
    files_to_rename = sorted_files[:num_notes]

    if len(files_to_rename) == 0:
        print(f"No files to rename (requested {num_notes}, found {len(sorted_files)})")
        return

    print(f"Found {len(sorted_files)} total markdown files")
    print(f"Renaming the {len(files_to_rename)} most recent files:")

    files_renamed = 0
    for filepath, original_date in files_to_rename:
        filename = os.path.basename(filepath)

        # Extract topic part (remove date prefix)
        filename_parts = filename.split("-", 3)
        if len(filename_parts) >= 4:
            topic_name = "-".join(filename_parts[3:])
        else:
            topic_name = filename

        # Generate random date
        random_date = generate_random_date()

        # Create new filename
        new_filename = f"{random_date}-{topic_name}"
        new_filepath = os.path.join(notes_dir, new_filename)

        try:
            os.rename(filepath, new_filepath)
            print(f"Renamed: {filename} -> {new_filename}")
            files_renamed += 1
        except Exception as e:
            print(f"Error renaming {filename}: {e}")

    print(f"\nSuccessfully renamed {files_renamed} files")


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Rename the last N notes to random dates within the past year"
    )
    parser.add_argument(
        "-n",
        "--num-notes",
        type=int,
        default=1,
        help="Number of notes to rename (default: 1)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    notes_dir = os.path.abspath("./notes")

    if not os.path.exists(notes_dir):
        print(f"Error: notes directory not found: {notes_dir}")
        exit(1)

    rename_notes_with_random_dates(notes_dir, args.num_notes)
