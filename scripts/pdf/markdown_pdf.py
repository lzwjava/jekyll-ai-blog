#!/usr/bin/env python3
import sys
import os
import argparse
from pdf_base import text_to_pdf_from_markdown


def main():
    parser = argparse.ArgumentParser(description="Convert markdown to PDF")
    parser.add_argument("markdown_file", help="Path to the markdown file")
    parser.add_argument(
        "--pt", type=int, default=16, help="Font size in points (default: 16)"
    )
    args = parser.parse_args()

    markdown_path = args.markdown_file

    if not os.path.isfile(markdown_path):
        print(f"Error: File not found: {markdown_path}")
        sys.exit(1)

    # Replace .md extension with .pdf, keep same directory
    if markdown_path.lower().endswith(".md"):
        pdf_path = markdown_path[:-3] + ".pdf"
    else:
        pdf_path = markdown_path + ".pdf"

    success = text_to_pdf_from_markdown(markdown_path, pdf_path, pt=args.pt)
    if success:
        print(f"Successfully converted {markdown_path} to {pdf_path}")
        sys.exit(0)
    else:
        print(f"Failed to convert {markdown_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
