import os
import glob
import frontmatter
from datetime import datetime
import argparse
import re


def extract_date_from_filename(filename):
    """Extract date from filename in format YYYY-MM-DD"""
    basename = os.path.basename(filename)
    # Look for date pattern YYYY-MM-DD at the beginning of filename
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", basename)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y-%m-%d")
        except ValueError:
            pass
    return None


def get_recent_posts(directory, num_posts=10):
    """Get the most recent markdown posts from a directory, sorted by date in filename"""
    # Get all .md files in the directory
    pattern = os.path.join(directory, "*.md")
    md_files = glob.glob(pattern)

    if not md_files:
        print(f"No markdown files found in {directory}")
        return []

    # Filter files that have valid dates in filename and sort by date
    files_with_dates = []
    files_without_dates = []

    for file_path in md_files:
        date = extract_date_from_filename(file_path)
        if date:
            files_with_dates.append((file_path, date))
        else:
            files_without_dates.append(file_path)

    # Sort files with dates by date (most recent first)
    files_with_dates.sort(key=lambda x: x[1], reverse=True)

    # Sort files without dates by modification time (fallback)
    files_without_dates.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Combine: prioritize files with dates, then files without dates
    sorted_files = [
        file_path for file_path, _ in files_with_dates
    ] + files_without_dates

    # Return the most recent num_posts files
    return sorted_files[:num_posts]


def extract_text_from_post(file_path):
    """Extract text content from a markdown post, removing frontmatter"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Get the content without frontmatter
        content = post.content

        # Get title from frontmatter if available
        title = post.metadata.get("title", os.path.basename(file_path))

        return title, content
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None


def extract_and_save_posts(
    original_dir="original", output_file="tmp/posts.txt", num_posts=10
):
    """Extract text from recent posts and save to a file"""

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Get recent posts
    recent_posts = get_recent_posts(original_dir, num_posts)

    if not recent_posts:
        print("No posts found to process")
        return

    print(f"Processing {len(recent_posts)} recent posts from {original_dir}")

    # Extract text and save to file
    with open(output_file, "w", encoding="utf-8") as f:
        for i, post_file in enumerate(recent_posts, 1):
            print(f"Processing {i}/{len(recent_posts)}: {os.path.basename(post_file)}")

            title, content = extract_text_from_post(post_file)

            if title and content:
                # Write content directly without headers
                f.write(content.strip())
                f.write("\n\n")

    print(f"Text extracted and saved to {output_file}")

    # Print summary
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        word_count = len(content.split())
        char_count = len(content)

    print("Summary:")
    print(f"  - Posts processed: {len(recent_posts)}")
    print(f"  - Total words: {word_count:,}")
    print(f"  - Total characters: {char_count:,}")
    print(f"  - Output file: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from recent markdown posts"
    )
    parser.add_argument(
        "--original-dir",
        default="original",
        help="Directory containing original posts (default: original)",
    )
    parser.add_argument(
        "--output",
        default="tmp/posts.txt",
        help="Output file path (default: tmp/posts.txt)",
    )
    parser.add_argument(
        "--num-posts",
        type=int,
        default=10,
        help="Number of recent posts to extract (default: 10)",
    )

    args = parser.parse_args()

    extract_and_save_posts(
        original_dir=args.original_dir,
        output_file=args.output,
        num_posts=args.num_posts,
    )


if __name__ == "__main__":
    main()
