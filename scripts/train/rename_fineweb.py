#!/usr/bin/env python3
import os
import glob


def rename_fineweb_files():
    """Rename FineWeb parquet files to remove ?download=true suffix"""

    target_dir = "fineweb_test_dump"

    if not os.path.exists(target_dir):
        print(f"Directory {target_dir} does not exist!")
        return

    # Get all parquet files in the directory
    pattern = os.path.join(target_dir, "*.parquet*")
    files = glob.glob(pattern)

    renamed_count = 0

    for file_path in files:
        filename = os.path.basename(file_path)

        # Check if filename ends with ?download=true
        if filename.endswith("?download=true"):
            # Remove the ?download=true suffix
            new_filename = filename.replace("?download=true", "")
            new_path = os.path.join(target_dir, new_filename)

            # Rename the file
            try:
                os.rename(file_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
                renamed_count += 1
            except OSError as e:
                print(f"Error renaming {filename}: {e}")

    print(f"\nCompleted! Renamed {renamed_count} files.")


if __name__ == "__main__":
    rename_fineweb_files()
