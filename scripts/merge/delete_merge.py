import os
import sys
import argparse

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from scripts.create.delete import delete_md


def delete_combine_posts(posts):
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

    # Sort posts by date in descending order
    post_data.sort(key=lambda x: x["date"] if x["date"] else "", reverse=True)

    # Keep the original for the first post, delete others completely
    if post_data:
        print(f"Keeping original for: {post_data[0]['path']}")
        delete_md(post_data[0]["path"], False)

    # Delete all posts except the first one
    for post in post_data[1:]:
        print(f"Deleting post: {post['path']}")
        delete_md(post["path"], True)

    print("Delete operation completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Delete all posts except the first one (sorted by date). Original files are deleted by default."
    )
    parser.add_argument(
        "posts", nargs="+", help="Paths to post files. First by date will be kept."
    )

    args = parser.parse_args()
    delete_combine_posts(args.posts)
