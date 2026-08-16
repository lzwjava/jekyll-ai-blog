---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux Python安装清单
translated: true
type: note
---

这实际上是一台 **Linux** 机器（使用 Linuxbrew，而非 macOS 的 Homebrew）。以下是详细清单：

## 不同的 Python 安装版本（共 6 个）

| # | 版本 | 位置 | 来源 |
|---|---------|----------|--------|
| 1 | **3.14.3** | `/home/linuxbrew/.linuxbrew/bin/python3.14` | Linuxbrew（`python@3.14` Cellar） |
| 2 | **3.13.13** | `/home/lzw/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu` | uv 管理 |
| 3 | **3.12.11** | `/home/lzw/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu` | uv 管理 |
| 4 | **3.12.3** | `/usr/bin/python3.12` | 系统（Debian/Ubuntu apt） |
| 5 | **3.11.0rc1** | `/usr/bin/python3.11` | 系统（apt，候选发布版） |
| 6 | **3.10.20** | `/home/lzw/.local/share/uv/python/cpython-3.10-linux-x86_64-gnu` | uv 管理 |

## 虚拟环境（共 8 个）

- `/home/lzw/sglang-env` → 3.12.3（你的 sglang 环境）
- `/home/lzw/sglang-venv` → 3.11.0rc1
- `/home/lzw/projects/flux2/.venv` → 3.12.3
- `/home/lzw/projects/jekyll-ai-blog/.venv` → 3.14.3
- `/home/lzw/projects/whisper-playground/.venv` → 3.11.0rc1
- `/home/lzw/projects/ww/.venv` → 3.11.0rc1
- `/home/lzw/ww/.venv` → 3.12.3
- `/home/lzw/.hermes/hermes-agent/venv` → 3.11.0rc1

## 其他已存在内容
- **uv**（`/home/lzw/.local/bin/uv`）可按需下载多个版本（3.15.0b1、3.14.5、3.13.13+freethreaded、3.12.13、3.11.15、3.9.x、3.8.x、PyPy、GraalPy）
- **Pre-commit 缓存**（`~/.cache/pre-commit` 中约 10 个废弃的 `py_env-python3.14` 副本）
- **uv 构建/归档缓存**（`~/.cache/uv` 中 3.11/3.12/3.13 的临时副本）
- 无 conda、pyenv 或 mamba

**总结：6 个实际安装版本 + 8 个虚拟环境**（虚拟环境复用了 6 个基础安装版本，因此并非独立的 Python）。注意，当前 PATH 上的 `python3` 指向 Linuxbrew 的 3.14.3，而默认 `uv python` 版本为 3.13.13。