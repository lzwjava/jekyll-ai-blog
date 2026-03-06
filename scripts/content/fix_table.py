import os
import re
import markdown
import argparse


def process_tables_in_file(filepath, fix_tables=False):
    """
    Processes markdown tables in a file.
    If fix_tables is True, ensures each table has a blank line before it.

    Args:
        filepath (str): The path to the markdown file to process.
        fix_tables (bool): Whether to add blank lines before tables.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse markdown to identify code blocks
        md = markdown.Markdown(extensions=["fenced_code"])
        html_content = md.convert(content)

        # Identify code blocks using regex
        code_blocks = list(
            re.finditer(r"<pre><code.*?>.*?</code></pre>", html_content, re.DOTALL)
        )

        # Extract code block content and their positions
        code_block_data = []
        for match in code_blocks:
            code_block_data.append(
                {"start": match.start(), "end": match.end(), "content": match.group(0)}
            )

        def process_tables(text):
            temp_text = text
            for cb in code_block_data:
                temp_text = temp_text.replace(cb["content"], "CODE_BLOCK_PLACEHOLDER")

            # Pattern to match headings (## or ###) followed by tables without blank line
            # This matches when a table directly follows a heading (but not a blank line)
            pattern = r"(^#{2,3}\s+.*?\n)(\|.*?\|\n(?:\|.*\|\n)*)"

            def replacer(match):
                heading = match.group(1)
                table = match.group(2)

                # Check if there's already a blank line between heading and table
                if heading.endswith("\n\n"):
                    return match.group(0)  # Already has blank line

                # Only add blank line if fix_tables is True
                if fix_tables:
                    return heading.rstrip() + "\n\n" + table
                return match.group(0)

            temp_text = re.sub(pattern, replacer, temp_text, flags=re.MULTILINE)

            for cb in code_block_data:
                temp_text = temp_text.replace("CODE_BLOCK_PLACEHOLDER", cb["content"])
            return temp_text

        updated_content = process_tables(content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print(f"Processed {filepath}")
        if fix_tables:
            print(f"- Added blank lines before tables")
        return True

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False


def process_tables_in_markdown(directory, max_files=None, fix_tables=False):
    """
    Finds all markdown files in a directory and processes tables.

    Args:
        directory (str): The directory to search for markdown files.
        max_files (int, optional): Maximum number of files to process. Defaults to None (unlimited).
        fix_tables (bool): Whether to add blank lines before tables.
    """
    files_processed = 0
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                success = process_tables_in_file(filepath, fix_tables)
                if success:
                    files_processed += 1

                if max_files and files_processed >= max_files:
                    print(f"Maximum files processed ({max_files}). Exiting directory.")
                    return


def main():
    """
    Main function to process either a single file or directories.
    """
    parser = argparse.ArgumentParser(
        description="Fix markdown tables by ensuring they have blank lines before them."
    )
    parser.add_argument(
        "--maxfiles", type=int, help="Maximum number of files to process."
    )
    parser.add_argument(
        "--file", type=str, help="Path to a specific markdown file to process."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Add blank lines before tables.",
    )
    args = parser.parse_args()

    if args.file:
        # Process a single file
        if os.path.exists(args.file) and args.file.endswith(".md"):
            process_tables_in_file(args.file, args.fix)
        else:
            print(f"Invalid file path or not a markdown file: {args.file}")
    else:
        # Process directories
        directories = ["notes"]
        for directory in directories:
            if os.path.exists(directory):
                process_tables_in_markdown(
                    directory, max_files=args.maxfiles, fix_tables=args.fix
                )
            else:
                print(f"Directory not found: {directory}")


if __name__ == "__main__":
    main()
