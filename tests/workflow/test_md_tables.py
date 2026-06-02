import unittest
import re
import os


def scan_markdown_files_for_table_issues():
    """Scan all markdown files for tables that immediately follow headers without blank lines."""
    issues = []

    # Define directories to scan
    directories_to_scan = ["_posts", "original"]

    for directory in directories_to_scan:
        if not os.path.exists(directory):
            continue

        # Walk through all subdirectories
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if not filename.endswith(".md"):
                    continue

                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Find headers immediately followed by tables
                    # Pattern: header (### or ####) followed by table without blank line
                    pattern = r"(#{2,4}[^\n]*)\n(\|[^\n]*\|)"
                    matches = re.finditer(pattern, content, re.MULTILINE)

                    for match in matches:
                        header = match.group(1).strip()
                        table_line = match.group(2).strip()
                        line_number = content[: match.start()].count("\n") + 1

                        issues.append(
                            {
                                "file": file_path,
                                "line": line_number,
                                "header": header,
                                "table_line": table_line,
                            }
                        )

                except (UnicodeDecodeError, IOError):
                    # Skip files that can't be read
                    continue

    return issues


class TestMdTables(unittest.TestCase):
    def test_md_tables(self):
        """Test that tables don't immediately follow headers without blank lines."""
        table_issues = scan_markdown_files_for_table_issues()

        if table_issues:
            details = "\n".join(
                [
                    f"{issue['file']}:{issue['line']} - Header '{issue['header']}' immediately followed by table '{issue['table_line'][:50]}...'"
                    for issue in table_issues
                ]
            )
            self.fail(
                f"Found {len(table_issues)} markdown table formatting issues:\n{details}"
            )


if __name__ == "__main__":
    unittest.main()
