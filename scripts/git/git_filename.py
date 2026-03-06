import subprocess
import re
import sys

#!/usr/bin/env python3


def check_git_filenames():
    """Check if all git-tracked filenames contain only allowed characters"""
    try:
        # Get all git-tracked files
        result = subprocess.run(
            ["git", "ls-files"], capture_output=True, text=True, check=True
        )
        filenames = result.stdout.strip().split("\n")

        # Pattern for general files: A-Za-z0-9, ., _
        general_pattern = re.compile(r"^[A-Za-z0-9._/]+$")
        # Pattern for markdown files: A-Za-z0-9, ., _, -
        markdown_pattern = re.compile(r"^[A-Za-z0-9._/-]+$")

        invalid_files = []

        for filename in filenames:
            if filename:
                if filename.endswith(".md"):
                    if not markdown_pattern.match(filename):
                        invalid_files.append(filename)
                else:
                    if not general_pattern.match(filename):
                        invalid_files.append(filename)

        if invalid_files:
            print("Files with invalid characters found:")
            for file in invalid_files:
                print(f"  {file}")
            return False
        else:
            print("All filenames contain only allowed characters")
            return True

    except subprocess.CalledProcessError:
        print("Error: Not in a git repository or git command failed")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    success = check_git_filenames()
    sys.exit(0 if success else 1)
