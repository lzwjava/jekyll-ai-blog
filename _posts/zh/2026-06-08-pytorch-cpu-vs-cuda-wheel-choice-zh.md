---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch CPU与CUDA轮子选择
translated: true
type: note
---

**问题：** PyTorch 如何分发仅 CPU 版与 CUDA 版 wheel 包？在 Windows 上我应该安装哪一个？

## 答案

PyTorch 分发**独立的 wheel 包**，因为 CUDA 二进制文件体积庞大且非必需。CPU 版 wheel 包（约 200 MB）仅包含：

- PyTorch 运行时代码
- CPU 内核（BLAS、MKL-DNN）
- Python 绑定

CUDA 版 wheel 包（2-3 GB）捆绑了：

- CPU 版 wheel 包的所有内容
- NVIDIA CUDA 运行时库（cudart、cublas、cunn 等）
- cuDNN（深度学习原语）
- 针对你的 CUDA 版本编译的 GPU 内核

**为什么？** 仅在 CPU 系统上运行推理的用户不需要 2GB 未使用的 CUDA 二进制文件。捆绑 CUDA 的 wheel 包还会将你锁定到特定的 CUDA 版本——如果你以后升级 CUDA，捆绑的 wheel 包将不匹配。

### 在 Windows 上安装

**仅 CPU 版**（安装最快，无 GPU）：

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**CUDA 12.4**（最常见，需要 NVIDIA GPU + 已安装 CUDA 12.4）：

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

**CUDA 11.8**：

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

`--index-url` 标志告诉 pip 从 PyTorch 的 wheel 仓库获取包，而不是 PyPI（默认只托管 CPU 版 wheel 包）。

### 验证安装

```python
import torch
print(torch.cuda.is_available())  # 若正确安装 CUDA 版 wheel 包则返回 True
print(torch.__version__)
print(torch.version.cuda)         # CPU 版为 None，CUDA 12.4 版本为 "12.4"，依此类推
```

### 关键细节

- **你需要单独安装 CUDA 运行时**——wheel 包捆绑了 cuBLAS/cuDNN，但仍需要 NVIDIA 驱动 + CUDA 工具包。检查：`nvidia-smi` 应能正常工作。
- **CUDA 12.4 wheel 包可配合 CUDA 12.1+ 使用**（在主版本内向前兼容）。
- **你工作站的 RTX 4070** 需要 CUDA 12.x。请使用 cu124 wheel 包。
- **安装一次，随处可用**——`pip install` 之后，只需 `import torch` 并选择设备：`torch.device('cuda')` 或 `torch.device('cpu')`。

如果你要在 4070 上进行严肃的训练，不要跳过 CUDA 版 wheel 包。在有 GPU 能力的机器上用 CPU 训练会非常痛苦。
