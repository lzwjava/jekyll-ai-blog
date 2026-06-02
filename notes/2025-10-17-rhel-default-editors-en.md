---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Default Text Editors in RHEL Minimal
translated: false
type: note
---

In Red Hat Enterprise Linux (RHEL), particularly in a minimal installation (the default for servers and lightweight setups), the only text editor available out of the box is **vi**, provided by the `vim-minimal` package. This gives you a basic, compatible implementation of the classic `vi` command for editing files in the terminal.

- **Full `vim`** (the enhanced version with more features, syntax highlighting, etc.) is not installed by default. You can add it with `sudo dnf install vim-enhanced`.
- **Nano** and **Emacs** are not included in the minimal install. They are available in the repositories but require explicit installation:
  - For Nano: `sudo dnf install nano`
  - For Emacs: `sudo dnf install emacs`

This keeps the minimal install lean (around 200-300 packages total) to prioritize security and performance. If you're doing a full desktop or server install (not minimal), more tools might be pulled in depending on the selected environment.

[Getting started with Nano (Red Hat)](https://www.redhat.com/en/blog/getting-started-nano)
[Why RHEL has two vim installed by default?](https://unix.stackexchange.com/questions/699071/why-rhel-has-two-vim-installed-by-default)
[RHEL 9 Package Manifest](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html-single/package_manifest/index)
