---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python 3.11 Safe to Delete
translated: false
type: note
---

Here's the analysis:

---

**`/usr/local/bin/python3` (Python 3.11.6) — SAFE TO DELETE**

This is from the python.org installer (the "Framework" build). You have:

- Homebrew's own `python@3.11` (3.11.14) at `/opt/homebrew/bin/python3.11`
- All Homebrew scripts shebang to `/opt/homebrew/opt/python@3.11/...`, not this one
- It has 41 pip packages installed, but those are likely duplicated by Homebrew or your venvs

The official uninstall procedure:

```bash
# 1. Remove the framework
sudo rm -rf /Library/Frameworks/Python.framework/Versions/3.11

# 2. Remove symlinks in /usr/local/bin
sudo rm -f /usr/local/bin/python3.11 /usr/local/bin/python3
sudo rm -f /usr/local/bin/python3.11-config /usr/local/bin/python3-config
sudo rm -f /usr/local/bin/python3.11-intel64 /usr/local/bin/python3-intel64
sudo rm -f /usr/local/bin/pip3.11 /usr/local/bin/pip3
sudo rm -f /usr/local/bin/easy_install-3.11 /usr/local/bin/idle3.11
sudo rm -f /usr/local/bin/pydoc3.11 /usr/local/bin/2to3-3.11

# 3. Remove the Applications folder
sudo rm -rf "/Applications/Python 3.11"
```

---

**`/usr/bin/python3` (Python 3.9.6) — DO NOT DELETE**

This is the **macOS system Python** bundled with Xcode Command Line Tools. It lives under SIP (System Integrity Protection) at `/usr/bin/`, which means:

- macOS protects it — you can't delete it without disabling SIP
- Xcode and some Apple dev tools depend on it
- It's harmless — it sits at the bottom of your PATH and never wins against Homebrew

Leave it alone.
