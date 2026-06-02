import unittest
import subprocess
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.search.search_filename import check_ack, search_filenames


class TestSearchFilename(unittest.TestCase):
    @patch("shutil.which")
    def test_check_ack_installed(self, mock_which):
        # Test when ack is installed
        mock_which.return_value = "/usr/bin/ack"

        # Should not raise exception
        try:
            check_ack()
        except SystemExit:
            self.fail("check_ack() raised SystemExit unexpectedly")

    @patch("shutil.which")
    @patch("builtins.print")
    def test_check_ack_not_installed(self, mock_print, mock_which):
        # Test when ack is not installed
        mock_which.return_value = None

        with self.assertRaises(SystemExit):
            check_ack()

        # Should print installation instructions
        self.assertEqual(mock_print.call_count, 4)
        calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn("Error: ack is not installed.", calls)
        self.assertIn("Please install it first:", calls)

    @patch("scripts.search.search_filename.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_filenames_success(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock successful search result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "original/2024-01-01-english-en.md\noriginal/2024-02-01-english-practice-en.md"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_filenames("english", ignore_case=False)

        # Verify ack command was constructed correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]

        self.assertEqual(cmd[0], "/usr/bin/ack")
        self.assertIn("-g", cmd)  # Filename search flag
        self.assertIn("--type-add=md=.md,.markdown", cmd)
        self.assertIn("--md", cmd)
        self.assertIn("english", cmd)
        self.assertIn("original", cmd)

        # Verify output was printed
        mock_print.assert_called()
        printed_output = mock_print.call_args[0][0]
        self.assertIn("english-en.md", printed_output)

    @patch("scripts.search.search_filename.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_filenames_ignore_case(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock successful search result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "original/test-file.md"
        mock_run.return_value = mock_result

        with patch("builtins.print"):
            search_filenames("TEST", ignore_case=True)

        # Verify -i flag was added
        args, kwargs = mock_run.call_args
        cmd = args[0]
        self.assertIn("-i", cmd)

    @patch("scripts.search.search_filename.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_filenames_no_matches(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock no matches found (return code 1)
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_filenames("nonexistent")

        # Should print "No matching filenames found"
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        self.assertIn("No matching filenames found", calls)

    @patch("scripts.search.search_filename.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_filenames_error(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock command error (return code > 1)
        mock_result = MagicMock()
        mock_result.returncode = 2
        mock_result.stderr = "Directory not found"
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_filenames("test")

        # Should print error message
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        self.assertIn("Error executing search command", calls)
        self.assertIn("Directory not found", calls)

    @patch("scripts.search.search_filename.check_ack")
    @patch("subprocess.run")
    def test_search_filenames_exception(self, mock_run, mock_check):
        # Mock subprocess exception
        mock_run.side_effect = subprocess.CalledProcessError(1, "ack")

        with patch("builtins.print") as mock_print:
            search_filenames("test")

        # Should handle exception gracefully
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        error_messages = [call for call in calls if "Error executing search" in call]
        self.assertTrue(len(error_messages) > 0)

    @patch("scripts.search.search_filename.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_filenames_multiple_results(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock search result with multiple filenames
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = """original/2021-01-25-english-en.md
original/2025-02-15-english-practice-en.md
original/2025-07-10-english-animation-en.md"""
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_filenames("english")

        # Verify output contains all filenames
        printed_output = mock_print.call_args[0][0]
        self.assertIn("2021-01-25-english-en.md", printed_output)
        self.assertIn("2025-02-15-english-practice-en.md", printed_output)
        self.assertIn("2025-07-10-english-animation-en.md", printed_output)

    @patch("scripts.search.search_filename.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_filenames_whitespace_handling(
        self, mock_run, mock_which, mock_check
    ):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock search result with leading/trailing whitespace
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "  original/test-file.md  \n"
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_filenames("test")

        # Verify whitespace is stripped
        printed_output = mock_print.call_args[0][0]
        self.assertEqual(printed_output, "original/test-file.md")
        self.assertFalse(printed_output.startswith(" "))
        self.assertFalse(printed_output.endswith(" "))

    def test_search_directory_constraint(self):
        # Test that the search is constrained to 'original' directory
        with patch("scripts.search.search_filename.check_ack"):
            with patch("shutil.which", return_value="/usr/bin/ack"):
                with patch("subprocess.run") as mock_run:
                    mock_result = MagicMock()
                    mock_result.returncode = 0
                    mock_result.stdout = ""
                    mock_run.return_value = mock_result

                    with patch("builtins.print"):
                        search_filenames("test")

                    args, kwargs = mock_run.call_args
                    cmd = args[0]

                    # Should only search in 'original' directory
                    self.assertIn("original", cmd)
                    # Should not search in other directories like '_posts/en' or 'notes'
                    self.assertNotIn("_posts/en", cmd)
                    self.assertNotIn("notes", cmd)


if __name__ == "__main__":
    unittest.main()
