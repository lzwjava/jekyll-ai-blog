---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Python Version Mismatch Issue
translated: false
type: note
---

Got it — you’re running into a **Python version mismatch** issue.

Your logs show:

* `python3` → **3.10.12**
* `python` → **3.13.7**

So when Claude Code (or your research agent script) invokes `python3`, it uses 3.10, which doesn’t have `pyperclip` installed. You installed `pyperclip` into 3.13’s environment instead, so 3.10 can’t see it.

Here are some ways to fix it:

---

### 1. Run Claude Code with the Python you want

If you want Claude Code to always use Python 3.13, explicitly set the executable in your shell:

```bash
export PYTHON_EXECUTABLE=$(which python)
```

Or if you want `python3` specifically:

```bash
export PYTHON_EXECUTABLE=$(which python3)
```

Then when starting Claude Code or your agent, it can read that env var.

---

### 2. Point `python3` to Python 3.13

On Ubuntu you can update the `alternatives` system:

```bash
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 2
sudo update-alternatives --config python3
```

Then choose Python 3.13.

---

### 3. Install `pyperclip` into Python 3.10

If you want to keep using 3.10 for `python3`, just install there:

```bash
python3 -m pip install --user pyperclip
```

This ensures `python3` can import it.

---

### 4. Use a virtual environment

Best practice: create a venv with the Python you want and run Claude Code inside it:

```bash
python3.13 -m venv ~/.venvs/claude
source ~/.venvs/claude/bin/activate
pip install pyperclip
```

Then launch your agent inside this venv, so it always uses 3.13.

---

👉 Question for you: do you want Claude Code to **always run with Python 3.13**, or are you fine keeping 3.10 as `python3` but just fixing the missing module?
