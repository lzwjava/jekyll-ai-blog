#!/usr/bin/env python3
"""
Script to open multiple Ghostty terminal windows
"""

import argparse
import subprocess
import sys
import os


def run_command(cmd):
    """Run a shell command."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result
    except Exception as e:
        print(f"Error running command: {e}")
        return None


def open_ghostty_at_path(path, number):
    """Open Ghostty terminal windows at different positions."""
    if not path:
        print("Error: Path is required")
        return False

    if number <= 0:
        print("Error: Number must be greater than 0")
        return False

    # Expand tilde if present
    path = os.path.expanduser(path)

    # Check if path exists
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist")
        return False

    opened = 0
    for i in range(number):
        # Use open -na ghostty.app with working directory argument
        # The -na flag opens a new instance (-n) without bringing it to front (-a)
        # macOS will naturally position new windows in a cascade (different positions)
        cmd = f'open -na ghostty.app --args --working-directory="{path}"'
        result = run_command(cmd)

        if result and result.returncode == 0:
            opened += 1
            print(f"Opened Ghostty window {i + 1}/{number} in {path}")
        else:
            print(f"Failed to open Ghostty window {i + 1}/{number}")
            if result and result.stderr:
                print(f"Error: {result.stderr}")

    print(f"\nSuccessfully opened {opened}/{number} Ghostty terminal window(s)")
    print("Note: macOS will naturally position the windows at different locations (cascade)")
    return opened == number


def main():
    parser = argparse.ArgumentParser(
        description="Open multiple Ghostty terminal windows"
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The directory path to open in each terminal"
    )
    parser.add_argument(
        "--number",
        type=int,
        required=True,
        help="The number of terminals to open"
    )

    args = parser.parse_args()

    success = open_ghostty_at_path(args.path, args.number)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
