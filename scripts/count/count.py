import sys
import os
import argparse
import re

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from scripts.count.count_lang import count_files
from count_original import count_md_files_in_original
from scripts.generate.count_notes import count_notes


def get_file_counts():
    """Collect all file counts and return as a list of tuples (category, count)"""
    base_dir = "./"
    counts = []

    # Count Python files in scripts directory (excluding ml)
    scripts_dir = os.path.join(base_dir, "scripts")
    py_count = count_files(scripts_dir, [".py"], exclude_dirs=["ml"])
    counts.append(("Python files ([scripts](scripts), excluding ml)", py_count))

    # Count Python files in scripts/ml directory
    ml_dir = os.path.join(base_dir, "scripts", "ml")
    ml_count = count_files(ml_dir, [".py"])
    counts.append(("Python files ([scripts/ml](scripts/ml))", ml_count))

    # Count Python test files in tests directory
    tests_dir = os.path.join(base_dir, "tests")
    tests_count = count_files(tests_dir, [".py"])
    counts.append(("Python test files ([tests](tests))", tests_count))

    # Count C files
    c_dir = os.path.join(base_dir, "c")
    c_count = count_files(c_dir, [".c", ".h"])
    counts.append(("C files ([c](c))", c_count))

    # Count Rust files
    rust_dir = os.path.join(base_dir, "rust")
    rust_count = count_files(rust_dir, [".rs"])
    counts.append(("Rust files ([rust](rust))", rust_count))

    # Count C++ files
    cpp_dir = os.path.join(base_dir, "cpp")
    cpp_count = count_files(cpp_dir, [".cpp", ".hpp", ".h"])
    counts.append(("C++ files ([cpp](cpp))", cpp_count))

    # Count markdown files in original
    original_count = count_md_files_in_original(quiet=True)
    counts.append(("Markdown files ([original](original))", original_count))

    # Count notes files
    notes_count = count_notes()
    counts.append(("Notes files ([notes](notes))", notes_count))

    return counts


def print_markdown_table(counts):
    """Print counts as a markdown table"""
    print("| File Type | Count |")
    print("|-----------|-------|")
    for category, count in counts:
        print(f"| {category} | {count} |")


def generate_statistics_text(counts):
    """Generate statistics text in markdown table format for README.md"""
    stats_text = "## Statistics\n\n"
    stats_text += "| File Type | Count |\n"
    stats_text += "|-----------|-------|\n"

    for category, count in counts:
        stats_text += f"| {category} | {count} |\n"

    return stats_text.rstrip()


def update_readme(counts):
    """Update README.md with new statistics"""
    readme_path = "README.md"

    # Read current README content
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Generate new statistics section
    new_stats = generate_statistics_text(counts)

    # Find the start and end of the statistics section
    stats_start = content.find("## Statistics")
    if stats_start != -1:
        # Find the next section (starts with ##)
        next_section_start = content.find("\n##", stats_start + 1)
        if next_section_start != -1:
            # Replace everything between ## Statistics and the next section
            updated_content = (
                content[:stats_start]
                + new_stats
                + "\n\n"
                + content[next_section_start + 1 :]
            )
        else:
            # No next section found, replace from ## Statistics to end
            updated_content = content[:stats_start] + new_stats + "\n"
    else:
        # If no existing statistics section, insert after the intro
        intro_end = content.find("\n\n", content.find("Welcome to my personal blog!"))
        if intro_end != -1:
            updated_content = (
                content[:intro_end] + "\n\n" + new_stats + "\n" + content[intro_end:]
            )
        else:
            updated_content = content + "\n\n" + new_stats + "\n"

    # Write updated content back to README
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"Updated {readme_path} with current statistics")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Count files and optionally update README.md"
    )
    parser.add_argument(
        "--readme", action="store_true", help="Update README.md with statistics"
    )

    args = parser.parse_args()
    counts = get_file_counts()

    if args.readme:
        update_readme(counts)
    else:
        print_markdown_table(counts)
