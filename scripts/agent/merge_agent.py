import sys
import argparse
from pathlib import Path
from ww.llm.openrouter_client import call_openrouter_api

#!/usr/bin/env python3
"""
Table of Contents Generator for Jekyll Posts
Generates TOC from markdown headers in Jekyll post files using AI and merges multiple posts.
"""


def generate_toc_with_ai(content):
    """Generate table of contents using AI."""
    prompt = f"""Please generate a table of contents for the following markdown content.
Follow these rules:
1. Only include headers from level 2 (##) to level 6 (######)
2. Create Jekyll-compatible anchor links (lowercase, hyphens for spaces, no special chars)
3. Use proper indentation (4 spaces per level)
4. Start with "### Table of Contents" as the title
5. Format as: `- [Header Title](#anchor-link)`

Markdown content:
{content}

Generate only the table of contents in markdown format:"""

    try:
        response = call_openrouter_api(prompt)
        return response.strip()
    except Exception as e:
        print(f"Error calling AI API: {e}", file=sys.stderr)
        return None


def process_file(file_path, output_only=False):
    """Process a single Jekyll post file."""
    try:
        # Resolve relative path to absolute path
        file_path = Path(file_path).resolve()
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        toc = generate_toc_with_ai(content)

        if toc is None:
            return None, None

        if output_only:
            print(toc)
        else:
            print(f"Generated TOC for {file_path}:")
            print(toc)
            print()

        return toc, content

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None, None


def merge_contents(main_content, other_contents):
    """Merge multiple markdown contents into the main content."""
    merged_content = main_content
    for i, content in enumerate(other_contents, 1):
        merged_content += f"\n\n## Additional Content {i}\n{content}"
    return merged_content


def main():
    parser = argparse.ArgumentParser(
        description="Generate TOC for Jekyll posts using AI and merge multiple posts"
    )
    parser.add_argument(
        "files", nargs="*", help="Markdown files to process, first one treated as main"
    )
    parser.add_argument(
        "--output-only", action="store_true", help="Output only TOC without file info"
    )

    args = parser.parse_args()

    if not args.files:
        # If no files specified, look for markdown files in current directory
        md_files = list(Path(".").glob("*.md"))
        if not md_files:
            print("No markdown files found. Please specify files to process.")
            sys.exit(1)
        args.files = md_files

    contents = []
    tocs = []
    for file_path in args.files:
        toc, content = process_file(file_path, args.output_only)
        if toc and content:
            tocs.append(toc)
            contents.append(content)

    if len(contents) > 1:
        # Merge contents if there are multiple files
        merged_content = merge_contents(contents[0], contents[1:])
        merged_toc = generate_toc_with_ai(merged_content)
        if merged_toc:
            if args.output_only:
                print(merged_toc)
            else:
                print("Generated TOC for merged content:")
                print(merged_toc)


if __name__ == "__main__":
    main()
