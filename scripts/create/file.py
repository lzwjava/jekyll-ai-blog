import os
import datetime
import sys
from delete import delete_md


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
