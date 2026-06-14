"""
Catch bare Liquid tags ({% %}) in markdown files before they reach CI.

Jekyll's Liquid parser processes ALL content (even inside fenced code blocks)
unless the file is wrapped in {% raw %}...{% endraw %}.  A bare {% %} causes
a fatal Liquid::SyntaxError that crashes the GitHub Actions build.

This test scans _posts/ and notes/ for patterns that break the build.

Run:
    python -m unittest tests.workflow.test_liquid_syntax -v
"""

import re
import unittest
from pathlib import Path


# Directories Jekyll processes (excluded dirs are in _config.yml)
SCAN_DIRS = ["_posts", "notes"]

# Regex: find {% ... %} that is NOT {% raw %} or {% endraw %} or {% raw %}{% %}{% endraw %}
# We look for {% followed by anything then %}, but exclude the known-safe patterns.
BARE_LIQUID_TAG = re.compile(r"\{%-?\s*%-?\}")  # matches {% %} (empty tag)
ENDRAW_TAG = re.compile(r"\{%\-?\s*endraw\s*%\-?\}")
RAW_TAG = re.compile(r"\{%\-?\s*raw\s*%\-?\}")


def _is_inside_raw_block(lines: list[str], target_line_idx: int) -> bool:
    """Check if target_line_idx is between a {% raw %} and {% endraw %} pair.

    Handles both file-level wrappers (raw on early line, endraw on last line)
    and inline wrappers ({% raw %}{% %}{% endraw %} on the same line).
    """
    # Check inline: {% raw %}{% %}{% endraw %} on the same line
    line = lines[target_line_idx]
    if RAW_TAG.search(line) and ENDRAW_TAG.search(line):
        return True

    # Check file-level wrapper: find nearest raw before and endraw after
    raw_line = None
    for i in range(target_line_idx, -1, -1):
        if RAW_TAG.search(lines[i]):
            raw_line = i
            break

    if raw_line is None:
        return False

    endraw_line = None
    for i in range(raw_line + 1, len(lines)):
        if ENDRAW_TAG.search(lines[i]):
            endraw_line = i
            break

    if endraw_line is None:
        return False

    return raw_line < target_line_idx < endraw_line


def scan_for_bare_liquid_tags() -> list[dict]:
    """Scan markdown files for bare {% %} outside raw blocks."""
    project_root = Path(__file__).parent.parent.parent
    violations = []

    for scan_dir in SCAN_DIRS:
        dir_path = project_root / scan_dir
        if not dir_path.exists():
            continue

        for md_file in sorted(dir_path.rglob("*.md")):
            try:
                content = md_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            # Skip files that don't contain {% at all
            if "{%" not in content:
                continue

            lines = content.splitlines()

            for i, line in enumerate(lines):
                if BARE_LIQUID_TAG.search(line):
                    if not _is_inside_raw_block(lines, i):
                        violations.append(
                            {
                                "file": str(md_file.relative_to(project_root)),
                                "line": i + 1,
                                "content": line.strip()[:120],
                            }
                        )

    return violations


class TestLiquidSyntax(unittest.TestCase):
    """Detect bare Liquid tags that crash Jekyll builds."""

    def test_no_bare_liquid_tags(self):
        """All {% %} must be inside {% raw %} blocks or inline escapes."""
        violations = scan_for_bare_liquid_tags()

        if violations:
            details = []
            for v in violations:
                details.append(f"  {v['file']}:{v['line']}  {v['content']}")
            joined = "\n".join(details)
            self.fail(
                f"Found {len(violations)} bare Liquid tag(s) that will crash CI:\n"
                f"{joined}\n\n"
                f"Fix: wrap in {{% raw %}}...{{% endraw %}} or use inline "
                f"{{% raw %}}{{% %}}{{% endraw %}}"
            )


if __name__ == "__main__":
    unittest.main()
