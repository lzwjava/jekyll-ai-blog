---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Triton Python 安装摘要
translated: true
type: note
---

以下是所有安装了 **triton** 包的 Python 环境的完整汇总：

## 系统 Python

| Python 版本 | triton 版本 | 位置 |
| -------- | --------------- | ---------- |
| `/usr/bin/python3.11` | **3.6.0** | `~/.local/lib/python3.11/site-packages` |
| `/usr/bin/python3.12` | **3.6.0** | `~/.local/lib/python3.12/site-packages` |
| `/usr/bin/python3` (→3.12) | **3.6.0** | `~/.local/lib/python3.12/site-packages` |
| Homebrew `python3` (3.14) | **3.6.0** | `~/.local/lib/python3.14/site-packages` |

## 虚拟环境

| 环境 | triton 版本 | 位置 |
| ----- | --------------- | ---------- |
| `/home/lzw/sglang-env` | **3.3.1** | `sglang-env/lib/python3.12/site-packages` |
| `/home/lzw/sglang-venv` | **3.6.0** | `sglang-venv/lib/python3.11/site-packages` |
| `/home/lzw/ww/.venv` | ❌ **未安装** | — |

## uv 管理的 Python（`~/.local/share/uv/python/`）

| Python 版本 | triton 版本 |
| -------- | --------------- |
| cpython-3.10.x | **2.0.0** |
| cpython-3.11.x | **3.6.0** |
| cpython-3.12.x | **3.6.0** |
| cpython-3.13.x | **3.3.1** |

**值得注意的是：** triton 3.6.0 是分布最广的版本。唯一没有安装它的 Python 环境是 `ww/.venv`，而 uv 构建的 3.10 版本仍搭载着旧的 2.0.0 版本。
