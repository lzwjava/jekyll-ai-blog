---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows pip install location and PATH
translated: false
type: note
---

**Question:** Where does `pip install` place packages on Windows, and how do you configure PATH to run installed commands directly instead of using `python -m`?

**Answer:**

## Where pip installs packages

On Windows, `pip install` places packages in:

```
C:\Users\<USERNAME>\AppData\Local\Programs\Python\Python3xx\Lib\site-packages\
```

Or if you're in a virtual environment:

```
<venv-path>\Lib\site-packages\
```

## Where executable scripts go

When a package installs a CLI tool (like `black`, `pytest`, `numpy`), the **executable** lands in:

```
C:\Users\<USERNAME>\AppData\Local\Programs\Python\Python3xx\Scripts\
```

Or in a venv:

```
<venv-path>\Scripts\
```

## Why you need PATH

By default, Windows doesn't know where `Scripts\` is. You have two options:

### Option 1: Add Python Scripts to system PATH (permanent)

1. Find your Python Scripts path:

```python
import site
import os
print(os.path.dirname(site.PREFIXES[0]))  # Shows Python root
# Then Scripts is at: <root>\Scripts
```

2. Add to system PATH:
   - Win+X → System → Advanced system settings
   - Environment Variables → Edit system PATH
   - Add: `C:\Users\<USERNAME>\AppData\Local\Programs\Python\Python3xx\Scripts`
   - Restart terminal

3. Now run commands directly:

```bash
black myfile.py
pytest
```

### Option 2: Use python -m (always works, no setup)

```bash
python -m pip install black
python -m black myfile.py
python -m pytest
```

This works because `python.exe` is already in PATH, so Python finds the module internally.

## Verify it worked

```bash
where pytest   # Shows the path to pytest executable
pip show -f black  # Shows where package + scripts are installed
```

## Pro tip: Use virtual environments

Stop fighting with system PATH. Use a venv instead:

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # macOS/Linux
pip install black pytest
black .   # Now works directly in the venv context
```

When you activate a venv, its `Scripts\` folder is automatically prepended to PATH for that terminal session.

---

**TL;DR:** `pip` installs to `site-packages\` (the lib storage) and scripts to `Scripts\`. Add `Scripts\` to your system PATH, or use a virtual environment so you don't pollute your system Python.
