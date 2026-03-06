#!/usr/bin/env python3
"""
Sync gitmessageai.py script to ~/bin/
"""

import os
import shutil


def main():
    """Main sync function."""
    source_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "github",
        "gitmessageai.py",
    )
    target_path = os.path.expanduser("~/bin/gitmessageai.py")

    print(f"Syncing gitmessageai.py...")
    print(f"Source: {source_path}")
    print(f"Target: {target_path}")

    if not os.path.exists(source_path):
        print(f"Error: Source file does not exist: {source_path}")
        return

    # Copy the file
    shutil.copy2(source_path, target_path)

    # Make executable
    os.chmod(target_path, 0o755)

    print("Sync completed successfully!")


if __name__ == "__main__":
    main()
