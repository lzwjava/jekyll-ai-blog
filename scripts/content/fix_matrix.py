import os
import re
import markdown
import argparse


def process_matrix_in_file(filepath, matrix_flag=False):
    """
    Processes LaTeX matrix expressions in a markdown file.
    If matrix_flag is True, updates \\ to \\\\ in matrix environments.

    Args:
        filepath (str): The path to the markdown file to process.
        matrix_flag (bool): Whether to update \\ to \\\\ in matrix environments.
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

        def process_matrix(text):
            temp_text = text
            for cb in code_block_data:
                temp_text = temp_text.replace(cb["content"], "CODE_BLOCK_PLACEHOLDER")

            # Pattern to match matrix environments
            pattern = r"(\\begin\{pmatrix\}.*?\\end\{pmatrix\})"

            def replacer(match):
                content = match.group(1)
                if matrix_flag:
                    # Only replace \\ with \\\\ when matrix_flag is True
                    content = content.replace("\\\\", "\\\\\\")
                return content

            temp_text = re.sub(pattern, replacer, temp_text, flags=re.DOTALL)

            for cb in code_block_data:
                temp_text = temp_text.replace("CODE_BLOCK_PLACEHOLDER", cb["content"])
            return temp_text

        updated_content = process_matrix(content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print(f"Processed {filepath}")
        if matrix_flag:
            print("- Updated \\\\ to \\\\\\\\ in matrix environments")
        return True

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False


def process_matrix_in_markdown(directory, max_files=None, matrix_flag=False):
    """
    Finds all markdown files in a directory and processes matrix expressions.

    Args:
        directory (str): The directory to search for markdown files.
        max_files (int, optional): Maximum number of files to process. Defaults to None (unlimited).
        matrix_flag (bool): Whether to update \\ to \\\\ in matrix environments.
    """
    files_processed = 0
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                success = process_matrix_in_file(filepath, matrix_flag)
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
        description="Process LaTeX matrix expressions in Markdown files."
    )
    parser.add_argument(
        "--maxfiles", type=int, help="Maximum number of files to process."
    )
    parser.add_argument(
        "--file", type=str, help="Path to a specific markdown file to process."
    )
    parser.add_argument(
        "--matrix",
        action="store_true",
        help="Update \\\\ to \\\\\\\\ in matrix environments.",
    )
    args = parser.parse_args()

    if args.file:
        # Process a single file
        if os.path.exists(args.file) and args.file.endswith(".md"):
            process_matrix_in_file(args.file, args.matrix)
        else:
            print(f"Invalid file path or not a markdown file: {args.file}")
    else:
        # Process directories
        directories = ["_posts", "original", "notes"]
        for directory in directories:
            if os.path.exists(directory):
                process_matrix_in_markdown(
                    directory, max_files=args.maxfiles, matrix_flag=args.matrix
                )
            else:
                print(f"Directory not found: {directory}")


if __name__ == "__main__":
    main()
