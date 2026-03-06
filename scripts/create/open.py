#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import re
from pathlib import Path


def get_latest_notes(notes_dir, count=10):
    """Get the latest modified notes sorted by modification time"""
    notes_path = Path(notes_dir)
    if not notes_path.exists():
        print(f"Notes directory {notes_dir} does not exist")
        return []

    notes = []
    for note_file in notes_path.glob("*.md"):
        mtime = note_file.stat().st_mtime
        notes.append((mtime, note_file))

    notes.sort(key=lambda x: x[0], reverse=True)
    return [note[1] for note in notes[:count]]


def get_note_url(note_filename):
    """Generate the URL for a note based on its filename"""
    base_name = note_filename.stem
    return f"https://lzwjava.github.io/notes/{base_name}"


def get_note_title(note_path):
    """Extract title from the frontmatter of a markdown file"""
    try:
        with open(note_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Look for frontmatter between --- delimiters
        frontmatter_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            # Look for title field
            title_match = re.search(r"^title:\s*(.+)$", frontmatter, re.MULTILINE)
            if title_match:
                return title_match.group(1).strip()

        # Fallback to filename without extension if no title found
        return note_path.stem
    except Exception as e:
        print(f"Warning: Could not read title from {note_path.name}: {e}")
        return note_path.stem


def open_browser(url):
    """Open URL in default browser"""
    try:
        if sys.platform.startswith("darwin"):
            subprocess.run(["open", url])
        elif sys.platform.startswith("win"):
            subprocess.run(["start", url], shell=True)
        else:
            subprocess.run(["xdg-open", url])
    except Exception as e:
        print(f"Failed to open browser: {e}")


def main():
    parser = argparse.ArgumentParser(description="Open latest note in browser")
    parser.add_argument(
        "--notes-dir",
        default="./notes",
        help="Path to notes directory (default: ./notes)",
    )

    args = parser.parse_args()

    notes_dir = Path(args.notes_dir).resolve()
    if not notes_dir.is_absolute():
        notes_dir = Path(__file__).parent / args.notes_dir

    # Get latest 10 notes
    latest_notes = get_latest_notes(notes_dir, 10)

    if not latest_notes:
        print("No notes found")
        return

    # Display the list of notes numbered 0-9
    print("Recent notes:")
    for i, note in enumerate(latest_notes):
        title = get_note_title(note)
        print(f"{i}: {title}")

    # Get user input for selection
    while True:
        try:
            selection = input("Select a note (0-9): ").strip()
            selection_idx = int(selection)
            if 0 <= selection_idx < len(latest_notes):
                break
            else:
                print(f"Please enter a number between 0 and {len(latest_notes) - 1}")
        except ValueError:
            print("Please enter a valid number")

    selected_note = latest_notes[selection_idx]
    note_url = get_note_url(selected_note)

    print(f"Opening: {selected_note.name}")
    print(f"URL: {note_url}")

    open_browser(note_url)


if __name__ == "__main__":
    main()
