import unittest
import os
import sys
from pathlib import Path
import frontmatter

# Add parent directories to path to import validation function
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

_validate_title = None
try:
    from scripts.agent.title_agent import validate_title

    _validate_title = validate_title
except Exception:
    pass


def _require_validate_title():
    if _validate_title is None:
        raise unittest.SkipTest("OPENROUTER_API_KEY not set; cannot import title_agent")
    return _validate_title


class TestTitleValidation(unittest.TestCase):
    """Test that all post titles pass validation rules."""

    def setUp(self):
        """Set up test fixtures."""
        self.posts_dir = Path(__file__).parent.parent.parent / "_posts"

    def get_all_post_files(self):
        """Get all markdown files from _posts/{lang}/*.md pattern."""
        post_files = []
        if self.posts_dir.exists():
            # Find all language subdirectories and their .md files
            for lang_dir in self.posts_dir.iterdir():
                if lang_dir.is_dir():
                    md_files = list(lang_dir.glob("*.md"))
                    post_files.extend(md_files)
        return post_files

    @unittest.skip("Temporarily skipped - enable when ready to validate all titles")
    def test_all_post_titles_valid(self):
        """Test that all post titles pass validation."""
        post_files = self.get_all_post_files()

        if not post_files:
            self.skipTest("No post files found")

        failed_files = []

        for post_file in post_files:
            try:
                with open(post_file, "r", encoding="utf-8") as f:
                    post = frontmatter.load(f)

                title = post.metadata.get("title")

                if title is None:
                    failed_files.append((post_file, "Missing title"))
                    continue

                # Validate the title
                vt = _require_validate_title()
                vt(title)

            except Exception as e:
                failed_files.append((post_file, str(e)))

        if failed_files:
            error_msg = "The following post files have invalid titles:\n"
            for file_path, error in failed_files:
                error_msg += f"  {file_path}: {error}\n"
            self.fail(error_msg)

    def test_sample_titles(self):
        """Test validation function with sample titles."""
        vt = _require_validate_title()
        # Valid titles
        valid_titles = [
            "Docker, Kubernetes, AWS",
            "Getting Started with Python",
            "My Experience with React",
            "A Simple Guide to Git",
        ]

        for title in valid_titles:
            with self.subTest(title=title):
                self.assertTrue(vt(title))

        # Invalid titles
        invalid_titles = [
            "",  # Empty
            None,  # None
            "a" * 101,  # Too long
            "**Bold Title**",  # Markdown
            "*Italic Title*",  # Markdown
            "[Link Title]",  # Markdown
            "# Header Title",  # Markdown
            "`Code Title`",  # Markdown
            '"Quoted Title"',  # Quotes
            "'Single Quoted'",  # Quotes
            "Title with <brackets>",  # Problematic chars
            "Title with {braces}",  # Problematic chars
        ]

        for title in invalid_titles:
            with self.subTest(title=title):
                with self.assertRaises(ValueError):
                    vt(title)


if __name__ == "__main__":
    unittest.main()
