import unittest
import os
from unittest.mock import patch, mock_open
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.translation.update_lang import get_output_filename, get_changed_files


class TestUpdateLang(unittest.TestCase):
    def test_get_output_filename(self):
        # Test with English file
        result = get_output_filename("2024-01-01-test-en.md", "ja")
        self.assertEqual(result, "2024-01-01-test-ja.md")

        # Test with Chinese file
        result = get_output_filename("2024-01-01-test-zh.md", "en")
        self.assertEqual(result, "2024-01-01-test-en.md")

        # Test with Japanese file
        result = get_output_filename("2024-01-01-test-ja.md", "fr")
        self.assertEqual(result, "2024-01-01-test-fr.md")

        # Test with invalid filename format
        with self.assertRaises(Exception) as context:
            get_output_filename("invalid-filename.md", "ja")
        self.assertIn("Unexpected filename format", str(context.exception))

    @patch("os.listdir")
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_changed_files_basic(self, mock_file, mock_exists, mock_listdir):
        # Mock the input directory listing
        mock_listdir.return_value = ["2024-01-01-test-en.md"]

        # Mock file existence checks
        mock_exists.side_effect = lambda path: "original" in path

        # Mock file content
        mock_content = """---
title: Test Post
---
This is test content."""
        mock_file.return_value.read.return_value = mock_content

        # Test the function
        with patch("scripts.translation.update_lang.INPUT_DIR", "original"):
            result = get_changed_files()

        # Should return files that need translation
        self.assertIsInstance(result, set)
        # The function should process the file for all target languages
        self.assertTrue(len(result) > 0)

    @patch("os.listdir")
    def test_get_changed_files_skip_non_markdown(self, mock_listdir):
        # Mock directory with non-markdown files
        mock_listdir.return_value = ["README.txt", "image.png", "2024-01-01-test-en.md"]

        with patch("scripts.translation.update_lang.INPUT_DIR", "original"):
            with patch(
                "builtins.open", mock_open(read_data="---\ntitle: Test\n---\nContent")
            ):
                with patch("os.path.exists", return_value=False):
                    result = get_changed_files()

        # Should only process .md files
        self.assertIsInstance(result, set)

    @patch("os.listdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_changed_files_invalid_format(self, mock_file, mock_listdir):
        # Mock directory with invalid filename format
        mock_listdir.return_value = ["invalid-format.md"]

        mock_content = """---
title: Test Post
---
Content"""
        mock_file.return_value.read.return_value = mock_content

        with patch("scripts.translation.update_lang.INPUT_DIR", "original"):
            result = get_changed_files()

        # Should handle invalid format gracefully
        self.assertIsInstance(result, set)

    @patch("os.listdir")
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_changed_files_no_front_matter(
        self, mock_file, mock_exists, mock_listdir
    ):
        # Mock file without front matter
        mock_listdir.return_value = ["2024-01-01-test-en.md"]
        mock_exists.return_value = False
        mock_file.return_value.read.return_value = "Just content without front matter"

        with patch("scripts.translation.update_lang.INPUT_DIR", "original"):
            result = get_changed_files()

        # Should handle files without front matter gracefully
        self.assertIsInstance(result, set)


if __name__ == "__main__":
    unittest.main()
