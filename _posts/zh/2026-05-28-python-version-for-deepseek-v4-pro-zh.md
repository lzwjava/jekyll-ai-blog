---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek V4-Pro Python 版本
translated: true
type: note
---

**问题：** DeepSeek V4-Pro 推理应使用哪个 Python 版本（需满足 `torch>=2.10.0`、`transformers>=5.0.0`、`safetensors>=0.7.0`、`fast_hadamard_transform`、`tilelang==0.1.8`）？

**答案：**

**Python 3.11** 是最佳选择。以下是约束条件链：

**关键约束是 `tilelang==0.1.8`：**

PyPI 上的 `tilelang` 要求 Python `>=3.9`，并明确支持 3.9、3.10、3.11、3.12、3.13、3.14。0.1.8 版本发布于 2026 年 2 月 16 日，远在 Python 3.8 终止支持之后。

v0.1.6.post2 是最后一个兼容 Python 3.8 的版本，因此 0.1.8 完全放弃了对 3.8 的支持。这意味着 **Python ≥ 3.9**。

**来自 `torch>=2.10.0` 的上限：**

PyTorch 2.10（截至 2026 年 5 月仍处于 nightly/pre-release 阶段）沿用与 2.x 相同的支持矩阵——它们在 2.0 中放弃了对 Python 3.8 的支持，目前稳定版本支持至 3.12，3.13 正在开发中。**避免使用 3.13+**，除非你想当小白鼠。

**推荐：Python 3.11**

| 版本 | 结论 |
|------|------|
| 3.9 | 可用但较旧；优化较少 |
| 3.10 | 尚可，略显过时 |
| **3.11** | ✅ 最佳：至今最快的 CPython，所有依赖稳定 |
| 3.12 | 可用，但部分生态包仍在追赶 |
| 3.13+ | 过于前沿；PyTorch 2.10 支持未保证 |

Python 3.11 性能最佳（由于专门的适应性解释器，在多数工作负载上比 3.10 快 15–60%），且你所有依赖都有稳定的 3.11 wheel 包。

```bash
# 在 Ubuntu 工作站或 AMD Dev Cloud 上
conda create -n dsv4 python=3.11
conda activate dsv4
pip install torch>=2.10.0 transformers>=5.0.0 safetensors>=0.7.0 \
    fast_hadamard_transform tilelang==0.1.8
```

或使用 `uv`（更快）：
```bash
uv venv --python 3.11 .venv
source .venv/bin/activate
uv pip install torch>=2.10.0 transformers>=5.0.0 safetensors>=0.7.0 \
    fast_hadamard_transform tilelang==0.1.8
```

**参考链接：**

- [tilelang PyPI](https://pypi.org/project/tilelang/)
- [tilelang GitHub](https://github.com/tile-ai/tilelang)
- [DeepSeek-V4-Pro 推理 README](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/inference/README.md)