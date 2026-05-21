---
audio: false
generated: true
image: false
lang: en
layout: post
title: VSCode Extension Cleanup Summary
translated: false
type: note
---

All 10 removed. Cleanup summary:

| Removed | Status |
|---|---|
| `tomoki1207.pdf` — PDF viewer | Gone |
| `yzane.markdown-pdf` — PDF export | Gone |
| `xdebug.php-pack` — PHP | Gone |
| `torn4dom4n.latex-support` — LaTeX | Gone |
| `moozzyk.arduino` — Arduino | Gone |
| `mcu-debug.*` (3 MCU debuggers) | Gone |
| `redhat.fabric8-analytics` | Gone |
| `azemoh.one-monokai` — duplicate theme | Gone |
| `vadimcn.vscode-lldb` (7 old versions) | Gone earlier |
| **Total: 59 → 42 extension directories** | **17 removed** |

The **biggest remaining win** is closing the extra VSCode windows. You have **12 open** right now. Each one spawns ~5 helper processes. If you close 10 of them, VSCode drops from ~23 GB to ~3-4 GB instantly.

`Cmd+Q` the ones you're not editing on this laptop (save the heavy coding for the remote machine).