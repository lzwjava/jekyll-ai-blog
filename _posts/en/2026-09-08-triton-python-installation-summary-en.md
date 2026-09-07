---
audio: false
generated: true
image: false
lang: en
layout: post
title: Triton Python Installation Summary
translated: false
type: note
---

Here's a full summary of which Python installations have the **triton** package:

## System Pythons

| Python | triton version | Location |
|--------|---------------|----------|
| `/usr/bin/python3.11` | **3.6.0** | `~/.local/lib/python3.11/site-packages` |
| `/usr/bin/python3.12` | **3.6.0** | `~/.local/lib/python3.12/site-packages` |
| `/usr/bin/python3` (→3.12) | **3.6.0** | `~/.local/lib/python3.12/site-packages` |
| Homebrew `python3` (3.14) | **3.6.0** | `~/.local/lib/python3.14/site-packages` |

## Virtualenvs

| Env | triton version | Location |
|-----|---------------|----------|
| `/home/lzw/sglang-env` | **3.3.1** | `sglang-env/lib/python3.12/site-packages` |
| `/home/lzw/sglang-venv` | **3.6.0** | `sglang-venv/lib/python3.11/site-packages` |
| `/home/lzw/ww/.venv` | ❌ **not installed** | — |

## uv-managed pythons (`~/.local/share/uv/python/`)

| Python | triton version |
|--------|---------------|
| cpython-3.10.x | **2.0.0** |
| cpython-3.11.x | **3.6.0** |
| cpython-3.12.x | **3.6.0** |
| cpython-3.13.x | **3.3.1** |

**Notable:** triton 3.6.0 is the most widespread version. The only Python without it is `ww/.venv`, and 3.10 uv-builds carry the old 2.0.0.