---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Black Missing Packaging Dependency
translated: false
type: note
---

**Question:** Why does running `python -m black scripts` fail with "ModuleNotFoundError: No module named 'packaging'" even though black is installed?

**Answer:**

The error occurs because the **black** package is installed, but one of its **dependencies** — the `packaging` library — is missing in your current Python environment.

This is the most common situation when:

- black was installed with `--no-deps` (intentionally or by some tool/script)
- the environment was partially corrupted / cleaned
- black was installed via some unusual method (e.g. `python -m pip install --no-deps black`)
- you are using a very new Python version (like Python 3.14 in your case) and some system/site-packages state became inconsistent
- you have multiple Python installations and black is in one but dependencies are missing in the interpreter you're actually using

### Quick fix (recommended)

```bash
# Reinstall black + all its dependencies
python -m pip install --force-reinstall black

# or the even cleaner version:
python -m pip uninstall black -y
python -m pip install black
```

Most people solve the problem with one of these two commands.

### Alternative fixes

1. Install the missing package manually (quick & dirty)

```bash
python -m pip install packaging
```

→ then try `python -m black scripts` again

2. If you suspect environment confusion / wrong python

```bash
# Check which python & pip you're actually using
which python
which pip
python --version
pip --version

# Make sure they match, otherwise use the full path:
python3.14 -m pip install --force-reinstall black
```

3. If you're in a virtual environment but forgot to activate it

```bash
source .venv/bin/activate          # macOS/Linux
# or
.\.venv\Scripts\activate           # Windows
```

then run `python -m pip install black` again.

### Summary – most likely causes & solutions

| Situation                              | Most likely fix                                 |
|----------------------------------------|--------------------------------------------------|
| Missing dependency                     | `pip install packaging` or reinstall black      |
| Corrupted / incomplete install         | `pip install --force-reinstall black`           |
| Wrong Python interpreter               | Use `python3.14 -m pip install black`           |
| Virtualenv not activated               | Activate venv first                             |
| Installed with `--no-deps`             | Reinstall without that flag                     |

In 95% of cases on macOS/homebrew + recent Python, just running

```bash
python -m pip install --force-reinstall black
```

resolves the issue.

Try that first and let me know if it still fails.
