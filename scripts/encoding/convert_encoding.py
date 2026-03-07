#!/usr/bin/env python3
"""
Encoding Conversion Script
Converts files to a target encoding, with options to process
individual files or all files in a directory.
"""

import sys
import chardet
from pathlib import Path
from typing import List, Tuple, Optional


def detect_file_encoding(file_path: Path) -> Optional[str]:
    """
    Detect the encoding of a file.

    Args:
        file_path: Path to the file to check

    Returns:
        str: Detected encoding or None if detection fails
    """
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read(10000)  # Read first 10KB for detection
    except Exception as e:
        print(f"  Error reading file: {e}")
        return None

    result = chardet.detect(raw_data)
    return result["encoding"] if result["encoding"] else None


def convert_file_encoding(file_path: Path, target_encoding: str) -> Tuple[bool, str]:
    """
    Convert a single file to target encoding.

    Args:
        file_path: Path to the file to convert
        target_encoding: The desired encoding

    Returns:
        Tuple[bool, str]: (success, message)
    """
    if not file_path.exists():
        return False, "File does not exist"

    try:
        current_encoding = detect_file_encoding(file_path)

        if current_encoding is None:
            return False, "Could not detect encoding"

        # Skip files that are already in the target encoding
        # Special case: ASCII to UTF-8 is a no-op since UTF-8 is backward compatible with ASCII
        if current_encoding.lower() == target_encoding.lower() or (
            current_encoding
            and current_encoding.lower() == "ascii"
            and target_encoding.lower() == "utf-8"
        ):
            return True, f"Already in {target_encoding} encoding"

        with open(file_path, "r", encoding=current_encoding) as f:
            content = f.read()

        with open(file_path, "w", encoding=target_encoding) as f:
            f.write(content)

        return True, f"Converted from {current_encoding} to {target_encoding}"

    except Exception as e:
        return False, f"Error: {str(e)}"


def process_files(
    paths: List[Path], target_encoding: str, extension: Optional[str] = None
) -> None:
    """
    Process files or directories for encoding conversion.

    Args:
        paths: List of paths to process
        target_encoding: The desired encoding
        extension: Optional file extension filter (e.g., '.py', '.txt')
    """
    files_to_process: List[Tuple[Path, str]] = []

    for path in paths:
        path = Path(path)
        if path.is_file():
            files_to_process.append((path, str(path)))
        elif path.is_dir():
            print(f"\nScanning directory: {path}")
            print("-" * 70)

            files = list(path.rglob("*"))
            for file in files:
                if file.is_file():
                    # Use provided extension or default to .py
                    file_ext = extension if extension else ".py"
                    if file.suffix == file_ext:
                        files_to_process.append((file, f"{file.relative_to(path)}"))

    if not files_to_process:
        print(f"No files found with extension: {extension or '.py'}")
        return

    print(f"\n{'=' * 70}")
    print(f"Found {len(files_to_process)} file(s) to check")
    print(f"Target encoding: {target_encoding}")
    print(f"Extension filter: {extension or '.py'}")
    print(f"{'=' * 70}\n")

    for file_path, display_name in files_to_process:
        detected = detect_file_encoding(file_path)
        print(f"\n{display_name}")

        if detected is None:
            print("  ✗ Could not detect encoding")
            continue

        if detected.lower() == target_encoding.lower():
            print(f"  ✓ Already has {target_encoding} encoding (skipped)")
            continue

        print(f"  Detected: {detected} | Target: {target_encoding}")

        success, message = convert_file_encoding(file_path, target_encoding)
        if success:
            print(f"  ✓ {message}")
        else:
            print(f"  ✗ {message}")

    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python convert_encoding.py <target_encoding> <path1> [path2] [extension]"
        )
        print("  target_encoding: The encoding to convert to (e.g., 'utf-8', 'gbk')")
        print("  path: File or directory path(s)")
        print("  extension: Optional file extension filter (default: '.py')")
        print("\nExamples:")
        print("  python convert_encoding.py utf-8 file.py")
        print("  python convert_encoding.py utf-8 /path/to/dir")
        print("  python convert_encoding.py gbk /path/to/dir .txt")
        print("  python convert_encoding.py utf-8 path1.py path2.txt")
        sys.exit(1)

    target_encoding = sys.argv[1]
    paths = sys.argv[2:]

    extension = ".py"
    if len(paths) >= 1:
        ext = paths[-1]
        if ext.startswith(".") and len(ext) <= 6:
            extension = ext
            paths = paths[:-1]

    if not paths:
        paths = ["."]

    print(f"Target encoding: {target_encoding}")
    print(f"Paths to process: {', '.join(str(p) for p in paths)}")
    if len(paths) > 0 and not paths[0].startswith("."):
        print(f"Extension filter: {extension}")

    paths_obj = [Path(p) for p in paths]
    process_files(paths_obj, target_encoding, extension)
