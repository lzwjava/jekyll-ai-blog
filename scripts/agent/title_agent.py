import re
import sys
import os
import argparse
from pathlib import Path
import frontmatter  # type: ignore[reportMissingImports]

# Add parent directories to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ww.llm.openrouter_client import call_openrouter_api

#!/usr/bin/env python3
"""
Title Updater for Jekyll Posts
Generates titles for Jekyll post files using AI.
"""


def generate_title_with_ai(content, custom_prompt=None, model="mistral-medium"):
    """Generate a title using AI."""
    print("Generating title with AI...")

    # Limit content to first 1000 characters to avoid overwhelming the AI
    truncated_content = content[:1000]
    if len(content) > 1000:
        truncated_content += "..."

    if custom_prompt:
        prompt = f"""{custom_prompt}

Content:
{truncated_content}"""
    else:
        prompt = f"""Generate a short, simple, and clean title for this content. Output ONLY the title text with no markdown formatting, quotes, or additional text. Keep it concise and straightforward.

PREFERRED FORMATS (in order of preference):
1. If possible, simplify to a format like "noun, noun, noun" (e.g., "Docker, Kubernetes, AWS")
2. If that doesn't work, use a clear descriptive title
3. Keep it under 40 characters if possible

IMPORTANT INSTRUCTIONS:
- Use original words from the section titles/content as much as possible
- Preserve key terms and concepts from the source material
- Avoid introducing new vocabulary not present in the content

Content:
{truncated_content}"""

    try:
        response = call_openrouter_api(prompt, model)
        stripped = response.strip()
        return stripped
    except Exception as e:
        print(f"Error calling AI API: {e}", file=sys.stderr)
        return None


def validate_title(title):
    """Validate the generated title for length, special characters, quotes, and markdown syntax."""
    if not title:
        raise ValueError("Title is empty or None")

    # Check length (under 100 characters)
    if len(title) > 100:
        raise ValueError(
            f"Title is too long ({len(title)} characters). Keep it under 100 characters."
        )

    # Check for markdown syntax (basic check for common patterns)
    markdown_patterns = [
        r"\*\*.*?\*\*",
        r"\*.*?\*",
        r"\[.*?\]",
        r"\(.*?\)",
        r"#+",
        r"`.*?`",
    ]
    for pattern in markdown_patterns:
        if re.search(pattern, title):
            raise ValueError(f"Title contains markdown syntax: {title}")

    # Check for quotes at the beginning or end
    if (
        title.startswith('"')
        or title.endswith('"')
        or title.startswith("'")
        or title.endswith("'")
    ):
        raise ValueError(f"Title contains quotes at the beginning or end: {title}")

    # Check for special characters that might cause issues (basic check)
    # Allow common punctuation but disallow potentially problematic characters
    problematic_chars = ["<", ">", "{", "}", "[", "]"]
    for char in problematic_chars:
        if char in title:
            raise ValueError(f"Title contains problematic character '{char}': {title}")

    return True


def process_file(
    file_path, output_only=False, custom_prompt=None, model="mistral-medium"
):
    """Process a single Jekyll post file to update its title."""
    print(f"Processing file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
            content = post.content

        title = generate_title_with_ai(content, custom_prompt, model)

        if title is None:
            return None

        # Validate the title
        try:
            validate_title(title)
        except ValueError as e:
            print(f"Title validation failed: {e}", file=sys.stderr)
            return None

        if output_only:
            print(title)
        else:
            print(f"Generated title for {file_path}:")
            print(title)
            print()

            # Update title in frontmatter using frontmatter library
            # Clean the title by removing markdown formatting and extra text
            clean_title = title.strip()
            # Remove common markdown formatting
            clean_title = re.sub(r"^[*#]+|[*#]+$", "", clean_title).strip()
            # Remove quotes
            clean_title = clean_title.strip("\"'")

            # Remove any existing title metadata and set the new one
            post.metadata.pop("title", None)  # Remove existing title if it exists
            post.metadata["title"] = clean_title

            # Serialize the post back to string format
            updated_content = frontmatter.dumps(post)

            # Write updated content back to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)

        return title

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None
    finally:
        print(f"Finished processing: {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate titles for Jekyll posts using AI"
    )
    parser.add_argument("files", nargs="*", help="Markdown files to process")
    parser.add_argument(
        "--output-only", action="store_true", help="Output only title without file info"
    )
    parser.add_argument("--prompt", type=str, help="Custom prompt for title generation")
    parser.add_argument(
        "--model",
        type=str,
        default="mistral-medium",
        help="Model to use for title generation",
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
        process_file(file_path, args.output_only, args.prompt, args.model)


if __name__ == "__main__":
    main()
