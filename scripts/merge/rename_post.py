import os
import shutil
import argparse
from datetime import datetime

date_threshold = datetime(2022, 9, 29)


def copy_file(source_file, target_file):
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    shutil.copy2(source_file, target_file)
    print(f"Copied {source_file} to {target_file}")


def get_original_lang_from_filename(filename):
    """Extract original language from filename like 2023-01-01-title-en.md"""
    for lang in ["en", "zh", "ja"]:
        if filename.endswith(f"-{lang}.md"):
            return lang
    return None


def process_posts_in_lang_dir(lang_dir, date_threshold):
    """Process posts in a specific language directory like _posts/en"""
    print(f"Processing posts in {lang_dir}")

    if not os.path.exists(lang_dir):
        print(f"  Directory {lang_dir} does not exist, skipping")
        return

    for filename in os.listdir(lang_dir):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(lang_dir, filename)
        print(f"  Processing {filepath}")

        try:
            parts = filename.split("-")
            if len(parts) < 4:
                print(f"    Skipped {filepath} due to invalid filename format.")
                continue

            date_str = "-".join(parts[:3])
            post_date = datetime.strptime(date_str, "%Y-%m-%d")
            print(f"    Post date: {post_date}")

            # Extract original language from filename
            original_lang = get_original_lang_from_filename(filename)
            if not original_lang:
                print(f"    Could not determine original language from {filename}")
                continue

            # Determine if this should be moved to original based on date and language
            should_move = False
            if original_lang == "en" and post_date > date_threshold:
                should_move = True
                reason = f"english post after {date_threshold}"
            elif original_lang == "zh" and post_date < date_threshold:
                should_move = True
                reason = f"chinese post before {date_threshold}"

            if should_move:
                target_file = os.path.join("original", filename)
                copy_file(filepath, target_file)
                print(
                    f"    Moved {filepath} to original folder because it is a {reason}"
                )
            else:
                print(f"    Skipped {filepath} due to date condition.")

        except Exception as e:
            print(f"    Error processing {filepath}: {e}")


def rename_post(old_name, new_name):
    """Rename a post file in both original/ and _posts/lang directories"""
    renamed_files = []

    # Check and rename in original/ directory
    original_old_path = os.path.join("original", old_name)
    original_new_path = os.path.join("original", new_name)

    if os.path.exists(original_old_path):
        os.rename(original_old_path, original_new_path)
        print(f"Renamed {original_old_path} to {original_new_path}")
        renamed_files.append(original_old_path)

    # Check and rename in _posts/lang directories
    posts_dir = "_posts"
    if os.path.exists(posts_dir):
        for lang in os.listdir(posts_dir):
            lang_dir = os.path.join(posts_dir, lang)
            if os.path.isdir(lang_dir):
                lang_old_path = os.path.join(lang_dir, old_name)
                lang_new_path = os.path.join(lang_dir, new_name)

                if os.path.exists(lang_old_path):
                    os.rename(lang_old_path, lang_new_path)
                    print(f"Renamed {lang_old_path} to {lang_new_path}")
                    renamed_files.append(lang_old_path)

    if not renamed_files:
        print(f"File {old_name} not found in any directory")
    else:
        print(f"Successfully renamed {len(renamed_files)} file(s)")


def main():
    parser = argparse.ArgumentParser(
        description="Rename post files or process posts based on date"
    )
    parser.add_argument(
        "--rename",
        nargs=2,
        metavar=("OLD_NAME", "NEW_NAME"),
        help="Rename a post file (e.g., --rename old.md new.md)",
    )
    parser.add_argument(
        "--process",
        action="store_true",
        help="Process posts based on date threshold (original functionality)",
    )

    args = parser.parse_args()

    if args.rename:
        old_name, new_name = args.rename
        rename_post(old_name, new_name)
    elif args.process:
        # Original functionality
        os.makedirs("original", exist_ok=True)
        print("Created directory 'original'")

        posts_dir = "_posts"
        if os.path.exists(posts_dir):
            for item in os.listdir(posts_dir):
                lang_dir = os.path.join(posts_dir, item)
                if os.path.isdir(lang_dir) and item != "original":
                    process_posts_in_lang_dir(lang_dir, date_threshold)
        else:
            print(f"Directory {posts_dir} does not exist")
    else:
        print("Please specify either --rename or --process option")
        parser.print_help()


if __name__ == "__main__":
    main()
