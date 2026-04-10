import sys
import argparse
from pathlib import Path
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.llm.openrouter_client import call_openrouter_api
from scripts.agent.git_utils import (
    get_git_diff_lines,
    extract_changed_content,
    apply_grammar_fixes_to_original,
    get_changed_md_files_in_last_n_commits,
)
from scripts.agent.validate_utils import (
    validate_grammar_fix,
)

#!/usr/bin/env python3
"""
Grammar Fixer for Jekyll Posts
Fixes grammar in Jekyll post files using AI with minimal changes.
"""


def fix_grammar_with_ai(content):
    """Fix grammar using AI with minimal changes."""
    prompt = f"""Please fix only the grammar errors in the following markdown content.
Follow these rules:
1. Make MINIMAL changes - only fix clear grammar errors
2. Preserve the original writing style and tone
3. Keep all markdown formatting intact - DO NOT add new ** or * markdown syntax
4. Don't change technical terms or code blocks
5. Don't rewrite sentences unless absolutely necessary for grammar
6. Maintain the same paragraph structure and similar content length
7. Return ONLY the corrected content without any explanations or markdown code blocks

Markdown content:
{content}

Return the corrected content:"""

    try:
        response = call_openrouter_api(prompt)
        # Clean up the response - remove markdown code blocks if present
        cleaned_response = response.strip()
        if cleaned_response.startswith("```"):
            lines = cleaned_response.split("\n")
            # Remove first and last lines if they are markdown code block markers
            if lines[0].startswith("```") and lines[-1].strip() == "```":
                cleaned_response = "\n".join(lines[1:-1])

        # Validate the grammar fix
        validate_grammar_fix(content, cleaned_response)

        return cleaned_response
    except Exception as e:
        print(f"Error in grammar fixing: {e}", file=sys.stderr)
        return None


def process_file(file_path, dry_run=False, base_range=None):
    """Process a single Jekyll post file."""
    try:
        # Convert relative path to absolute path
        abs_file_path = os.path.abspath(file_path)

        # Get changed lines from git diff (optionally use a base range)
        changed_lines = get_git_diff_lines(abs_file_path, base_range)

        if not changed_lines:
            print(f"No changes to fix in {file_path}")
            return None

        with open(abs_file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        # Extract only the changed content with context
        changed_content = extract_changed_content(original_content, changed_lines)

        if not changed_content.strip():
            print(f"No substantial changes to fix in {file_path}")
            return None

        print(f"Fixing grammar for changed sections in {file_path}...")
        print(f"Changed lines: {sorted(changed_lines)}")

        if dry_run:
            print("\n[DRY RUN] Content to fix:")
            print(changed_content)
            print("\n" + "=" * 50 + "\n")

        fixed_content = fix_grammar_with_ai(changed_content)

        if fixed_content is None:
            return None

        if dry_run:
            print(f"[DRY RUN] Grammar-fixed content for {file_path}:")
            print(fixed_content)
            print(
                "\n[DRY RUN] File would be updated but no changes made due to dry-run mode"
            )
        else:
            # Apply the grammar fixes to the full content
            # For now, we'll replace the changed sections in the original content
            # This is a simplified approach - in practice, you might want more sophisticated merging

            # Create new content by applying fixes to the original
            new_content = apply_grammar_fixes_to_original(
                original_content, changed_content, fixed_content, changed_lines
            )

            # Write the updated content back to the file
            with open(abs_file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"✅ Grammar fixes applied to {file_path}")
            print(f"Fixed lines: {sorted(changed_lines)}")

        return fixed_content

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Fix grammar in Jekyll posts using AI")
    parser.add_argument("files", nargs="*", help="Markdown files to process")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files",
    )
    parser.add_argument(
        "--commits",
        type=int,
        default=0,
        help="If >0, consider changes in the last N commits under original/ and prompt to select a file",
    )

    args = parser.parse_args()

    # Handle commits option: if >0, find changed markdown files in last N commits
    if args.commits > 0:
        changed_md = get_changed_md_files_in_last_n_commits(args.commits)
        if not changed_md:
            print(
                f"No changed markdown files found in the last {args.commits} commits."
            )
            sys.exit(0)
        if len(changed_md) == 1:
            args.files = [changed_md[0]]
        else:
            print("Multiple changed markdown files found:")
            for i, f in enumerate(changed_md):
                print(f"{i + 1}. {f}")
            choice = input("Select a file by number: ").strip()
            try:
                idx = int(choice) - 1
                if idx < 0 or idx >= len(changed_md):
                    print("Invalid selection.")
                    sys.exit(1)
                args.files = [changed_md[idx]]
            except Exception:
                print("Invalid input.")
                sys.exit(1)
        base_range = f"HEAD~{args.commits}..HEAD"
    else:
        base_range = None
        if not args.files:
            # If no files specified, look for markdown files in current directory
            md_files = list(Path(".").glob("*.md"))
            if not md_files:
                print("No markdown files found. Please specify files to process.")
                sys.exit(1)
            args.files = md_files

    for file_path in args.files:
        process_file(file_path, args.dry_run, base_range=base_range)


if __name__ == "__main__":
    main()
