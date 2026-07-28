---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python 3.11 Recommended for nano-vllm
translated: false
type: note
---

For this project (**nano-vllm**), the `pyproject.toml` defines:

```toml
requires-python = ">=3.10,<3.13"
```

So valid choices are **Python 3.10**, **3.11**, or **3.12**.

### Recommendation: **Python 3.11**

Here's why:

| Factor | 3.11 | 3.12 |
|---|---|---|
| **triton support** ✅ | Excellent, widely tested | Good, but some edge cases historically |
| **torch compatibility** ✅ | Fully supported | Supported |
| **CUDA graph stability** ✅ | Most battle-tested | Fine, but newer |
| **Package ecosystem** ✅ | Maximum compatibility for ML | Some packages were late to support |

Since this project depends on `triton>=3.0.0` and `torch>=2.4.0` and uses **CUDA graphs** + **tensor parallelism** (GPU-centric ML), **Python 3.11** is the safest, most battle-tested choice.

### How to set it in Zed

1. Open Command Palette (`Cmd+Shift+P`)
2. Run **"Zed: Select Python Environment"**
3. Choose your **Python 3.11** interpreter

Or create a `.python-version` file at the project root:

```bash
echo "3.11" > /mnt/data/nano-vllm/.python-version
```

Then select that venv/interpreter in Zed.