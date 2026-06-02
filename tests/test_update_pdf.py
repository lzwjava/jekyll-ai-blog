import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.pdf.update_pdf import get_all_md_files, get_last_n_files, get_changed_files


class TestUpdatePdf(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.test_dir, "_posts")
        os.makedirs(self.input_dir)

        # Create language directories with test files
        for lang in ["en", "zh", "ja"]:
            lang_dir = os.path.join(self.input_dir, lang)
            os.makedirs(lang_dir)

            # Create test markdown files
            for i in range(3):
                test_file = os.path.join(lang_dir, f"test-{i}.md")
                with open(test_file, "w") as f:
                    f.write(f"# Test file {i} for {lang}")

    def tearDown(self):
        # Clean up temporary directory
        import shutil

        shutil.rmtree(self.test_dir)

    @patch("scripts.pdf.update_pdf.LANGUAGES", ["en", "zh", "ja"])
    def test_get_all_md_files(self):
        # Test getting all markdown files
        md_files = get_all_md_files(self.input_dir)

        # Should find all 9 files (3 languages × 3 files each)
        self.assertEqual(len(md_files), 9)

        # All returned files should end with .md
        for file_path in md_files:
            self.assertTrue(file_path.endswith(".md"))
            self.assertTrue(os.path.exists(file_path))

    @patch("scripts.pdf.update_pdf.LANGUAGES", ["nonexistent"])
    def test_get_all_md_files_nonexistent_dir(self):
        # Test with non-existent language directory
        md_files = get_all_md_files(self.input_dir)

        # Should return empty list when no matching directories exist
        self.assertEqual(len(md_files), 0)

    @patch("scripts.pdf.update_pdf.get_all_md_files")
    @patch("os.path.getmtime")
    def test_get_last_n_files(self, mock_getmtime, mock_get_all):
        # Mock file list and modification times
        mock_files = ["/path/file1.md", "/path/file2.md", "/path/file3.md"]
        mock_get_all.return_value = mock_files

        # Mock modification times (file3 is newest, file1 is oldest)
        mock_getmtime.side_effect = lambda x: {
            "/path/file1.md": 1000,
            "/path/file2.md": 2000,
            "/path/file3.md": 3000,
        }[x]

        # Test getting last 2 files
        result = get_last_n_files("dummy_dir", n=2)

        # Should return files sorted by modification time (newest first)
        expected = ["/path/file3.md", "/path/file2.md"]
        self.assertEqual(result, expected)

    @patch("scripts.pdf.update_pdf.get_all_md_files")
    def test_get_last_n_files_error_handling(self, mock_get_all):
        # Mock an exception
        mock_get_all.side_effect = Exception("Test error")

        with patch("builtins.print") as mock_print:
            result = get_last_n_files("dummy_dir")

            # Should return empty list on error
            self.assertEqual(result, [])

            # Should print error message
            mock_print.assert_called_once()
            self.assertIn("Error retrieving files", mock_print.call_args[0][0])

    @patch("subprocess.run")
    def test_get_changed_files_success(self, mock_run):
        # Mock successful git command
        mock_result = MagicMock()
        mock_result.stdout = "_posts/en/file1.md\n_posts/zh/file2.md\nother/file.txt\n"
        mock_run.return_value = mock_result

        result = get_changed_files()

        # Should only return .md files from _posts directory
        expected = ["_posts/en/file1.md", "_posts/zh/file2.md"]
        self.assertEqual(result, expected)

        # Verify git command was called correctly
        mock_run.assert_called_once_with(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("subprocess.run")
    def test_get_changed_files_error(self, mock_run):
        # Mock git command failure
        mock_run.side_effect = Exception("Git error")

        with patch("builtins.print") as mock_print:
            result = get_changed_files()

            # Should return empty list on error
            self.assertEqual(result, [])

            # Should print error message
            mock_print.assert_called_once()
            self.assertIn("Error getting changed files", mock_print.call_args[0][0])


if __name__ == "__main__":
    unittest.main()
