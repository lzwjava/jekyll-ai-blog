---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Adding Executable Scripts to Pip Packages
translated: false
type: note
---

### Creating Executable Scripts in a Python Pip Package

To include executable scripts (i.e., command-line tools) in a Python package that can be installed via `pip`, you define **entry points** in your package's configuration file. This allows users to run your scripts directly after installation (e.g., `my-script` from the terminal).

We'll use a simple example: a package called `mytools` with a script `greet` that prints a greeting.

#### Step 1: Set Up Your Package Structure

Create a directory structure like this:

```
mytools/
├── pyproject.toml          # Modern config file (recommended over setup.py)
├── README.md
└── src/
    └── mytools/
        ├── __init__.py     # Makes it a package
        └── greet.py        # Your script logic
```

In `src/mytools/__init__.py` (can be empty or with version info):

```python
__version__ = "0.1.0"
```

In `src/mytools/greet.py` (the function your script will call):

```python
import sys

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(f"Hello, {name}!")

if __name__ == "__main__":
    main()
```

#### Step 2: Configure Entry Points in `pyproject.toml`

Use the `[project.scripts]` section to define console scripts. This tells pip to create executable wrappers.

```toml
[build-system]
requires = ["hatchling"]  # Or "setuptools", "flit", etc.
build-backend = "hatchling.build"

[project]
name = "mytools"
version = "0.1.0"
description = "A simple tool package"
readme = "README.md"
requires-python = ">=3.8"
dependencies = []  # Add your deps here, e.g., "requests"

[project.scripts]
greet = "mytools.greet:main"  # Format: script_name = package.module:function
```

- `greet` is the command users will run (e.g., `greet Alice`).
- `mytools.greet:main` points to the `main()` function in `greet.py`.

If you prefer the older `setup.py` (still works but less recommended):

```python
from setuptools import setup, find_packages

setup(
    name="mytools",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "greet = mytools.greet:main"
        ]
    },
    # ... other fields like description, install_requires
)
```

#### Step 3: Build and Install the Package

1. Install build tools: `pip install build twine` (or `hatchling` if using that backend).

2. Build the package:

   ```
   python -m build
   ```

   This creates `dist/` with `.tar.gz` and `.whl` files.

3. Install locally to test:

   ```
   pip install -e .  # Editable mode (changes reflect immediately)
   ```

   Or for a clean install: `pip install dist/mytools-0.1.0-py3-none-any.whl`.

4. Test: Run `greet Alice` in your terminal. It should output "Hello, Alice!".

#### Step 4: Distribute (Optional)

- Upload to PyPI: `twine upload dist/*` (requires PyPI account).
- Users can then `pip install mytools` and run `greet`.

#### Tips

- **Multiple scripts**: Add more lines to `[project.scripts]`, e.g., `another-script = mytools.other:main`.
- **Arguments**: Use `argparse` in your `main()` for better CLI handling.
- **Dependencies**: List them in `[project.dependencies]` (e.g., `click` for CLI frameworks).
- **Virtual env**: Always use one (`python -m venv env; source env/bin/activate`) to avoid conflicts.
- **Errors?** Check `pip install --verbose` for details. Ensure your function takes no args (or handles `sys.argv`).

For more advanced setups (e.g., with Poetry or Flit), check the official docs.

#### References

- [Python Packaging User Guide: Entry Points](https://packaging.python.org/en/latest/guides/writing-entry-points/)
- [PyPI: Building and Publishing](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
