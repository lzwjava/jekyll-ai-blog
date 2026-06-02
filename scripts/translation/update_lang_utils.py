#!/usr/bin/env python3

import os
import re


def get_original_file_for_md_file(md_file):
    """Find the original file for a given post file."""
    # Determine the post type by reading frontmatter
    try:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        # Parse frontmatter
        first_marker = content.find("---")
        second_marker = content.find("---", first_marker + 3)
        if first_marker == -1 or second_marker == -1:
            print(f"  Warning: No valid frontmatter found in {md_file}")
            return None
        frontmatter = content[first_marker : second_marker + 3]
        post_type = "note" if "type: note" in frontmatter else "post"
    except (UnicodeDecodeError, IOError) as e:
        print(f"  Warning: Could not read frontmatter from {md_file}: {e}")
        return None

    # Extract base name and language from post file
    # e.g., _posts/zh/2024-11-29-vision-tips-zh.md -> 2024-11-29-vision-tips, zh
    base_name = os.path.basename(md_file)
    if not base_name.endswith(".md"):
        return None

    # Remove .md extension
    base_name = base_name[:-3]

    # Extract language suffix
    lang_match = re.search(r"-([a-z]{2}|hant)$", base_name)
    if not lang_match:
        return None

    lang = lang_match.group(1)
    base_without_lang = base_name[: -len(lang) - 1]  # Remove -lang suffix

    # Look for original file based on post type
    if post_type == "note":
        notes_dir_flat = "notes"
        if os.path.exists(notes_dir_flat):
            for orig_lang in ["en", "zh", "ja"]:
                original_file = os.path.join(
                    notes_dir_flat, f"{base_without_lang}-{orig_lang}.md"
                )
                if os.path.exists(original_file):
                    return original_file, lang
    else:
        # For posts, look in original directory
        for orig_lang in ["en", "zh", "ja"]:
            original_file = os.path.join(
                "original", f"{base_without_lang}-{orig_lang}.md"
            )
            if os.path.exists(original_file):
                return original_file, lang

    return None
