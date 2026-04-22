import os


def count_files(directory, extensions, exclude_dirs=None, since_mtime=None):
    count = 0
    if exclude_dirs is None:
        exclude_dirs = []
    try:
        if not os.path.exists(directory):
            return 0
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path) and any(
                item.endswith(ext) for ext in extensions
            ):
                if since_mtime is None or os.path.getmtime(item_path) >= since_mtime:
                    count += 1
            elif os.path.isdir(item_path) and item not in exclude_dirs:
                count += count_files(item_path, extensions, exclude_dirs, since_mtime)
    except (PermissionError, FileNotFoundError):
        pass
    return count


def count_lang_files():
    base_dir = "./"  # Go up one level from count/ to the root of the repo

    # Count Python files in scripts directory (excluding ml subdirectory)
    scripts_dir = os.path.join(base_dir, "scripts")
    py_count = count_files(scripts_dir, [".py"], exclude_dirs=["ml"])
    print(f"Number of .py files in scripts directory (excluding ml): {py_count}")

    # Count Python files in scripts/ml directory
    ml_dir = os.path.join(base_dir, "scripts", "ml")
    ml_count = count_files(ml_dir, [".py"])
    print(f"Number of .py files in scripts/ml directory: {ml_count}")

    # Count C files in c directory
    c_dir = os.path.join(base_dir, "c")
    c_count = count_files(c_dir, [".c", ".h"])
    print(f"Number of C files in c directory: {c_count}")

    # Count Rust files in rust directory
    rust_dir = os.path.join(base_dir, "rust")
    rust_count = count_files(rust_dir, [".rs"])
    print(f"Number of Rust files in rust directory: {rust_count}")

    # Count C++ files in cpp directory
    cpp_dir = os.path.join(base_dir, "cpp")
    cpp_count = count_files(cpp_dir, [".cpp", ".hpp", ".h"])
    print(f"Number of C++ files in cpp directory: {cpp_count}")


if __name__ == "__main__":
    count_lang_files()
