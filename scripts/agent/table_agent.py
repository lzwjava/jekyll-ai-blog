import re
import sys
import os
import argparse
from pathlib import Path

# Add parent directories to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ww.llm.openrouter_client import call_openrouter_api

#!/usr/bin/env python3
"""
Table Optimizer for Jekyll Posts
Optimizes markdown tables for mobile-friendly reading using AI.
"""


def find_tables_in_content(content):
    """Find all markdown tables in content and return their positions."""
    lines = content.split("\n")
    tables = []
    current_table = None

    for i, line in enumerate(lines):
        # Check if line contains table separator (like |---|---|)
        if re.match(r"^\s*\|[\s\-\|:]+\|\s*$", line):
            if current_table is None:
                # Look for header row above
                if i > 0 and "|" in lines[i - 1]:
                    current_table = {"start": i - 1, "lines": [lines[i - 1], line]}
                else:
                    current_table = {"start": i, "lines": [line]}
            else:
                current_table["lines"].append(line)
        # Check if line is part of table (contains |)
        elif current_table is not None and "|" in line.strip():
            current_table["lines"].append(line)
        else:
            # End of current table
            if current_table is not None:
                current_table["end"] = i - 1
                current_table["content"] = "\n".join(current_table["lines"])
                tables.append(current_table)
                current_table = None

    # Handle table that goes to end of content
    if current_table is not None:
        current_table["end"] = len(lines) - 1
        current_table["content"] = "\n".join(current_table["lines"])
        tables.append(current_table)

    return tables


def analyze_table_complexity(table_content):
    """Analyze if table needs mobile optimization."""
    lines = table_content.strip().split("\n")
    table_lines = [line for line in lines if "|" in line]

    if len(table_lines) < 2:
        return False, "Not a valid table"

    # Count columns
    header_cols = len([cell for cell in table_lines[0].split("|") if cell.strip()])

    # Check if table is too wide for mobile
    if header_cols > 4:
        return True, f"Table has {header_cols} columns, consider splitting for mobile"

    # Check content length
    max_cell_length = 0
    for line in table_lines:
        cells = [cell.strip() for cell in line.split("|") if cell.strip()]
        for cell in cells:
            max_cell_length = max(max_cell_length, len(cell))

    if max_cell_length > 50:
        return True, "Table has long content, consider mobile optimization"

    return False, "Table is mobile-friendly"


def optimize_table_with_ai(table_content):
    """Optimize table for mobile using AI."""
    print("Optimizing table with AI...")
    prompt = f"""Optimize this markdown table for mobile-friendly reading following these rules:

1. If table has more than 4 columns, split it into multiple smaller tables
2. If table has long content, consider breaking it into sections
3. Maintain all original data and information
4. Use clear section headers for split tables
5. Ensure each new table is properly formatted with headers and separators
6. Add brief explanatory text between tables if needed

Guidelines for splitting:
- Group related columns together
- Keep the most important identifying column (like name/id) in each table
- Use descriptive headers for each new table section
- Format: Use standard markdown table syntax

Original table:
{table_content}

Return the optimized version with proper markdown formatting."""

    try:
        response = call_openrouter_api(prompt)
        print(f"AI Response:\n{response}\n---End of AI Response---")
        stripped = response.strip()
        # Remove markdown code blocks if present
        if stripped.startswith("```") and stripped.endswith("```"):
            lines = stripped.split("\n")
            stripped = "\n".join(lines[1:-1])
        return stripped
    except Exception as e:
        print(f"Error calling AI API: {e}", file=sys.stderr)
        return None


def process_file(file_path, output_only=False, update=False):
    """Process a single file to optimize tables for mobile."""
    print(f"Processing file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all tables in content
        tables = find_tables_in_content(content)

        if not tables:
            print(f"No tables found in {file_path}")
            return None

        print(f"Found {len(tables)} table(s) in {file_path}")

        # Process each table
        updated_content = content
        offset = 0  # Track content length changes

        for i, table in enumerate(tables):
            print(f"\nAnalyzing table {i + 1}...")
            needs_optimization, reason = analyze_table_complexity(table["content"])
            print(f"Table {i + 1}: {reason}")

            if needs_optimization:
                print(f"Optimizing table {i + 1}...")
                optimized_table = optimize_table_with_ai(table["content"])

                if optimized_table:
                    if output_only:
                        print(f"\nOptimized table {i + 1}:")
                        print(optimized_table)
                    else:
                        # Calculate positions with offset
                        start_pos = table["start"] + offset
                        end_pos = table["end"] + offset + 1

                        # Find actual line positions in current content
                        lines = updated_content.split("\n")
                        table_start_line = None
                        table_end_line = None

                        # Find table boundaries more accurately
                        for line_idx, line in enumerate(lines):
                            if table["lines"][0].strip() == line.strip():
                                table_start_line = line_idx
                                break

                        if table_start_line is not None:
                            # Find end of this table
                            for line_idx in range(table_start_line, len(lines)):
                                if line_idx < len(lines) - 1:
                                    # Check if next line is not part of table
                                    next_line = lines[line_idx + 1]
                                    if "|" not in next_line or next_line.strip() == "":
                                        table_end_line = line_idx
                                        break
                                else:
                                    table_end_line = line_idx
                                    break

                            if table_end_line is not None:
                                # Replace the table
                                before_table = "\n".join(lines[:table_start_line])
                                after_table = "\n".join(lines[table_end_line + 1 :])
                                updated_content = (
                                    before_table
                                    + "\n"
                                    + optimized_table
                                    + "\n"
                                    + after_table
                                )

                                # Update offset
                                old_length = sum(
                                    len(line) + 1 for line in table["lines"]
                                )
                                new_length = len(optimized_table) + 1
                                offset += new_length - old_length

                        print(f"Table {i + 1} optimized and updated in content")
                else:
                    print(f"Failed to optimize table {i + 1}")
            else:
                print(f"Table {i + 1} is already mobile-friendly")

        # Write updated content if not output_only
        if not output_only and updated_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"\nFile {file_path} updated with optimized tables")

        return updated_content

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None
    finally:
        print(f"Finished processing: {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Optimize markdown tables for mobile-friendly reading using AI"
    )
    parser.add_argument("files", nargs="*", help="Markdown files to process")
    parser.add_argument(
        "--output-only",
        action="store_true",
        help="Output optimized tables without updating files",
    )
    parser.add_argument(
        "--check-only", action="store_true", help="Only check tables without optimizing"
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
        if args.check_only:
            # Just analyze tables without optimizing
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                tables = find_tables_in_content(content)
                if tables:
                    print(f"\n{file_path}:")
                    for i, table in enumerate(tables):
                        needs_optimization, reason = analyze_table_complexity(
                            table["content"]
                        )
                        status = (
                            "NEEDS OPTIMIZATION"
                            if needs_optimization
                            else "MOBILE-FRIENDLY"
                        )
                        print(f"  Table {i + 1}: {status} - {reason}")
                else:
                    print(f"{file_path}: No tables found")
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
        else:
            process_file(file_path, args.output_only, False)


if __name__ == "__main__":
    main()
