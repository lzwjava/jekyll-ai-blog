import os
import sys
import glob
import argparse
import re

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


def extract_content_length(file_path):
    """Extract the main content length from a markdown file, excluding front matter."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split by front matter delimiters
        parts = content.split("---", 2)
        if len(parts) >= 3:
            # Content after front matter
            main_content = parts[2].strip()
        else:
            # No front matter, entire content
            main_content = content.strip()

        return len(main_content)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0


def extract_title_from_file(file_path):
    """Extract title from front matter or filename."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Try to extract title from front matter
        parts = content.split("---", 2)
        if len(parts) >= 3:
            front_matter = parts[1]
            for line in front_matter.split("\n"):
                if line.strip().startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip("\"'")
                    return title

        # Fallback to filename
        filename = os.path.basename(file_path)
        # Remove date prefix and extension
        title = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", filename)
        title = re.sub(r"\.(md|markdown)$", "", title)
        return title.replace("-", " ").title()

    except Exception as e:
        return os.path.basename(file_path)


def find_short_posts(directory="original", max_length=500):
    """Find posts shorter than the specified character limit."""
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist")
        return

    # Find all markdown files
    pattern = os.path.join(directory, "*.md")
    md_files = glob.glob(pattern)

    if not md_files:
        print(f"No markdown files found in '{directory}'")
        return

    short_posts = []

    print(
        f"Scanning {len(md_files)} files in '{directory}' for posts shorter than {max_length} characters..."
    )
    print("-" * 80)

    for file_path in md_files:
        content_length = extract_content_length(file_path)
        if content_length <= max_length:
            title = extract_title_from_file(file_path)
            short_posts.append(
                {"file": file_path, "title": title, "length": content_length}
            )

    # Sort by length (shortest first)
    short_posts.sort(key=lambda x: x["length"])

    if short_posts:
        print(f"Found {len(short_posts)} posts shorter than {max_length} characters:\n")

        for i, post in enumerate(short_posts, 1):
            filename = os.path.basename(post["file"])
            print(f"{i:2d}. {filename}")
            print(f"    Title: {post['title']}")
            print(f"    Length: {post['length']} characters")
            print(f"    Path: {post['file']}")
            print()

        print("-" * 80)
        print(f"Summary: {len(short_posts)} short posts found (≤ {max_length} chars)")

        # Show file paths for easy copying
        print("\nFile paths for merging:")
        for post in short_posts:
            print(post["file"])

    else:
        print(f"No posts found shorter than {max_length} characters.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find short blog posts in the original directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python find_short_posts.py                    # Find posts ≤ 500 chars
  python find_short_posts.py --length 300       # Find posts ≤ 300 chars
  python find_short_posts.py --dir _posts       # Search in _posts directory
  python find_short_posts.py --length 1000 --dir original  # Custom length and directory
        """,
    )

    parser.add_argument(
        "--length",
        type=int,
        default=500,
        help="Maximum character length for short posts (default: 500)",
    )

    parser.add_argument(
        "--dir",
        default="original",
        help="Directory to search for markdown files (default: original)",
    )

    args = parser.parse_args()

    find_short_posts(args.dir, args.length)
