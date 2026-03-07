import os
import argparse
from type_flag_util import update_front_matter


def main():
    parser = argparse.ArgumentParser(
        description="Update front matter in blog post files"
    )
    parser.add_argument("-n", type=int, help="Maximum number of files to update")
    parser.add_argument(
        "--type",
        default="post",
        help="Type value to set in front matter (default: post)",
    )
    args = parser.parse_args()

    original_dir = "original"
    posts_dir = "_posts"
    count = 0

    # Process files in original directory
    if not args.n or count < args.n:
        for filename in os.listdir(original_dir):
            if filename.endswith(".md") and (not args.n or count < args.n):
                file_path = os.path.join(original_dir, filename)
                update_front_matter(file_path, args.type)
                count += 1

    # Process files in _posts directories
    if not args.n or count < args.n:
        for lang_dir in os.listdir(posts_dir):
            lang_dir_path = os.path.join(posts_dir, lang_dir)
            if os.path.isdir(lang_dir_path):
                for filename in os.listdir(lang_dir_path):
                    if filename.endswith(".md") and (not args.n or count < args.n):
                        file_path = os.path.join(lang_dir_path, filename)
                        update_front_matter(file_path)
                        count += 1


if __name__ == "__main__":
    main()
