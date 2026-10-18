"""
Catch bare Liquid tags ({% %}) in markdown files before they reach CI.

Jekyll's Liquid parser processes ALL content (even inside fenced code blocks)
unless the file is wrapped in {% raw %}...{% endraw %}.  A bare {% %} causes
a fatal Liquid::SyntaxError that crashes the GitHub Actions build.  An
unbalanced {% raw %}/{% endraw %} pair (raw without endraw, or endraw
without raw) is equally fatal.

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
ENDRAW_TAG = re.compile(r"\{%\-?\s*(endraw)\s*%\-?\}")
RAW_TAG = re.compile(r"\{%\-?\s*(raw)\s*%\-?\}")


def _front_matter_stripped(content: str) -> str:
    """Drop YAML front matter the way Jekyll does before Liquid runs."""
    return re.sub(r"\A---\n.*?\n---\n?", "", content, count=1, flags=re.S)


def scan_for_unbalanced_raw_blocks() -> list[dict]:
    """Find {% raw %}/{% endraw %} blocks Liquid cannot close.

    Liquid raw blocks are non-nesting: the first {% endraw %} after a
    {% raw %} closes it, and any raw/endraw tokens inside the block are
    literal text.  A raw block still open at EOF, or an endraw with no
    open block, raises a fatal Liquid::SyntaxError that aborts the build.
    """
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
            if "{%" not in content:
                continue

            body = _front_matter_stripped(content)
            depth = 0
            open_line = None
            for line_no, line in enumerate(body.splitlines(), 1):
                # Process tokens left-to-right exactly like Liquid: a raw
                # block ends at the first endraw after it, so raw tokens
                # inside an open block are literal text (depth > 0).
                tokens = sorted(
                    [(m.start(), m.group(1)) for m in RAW_TAG.finditer(line)]
                    + [(m.start(), m.group(1)) for m in ENDRAW_TAG.finditer(line)]
                )
                for _, tok in tokens:
                    if tok == "raw":
                        if depth == 0:
                            depth = 1
                            open_line = line_no
                    else:  # endraw
                        if depth == 0:
                            violations.append(
                                {
                                    "file": str(md_file.relative_to(project_root)),
                                    "line": line_no,
                                    "content": line.strip()[:120],
                                }
                            )
                        else:
                            depth -= 1
                            open_line = None
            if depth > 0:
                violations.append(
                    {
                        "file": str(md_file.relative_to(project_root)),
                        "line": open_line or 1,
                        "content": "unclosed {% raw %} block",
                    }
                )

    return violations


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

    def test_no_unbalanced_raw_blocks(self):
        """Every {% raw %} must have a matching {% endraw %} and vice versa."""
        violations = scan_for_unbalanced_raw_blocks()

        if violations:
            details = []
            for v in violations:
                details.append(f"  {v['file']}:{v['line']}  {v['content']}")
            joined = "\n".join(details)
            self.fail(
                f"Found {len(violations)} unbalanced {{% raw %}}/{{% endraw %}} "
                f"block(s) that will crash CI:\n{joined}\n\n"
                f'Fix: escape literal tags as `{{ "{{%" }} raw %}}` or close '
                f"the raw block with `{{% endraw %}}`."
            )


if __name__ == "__main__":
    unittest.main()
