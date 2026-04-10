import sys
import argparse
from pathlib import Path
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.llm.openrouter_client import call_openrouter_api

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
3. Keep all markdown formatting intact
4. Don't change technical terms or code blocks
5. Don't rewrite sentences unless absolutely necessary for grammar

Markdown content:
{content}

Return the corrected content:"""

    try:
        response = call_openrouter_api(prompt)
        return response.strip()
    except Exception as e:
        print(f"Error calling AI API: {e}", file=sys.stderr)
        return None


def process_file(file_path, output_only=False):
    """Process a single Jekyll post file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        fixed_content = fix_grammar_with_ai(content)

        if fixed_content is None:
            return None

        if output_only:
            print(fixed_content)
        else:
            print(f"Grammar-fixed content for {file_path}:")
            print(fixed_content)
            print()

        return fixed_content

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Fix grammar in Jekyll posts using AI")
    parser.add_argument("files", nargs="*", help="Markdown files to process")
    parser.add_argument(
        "--output-only",
        action="store_true",
        help="Output only fixed content without file info",
    )

    args = parser.parse_args()

    if not args.files:
        # If no files specified, look for markdown files in current directory
        md_files = list(Path(".").glob("*.md"))
        if not md_files:
            print("No markdown files found. Please specify files to process.")
            sys.exit(1)
        args.files = md_files

    for file_path in args.files:
        process_file(file_path, args.output_only)


if __name__ == "__main__":
    main()
