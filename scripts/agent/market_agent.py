#!/usr/bin/env python3

import os
import re
import yaml
import pyperclip
import argparse


def extract_frontmatter(file_path):
    """Extract YAML frontmatter from markdown file"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if file starts with frontmatter
    if not content.startswith("---"):
        return None, content

    # Find the end of frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content

    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2]
        return frontmatter, body
    except yaml.YAMLError:
        return None, content


def get_latest_posts(original_dir, count=5):
    """Get the latest posts by modification time"""
    posts = []

    for filename in os.listdir(original_dir):
        if filename.endswith(".md") and filename != "2025-01-14-error-en.md":
            file_path = os.path.join(original_dir, filename)
            frontmatter, _ = extract_frontmatter(file_path)

            if frontmatter and frontmatter.get("title"):
                # Get file modification time
                mtime = os.path.getmtime(file_path)

                # Extract date from filename
                date_match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
                date_str = date_match.group(1) if date_match else "1970-01-01"

                # Generate URL path - remove date prefix
                url_path = "/" + re.sub(
                    r"^\d{4}-\d{2}-\d{2}-", "", filename.replace(".md", "")
                )

                posts.append(
                    {
                        "title": frontmatter["title"],
                        "url": f"https://lzwjava.github.io{url_path}",
                        "date": date_str,
                        "mtime": mtime,
                        "filename": filename,
                    }
                )

    # Sort by modification time (most recent first)
    posts.sort(key=lambda x: x["mtime"], reverse=True)

    return posts[:count]


def format_for_wechat(posts):
    """Format posts for WeChat sharing - one line title, one line link"""
    formatted_lines = []

    for post in posts:
        formatted_lines.append(post["title"])
        formatted_lines.append(post["url"])
        formatted_lines.append("")  # Empty line for separation

    # Remove the last empty line
    if formatted_lines and formatted_lines[-1] == "":
        formatted_lines.pop()

    return "\n".join(formatted_lines)


def main():
    parser = argparse.ArgumentParser(description="Generate WeChat-formatted post list")
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=5,
        help="Number of latest posts to include (default: 5)",
    )

    args = parser.parse_args()

    # Path to original directory
    original_dir = "/Users/lzwjava/projects/lzwjava.github.io/original"

    # Get latest posts
    latest_posts = get_latest_posts(original_dir, args.count)

    print(f"Found {len(latest_posts)} latest posts:")
    for i, post in enumerate(latest_posts, 1):
        print(f"  {i}. {post['title']} ({post['date']})")

    # Format for WeChat
    wechat_format = format_for_wechat(latest_posts)

    # Copy to clipboard
    pyperclip.copy(wechat_format)

    print("\n✅ Formatted content copied to clipboard!")
    print("You can now paste it to WeChat to share with others.")
    print("\nPreview:")
    print("-" * 50)
    print(wechat_format)


if __name__ == "__main__":
    main()
