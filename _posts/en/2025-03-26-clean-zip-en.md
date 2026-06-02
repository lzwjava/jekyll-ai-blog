---
audio: false
generated: true
lang: en
layout: post
title: Clean Zip File
translated: false
type: note
---

1. **Reads a ZIP file** using `zipfile.ZipFile` and gets a list of all files inside.
2. **Filters out files without extensions**, while keeping directories (entries ending with `/`).
3. **Logs the removed files** to let the user know which ones were excluded.
4. **Creates a new ZIP file** with only valid files (those with extensions or directories).
5. **Uses `argparse` to accept a ZIP file path** as a command-line argument.

This ensures only proper files remain while preserving directory structures. 🚀

```python
import zipfile
import os
import argparse

def clean_zip(zip_path):
    output_path = os.path.splitext(zip_path)[0] + "_output.zip"

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_names = zip_ref.namelist()

        # Separate valid files and files without extensions (excluding directories)
        valid_files = [f for f in file_names if os.path.splitext(os.path.basename(f))[1] or f.endswith('/')]
        removed_files = [f for f in file_names if not os.path.splitext(os.path.basename(f))[1] and not f.endswith('/')]

        if not valid_files:
            print("No valid files with extensions found. Exiting.")
            return

        # Log removed files
        if removed_files:
            print("Removing the following files (no extensions detected):")
            for f in removed_files:
                print(f" - {f}")

        # Create a new zip file excluding invalid files
        with zipfile.ZipFile(output_path, 'w') as clean_zip:
            for file in valid_files:
                with zip_ref.open(file) as source:
                    clean_zip.writestr(file, source.read())

    print(f"Cleaned ZIP file created: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean a ZIP file by removing files without extensions.")
    parser.add_argument("zip_path", help="Path to the input ZIP file")
    args = parser.parse_args()
    clean_zip(args.zip_path)

```
