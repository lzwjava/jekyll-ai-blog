#!/usr/bin/env python3
"""Fix markdown tables that immediately follow headers without blank lines."""

import re
import os
import sys
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from tests.workflow.test_md_tables import scan_markdown_files_for_table_issues


def fix_markdown_table_formatting(file_path, dry_run=False):
    """
    Fix markdown tables that immediately follow headers by adding blank lines.

    Args:
        file_path: Path to the markdown file to fix
        dry_run: If True, only show what would be changed without modifying files

    Returns:
        tuple: (number of fixes applied, list of fixes applied)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()
    except (UnicodeDecodeError, IOError) as e:
        print(f"Error reading {file_path}: {e}")
        return 0, []

    # Pattern to match headers (### or ####) followed by table without blank line
    # Group 1: header line
    # Group 2: table line
    pattern = r"(#{2,4}[^\n]*)\n(\|[^\n]*\|)"

    fixes = []
    fixed_content = original_content

    def fix_table(match):
        header = match.group(1)
        table_line = match.group(2)
        fixed_text = f"{header}\n\n{table_line}"

        fix_description = f"Added blank line after header: '{header.strip()}'"
        fixes.append(
            {
                "header": header.strip(),
                "table_line": table_line.strip(),
                "fix": fix_description,
            }
        )

        return fixed_text

    # Apply the fix - replace all occurrences
    fixed_content = re.sub(pattern, fix_table, fixed_content, flags=re.MULTILINE)

    if not dry_run and fixed_content != original_content:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            print(f" Fixed {file_path}")
        except IOError as e:
            print(f"Error writing {file_path}: {e}")
            return 0, []

    return len(fixes), fixes


def main(auto_yes=False):
    """Main function to find and fix all markdown table formatting issues.

    Args:
        auto_yes: If True, automatically apply fixes without confirmation
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fix markdown table formatting issues")
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        dest="auto_yes",
        help="Automatically apply fixes without confirmation",
    )
    parser.add_argument("args", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    # Combine auto_yes parameter and --yes flag (parameter takes precedence)
    should_auto_yes = auto_yes or args.auto_yes

    print("Scanning for markdown table formatting issues...\n")

    # Get all table issues from the test function
    issues = scan_markdown_files_for_table_issues()

    if not issues:
        print(" No markdown table formatting issues found!")
        return 0

    # Group issues by file
    files_to_fix = {}
    for issue in issues:
        file_path = issue["file"]
        if file_path not in files_to_fix:
            files_to_fix[file_path] = []
        files_to_fix[file_path].append(issue)

    print(f"Found {len(issues)} formatting issue(s) in {len(files_to_fix)} file(s)\n")

    # Show what will be fixed
    total_fixes = 0
    for file_path, file_issues in files_to_fix.items():
        print(f"\n{file_path}:")
        for issue in file_issues:
            print(
                f"  Line {issue['line']}: Header '{issue['header']}' immediately followed by table"
            )
            total_fixes += 1

    print(f"\n{'=' * 60}")
    print(f"Total: {total_fixes} fix(es) needed in {len(files_to_fix)} file(s)")
    print(f"{'=' * 60}\n")

    # Ask for confirmation before applying fixes (unless auto_yes is True)
    if should_auto_yes:
        print("Applying fixes automatically (--yes flag set)...\n")
    else:
        response = input("Apply these fixes? (y/n): ").strip().lower()
        if response != "y":
            print("Aborted.")
            return 0

    # Apply fixes
    print("\nApplying fixes...\n")
    all_fixes = 0
    for file_path in files_to_fix.keys():
        num_fixes, fixes = fix_markdown_table_formatting(file_path, dry_run=False)
        if num_fixes > 0:
            all_fixes += num_fixes
            for fix in fixes:
                print(f"  - {fix['fix']}")

    print(f"\n Successfully applied {all_fixes} fix(es)!")

    # Verify the fixes
    print("\nVerifying fixes...")
    remaining_issues = scan_markdown_files_for_table_issues()

    if remaining_issues:
        print(f"  Warning: {len(remaining_issues)} issue(s) still remain!")
        return 1
    else:
        print(" All markdown table formatting issues have been fixed!")
        return 0


if __name__ == "__main__":
    exit(main(auto_yes=False))
