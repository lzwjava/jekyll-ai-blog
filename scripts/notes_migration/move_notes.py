#!/usr/bin/env python3

import os
import shutil
import argparse

parser = argparse.ArgumentParser(description="Move note files from _notes to _posts")
parser.add_argument("-n", type=int, help="Number of notes to move")
args = parser.parse_args()

moved_count = 0

for lang in os.listdir("_notes"):
    lang_dir = os.path.join("_notes", lang)
    if not os.path.isdir(lang_dir):
        continue
    posts_lang_dir = os.path.join("_posts", lang)
    if not os.path.exists(posts_lang_dir):
        os.makedirs(posts_lang_dir)
    for filename in os.listdir(lang_dir):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(lang_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        # Simple frontmatter check
        first_marker = content.find("---")
        second_marker = content.find("---", first_marker + 3)
        if first_marker == -1 or second_marker == -1:
            continue  # Not proper frontmatter
        frontmatter = content[first_marker : second_marker + 3]
        if "type: note" not in frontmatter:
            continue
        if args.n is not None and moved_count >= args.n:
            continue
        dest_path = os.path.join(posts_lang_dir, filename)
        if os.path.exists(dest_path):
            raise Exception(f"Destination file already exists: {dest_path}")
        shutil.move(filepath, dest_path)
        print(f"Moved {filepath} -> {dest_path}")
        moved_count += 1

print(f"Total moved: {moved_count}")
