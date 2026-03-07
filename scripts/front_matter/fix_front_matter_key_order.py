import os
import argparse
import frontmatter
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from tests.workflow.test_front_matter_key import (
    scan_markdown_files_for_front_matter_key_order,
)


# Wrapper to maintain existing interface
def scan_markdown_files_for_front_matter_key_order_wrapper(verbose=False):
    """Wrapper around imported function to maintain interface that returns (issues, total_scanned)."""
    # Get issues from the imported function
    raw_issues = scan_markdown_files_for_front_matter_key_order()

    # Transform issues to match original format
    issues = []
    for issue in raw_issues:
        try:
            # Load the post with frontmatter for fixing
            post = frontmatter.load(issue["file"])
            issues.append(
                {
                    "file_path": issue["file"],
                    "post": post,
                    "actual_keys": issue["actual_order"],
                    "sorted_keys": issue["expected_order"],
                }
            )
        except Exception as e:
            if verbose:
                print(f"Error loading frontmatter for {issue['file']}: {e}")
            continue

    # Calculate total_scanned by counting files in the same directories
    total_files_scanned = 0
    # Define directories to scan (same as in test function)
    directories_to_scan = ["_posts", "original", "notes", "_notes"]

    for directory in directories_to_scan:
        if not os.path.exists(directory):
            continue
        # Walk through all subdirectories
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".md"):
                    total_files_scanned += 1

    return issues, total_files_scanned


def fix_front_matter_key_order_for_file(file_path, post, actual_keys, sorted_keys):
    """Fix the front matter key order for a single file using frontmatter library."""
    try:
        # Create new metadata with sorted keys, ensuring all sorted_keys are included
        # This handles cases where expected order might include keys not present in actual file
        sorted_metadata = {}
        for key in sorted_keys:
            if key in post.metadata:
                sorted_metadata[key] = post.metadata[key]
            else:
                # If key doesn't exist, we'll skip it for now to avoid adding empty keys
                # The validation should catch missing expected keys
                continue

        # Preserve any keys that exist in file but might not be in expected order
        # This ensures we don't lose any metadata during the process
        for key in post.metadata:
            if key not in sorted_metadata:
                sorted_metadata[key] = post.metadata[key]

        # Final sort to ensure alphabetical ordering within the sorted_keys
        final_metadata = {}
        for key in sorted(sorted_metadata.keys()):
            final_metadata[key] = sorted_metadata[key]

        # Update the post with sorted metadata
        post.metadata = final_metadata

        # Write the file back with sorted front matter
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return True

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def fix_front_matter_key_order(max_files=None, verbose=False):
    """Fix front matter key order issues in all markdown files."""
    print("Scanning markdown files for front matter key order issues...")
    issues, total_scanned = scan_markdown_files_for_front_matter_key_order_wrapper(
        verbose=verbose
    )

    if not issues:
        print("No front matter key order issues found.")
        if verbose:
            print(f"Total files scanned: {total_scanned}")
        return

    # Limit the number of files if specified
    if max_files:
        issues = issues[:max_files]
        print(
            f"Found {len(issues)} files with front matter key order issues (limited to {max_files})."
        )
    else:
        print(f"Found {len(issues)} files with front matter key order issues.")

    if verbose:
        print(f"Total files scanned: {total_scanned}")

    fixed_count = 0
    for issue in issues:
        print(f"Fixing {issue['file_path']}...")
        success = fix_front_matter_key_order_for_file(
            issue["file_path"],
            issue["post"],
            issue["actual_keys"],
            issue["sorted_keys"],
        )
        if success:
            fixed_count += 1
        else:
            print(f"Failed to fix {issue['file_path']}")

    print(f"Successfully fixed {fixed_count} out of {len(issues)} files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fix front matter key order in markdown files."
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

    fix_front_matter_key_order(max_files=args.number, verbose=args.verbose)
