import os
import datetime
import sys
import re
from pathlib import Path
from delete import delete_md


def _extract_content_without_frontmatter(file_path):
    """Extract content without front matter."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        sections = content.split("---", 2)
        if len(sections) >= 3:
            return sections[2].strip()
        return content.strip()
    except Exception:
        return ""


def _are_notes_quick_similar(content1, content2):
    """Fast similarity check between two note contents."""
    if not content1 or not content2:
        return False
    len1 = len(content1)
    len2 = len(content2)
    if max(len1, len2) == 0:
        return False
    if abs(len1 - len2) / max(len1, len2) > 0.05:
        return False
    if len1 < 100 or len2 < 100:
        return content1.strip() == content2.strip()
    first200_1 = content1[:200]
    first200_2 = content2[:200]
    if first200_1[:100] == first200_2[:100]:
        matches = sum(c1 == c2 for c1, c2 in zip(first200_1, first200_2))
        if matches >= 180:
            return True
    return False


def check_duplicate_before_create(content, notes_dir="notes"):
    """Check if content is duplicate of existing notes."""
    notes_path = Path(notes_dir)
    if not notes_path.exists():
        return False
    note_files = sorted(
        notes_path.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True
    )
    for note_file in note_files[:200]:
        existing_content = _extract_content_without_frontmatter(note_file)
        if _are_notes_quick_similar(content, existing_content):
            print(f"[warn] Duplicate detected: similar to {note_file.name}")
            return True
    return False


def create_md(name, lang="en"):
    """Create a draft Markdown file in the _drafts directory."""
    # Get today's date
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")

    # Define file paths
    drafts_dir = "_drafts"
    if not os.path.exists(drafts_dir):
        os.makedirs(drafts_dir)

    file_path = os.path.join(drafts_dir, f"{date_str}-{name}-{lang}.md")

    # Front matter
    front_matter = f"""---
audio: false
generated: false
image: false
lang: {lang}
layout: post
title: {name}
translated: false
---"""

    # Create the markdown file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(front_matter)

    print(f"Created file: {file_path}")


def create_note(name, lang="en"):
    """Create a note Markdown file in the notes directory."""
    # Get today's date
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")

    # Define file paths
    notes_dir = "notes"
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)

    note_file_path = os.path.join(notes_dir, f"{date_str}-{name}-{lang}.md")

    # Check for duplicates before creating
    if check_duplicate_before_create(name, notes_dir):
        raise ValueError(f"Duplicate note detected for: {name}")

    # Note front matter (simplified version, adjust as needed)
    note_front_matter = f"""---
audio: false
generated: true
lang: {lang}
layout: post
title: {name}
translated: false
---"""

    # Create the note markdown file
    with open(note_file_path, "w", encoding="utf-8") as note_file:
        note_file.write(note_front_matter)

    print(f"Created note: {note_file_path}")


def create_original(name, lang="en"):
    """Create an original Markdown file directly in the _posts/{lang} directory."""
    # Get today's date
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")

    # Define file paths
    posts_dir = os.path.join("_posts", lang)
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)

    file_path = os.path.join(posts_dir, f"{date_str}-{name}-{lang}.md")

    # Front matter (same as create_md)
    front_matter = f"""---
audio: false
generated: false
image: false
lang: {lang}
layout: post
title: {name}
translated: false
---"""

    # Create the markdown file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(front_matter)

    print(f"Created original file: {file_path}")


def move(file_path):
    """Deletes the specified files and moves the original English markdown file to the notes directory."""
    # Extract the file name from the path
    file_name = os.path.basename(file_path)
    name = file_name.split("-en.md")[0]
    delete_md(name)

    if os.path.exists(file_path):
        notes_file = os.path.join("notes", file_name)
        os.makedirs("notes", exist_ok=True)
        os.rename(file_path, notes_file)
        print(f"Moved {file_path} to {notes_file}")
    else:
        print(f"Original file not found: {file_path}")


if __name__ == "__main__":
    """Main entry point to handle command-line arguments."""
    if len(sys.argv) < 3:
        print(
            "Usage: python scripts/file.py <create|create-note|create-original|delete|move> <name> [<lang>]"
        )
        print("For create actions, <lang> is optional, defaults to 'en'.")
        sys.exit(1)

    action = sys.argv[1]
    name = sys.argv[2]
    lang = "en" if len(sys.argv) < 4 else sys.argv[3]

    if action in ["create", "create-note", "create-original"]:
        if action == "create":
            create_md(name, lang=lang)
        elif action == "create-note":
            create_note(name, lang=lang)
        elif action == "create-original":
            create_original(name, lang=lang)
    elif action == "delete":
        delete_md(name)
    elif action == "move":
        move(name)
    else:
        print(
            "Invalid action. Use 'create', 'create-note', 'create-original', 'delete', or 'move'."
        )
