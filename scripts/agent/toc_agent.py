import re
import sys
import os
import argparse
from pathlib import Path

# Add parent directories to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.llm.openrouter_client import call_openrouter_api

#!/usr/bin/env python3
"""
Table of Contents Generator for Jekyll Posts
Generates TOC from markdown headers in Jekyll post files using AI.
"""


def validate_toc(toc):
    """Validate the generated TOC for format, numbering, links, etc."""
    if not toc:
        raise ValueError("TOC is empty or None")

    lines = toc.strip().split("\n")

    # Check if first line is "### Table of Contents"
    if not lines or lines[0].strip() != "### Table of Contents":
        raise ValueError("TOC must start with '### Table of Contents'")

    # Check numbering and format
    item_count = 0
    for line in lines[1:]:  # Skip the first line
        line = line.rstrip()
        if not line:  # Skip empty lines
            continue

        # Check for numbered items like "1. [Title](#anchor)" or "1. **[Title](#anchor)**"
        if re.match(r"^\d+\.\s+\**\[.*\]\(#.*\)\**$", line.strip()):
            item_count += 1
            # Extract the link text and anchor
            match = re.match(r"^\d+\.\s+\**\[(.*)\]\((#.*)\)\**$", line.strip())
            if match:
                link_text, anchor = match.groups()
                # Check if anchor starts with #
                if not anchor.startswith("#"):
                    raise ValueError(
                        f"Anchor '{anchor}' must start with '#' in line: {line}"
                    )
                # Basic check for valid anchor characters (alphanumeric, dash, underscore)
                anchor_name = anchor[1:]  # Remove the #
                if not re.match(r"^[a-zA-Z0-9\-_]+$", anchor_name):
                    raise ValueError(
                        f"Invalid characters in anchor '{anchor_name}' in line: {line}"
                    )
        # Check for bullet points under numbered items
        elif re.match(r"^\s+-\s+.*$", line):
            # Check if this is a valid bullet point (indented with hyphen)
            if len(line) > 150:  # Increased limit for bullet point length
                raise ValueError(f"Bullet point too long in line: {line}")

    # Check if we have at least one numbered item
    if item_count == 0:
        raise ValueError("TOC must contain at least one numbered item")

    return True


def generate_toc_with_ai(content):
    """Generate table of contents using AI."""
    print("Generating TOC with AI...")
    prompt = f"""Generate a concise table of contents for this markdown following STRICT rules:

1. List main headers (##) as numbered points (1., 2.)
2. For each main header, extract 3-5 key summarized points from section content
   - Summarize core ideas, NOT subheaders (5-7 words max per point)
   - Exclude redundant points
3. Format:
### Table of Contents

1. [Main Topic](#anchor)
   - Key insight 1
   - Key insight 2
   - Key insight 3

4. Never include subheaders as bullet points
5. Never exceed 5 points per section
6. Never use markdown code blocks
7. Never use bold formatting (**)

Example Output:
1. [Team Scaling](#team-scaling)
   - Plan long-term financial runway
   - Maintain elite hiring standards
   - Remove poor performers quickly

Markdown content:
{content}"""

    try:
        response = call_openrouter_api(prompt)
        print(
            f"AI Response:\n{response}\n---End of AI Response---"
        )  # Log the raw AI response
        stripped = response.strip()
        # Remove any bold formatting that might have been added despite prompt instruction
        stripped = stripped.replace("**[", "[").replace("]**", "]")
        # Raise exception if markdown code blocks still appear despite prompt instruction
        if stripped.startswith("```") and stripped.endswith("```"):
            raise ValueError(
                "TOC contains markdown code blocks despite prompt instructions"
            )
        return stripped
    except Exception as e:
        print(f"Error calling AI API: {e}", file=sys.stderr)
        return None


def find_existing_toc(content):
    """Find existing TOC in content and return start and end positions."""
    toc_start = content.find("### Table of Contents")
    if toc_start == -1:
        return None, None

    # Find the end of the TOC (next header or end of content)
    toc_end_patterns = [
        "\n### ",  # Next level 3 header
        "\n## ",  # Next level 2 header
        "\n# ",  # Next level 1 header
    ]

    toc_end = len(content)  # Default to end of content

    for pattern in toc_end_patterns:
        pos = content.find(pattern, toc_start)
        if pos != -1 and pos < toc_end:
            toc_end = pos

    return toc_start, toc_end


def process_file(file_path, output_only=False, update=False):
    """Process a single Jekyll post file."""
    print(f"Processing file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        toc = generate_toc_with_ai(content)

        if toc is None:
            return None

        # Validate the TOC
        try:
            validate_toc(toc)
        except ValueError as e:
            print(f"TOC validation failed: {e}", file=sys.stderr)
            return None

        if output_only:
            print(toc)
        else:
            print(f"Generated TOC for {file_path}:")
            print(toc)
            print()

            # Insert or update TOC in the file
            frontmatter_end = content.find("---\n", 3) + 4  # Find second ---\n

            if update:
                # Find existing TOC and replace it
                toc_start, toc_end = find_existing_toc(content)
                if toc_start is not None and toc_end is not None:
                    # Replace existing TOC
                    updated_content = content[:toc_start] + toc + content[toc_end:]
                else:
                    # No existing TOC found, insert after frontmatter
                    updated_content = (
                        content[:frontmatter_end]
                        + "\n"
                        + toc
                        + "\n\n"
                        + content[frontmatter_end:]
                    )
            else:
                # Insert TOC after frontmatter
                updated_content = (
                    content[:frontmatter_end]
                    + "\n"
                    + toc
                    + "\n\n"
                    + content[frontmatter_end:]
                )

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)

        return toc

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None
    finally:
        print(f"Finished processing: {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate TOC for Jekyll posts using AI"
    )
    parser.add_argument("files", nargs="*", help="Markdown files to process")
    parser.add_argument(
        "--output-only", action="store_true", help="Output only TOC without file info"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update existing TOC instead of adding new one",
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
        process_file(file_path, args.output_only, args.update)


if __name__ == "__main__":
    main()
