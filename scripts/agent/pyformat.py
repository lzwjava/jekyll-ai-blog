import os
import subprocess
from pathlib import Path


def format_directory(directory):
    """
    Format all Python files in the given directory using the black command.

    Args:
        directory (str): Path to the directory containing Python files to format.
    """
    directory_path = Path(directory)
    print(f"Formatting files in {directory_path}")
    try:
        subprocess.run(["black", str(directory_path)])
    except Exception as e:
        print(f"Error formatting directory {directory_path}: {e}")


if __name__ == "__main__":
    scripts_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"
    )
    format_directory(scripts_dir)
