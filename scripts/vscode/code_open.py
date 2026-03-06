#!/usr/bin/env python3
import sys
import os
import subprocess
import re
from urllib.parse import urlparse


def get_local_file_from_url(url):
    """Convert a GitHub Pages URL to the corresponding local file path"""
    parsed = urlparse(url)

    # Extract the path from the URL
    path = parsed.path.strip("/")

    if not path:
        return None

    # Extract language from the path (e.g., "portfolio-fr" -> "fr")
    match = re.match(r"([^-]+)-([a-z]{2,4})$", path)
    if not match:
        return None

    page_name = match.group(1)
    lang = match.group(2)

    # Map to the local file structure
    # Look for files matching the pattern in _posts/{lang}/
    posts_dir = f"_posts/{lang}"
    if not os.path.exists(posts_dir):
        return None

    # Find the file that matches the pattern
    for filename in os.listdir(posts_dir):
        if filename.endswith(f"-{page_name}-{lang}.md"):
            return os.path.join(posts_dir, filename)

    return None


def open_file_in_vscode(file_path):
    """Open the file in VS Code"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    try:
        subprocess.run(["code", file_path], check=True)
        print(f"Opened: {file_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error opening file: {e}")
        return False
    except FileNotFoundError:
        print(
            "VS Code (code command) not found. Please install VS Code command line tools."
        )
        return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python code_open.py <url_or_file_path>")
        sys.exit(1)

    arg = sys.argv[1]

    # Check if the argument is a URL
    if arg.startswith(("http://", "https://")):
        file_path = get_local_file_from_url(arg)
        if file_path:
            success = open_file_in_vscode(file_path)
            if not success:
                sys.exit(1)
        else:
            print(f"Could not map URL to local file: {arg}")
            sys.exit(1)
    else:
        # Treat as a file path
        success = open_file_in_vscode(arg)
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()
