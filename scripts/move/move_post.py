import os
import shutil
import frontmatter
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


def main():
    # Create original directory
    os.makedirs("original", exist_ok=True)
    print("Created directory 'original'")

    # Get all language directories in _posts
    posts_dir = "_posts"
    if os.path.exists(posts_dir):
        for item in os.listdir(posts_dir):
            lang_dir = os.path.join(posts_dir, item)
            if os.path.isdir(lang_dir) and item != "original":
                process_posts_in_lang_dir(lang_dir, date_threshold)
    else:
        print(f"Directory {posts_dir} does not exist")


if __name__ == "__main__":
    main()
