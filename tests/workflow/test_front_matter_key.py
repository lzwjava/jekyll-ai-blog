import unittest
import os
import frontmatter


def scan_markdown_files_for_front_matter_key_order():
    """Scan all markdown files for front matter where keys are not in alphabetical order."""
    issues = []

    # Define directories to scan
    directories_to_scan = ["_posts", "original", "notes", "_notes"]

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
                    # Use frontmatter library for proper YAML parsing
                    post = frontmatter.load(file_path)
                    if not post.metadata:
                        continue

                    # Check if keys are in alphabetical order
                    actual_keys = list(post.metadata.keys())
                    sorted_keys = sorted(actual_keys)

                    if actual_keys != sorted_keys:
                        # Find line number of the front matter start
                        with open(file_path, "r", encoding="utf-8") as f:
                            lines = f.readlines()

                        # Count lines until first front matter key
                        line_number = 1
                        for line in lines[:50]:
                            if line.strip().startswith("---"):
                                break
                            line_number += 1

                        # Find first out-of-order key
                        first_out_of_order_index = None
                        for i in range(len(actual_keys) - 1):
                            if actual_keys[i] > actual_keys[i + 1]:
                                first_out_of_order_index = i
                                break

                        issues.append(
                            {
                                "file": file_path,
                                "line": line_number,
                                "expected_order": sorted_keys,
                                "actual_order": actual_keys,
                                "first_misplaced_key": actual_keys[
                                    first_out_of_order_index
                                ]
                                if first_out_of_order_index is not None
                                else None,
                            }
                        )

                except (UnicodeDecodeError, IOError, Exception):
                    # Skip files that can't be read or parsed
                    continue

    return issues


class TestFrontMatterKey(unittest.TestCase):
    def test_front_matter_key_order(self):
        """Test that front matter keys are in alphabetical order."""
        key_order_issues = scan_markdown_files_for_front_matter_key_order()

        if key_order_issues:
            details = "\n".join(
                [
                    f"{issue['file']}:{issue['line']} - Front matter keys not in alphabetical order. "
                    f"First misplaced key: {issue['first_misplaced_key']}. "
                    f"Expected: {issue['expected_order']}, Actual: {issue['actual_order']}"
                    for issue in key_order_issues
                ]
            )
            self.fail(
                f"Found {len(key_order_issues)} front matter key ordering issues:\n{details}"
            )


if __name__ == "__main__":
    unittest.main()
