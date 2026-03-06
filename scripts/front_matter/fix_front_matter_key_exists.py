import os
import argparse
import frontmatter
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from tests.workflow.test_front_matter_key import (
    scan_markdown_files_for_front_matter_key_order,
)

# Define the required keys and their expected values based on directory
REQUIRED_KEYS = ["audio", "generated", "lang", "layout", "title", "translated", "type"]


def get_expected_translated_value(file_path):
    """Determine the expected 'translated' value based on file location."""
    if "/original/" in file_path or file_path.startswith("original/"):
        return False
    elif "/_posts/" in file_path or file_path.startswith("_posts/"):
        return True
    elif (
        "/notes/" in file_path
        or "/_notes/" in file_path
        or file_path.startswith("notes/")
        or file_path.startswith("_notes/")
    ):
        return True
    else:
        # Default to True for other locations
        return True


def scan_markdown_files_for_missing_keys():
    """Scan all markdown files and identify missing keys."""
    issues = []
    directories_to_scan = ["_posts", "original", "notes", "_notes"]

    for directory in directories_to_scan:
        if not os.path.exists(directory):
            continue

        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".md"):
                    file_path = os.path.join(root, filename)
                    try:
                        post = frontmatter.load(file_path)
                        metadata = post.metadata

                        missing_keys = []
                        for key in REQUIRED_KEYS:
                            if key not in metadata:
                                missing_keys.append(key)

                        if missing_keys:
                            issues.append(
                                {
                                    "file_path": file_path,
                                    "post": post,
                                    "missing_keys": missing_keys,
                                    "all_metadata": metadata,
                                }
                            )
                    except Exception as e:
                        print(f"Error loading {file_path}: {e}")
                        continue

    return issues


def fix_front_matter_key_exists_for_file(file_path, post, missing_keys, all_metadata):
    """Fix missing keys for a single file."""
    try:
        metadata = all_metadata.copy()

        # Add missing keys
        for key in missing_keys:
            if key == "translated":
                # Set translated based on file location
                metadata[key] = get_expected_translated_value(file_path)
            elif key == "title":
                # Use filename (without extension) as title
                filename = os.path.basename(file_path)
                # Remove date prefix if present (e.g., "2025-01-06-")
                title = filename.replace(".md", "")
                # Remove date prefix pattern
                title = title.replace(".md", "")
                # Simple title extraction - take everything after date prefix
                parts = title.split("-", 3)
                if len(parts) >= 4:
                    title = parts[3].replace("-", " ").strip()
                else:
                    title = title.replace("-", " ").strip()
                metadata[key] = title
            elif key == "lang":
                # Use 'en' as default
                metadata[key] = "en"
            elif key == "type":
                # Use 'blog' as default
                metadata[key] = "blog"
            elif key == "layout":
                # Use 'post' as default
                metadata[key] = "post"
            elif key == "audio":
                # Use false as default
                metadata[key] = False
            elif key == "generated":
                # Set to False by default
                metadata[key] = False

        # Sort keys alphabetically
        sorted_metadata = {}
        for key in sorted(metadata.keys()):
            sorted_metadata[key] = metadata[key]

        # Update the post with sorted metadata
        post.metadata = sorted_metadata

        # Write the file back with fixed front matter
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return True

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def fix_front_matter_key_exists(max_files=None, verbose=False):
    """Fix missing front matter keys in all markdown files."""
    print("Scanning markdown files for missing front matter keys...")
    issues = scan_markdown_files_for_missing_keys()

    if not issues:
        print("No files with missing front matter keys found.")
        return

    # Limit the number of files if specified
    if max_files:
        issues = issues[:max_files]
        print(
            f"Found {len(issues)} files with missing front matter keys (limited to {max_files})."
        )
    else:
        print(f"Found {len(issues)} files with missing front matter keys.")

    fixed_count = 0
    for issue in issues:
        if verbose:
            print(f"Fixing {issue['file_path']}...")
            print(f"  Missing keys: {issue['missing_keys']}")
        success = fix_front_matter_key_exists_for_file(
            issue["file_path"],
            issue["post"],
            issue["missing_keys"],
            issue["all_metadata"],
        )
        if success:
            fixed_count += 1
        else:
            print(f"Failed to fix {issue['file_path']}")

    print(f"Successfully fixed {fixed_count} out of {len(issues)} files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fix missing front matter keys in markdown files."
    )
    parser.add_argument(
        "-n", "--number", type=int, help="Limit the number of files to process"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output showing directories and files being processed",
    )
    args = parser.parse_args()

    fix_front_matter_key_exists(max_files=args.number, verbose=args.verbose)
