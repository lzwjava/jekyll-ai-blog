---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding Python's -m Flag
translated: false
type: note
---

**Question:** How does the `-m` flag work in Python?

**Answer:**

## What `-m` does

`python -m <module>` tells Python to **locate and execute a module as a script**, rather than running a file directly.

## The mechanics

When you run:

```bash
python -m black myfile.py
```

Python does this:

1. **Search for the module** in `sys.path` (PYTHONPATH + site-packages + stdlib)
2. **Find `black/__main__.py`** or `black.py` in the package
3. **Execute it as `__main__`** (set `__name__ = "__main__"`)
4. **Pass remaining args** (`myfile.py`) as `sys.argv[1:]`

## How Python finds modules

```bash
# Python searches these locations in order:
python -c "import sys; print('\n'.join(sys.path))"
```

Output on typical system:

```
/current/working/directory
/usr/lib/python3.11
/usr/lib/python3.11/lib-dynload
/home/user/.local/lib/python3.11/site-packages
/usr/local/lib/python3.11/dist-packages
```

## How `-m` differs from direct execution

```bash
# ❌ Direct execution (looks for file on disk)
python black.py myfile.py
# Error: No such file or directory (unless black.py is in current dir)

# ✅ Module execution (searches sys.path)
python -m black myfile.py
# Works! Finds black in site-packages/black/__main__.py
```

## Inside a package: `__main__.py`

For a package to be executable with `-m`, it needs this structure:

```
black/
├── __init__.py
├── __main__.py      # ← This gets executed
├── core.py
└── ...
```

`__main__.py`:

```python
import sys
from black import main

if __name__ == "__main__":
    sys.exit(main())
```

When you run `python -m black`, Python:

1. Imports the `black` package
2. Finds `black/__main__.py`
3. Executes it with `__name__ == "__main__"`

## Single-file modules

For a single `.py` file module (not a package):

```bash
python -m json.tool input.json   # Executes /path/to/json/tool.py
```

Python finds `json/tool.py` in stdlib and runs it.

## Why `-m` is useful

```bash
# ❌ Hard to remember: where is pip actually installed?
C:\path\to\Scripts\pip.exe install requests

# ✅ Always works: Python knows where pip is
python -m pip install requests

# ❌ Brittle: depends on your PATH
pytest tests/

# ✅ Reliable: uses installed pytest in current environment
python -m pytest tests/
```

## Practical example: build your own CLI

Create a package:

```
myapp/
├── __init__.py
├── __main__.py
└── cli.py
```

`__main__.py`:

```python
import sys
from myapp.cli import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

`cli.py`:

```python
def main(args):
    print(f"Running with args: {args}")
    return 0
```

Now run it:

```bash
python -m myapp arg1 arg2
# Output: Running with args: ['arg1', 'arg2']
```

## Under the hood (simplified)

```python
# This is roughly what python -m does internally:
import sys
import runpy

module_name = "black"
sys.argv = ["black", "myfile.py"]  # Set sys.argv

# Find and execute the module
runpy.run_module(module_name, run_name="__main__", alter_sys=True)
```

The key is `alter_sys=True` — it modifies `sys.argv` and `sys.modules` so the module thinks it's the main entry point.

---

**TL;DR:** `-m` searches `sys.path` for a module, then executes `__main__.py` (or the module itself) with `__name__ == "__main__"`. It's portable, reliable, and doesn't depend on PATH or file locations.
