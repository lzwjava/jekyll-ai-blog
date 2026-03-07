import os
import sys
import argparse
import re

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from scripts.create.delete import delete_md


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


def merge_post_contents_with_filenames(post_data):
    """Merge multiple post contents into one, using filename for date extraction."""
    contents = [post["content"] for post in post_data]
    filenames = [post["filename"] for post in post_data]

    if len(contents) < 2:
        print("Error: At least 2 posts are required")
        return None
    if len(contents) > 10:
        print("Error: Maximum 10 posts allowed")
        return None

    # Process posts (maintain argument order)
    processed_posts = []
    for i, content in enumerate(contents):
        filename = filenames[i] if i < len(filenames) else None
        processed_posts.append(process_post_content(content, filename))

    # First post is main post
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


def delete_other_posts(posts):
    """Delete all posts except the first one (sorted by date)."""
    if len(posts) < 2:
        print("Error: At least 2 posts are required")
        return
    if len(posts) > 10:
        print("Error: Maximum 10 posts allowed")
        return

    # Read posts and extract dates
    post_data = []
    for path in posts:
        abs_path = os.path.abspath(path) if not os.path.isabs(path) else path
        if not os.path.exists(abs_path):
            print(f"Error: Post file not found: {abs_path}")
            return

        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
                date = None
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    front_matter = parts[1]
                    for line in front_matter.split("\n"):
                        if line.startswith("date:"):
                            date = line.split(":", 1)[1].strip().strip("\"'")
                            break
                post_data.append({"path": abs_path, "date": date})
        except Exception as e:
            print(f"Error reading file {abs_path}: {e}")
            return

    # Keep argument order (first post in arguments is kept)
    if post_data:
        print(f"Keeping original for: {post_data[0]['path']}")
        delete_md(post_data[0]["path"], False)

    # Delete all posts except the first one
    for post in post_data[1:]:
        print(f"Deleting post: {post['path']}")
        delete_md(post["path"], True)


def merge_then_delete_posts(posts):
    """Merge multiple posts into one, then delete the source posts (except the main one)."""
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
                    {
                        "content": content,
                        "filename": os.path.basename(abs_path),
                        "path": abs_path,
                    }
                )
        except Exception as e:
            print(f"Error reading file {abs_path}: {e}")
            return

    # Merge contents
    combined_content = merge_post_contents_with_filenames(post_data)
    if combined_content is None:
        return

    # Use first post in argument order as main file
    main_path = post_data[0]["path"]

    # Write result to the main file
    try:
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(combined_content)
        print(f"Successfully combined content into: {main_path}")
    except Exception as e:
        print(f"Error writing combined content: {e}")
        return

    # Delete other posts (except the main one)
    posts_to_delete = [post["path"] for post in post_data[1:]]
    for path in posts_to_delete:
        print(f"Deleting post: {path}")
        delete_md(path, True)

    print("Merge and delete operation completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge multiple blog posts (max 10) and delete source posts except the main one"
    )
    parser.add_argument(
        "posts",
        nargs="+",
        help="Paths to post files. Main post will be determined by date.",
    )

    args = parser.parse_args()
    merge_then_delete_posts(args.posts)
