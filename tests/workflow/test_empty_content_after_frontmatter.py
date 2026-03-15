import argparse
import os
import unittest


def scan_for_empty_content_after_frontmatter():
    """Scan all markdown files where body content is empty (only --- after front matter)."""
    issues = []

    directories_to_scan = ["_posts", "original", "notes"]

    for directory in directories_to_scan:
        if not os.path.exists(directory):
            continue

        for root, dirs, files in os.walk(directory):
            for filename in files:
                if not filename.endswith(".md"):
                    continue

                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except (UnicodeDecodeError, IOError):
                    continue

                if not content.startswith("---"):
                    continue

                # Find the closing --- of the front matter
                first_end = content.find("\n---", 3)
                if first_end == -1:
                    continue

                # Everything after the closing ---\n
                after_frontmatter = content[first_end + 4 :]  # skip '\n---'

                # Strip leading whitespace/newlines from the body
                stripped = after_frontmatter.lstrip("\n\r ")

                # If body starts with ---, it means there's a bare --- right after front matter
                if stripped.startswith("---"):
                    issues.append(file_path)

    return issues


def fix_empty_content_after_frontmatter():
    """Remove bare --- lines that appear immediately after front matter."""
    issues = scan_for_empty_content_after_frontmatter()

    if not issues:
        print("No issues found")
        return

    print(f"Found {len(issues)} file(s) to fix")
    fixed_count = 0

    for file_path in issues:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Find end of front matter
            first_end = content.find("\n---", 3)
            if first_end == -1:
                continue

            frontmatter = content[: first_end + 4]  # up to and including '\n---'
            after_frontmatter = content[first_end + 4 :]

            # Remove bare --- lines but keep blank lines
            lines = after_frontmatter.splitlines(keepends=True)
            result_lines = []
            leading = True
            for line in lines:
                stripped = line.strip()
                if leading and stripped == "---":
                    continue  # remove stray --- line only
                elif leading and stripped == "":
                    result_lines.append(line)  # keep blank lines
                else:
                    leading = False
                    result_lines.append(line)

            remaining = "".join(result_lines)
            new_content = frontmatter + remaining

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"  Fixed: {file_path}")
            fixed_count += 1
        except Exception as e:
            print(f"  Failed to fix {file_path}: {e}")

    print(f"Fixed {fixed_count} file(s)")


class TestEmptyContentAfterFrontmatter(unittest.TestCase):
    def test_no_empty_content_after_frontmatter(self):
        """Fail if any file has only --- (or nothing) immediately after its front matter."""
        issues = scan_for_empty_content_after_frontmatter()

        if issues:
            details = "\n".join(issues)
            self.fail(
                f"Found {len(issues)} file(s) with a bare '---' immediately after front matter "
                f"(empty body or accidental duplicate separator):\n{details}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Detect and optionally fix bare --- after front matter"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Remove bare --- lines instead of just testing",
    )

    args = parser.parse_args()

    if args.fix:
        fix_empty_content_after_frontmatter()
    else:
        unittest.main(argv=[""])
