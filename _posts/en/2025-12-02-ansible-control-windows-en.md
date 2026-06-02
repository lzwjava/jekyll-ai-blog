---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ansible Control Node Windows Limitation Explained
translated: false
type: note
---

Question: Why can't Ansible control node run on Windows, and what role does os.set_blocking have in this?

Answer:

Ansible's control node (the machine from which you run `ansible` or `ansible-playbook`) is **not supported on Windows** for fundamental technical reasons related to Python's behavior and Unix/POSIX assumptions in Ansible's core code. The most commonly cited specific blocker is the use of low-level file descriptor functions like `os.set_blocking()`.

### Key Reasons Why Windows Is Not Supported

1. **os.set_blocking() is Unix-only**
   In several places (especially in Ansible's connection plugins and process handling), Ansible calls:

   ```python
   os.set_blocking(fd, False)   # to make a pipe or socket non-blocking
   ```

   This function **does not exist on Windows** — it is a POSIX-specific method added in Python 3.5+ only on Unix-like systems. On Windows attempting to call it raises `AttributeError`.
   This is used heavily in Ansible’s `ansible-connection` process and in the `persistent connection` logic.

2. **Heavy reliance on fork()**
   Ansible historically used `os.fork()` extensively (especially before the "strategy" plugins were made fully daemonized). Windows has no native `fork()`, only the limited `subprocess` alternatives, which are much slower and behave differently.

3. **POSIX paths, signals, pseudo-terminals (pty), and /dev/**
   - Many modules expect `/bin/sh`, `/usr/bin/python`, etc.
   - Code uses `os.kill()`, `signal.SIGTERM`, `pty.fork()`, etc.
   - Windows lacks a true `pty` implementation until very recently (Windows 10+ has the "ConPTY" API, but Ansible doesn't use it).

4. **Shebang and executable assumptions**
   Almost all Ansible modules are written with `#!/usr/bin/python` or `#!/bin/bash` shebangs that Windows can't interpret natively.

5. **Windows Subsystem for Linux (WSL) is not officially supported either**
   Even though many people successfully run Ansible inside WSL/WSL2, it is **not officially supported or tested** by Red Hat/Ansible because of subtle differences in process handling, file-descriptor behavior, and occasional deadlocks.

### Current Official Status (as of Ansible 10.x / ansible-core 2.17+ in 2025)

- **Control node**: Linux, macOS, and other Unix-like OSes only
- **Managed nodes**: Windows is fully supported (via WinRM/PowerShell remoting)
- There is **no plan** to make Windows a first-class control node platform because the amount of code that would need rewriting is massive.

### Workarounds People Use

- Run Ansible inside WSL2 (works for most cases today)
- Use a Linux virtual machine or Docker container
- Use Ansible Tower/AWX or the Automation Platform, which run on Linux anyway

In short: the direct technical blocker that causes immediate import/crash errors on Windows is `os.set_blocking()`, but the real reason is much deeper — Ansible was built from the ground up assuming a POSIX environment.

- [Ansible Documentation – Platform Support](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#control-node-requirements)
- [GitHub Issue discussing os.set_blocking on Windows](https://github.com/ansible/ansible/issues/29676)
- [Ansible Connection Framework – set_blocking usage](https://github.com/ansible/ansible/blob/devel/lib/ansible/executor/task_executor.py)
