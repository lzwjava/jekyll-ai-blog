---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Python Glob Module File Matching Guide
translated: false
type: note
---

### Importing Glob
To use glob in Python, import the module from the standard library:
```python
import glob
```

### Basic Functionality
The `glob.glob()` function takes a pattern string and returns a list of matching file or directory paths. It uses Unix shell-style wildcards:

- `*`: Matches any sequence of characters (except path separators).
- `?`: Matches any single character.
- `[seq]`: Matches any character in seq (e.g., `[0-9]` for digits).
- `**`: Matches directories recursively (requires `recursive=True`).

Patterns are relative to the current directory unless an absolute path is specified.

### Usage Examples

#### 1. Find all .txt files in the current directory
```python
import glob

files = glob.glob("*.txt")
print(files)  # Output: ['file1.txt', 'file2.txt', ...]
```

#### 2. Find files with specific extensions in a subdirectory
```python
files = glob.glob("documents/*.pdf")
print(files)  # Output: ['documents/doc1.pdf', ...]
```

#### 3. Match specific patterns (e.g., files starting with 'log' and ending with numbers)
```python
files = glob.glob("log[0-9].txt")
print(files)  # Output: ['log1.txt', 'log2.txt', ...] if such files exist
```

#### 4. Recursive search in subdirectories
Use `**` with `recursive=True` to search directories and subdirectories:
```python
files = glob.glob("**/*.py", recursive=True)
print(files)  # Output: ['script1.py', 'subdir/script2.py', ...]
```

### Important Notes
- Results are unsorted by default; use `sorted()` if you need order: `sorted(glob.glob("*.txt"))`.
- For case-insensitive matching on case-sensitive filesystems, consider combining with `fnmatch` or handling in code, as glob is case-sensitive.
- Glob doesn't follow symbolic links unless explicitly handled; use `os.walk()` for more complex traversals.
- For one match at a time, use `glob.iglob()` which returns an iterator to save memory on large results: `for file in glob.iglob("*.txt"): print(file)`.

This covers the essentials; refer to the [Python documentation](https://docs.python.org/3/library/glob.html) for more details.
