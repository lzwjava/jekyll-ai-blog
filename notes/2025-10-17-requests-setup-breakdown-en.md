---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Requests Setup.py File Breakdown
translated: false
type: note
---

### Overview

This is a `setup.py` file, which is a standard Python script used with `setuptools` to define and build a Python package. Specifically, this one is for the **Requests** library—a popular HTTP client for Python. It handles metadata like the package name, version, dependencies, and classifiers (for PyPI distribution). When you run `pip install requests`, this script (or its built artifacts) is what gets executed behind the scenes to install the package.

The script is structured as a single `setup()` function call, but it includes some guards, helpers, and dynamic reads from other files. I'll break it down section by section.

### 1. Imports and Python Version Check

```python
#!/usr/bin/env python
import os
import sys
from codecs import open

from setuptools import setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 9)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    # Error message and exit
    sys.exit(1)
```

- **Shebang (`#!/usr/bin/env python`)**: Makes the file executable on Unix-like systems, running it with the system's Python interpreter.
- **Imports**: Brings in `os` and `sys` for system interactions, `codecs.open` for UTF-8 file reading (to handle non-ASCII safely), and `setup` from `setuptools` for building the package.
- **Version Check**: Ensures the user is running Python 3.9 or higher. If not, it prints a helpful error message suggesting an upgrade or pinning to an older Requests version (<2.32.0), then exits with code 1 (failure). This enforces compatibility, as Requests dropped support for older Pythons.

### 2. Publish Shortcut

```python
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()
```

- A convenience for maintainers: If you run `python setup.py publish`, it:
  - Builds source distribution (`sdist`) and wheel (`bdist_wheel`) archives in the `dist/` folder.
  - Uploads them to PyPI using `twine` (a secure uploader).
- This is a quick way to release a new version without manual commands. It exits after running.

### 3. Dependencies

```python
requires = [
    "charset_normalizer>=2,<4",
    "idna>=2.5,<4",
    "urllib3>=1.21.1,<3",
    "certifi>=2017.4.17",
]
test_requirements = [
    "pytest-httpbin==2.1.0",
    "pytest-cov",
    "pytest-mock",
    "pytest-xdist",
    "PySocks>=1.5.6, !=1.5.7",
    "pytest>=3",
]
```

- **`requires`**: Core dependencies installed when you `pip install requests`. These handle encoding (`charset_normalizer`), internationalized domain names (`idna`), HTTP transport (`urllib3`), and SSL certificates (`certifi`).
- **`test_requirements`**: Only installed if you run tests (e.g., via `pip install -e '.[tests]'`). Includes testing tools like `pytest` variants for HTTP mocking, coverage, and parallel testing. `PySocks` is for SOCKS proxy support in tests.

### 4. Dynamic Metadata Loading

```python
about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "src", "requests", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()
```

- **`about` dict**: Reads metadata from `src/requests/__version__.py` (e.g., `__title__`, `__version__`, `__description__`, etc.) using `exec()`. This keeps version info centralized—update it once, and `setup.py` pulls it in.
- **`readme`**: Loads the entire `README.md` file as a string for the package's long description on PyPI.

### 5. The Main `setup()` Call

This is the heart of the file. It configures the package for building/installation:

```python
setup(
    name=about["__title__"],  # e.g., "requests"
    version=about["__version__"],  # e.g., "2.32.3"
    description=about["__description__"],  # Short summary
    long_description=readme,  # Full README
    long_description_content_type="text/markdown",  # Renders as Markdown on PyPI
    author=about["__author__"],  # e.g., "Kenneth Reitz"
    author_email=about["__author_email__"],
    url=about["__url__"],  # e.g., GitHub repo
    packages=["requests"],  # Installs the 'requests' package
    package_data={"": ["LICENSE", "NOTICE"]},  # Includes non-Python files
    package_dir={"": "src"},  # Source code is in 'src/'
    include_package_data=True,  # Pulls in all data files
    python_requires=">=3.9",  # Mirrors the version check
    install_requires=requires,  # From earlier
    license=about["__license__"],  # e.g., "Apache 2.0"
    zip_safe=False,  # Allows editing installed files (common for libs)
    classifiers=[  # PyPI categories for discoverability
        "Development Status :: 5 - Production/Stable",
        # ... (full list includes Python versions, OS, topics)
    ],
    tests_require=test_requirements,  # For `pip install -e '.[tests]'`
    extras_require={  # Optional dependencies
        "security": [],  # Empty—maybe for future use
        "socks": ["PySocks>=1.5.6, !=1.5.7"],  # SOCKS proxy support
        "use_chardet_on_py3": ["chardet>=3.0.2,<6"],  # Legacy charset fallback
    },
    project_urls={  # Links on PyPI page
        "Documentation": "https://requests.readthedocs.io",
        "Source": "https://github.com/psf/requests",
    },
)
```

- **Key Args**:
  - **Name/Version/Description**: Pulled from `__version__.py` for easy maintenance.
  - **Packages/Package Dir**: Tells setuptools the package is under `src/requests/` and to install it as `import requests`.
  - **Classifiers**: A list of strings that categorize the package (e.g., stable, Python 3.9+, Apache license, web/HTTP topic). This helps users find it on PyPI.
  - **Extras Require**: Lets users install optional features, like `pip install requests[socks]` for proxy support.
  - **Project URLs**: Adds clickable links to docs and source on the PyPI page.

### How It Works in Practice

- **Installation**: `pip install .` (from the repo) or `pip install requests` (from PyPI) runs this to copy files, install deps, and set up the package.
- **Building**: `python setup.py sdist` creates distributable archives.
- **Why This Structure?** It's a "src layout" (code in `src/`), which is modern best practice to avoid accidental imports during development. The file is self-contained but delegates details to other files like `__version__.py`.

This setup.py is from the official Requests repo and hasn't changed much over versions—it's battle-tested for reliability.

### References

- [Requests Documentation](https://requests.readthedocs.io/en/latest/)
- [Requests GitHub Repository](https://github.com/psf/requests)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
