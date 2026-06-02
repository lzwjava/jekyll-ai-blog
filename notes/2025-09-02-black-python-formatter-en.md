---
audio: false
generated: true
image: false
lang: en
layout: post
title: Black Python Code Formatter Guide
translated: false
type: note
---

The `black` package on PyPI is a **Python code formatter**. It automatically reformats your Python code to follow consistent style rules (PEP 8-compatible, but with its own strict opinions). Here’s how to use it:

---

### 1. Install Black

```bash
pip install black
```

If you want to ensure you always get the latest stable version:

```bash
pip install -U black
```

---

### 2. Format a File or Directory

Run Black on a file:

```bash
black my_script.py
```

Run Black on a whole directory (recursively):

```bash
black src/
```

By default, it will overwrite files in place with formatted code.

---

### 3. Check Formatting Without Changing

Use `--check` to see if your files need reformatting:

```bash
black --check my_script.py
```

This is useful for CI pipelines, to ensure style consistency.

---

### 4. Common Options

* `--line-length 88` → Change line length (default: 88).
* `--diff` → Show what would change, without modifying the file.
* `--skip-string-normalization` → Don’t change string quotes.
* `--exclude` → Skip certain files/folders.

Example:

```bash
black --line-length 100 --diff src/
```

---

### 5. Integration

* **IDE support**: Black is available as a plugin in PyCharm, VS Code, Vim, Emacs, etc.
* **Pre-commit hook**: Add Black to `.pre-commit-config.yaml` so code is formatted before commits:

  ```yaml
  repos:
    - repo: https://github.com/psf/black
      rev: stable
      hooks:
        - id: black
  ```
* **CI/CD**: Add `black --check .` in your CI pipeline.

---

👉 Do you want me to also show how to set up **automatic formatting in VSCode or PyCharm**, so you don’t need to run `black` manually?
