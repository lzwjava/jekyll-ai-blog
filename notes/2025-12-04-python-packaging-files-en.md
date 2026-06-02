---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Python Packaging Files Explained
translated: false
type: note
---

Question: What are MANIFEST.in and setup.py in Python, and how do they work?

Answer:

In Python, when creating distributable packages (e.g., uploading to PyPI or sharing code), two important files are commonly used with the older **setup.py**-based packaging system (still widely used, though moving toward pyproject.toml):

### 1. **setup.py**
- **Purpose**: This is the build script for your Python package. It tells Python's packaging tools (like `setuptools`) how to install, build, or distribute your project.
- **How it works**: You run commands like:
  ```bash
  python setup.py sdist    # creates a source distribution (tar.gz)
  python setup.py bdist_wheel  # creates a wheel (.whl)
  python setup.py install   # installs the package locally
  ```
- **Common contents** (example):
  ```python
  from setuptools import setup, find_packages

  setup(
      name="my-awesome-package",
      version="1.0.0",
      author="Your Name",
      author_email="you@example.com",
      description="A short description",
      packages=find_packages(),  # automatically finds packages with __init__.py
      install_requires=[
          "requests>=2.25",
          "numpy",
      ],
      python_requires=">=3.8",
      entry_points={
          "console_scripts": [
              "mycommand=my_package.cli:main",
          ]
      },
  )
  ```
- This file is executed as a Python script when building or installing the package.

### 2. **MANIFEST.in**
- **Purpose**: Controls which **additional files** (not Python code) get included in the source distribution (`sdist`) created by `setup.py sdist`.
- By default, `setuptools` includes:
  - All `.py` files
  - `setup.py`, `pyproject.toml`, etc.
- But it **does NOT automatically include** things like:
  - README.md, LICENSE, data files, templates, docs, tests, etc.
- **MANIFEST.in** fixes that.

- **How it works**: It's a simple text file with declarative commands (one per line).

- **Common examples** (`MANIFEST.in`):
  ```text
  include README.md
  include LICENSE
  include requirements.txt
  recursive-include src *.txt *.json
  recursive-include docs *
  include tests/*
  graft data_files          # include entire directory
  global-exclude *.pyc      # exclude all .pyc files
  global-exclude __pycache__
  ```

- When you run `python setup.py sdist`, `setuptools`:
  1. Reads `MANIFEST.in`
  2. Generates a `MANIFEST` file listing all files to include
  3. Creates the `.tar.gz` with exactly those files

### Summary of How They Work Together

| Step                        | File Used         | Result |
|-----------------------------|-------------------|--------|
| Define package metadata & dependencies | `setup.py`        | Required for install/build |
| Specify non-Python files to include in source tarball | `MANIFEST.in`     | Only affects `sdist` (source distribution) |
| Build a source distribution | `python setup.py sdist` | Uses both files |

### Modern Alternative (Recommended since 2020+)
Use `pyproject.toml` + `setuptools` declarative config instead of `setup.py` and `MANIFEST.in`:
```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
# ... metadata ...

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
"my_package" = ["*.txt", "data/*.json"]
```

This avoids `MANIFEST.in` entirely and makes packaging cleaner.

**In short**:
- `setup.py` → the brain of your package (metadata, dependencies, build logic)
- `MANIFEST.in` → the packing list for extra files in source distributions

Both are still common in legacy projects, but new projects should prefer `pyproject.toml`.
