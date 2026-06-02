---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Python 3.14 Command Line Essentials
translated: false
type: note
---

This is the help output from Python 3.14, showing all the command-line options available when running Python. Let me break down the most useful parts:

## Common Usage Patterns

**Running Python:**
- `python file.py` - Execute a script
- `python -m module` - Run a module as a script (like `python -m pip install package`)
- `python -c "code"` - Execute a single command
- `python` - Start interactive mode

## Key Options You'll Actually Use

**`-m mod`** - Run a library module as a script. This is how you run tools like pip, venv, or http.server:
```bash
python -m pip install requests
python -m venv myenv
python -m http.server 8000
```

**`-i`** - Inspect interactively after running a script. Great for debugging - your script runs, then drops you into an interactive prompt with all variables still available.

**`-c cmd`** - Execute a one-liner:
```bash
python -c "print('Hello')"
```

**`-u`** - Unbuffered output. Useful when piping Python output or running in Docker so you see prints immediately.

**`-B`** - Don't write `.pyc` files. Keeps your directories clean during development.

**`-I`** - Isolation mode. Ignores environment variables and user site-packages - useful for reproducible environments.

## Optimization Options

**`-O`** - Removes assert statements and `__debug__` checks
**`-OO`** - Also removes docstrings to save memory

## The Proxy Notice

The `🚀 Proxy Settings Detected` at the top isn't from Python itself - it's from your shell environment showing that HTTP/HTTPS traffic is being routed through `127.0.0.1:7890` (likely a VPN or proxy tool).

Most developers use maybe 3-4 of these options regularly. The `-m` flag is probably the most common in everyday use.
