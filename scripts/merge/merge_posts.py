import os
import sys
import argparse
import re

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


def get_post_date(content):
    """Extract date from post front matter."""
    parts = content.split("---", 2)
    if len(parts) >= 3:
        front_matter = parts[1]
        for line in front_matter.split("\n"):
            if line.startswith("date:"):
                return line.split(":", 1)[1].strip().strip("\"'")
    return None


def extract_date_from_filename(filename):
    """Extract date from filename in format YYYY-MM-DD."""
    # Match dates in filenames like 2025-07-30-beyond-expectations-en.md
    match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
    if match:
        date_str = match.group(1)
        # Convert from YYYY-MM-DD to YYYY.MM.DD format
        return date_str.replace("-", ".")
    return None


def process_post_content(content, filename=None):
    """Process a single post's content and extract metadata."""
    sub_parts = content.split("---", 2)
    date = None
    title = None
    body = content

    if len(sub_parts) >= 3:
        front_matter = sub_parts[1]
        body = sub_parts[2].strip()

        for line in front_matter.split("\n"):
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip("\"'")
            elif line.startswith("date:"):
                date = line.split(":", 1)[1].strip().strip("\"'")

    # If no date in front matter, try to extract from filename
    if not date and filename:
        date = extract_date_from_filename(filename)

    return {"content": content, "body": body, "title": title, "date": date}


def merge_post_contents(contents):
    """Merge multiple post contents into one."""
    if len(contents) < 2:
        print("Error: At least 2 posts are required")
        return None
    if len(contents) > 10:
        print("Error: Maximum 10 posts allowed")
        return None

    # Process and sort posts
    post_data = [process_post_content(content) for content in contents]
    post_data.sort(key=lambda x: x["date"] if x["date"] else "", reverse=True)

    # First post is main post
    main_content = post_data[0]["content"]
    combined_content = main_content

    # Process sub posts
    for post in post_data[1:]:
        if post["title"]:
            header = f"## {post['title']}"
            if post["date"]:
                header += f", {post['date']}"
            sub_body = f"{header}\n\n{post['body']}"
        else:
            sub_body = post["body"].strip()

        if sub_body:
            combined_content += "\n\n---\n\n" + sub_body

    return combined_content


def merge_post_contents_with_filenames(post_data):
    """Merge multiple post contents into one, using argument order (first argument becomes main post)."""
    contents = [post["content"] for post in post_data]
    filenames = [post["filename"] for post in post_data]

    if len(contents) < 2:
        print("Error: At least 2 posts are required")
        return None
    if len(contents) > 10:
        print("Error: Maximum 10 posts allowed")
        return None

    # Process posts (keep argument order - first is main)
    processed_posts = []
    for i, content in enumerate(contents):
        filename = filenames[i] if i < len(filenames) else None
        processed_posts.append(process_post_content(content, filename))

    # First argument becomes main post (no sorting by date)
    main_content = processed_posts[0]["content"]
    combined_content = main_content

    # Process sub posts - add date in the format *2025.07.12* after the section title
    for post in processed_posts[1:]:
        if post["title"]:
            header = f"## {post['title']}"
            if post["date"]:
                # Date is already in format YYYY.MM.DD from filename extraction
                header += f"\n\n*{post['date']}*"
            sub_body = f"{header}\n\n{post['body']}"
        else:
            sub_body = post["body"].strip()

        if sub_body:
            combined_content += "\n\n---\n\n" + sub_body

    return combined_content


def combine_posts(posts):
    """Combine multiple posts from files."""
    # Read contents from files
    post_data = []
    for path in posts:
        abs_path = os.path.abspath(path) if not os.path.isabs(path) else path
        if not os.path.exists(abs_path):
            print(f"Error: Post file not found: {abs_path}")
            return

        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
                post_data.append(
                    {"content": content, "filename": os.path.basename(abs_path)}
                )
        except Exception as e:
            print(f"Error reading file {abs_path}: {e}")
            return

    # Merge contents
    combined_content = merge_post_contents_with_filenames(post_data)
    if combined_content is None:
        return

    # Write result back to first file
    main_path = os.path.abspath(posts[0])
    try:
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(combined_content)
        print(f"Successfully combined content into: {main_path}")
    except Exception as e:
        print(f"Error writing combined content: {e}")
        return

    print("Combine operation completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine multiple blog posts (max 10)")
    parser.add_argument(
        "posts",
        nargs="+",
        help="Paths to post files. First will be main post, others will be appended to it.",
    )

    args = parser.parse_args()
    combine_posts(args.posts)
