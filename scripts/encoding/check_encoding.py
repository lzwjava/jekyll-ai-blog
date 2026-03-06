#!/usr/bin/env python3
"""
Encoding Check Script
Checks the encoding of a given file and reports it.
"""

import sys
import chardet
from pathlib import Path


def detect_encoding(file_path):
    """
    Detect the encoding of a file.

    Args:
        file_path: Path to the file to check

    Returns:
        dict: Dictionary containing encoding information
    """
    try:
        # Read the file in binary mode
        with open(file_path, "rb") as f:
            raw_data = f.read()
    except Exception as e:
        return {"error": str(e)}

    # Detect encoding using chardet
    result = chardet.detect(raw_data)

    return {
        "encoding": result["encoding"],
        "confidence": result["confidence"],
        "language": result.get("language", "unknown"),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_encoding.py <file_path>")
        print("Example: python check_encoding.py /path/to/file.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    # Check if file exists
    if not Path(file_path).exists():
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    print(f"Checking encoding for: {file_path}")
    print("-" * 50)

    result = detect_encoding(file_path)

    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)

    print(f"Encoding:        {result['encoding']}")
    print(f"Confidence:      {result['confidence']:.2%}")

    if result.get("language") and result["language"] != "unknown":
        print(f"Detected Lang:   {result['language']}")

    # Try to read the file with detected encoding to verify
    if result["encoding"]:
        try:
            with open(file_path, "r", encoding=result["encoding"]) as f:
                first_line = f.readline()
                print(f"\nFirst line preview (with {result['encoding']} encoding):")
                print(
                    f"  {first_line[:100]}..."
                    if len(first_line) > 100
                    else f"  {first_line}"
                )
        except Exception as e:
            print(f"\nNote: Could not read file with detected encoding: {e}")


if __name__ == "__main__":
    main()
