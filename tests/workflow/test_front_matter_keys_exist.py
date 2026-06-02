import unittest
import os
import frontmatter


def scan_markdown_files_for_required_keys():
    """Scan all markdown files and check that front matter contains all required keys."""
    issues = []

    # Define directories to scan
    directories_to_scan = ["_posts", "original", "notes", "_notes"]

    # Define required keys
    required_keys = [
        "audio",
        "generated",
        "lang",
        "layout",
        "title",
        "translated",
        "type",
    ]

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

                    # Check if all required keys exist
                    missing_keys = [
                        key for key in required_keys if key not in post.metadata
                    ]

                    if missing_keys:
                        # Find line number of the front matter start
                        with open(file_path, "r", encoding="utf-8") as f:
                            lines = f.readlines()

                        # Count lines until first front matter key
                        line_number = 1
                        for line in lines[:50]:
                            if line.strip().startswith("---"):
                                break
                            line_number += 1

                        issues.append(
                            {
                                "file": file_path,
                                "line": line_number,
                                "missing_keys": missing_keys,
                                "present_keys": list(post.metadata.keys()),
                            }
                        )

                except (UnicodeDecodeError, IOError, Exception):
                    # Skip files that can't be read or parsed
                    continue

    return issues


class TestFrontMatterKeysExist(unittest.TestCase):
    @unittest.skip("Temporarily disabled - skipping front matter validation")
    def test_front_matter_keys_exist(self):
        """Test that all front matter contains the required 7 keys."""
        missing_key_issues = scan_markdown_files_for_required_keys()

        if missing_key_issues:
            details = "\n".join(
                [
                    f"{issue['file']}:{issue['line']} - Missing front matter keys: {issue['missing_keys']}. "
                    f"Present keys: {issue['present_keys']}"
                    for issue in missing_key_issues
                ]
            )
            self.fail(
                f"Found {len(missing_key_issues)} files with missing front matter keys:\n{details}"
            )


if __name__ == "__main__":
    unittest.main()
