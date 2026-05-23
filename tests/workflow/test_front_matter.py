import unittest
import os
import frontmatter


def scan_markdown_files_for_front_matter_issues():
    """Scan all markdown files for front matter that doesn't have a newline after closing ---."""
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
                    # Read the raw file content first to check for the newline issue
                    with open(file_path, "r", encoding="utf-8") as f:
                        raw_content = f.read()
                        lines = raw_content.splitlines(keepends=True)

                    # Check if file starts with front matter by looking for the opening ---
                    if not raw_content.startswith("---\n"):
                        continue

                    # Check first 15 lines for the closing --- issue
                    content_subset = (
                        "".join(lines[:15]) if len(lines) >= 15 else raw_content
                    )

                    # Find the closing --- and check if it's followed by a newline
                    if content_subset.count("---") >= 2:
                        # Find the position of the second ---
                        second_dash_pos = content_subset.find(
                            "---", 3
                        )  # Skip first ---
                        if second_dash_pos != -1:
                            # Check what comes after the closing ---
                            after_closing = content_subset[
                                second_dash_pos + 3 : second_dash_pos + 10
                            ]

                            # If there's no newline immediately after closing ---
                            if after_closing and not after_closing.startswith("\n"):
                                line_number = (
                                    content_subset[:second_dash_pos].count("\n") + 1
                                )
                                following_char = (
                                    repr(after_closing[0]) if after_closing else "EOF"
                                )

                                issues.append(
                                    {
                                        "file": file_path,
                                        "line": line_number,
                                        "following_char": following_char,
                                        "issue": "Front matter closing --- not followed by newline",
                                    }
                                )
                                continue

                    # Try to parse with frontmatter to validate YAML structure
                    try:
                        post = frontmatter.loads(raw_content)
                        # Verify that frontmatter was actually parsed
                        if not hasattr(post, "metadata") or post.metadata is None:
                            # No front matter was parsed, skip this check
                            pass
                    except Exception as e:
                        # YAML parsing error - front matter might be malformed
                        issues.append(
                            {
                                "file": file_path,
                                "line": 1,
                                "issue": f"YAML parsing error in front matter: {str(e)}",
                                "error": str(e),
                            }
                        )

                except (UnicodeDecodeError, IOError) as e:
                    # Skip files that can't be read
                    continue

    return issues


class TestFrontMatter(unittest.TestCase):
    def test_front_matter_newline(self):
        """Test that front matter closing --- is followed by a newline."""
        front_matter_issues = scan_markdown_files_for_front_matter_issues()

        if front_matter_issues:
            details = []
            for issue in front_matter_issues:
                if "issue" in issue:
                    detail = f"{issue['file']}:{issue['line']} - {issue['issue']}"
                else:
                    detail = f"{issue['file']}:{issue['line']} - Front matter closing --- immediately followed by {issue.get('following_char', 'unknown')}"
                details.append(detail)

            joined = "\n".join(details)
            self.fail(
                f"Found {len(front_matter_issues)} front matter formatting issues:\n{joined}"
            )


if __name__ == "__main__":
    unittest.main()
