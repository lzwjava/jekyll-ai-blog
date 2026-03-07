#!/usr/bin/env python
import os
import shutil
import sys


def sync_git_hooks():
    # Define source and destination directories
    source_dir = "scripts/githook"
    dest_dir = ".git/hooks"

    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory {source_dir} does not exist")
        sys.exit(1)

    # Check if destination directory exists
    if not os.path.exists(dest_dir):
        print(f"Error: Destination directory {dest_dir} does not exist")
        sys.exit(1)

    # Get all files in source directory, excluding .py files
    # Include .sh files and files without extensions (git hooks don't have extensions)
    files_to_copy = [
        f
        for f in os.listdir(source_dir)
        if (
            f.endswith(".sh")  # Shell scripts
            or (
                "." not in f and os.path.isfile(os.path.join(source_dir, f))
            )  # Files without extension
        )
        and f != "sync_githook.py"  # Exclude the sync script itself
    ]

    print(f"Found {len(files_to_copy)} hook file(s) to sync: {files_to_copy}")

    # Copy each file to the hooks directory
    for file in files_to_copy:
        source_path = os.path.join(source_dir, file)
        dest_path = os.path.join(dest_dir, file)

        try:
            shutil.copy2(source_path, dest_path)
            # Make the hook executable
            os.chmod(dest_path, 0o755)
            print(f"Synced {file} to {dest_dir}")
        except Exception as e:
            print(f"Error copying {file}: {e}")
            sys.exit(1)

    print("Git hooks sync completed successfully.")


if __name__ == "__main__":
    sync_git_hooks()
