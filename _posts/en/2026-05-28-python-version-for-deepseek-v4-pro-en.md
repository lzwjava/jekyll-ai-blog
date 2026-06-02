---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Version for DeepSeek V4-Pro
translated: false
type: note
---

**Question:** What Python version should be used for DeepSeek V4-Pro inference (with `torch>=2.10.0`, `transformers>=5.0.0`, `safetensors>=0.7.0`, `fast_hadamard_transform`, `tilelang==0.1.8`)?

**Answer:**

**Python 3.11** is the sweet spot. Here's the constraint chain:

**The binding constraint is `tilelang==0.1.8`:**

`tilelang` on PyPI requires Python `>=3.9` and explicitly supports 3.9, 3.10, 3.11, 3.12, 3.13, 3.14. Version 0.1.8 was released Feb 16, 2026, well after the Python 3.8 EOL.

v0.1.6.post2 was the last version compatible with Python 3.8, so 0.1.8 drops 3.8 support entirely. That means **Python ≥ 3.9**.

**Upper bound from `torch>=2.10.0`:**

PyTorch 2.10 (currently nightly/pre-release territory as of May 2026) follows the same support matrix as 2.x — they dropped Python 3.8 in 2.0 and currently target up to 3.12 stable, with 3.13 in progress. **Avoid 3.13+** unless you want to be a beta tester.

**Recommendation: Python 3.11**

| Version | Verdict |
|---------|---------|
| 3.9 | Works but old; fewer optimizations |
| 3.10 | Fine, slightly dated |
| **3.11** | ✅ Best: fastest CPython to date, all deps stable |
| 3.12 | Works, but some ecosystem packages still catching up |
| 3.13+ | Too bleeding-edge; pytorch 2.10 support not guaranteed |

Python 3.11 has the best performance (15–60% faster than 3.10 on many workloads due to the specializing adaptive interpreter), and every dep in your stack has rock-solid 3.11 wheels.

```bash
# On your Ubuntu workstation or AMD Dev Cloud
conda create -n dsv4 python=3.11
conda activate dsv4
pip install torch>=2.10.0 transformers>=5.0.0 safetensors>=0.7.0 \
    fast_hadamard_transform tilelang==0.1.8
```

Or with `uv` (faster):

```bash
uv venv --python 3.11 .venv
source .venv/bin/activate
uv pip install torch>=2.10.0 transformers>=5.0.0 safetensors>=0.7.0 \
    fast_hadamard_transform tilelang==0.1.8
```

**References:**

- [tilelang PyPI](https://pypi.org/project/tilelang/)
- [tilelang GitHub](https://github.com/tile-ai/tilelang)
- [DeepSeek-V4-Pro inference README](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/inference/README.md)
