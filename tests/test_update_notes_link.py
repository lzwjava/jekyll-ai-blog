import unittest
import os
from unittest.mock import patch, mock_open
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generate.update_notes_link import (
    count_notes_files,
    count_links_in_notes_md,
    copy_original_to_posts,
)


class TestUpdateNotesLink(unittest.TestCase):
    @patch("os.listdir")
    def test_count_notes_files_success(self, mock_listdir):
        # Mock directory with markdown files
        mock_listdir.return_value = [
            "note1.md",
            "note2.md",
            "note3.txt",  # Non-markdown file
            "note4.md",
        ]

        result = count_notes_files()
        self.assertEqual(result, 3)  # Only .md files should be counted
        mock_listdir.assert_called_once_with("notes")

    @patch("os.listdir")
    def test_count_notes_files_error(self, mock_listdir):
        # Mock directory access error
        mock_listdir.side_effect = Exception("Directory not found")

        with patch("builtins.print") as mock_print:
            result = count_notes_files()
            self.assertEqual(result, 0)
            mock_print.assert_called_once()
            self.assertIn("Error counting notes files", mock_print.call_args[0][0])

    @patch("builtins.open", new_callable=mock_open)
    def test_count_links_in_notes_md_success(self, mock_file):
        # Mock file content with markdown links
        content = """# Notes

* [Note 1](/notes/note1.md)
* [Note 2](/notes/note2.md)
* [Regular link](https://example.com)
* [Note 3](/notes/note3.md)
* Not a link

Some other content.
"""
        mock_file.return_value.read.return_value = content

        result = count_links_in_notes_md()
        self.assertEqual(result, 3)  # Only notes links should be counted
        mock_file.assert_called_once_with(
            os.path.join("original", "2025-01-11-notes-en.md"), "r", encoding="utf-8"
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_count_links_in_notes_md_no_links(self, mock_file):
        # Mock file content without links
        content = """# Notes

This is a notes file without any links.
Just some regular text content.
"""
        mock_file.return_value.read.return_value = content

        result = count_links_in_notes_md()
        self.assertEqual(result, 0)

    @patch("builtins.open")
    def test_count_links_in_notes_md_error(self, mock_file):
        # Mock file read error
        mock_file.side_effect = Exception("File not found")

        with patch("builtins.print") as mock_print:
            result = count_links_in_notes_md()
            self.assertEqual(result, 0)
            mock_print.assert_called_once()
            self.assertIn(
                "Error counting links in notes markdown file",
                mock_print.call_args[0][0],
            )

    @patch("shutil.copy2")
    @patch("os.makedirs")
    @patch("os.path.basename")
    def test_copy_original_to_posts_success(
        self, mock_basename, mock_makedirs, mock_copy
    ):
        # Mock basename to return expected filename
        mock_basename.return_value = "2025-01-11-notes-en.md"

        with patch("builtins.print") as mock_print:
            copy_original_to_posts()

            # Verify directory creation
            mock_makedirs.assert_called_once_with("_posts/en", exist_ok=True)

            # Verify file copy
            mock_copy.assert_called_once()
            src_arg, dst_arg = mock_copy.call_args[0]
            self.assertEqual(
                src_arg, os.path.join("original", "2025-01-11-notes-en.md")
            )
            self.assertEqual(
                dst_arg, os.path.join("_posts/en", "2025-01-11-notes-en.md")
            )

            # Verify print message
            mock_print.assert_called_once()
            self.assertIn("Copied", mock_print.call_args[0][0])


if __name__ == "__main__":
    unittest.main()
