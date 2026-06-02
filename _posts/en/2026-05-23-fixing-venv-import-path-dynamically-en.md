---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing venv import path dynamically
translated: false
type: note
---

Here's a comprehensive summary of the fix:

## Problem

The `/note` command was failing with:
```
'ww' package not installed. Install with: pip install -e ~/projects/ww
```

## Root Cause

Hermes Agent runs in its own isolated Python virtual environment at `~/.hermes/hermes-agent/venv/`. The `ww` package was installed in the system Python (`/opt/homebrew/bin/python3.11`) but **not** in Hermes' venv. When the plugin tried to `from ww.note.create_note_from_clipboard import create_note_from_content`, it failed because:

1. `ww` wasn't in the venv's `site-packages`
2. Even if we installed it with `pip install -e ~/projects/ww`, the `pyperclip` dependency was also missing

## Solution (Two Parts)

### Part 1: Plugin Code Change (`~/.hermes/plugins/note/__init__.py`)

**Before:**
```python
try:
    from ww.note.create_note_from_clipboard import create_note_from_content
except ImportError:
    return "'ww' package not installed. Install with: pip install -e ~/projects/ww"
```

**After:**
```python
try:
    from ww.note.create_note_from_clipboard import create_note_from_content
except ImportError:
    # Add ww project to path if not installed in current venv
    import sys
    ww_path = str(Path.home() / "projects" / "ww")
    if ww_path not in sys.path:
        sys.path.insert(0, ww_path)
    try:
        from ww.note.create_note_from_clipboard import create_note_from_content
    except ImportError:
        return "'ww' package not installed. Install with: pip install -e ~/projects/ww"
```

**Why this works:**
- Instead of requiring `ww` to be pip-installed in every Python environment, the plugin now dynamically adds the source directory to `sys.path`
- This allows importing directly from the source tree at `~/projects/ww/`
- The fallback error message is preserved if the source directory doesn't exist

### Part 2: Installed Missing Dependency

```bash
~/.hermes/hermes-agent/venv/bin/python -m ensurepip
~/.hermes/hermes-agent/venv/bin/python -m pip install pyperclip
```

**Why this was needed:**
- `ww` depends on `pyperclip` for clipboard operations
- Even with the source directory in `sys.path`, the import chain fails if dependencies aren't installed
- `pyperclip` was installed in the system Python but not in Hermes' venv

## Verification

```bash
~/.hermes/hermes-agent/venv/bin/python -c "
import sys
from pathlib import Path
ww_path = str(Path.home() / 'projects' / 'ww')
if ww_path not in sys.path:
    sys.path.insert(0, ww_path)
from ww.note.create_note_from_clipboard import create_note_from_content
print('Import successful!')
"
# Output: Import successful!
```

## Key Insight

Hermes plugins run inside Hermes' isolated venv, not the system Python. When a plugin depends on local packages (like `ww`), you have two options:

1. **Install in the venv** — `~/.hermes/hermes-agent/venv/bin/pip install -e ~/projects/ww` (requires all dependencies)
2. **Add to sys.path** — dynamically inject the source directory (what we did)

Option 2 is more robust because it doesn't require pip-installing the package and its dependencies in every environment.
