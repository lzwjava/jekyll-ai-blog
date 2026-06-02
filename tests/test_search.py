import unittest
import subprocess
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.search.search import check_ack, search_posts


class TestSearch(unittest.TestCase):
    @patch("shutil.which")
    def test_check_ack_installed(self, mock_which):
        # Test when ack is installed
        mock_which.return_value = "/usr/bin/ack"

        # Should not raise exception or print anything
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

    @patch("scripts.search.search.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_posts_success(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock successful search result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "notes/test.md:10:This is a test line"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_posts("test", ignore_case=False)

        # Verify ack command was constructed correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]

        self.assertEqual(cmd[0], "/usr/bin/ack")
        self.assertIn("--type-add=md=.md,.markdown", cmd)
        self.assertIn("--md", cmd)
        self.assertIn("--color", cmd)
        self.assertIn("--color-match=red", cmd)
        self.assertIn("test", cmd)
        self.assertIn("_posts/en", cmd)
        self.assertIn("original", cmd)
        self.assertIn("notes", cmd)

        # Verify environment variable
        self.assertEqual(kwargs["env"]["CLICOLOR_FORCE"], "1")

    @patch("scripts.search.search.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_posts_ignore_case(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock successful search result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "test result"
        mock_run.return_value = mock_result

        with patch("builtins.print"):
            search_posts("test", ignore_case=True)

        # Verify -i flag was added
        args, kwargs = mock_run.call_args
        cmd = args[0]
        self.assertIn("-i", cmd)

    @patch("scripts.search.search.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_posts_no_matches(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock no matches found (return code 1)
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_posts("nonexistent")

        # Should print "No matches found"
        mock_print.assert_called()
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        self.assertIn("No matches found", calls)

    @patch("scripts.search.search.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_posts_error(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock command error (return code > 1)
        mock_result = MagicMock()
        mock_result.returncode = 2
        mock_result.stderr = "Command failed"
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_posts("test")

        # Should print error message
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        self.assertIn("Error executing search command", calls)
        self.assertIn("Command failed", calls)

    @patch("scripts.search.search.check_ack")
    @patch("subprocess.run")
    def test_search_posts_exception(self, mock_run, mock_check):
        # Mock subprocess exception
        mock_run.side_effect = subprocess.CalledProcessError(1, "ack")

        with patch("builtins.print") as mock_print:
            search_posts("test")

        # Should handle exception gracefully
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        error_messages = [call for call in calls if "Error executing search" in call]
        self.assertTrue(len(error_messages) > 0)

    @patch("scripts.search.search.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_posts_output_formatting(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock search result with different line formats
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = """notes/test-file-25:This is a match
notes/another-file-100-context line
--
different/format.md:10:Another match"""
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_posts("test")

        # Verify output formatting
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]

        # Should format file:line:content properly
        formatted_calls = [call for call in calls if ":" in call and "notes/" in call]
        self.assertTrue(len(formatted_calls) > 0)


if __name__ == "__main__":
    unittest.main()
