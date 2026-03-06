#!/usr/bin/env python3
"""
Git Show Python Command Helper

This script shows the last git commit and copies the command for running
the first Python script mentioned in the commit to the clipboard.

Usage:
    python3 scripts/git/git_show_command.py
    # Or make executable and run: ./scripts/git/git_show_command.py
"""

import subprocess
import sys
import os
import re
from pathlib import Path

# Try to import pyperclip for clipboard functionality
try:
    import pyperclip

    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("Note: pyperclip not found. To install: pip3 install pyperclip")


def get_last_commit_info():
    """Get information about the last commit including changed Python files."""
    try:
        # Get commit hash and message
        commit_cmd = ["git", "log", "-1", "--pretty=format:%H %s"]
        commit_info = subprocess.check_output(commit_cmd, text=True).strip()
        commit_hash, commit_message = commit_info.split(" ", 1)

        # Get changed files in this commit
        files_cmd = ["git", "show", "--name-only", "--format=%n", commit_hash]
        all_files = subprocess.check_output(files_cmd, text=True).strip().split("\n")
        all_files = [f.strip() for f in all_files if f.strip()]

        # Filter Python files from this commit
        python_files = [f for f in all_files if f.endswith(".py")]

        return {
            "hash": commit_hash[:8],  # Short hash
            "message": commit_message,
            "python_files": python_files,
            "all_files": all_files,
        }
    except subprocess.CalledProcessError as e:
        print(f"Error getting git info: {e}")
        return None


def format_file_list(files, title):
    """Format a list of files for display."""
    if not files:
        return f"  {title}: None"

    result = f"  {title}:"
    for i, file in enumerate(files, 1):
        result += f"\n    {i}. {file}"
    return result


def main():
    """Main function to display commit info and handle clipboard functionality."""
    print("=== Git Commit Python Command Helper ===\n")

    # Get commit information
    commit_info = get_last_commit_info()
    if not commit_info:
        print(
            "Could not retrieve git commit information. Make sure you're in a git repository."
        )
        return 1

    # Display commit information
    print(f"Last commit: {commit_info['hash']}")
    print(f"Message: {commit_info['message']}")
    print()
    print(format_file_list(commit_info["all_files"], "All changed files"))
    print()
    print(format_file_list(commit_info["python_files"], "Python files"))
    print()

    # Handle Python files
    if commit_info["python_files"]:
        first_py = commit_info["python_files"][0]
        python_cmd = f"python {first_py}"

        print(f"First Python file: {first_py}")

        # Copy to clipboard if available
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(python_cmd)
                print("✅ Command copied to clipboard!")
            except Exception as e:
                print(f"Could not copy to clipboard: {e}")
        else:
            print(
                "Install pyperclip for clipboard functionality: pip3 install pyperclip"
            )

        print(f"Command to try: {python_cmd}")

        # Check file existence
        if os.path.exists(first_py):
            print("✅ File exists and ready to run!")
        else:
            print("⚠️  File path might be relative. Check the file location.")

        print(f"\n💡 To try this script, run: {python_cmd}")
    else:
        print("No Python files found in the last commit.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
