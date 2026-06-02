---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Python Package Import Extractor
translated: false
type: note
---

### Python Script to Extract All Imported Packages

This script walks through a specified directory and its subdirectories, finds all Python files (`.py`), parses their import statements using Python's `ast` module (for safe, syntax-aware parsing), and accumulates all unique base module names (e.g., `os` from `import os`, or `collections` from `from collections import defaultdict`). It ignores builtins and focuses on external modules.

Save this as a `.py` file (e.g., `extract_imports.py`) and run it with a directory path as an argument, like `python extract_imports.py /path/to/directory`.

```python
import os
import ast
import sys

def extract_imports_from_file(file_path):
    """
    Parses a Python file and extracts imported module names.
    Handles 'import mod' and 'from mod import item' styles.
    """
    modules = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    modules.add(alias.name.split('.')[0])  # Get base module (e.g., 'import os.path' -> 'os')
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split('.')[0])  # Get base module from 'from mod.sub import ...'
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

    return modules

def get_all_imported_modules(directory):
    """
    Walks through the directory and subdirectories, collects all unique imported modules.
    """
    all_modules = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                modules = extract_imports_from_file(file_path)
                all_modules.update(modules)

    # Exclude common builtins (optional, as they are rarely external packages)
    excluded = {'sys', 'os', 're', 'math', 'random', 'json', 'time', 'datetime', 'collections', 'itertools', 'functools'}
    all_modules -= excluded

    return sorted(all_modules)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_imports.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    modules = get_all_imported_modules(directory)
    print("All unique imported packages:")
    for mod in modules:
        print(mod)
```

### How It Works

- **Directory Traversal**: Uses `os.walk` to recursively visit all subdirectories and files.
- **File Filtering**: Only processes `.py` files.
- **Import Parsing**: Employs `ast` to safely parse source code and identify `Import` and `ImportFrom` nodes. Splits on `.` to capture the top-level module (e.g., `numpy` from `import numpy.linalg`).
- **Accumulation**: Collects modules in a set for uniqueness, then sorts and prints them.
- **Edge Cases**: Skips builtins (you can customize the `excluded` set), handles syntax errors gracefully, and supports Unicode files.
- **Output**: A sorted list of unique package names. If run on your own project's directory, it will list packages like `requests`, `pandas`, etc., that you'd need to install.

This approach is efficient for codebase analysis and avoids executing potentially unsafe code. If you need refinements (e.g., handling relative imports differently or generating a requirements.txt), provide more details!
