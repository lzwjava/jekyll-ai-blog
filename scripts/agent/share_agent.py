import sys
import argparse
from pathlib import Path
from ww.llm.openrouter_client import call_openrouter_api

#!/usr/bin/env python3
"""
Summary Agent for Jekyll Posts
Generates summaries of Jekyll post files using AI.
"""


def generate_summary_with_ai(content):
    """Generate summary using AI."""
    prompt = f"""Please generate a concise summary of the following markdown content.
Follow these rules:
1. Create a brief, informative summary (2-3 sentences)
2. Capture the main points and key ideas
3. Use clear, accessible language
4. Focus on the core message and important details
5. Ignore markdown formatting and code blocks in the summary

Markdown content:
{content}

Return the summary:"""

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

        summary = generate_summary_with_ai(content)

        if summary is None:
            return None

        if output_only:
            print(summary)
        else:
            print(f"Summary for {file_path}:")
            print(summary)
            print()

        return summary

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate summaries of Jekyll posts using AI"
    )
    parser.add_argument("files", nargs="*", help="Markdown files to process")
    parser.add_argument(
        "--output-only",
        action="store_true",
        help="Output only summary without file info",
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
