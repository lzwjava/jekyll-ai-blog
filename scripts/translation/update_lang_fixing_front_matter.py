#!/usr/bin/env python3

import sys
import os
import argparse
import frontmatter

# Add the project root to the Python path to import from tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from tests.workflow.test_front_matter import scan_markdown_files_for_front_matter_issues


def fix_front_matter_issues(issues, target_languages=None, dry_run=False):
    """Fix front matter issues by directly editing the files using frontmatter library."""
    if not issues:
        print("No front matter formatting issues to fix.")
        return

    # Group issues by file
    files_with_issues = {}
    for issue in issues:
        file_path = issue["file"]
        if file_path not in files_with_issues:
            files_with_issues[file_path] = []
        files_with_issues[file_path].append(issue)

    fixed_count = 0

    for post_file, file_issues in files_with_issues.items():
        print(f"\nProcessing {post_file} with {len(file_issues)} front matter issues:")
        for issue in file_issues:
            print(
                f"  Line {issue['line']}: Front matter closing --- immediately followed by {issue['following_char']}"
            )

        # Check if this file's language is in target_languages
        if target_languages:
            # Extract language from file path
            lang_in_path = None
            for lang in target_languages:
                if f"-{lang}.md" in post_file or post_file.endswith(f"-{lang}.md"):
                    lang_in_path = lang
                    break
            if lang_in_path is None or lang_in_path not in target_languages:
                print(f"  Skipping file (language not in target list)")
                continue

        if dry_run:
            print(f"  Would fix front matter spacing in {post_file}")
            continue

        # Load the post using frontmatter library
        try:
            post = frontmatter.load(post_file)

            # Update the post (this ensures proper frontmatter formatting)
            # The frontmatter library automatically handles proper spacing
            with open(post_file, "w", encoding="utf-8") as f:
                f.write(frontmatter.dumps(post))

            print(f"  Successfully fixed front matter spacing in {post_file}")
            fixed_count += 1

        except Exception as e:
            print(f"  Error fixing {post_file}: {e}")

    if not dry_run:
        print(
            f"\nSuccessfully fixed {fixed_count} out of {len(files_with_issues)} files."
        )
    elif files_with_issues:
        print(f"\nDry run: Would fix {len(files_with_issues)} files.")


def main():
    """Main function to scan and fix front matter formatting issues."""
    parser = argparse.ArgumentParser(
        description="Fix front matter formatting issues by directly editing files."
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="all",
        help="Target language to fix (e.g., zh, ja, all).",
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Perform a dry run without modifying files.",
    )

    args = parser.parse_args()

    print("Scanning markdown files for front matter formatting issues...")
    issues = scan_markdown_files_for_front_matter_issues()

    if issues:
        print(f"\nFound {len(issues)} front matter formatting issues:")
        for issue in issues:
            print(
                f"{issue['file']}:{issue['line']} - Front matter closing --- immediately followed by {issue['following_char']}"
            )

        # Determine target languages
        target_languages = None
        if args.lang != "all":
            target_languages = [args.lang]

        # Fix the issues by directly editing the files
        fix_front_matter_issues(issues, target_languages, args.dry_run)
    else:
        print("No front matter formatting issues found.")


if __name__ == "__main__":
    main()
