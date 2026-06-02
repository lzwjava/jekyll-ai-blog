---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Zed vs VS Code: One-Eighth RAM Usage"
translated: false
type: note
---

Same project (`jekyll-ai-blog`), fresh comparison:

## Zed vs VS Code

| Metric | Zed | VS Code |
|---|---|---|
| **Processes** | **2** | **16** |
| **Total RAM** | **3,148 MB** (3 GB) | **24,190 MB** (24 GB) |
| RAM per process | 1.5 GB avg | 1.5 GB avg |
| Main window | 2.9 GB | 7.0 GB |
| **Snapshot** | Lightweight, native (Rust) | Electron-based, heavy |

**Zed uses 1/8th the RAM** of VS Code for the exact same project directory.

The difference is architectural:
- **Zed** is native (Rust/GPUI) — minimal overhead, only 2 processes
- **VS Code** is Electron (Chromium + Node) — each helper is a sandboxed process, 16 total

If you keep using Zed for lightweight editing on this laptop and save VS Code for your remote machine, you'll save ~20 GB of memory every time you code.
