---
audio: false
generated: true
image: false
lang: en
layout: post
title: Linux Python Installations Inventory
translated: false
type: note
---

This is actually a **Linux** machine (Linuxbrew, not macOS Homebrew). Here's the inventory:

## Distinct Python installations (6)

| # | Version | Location | Source |
| --- | --------- | ---------- | -------- |
| 1 | **3.14.3** | `/home/linuxbrew/.linuxbrew/bin/python3.14` | Linuxbrew (`python@3.14` Cellar) |
| 2 | **3.13.13** | `/home/lzw/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu` | uv-managed |
| 3 | **3.12.11** | `/home/lzw/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu` | uv-managed |
| 4 | **3.12.3** | `/usr/bin/python3.12` | System (Debian/Ubuntu apt) |
| 5 | **3.11.0rc1** | `/usr/bin/python3.11` | System (apt, a release candidate) |
| 6 | **3.10.20** | `/home/lzw/.local/share/uv/python/cpython-3.10-linux-x86_64-gnu` | uv-managed |

## Virtual environments (8)

- `/home/lzw/sglang-env` → 3.12.3 (your sglang env)
- `/home/lzw/sglang-venv` → 3.11.0rc1
- `/home/lzw/projects/flux2/.venv` → 3.12.3
- `/home/lzw/projects/jekyll-ai-blog/.venv` → 3.14.3
- `/home/lzw/projects/whisper-playground/.venv` → 3.11.0rc1
- `/home/lzw/projects/ww/.venv` → 3.11.0rc1
- `/home/lzw/ww/.venv` → 3.12.3
- `/home/lzw/.hermes/hermes-agent/venv` → 3.11.0rc1

## Also present

- **uv** (`/home/lzw/.local/bin/uv`) with several more versions available to download on demand (3.15.0b1, 3.14.5, 3.13.13+freethreaded, 3.12.13, 3.11.15, 3.9.x, 3.8.x, PyPy, GraalPy)
- **Pre-commit caches** (~10 throwaway `py_env-python3.14` copies in `~/.cache/pre-commit`)
- **uv build/archive caches** (temporary 3.11/3.12/3.13 copies in `~/.cache/uv`)
- No conda, pyenv, or mamba

**Summary: 6 real installs + 8 venvs** (the venvs reuse the 6 base installs, so they're not separate pythons). Note the current `python3` on PATH is Linuxbrew 3.14.3, and the default `uv python` is 3.13.13.
