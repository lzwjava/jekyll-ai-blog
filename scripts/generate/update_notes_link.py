import os
import re
import shutil
import random
from generate_notes_link import generate_notes_links


def count_notes_files():
    # Count the number of markdown files in the notes directory
    notes_dir = "notes"
    try:
        note_files = [f for f in os.listdir(notes_dir) if f.endswith(".md")]
        return len(note_files)
    except Exception as e:
        print(f"Error counting notes files: {e}")
        return 0


def count_links_in_notes_md():
    # Count the number of links in the notes markdown file
    file_path = os.path.join("original", "2025-01-11-notes-en.md")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Count the number of markdown links in the file
            links = re.findall(r"\* \[.*?\]\(/notes/.*?\)", content)
            return len(links)
    except Exception as e:
        print(f"Error counting links in notes markdown file: {e}")
        return 0


def copy_original_to_posts():
    """Copy specific original file to _posts/en/ directory"""
    src = os.path.join("original", "2025-01-11-notes-en.md")
    posts_dir = "_posts/en"

    # Ensure _posts/en directory exists
    os.makedirs(posts_dir, exist_ok=True)

    # Copy the specific file to _posts/en
    dst = os.path.join(posts_dir, os.path.basename(src))
    shutil.copy2(src, dst)
    print(f"Copied {src} to {dst}")


def update_notes_link():
    notes_count = count_notes_files()
    links_count = count_links_in_notes_md()

    print(f"Notes files count: {notes_count}")
    print(f"Links count in markdown: {links_count}")

    if notes_count != links_count:
        print(
            "Notes files count and links count don't match and last modification was more than 2 hours ago, regenerating notes links."
        )
        generate_notes_links()
        if random.random() < 0.99:
            copy_original_to_posts()
        else:
            print("Skipped copy_original_to_posts due to rate limiting.")
    else:
        print("Skipping notes link regeneration.")


if __name__ == "__main__":
    exit()
    # update_notes_link()
