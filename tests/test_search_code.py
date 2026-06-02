import unittest
import subprocess
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.search.search_code import check_ack, search_code


class TestSearchCode(unittest.TestCase):
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

    @patch("scripts.search.search_code.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_code_success(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock successful search result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "scripts/test.py:25:def test_function():"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_code("test_function", ignore_case=False)

        # Verify ack command was constructed correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]

        self.assertEqual(cmd[0], "/usr/bin/ack")

        # Check for code file types
        type_add_found = False
        for arg in cmd:
            if arg.startswith("--type-add=code=") and ".py" in arg and ".js" in arg:
                type_add_found = True
                break
        self.assertTrue(type_add_found, "Code file types not properly configured")

        self.assertIn("--code", cmd)
        self.assertIn("--color", cmd)
        self.assertIn("--color-match=red", cmd)
        self.assertIn("test_function", cmd)
        self.assertIn(".", cmd)  # Search current directory

        # Verify environment variable
        self.assertEqual(kwargs["env"]["CLICOLOR_FORCE"], "1")

    @patch("scripts.search.search_code.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_code_ignore_case(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock successful search result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "test result"
        mock_run.return_value = mock_result

        with patch("builtins.print"):
            search_code("TEST", ignore_case=True)

        # Verify -i flag was added
        args, kwargs = mock_run.call_args
        cmd = args[0]
        self.assertIn("-i", cmd)

    @patch("scripts.search.search_code.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_code_no_matches(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock no matches found (return code 1)
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_code("nonexistent_function")

        # Should print "No matches found"
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        self.assertIn("No matches found", calls)

    @patch("scripts.search.search_code.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_code_error(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock command error (return code > 1)
        mock_result = MagicMock()
        mock_result.returncode = 2
        mock_result.stderr = "Search failed"
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_code("test")

        # Should print error message
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        self.assertIn("Error executing search command", calls)
        self.assertIn("Search failed", calls)

    @patch("scripts.search.search_code.check_ack")
    @patch("subprocess.run")
    def test_search_code_exception(self, mock_run, mock_check):
        # Mock subprocess exception
        mock_run.side_effect = subprocess.CalledProcessError(1, "ack")

        with patch("builtins.print") as mock_print:
            search_code("test")

        # Should handle exception gracefully
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        error_messages = [call for call in calls if "Error executing search" in call]
        self.assertTrue(len(error_messages) > 0)

    @patch("scripts.search.search_code.check_ack")
    @patch("shutil.which")
    @patch("subprocess.run")
    def test_search_code_output_formatting(self, mock_run, mock_which, mock_check):
        # Mock ack being available
        mock_which.return_value = "/usr/bin/ack"

        # Mock search result with code file matches
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = """scripts/bot/test-bot-15:def send_message():
src/utils/helper-10-    return result
--
tests/test-file-5.py:20:class TestClass:"""
        mock_run.return_value = mock_result

        with patch("builtins.print") as mock_print:
            search_code("def")

        # Verify output formatting
        calls = [call[0][0] for call in mock_print.call_args_list if call[0]]

        # Should format file:line:content properly for code files
        formatted_calls = [
            call
            for call in calls
            if ":" in call
            and ("scripts/" in call or "src/" in call or "tests/" in call)
        ]
        self.assertTrue(len(formatted_calls) > 0)

    def test_code_file_extensions(self):
        # Test that the file extension list includes common code file types
        with patch("scripts.search.search_code.check_ack"):
            with patch("shutil.which", return_value="/usr/bin/ack"):
                with patch("subprocess.run") as mock_run:
                    mock_result = MagicMock()
                    mock_result.returncode = 0
                    mock_result.stdout = ""
                    mock_run.return_value = mock_result

                    with patch("builtins.print"):
                        search_code("test")

                    args, kwargs = mock_run.call_args
                    cmd = args[0]

                    # Find the type-add argument
                    type_add_arg = None
                    for arg in cmd:
                        if arg.startswith("--type-add=code="):
                            type_add_arg = arg
                            break

                    self.assertIsNotNone(type_add_arg)

                    # Check for important file extensions
                    extensions = [
                        ".py",
                        ".js",
                        ".ts",
                        ".rs",
                        ".c",
                        ".cpp",
                        ".java",
                        ".go",
                        ".rb",
                    ]
                    for ext in extensions:
                        self.assertIn(
                            ext,
                            type_add_arg,
                            f"Extension {ext} not found in code file types",
                        )


if __name__ == "__main__":
    unittest.main()
