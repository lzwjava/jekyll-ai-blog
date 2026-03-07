#!/usr/bin/env python3

import os
import re
import yaml


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


def get_latest_posts(original_dir, count=10):
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
                        "url": url_path,
                        "date": date_str,
                        "mtime": mtime,
                        "filename": filename,
                    }
                )

    # Sort by modification time (most recent first)
    posts.sort(key=lambda x: x["mtime"], reverse=True)

    return posts[:count]


def update_404_page(error_file, posts):
    """Update the 404 page with latest posts"""
    with open(error_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the section to replace - look for everything after the ---- line
    lines = content.split("\n")
    new_lines = []
    found_section = False

    for line in lines:
        new_lines.append(line)
        if line.strip() == "----" and not found_section:
            found_section = True
            # Add the posts after the ---- line
            new_lines.append("")
            for post in posts:
                new_lines.append(f"* [{post['title']}]({post['url']})")
            break

    # Join all lines back together
    new_content = "\n".join(new_lines) + "\n"

    # Write back to file
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(new_content)


def main():
    # Paths
    original_dir = "/Users/lzwjava/projects/lzwjava.github.io/original"
    error_file = (
        "/Users/lzwjava/projects/lzwjava.github.io/original/2025-01-14-error-en.md"
    )

    # Get latest posts
    latest_posts = get_latest_posts(original_dir, 10)

    print(f"Found {len(latest_posts)} latest posts:")
    for post in latest_posts:
        print(f"  - {post['title']} ({post['filename']})")

    # Update 404 page
    update_404_page(error_file, latest_posts)
    print(f"\nUpdated {error_file} with latest posts")


if __name__ == "__main__":
    main()
