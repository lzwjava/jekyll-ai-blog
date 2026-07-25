---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD ROCm PyTorch 诊断报告
translated: true
type: note
---

以下是完整的诊断报告：

---

## ✅ PyTorch + ROCm 状态

| 组件 | 状态 |
|-----------|--------|
| **PyTorch**（系统虚拟环境） | ✅ **2.9.1+rocm** 已安装于 `/opt/venv` |
| **torchaudio** | ✅ 2.9.0 |
| **torchvision** | ✅ 0.24.1 |
| **vLLM** | ✅ 0.16.1.dev0（基于 ROCm 7.2.1 构建） |
| **APEX** | ✅ 1.9.0+rocm7.2.1 |
| **amdsmi** | ✅ 26.2.2 |
| **amd-aiter** | ✅ 0.1.7 |

### 🖥️ GPU 硬件 — **8× AMD Radeon（gfx1100 / RDNA3）**

```
Device ID:  1002:744b → gfx1100 (AMD Radeon RX 7000 series)
VRAM each:  48 GiB (51,522,830,336 bytes)
Total VRAM: ~384 GiB
```

来自 `lspci` 的完整 GPU 列表：
```
03:00.0, 23:00.0, 43:00.0, 63:00.0
83:00.0, a3:00.0, c3:00.0, e3:00.0
```

以及一个用于显示的 ASPEED BMC（`1a03:2000`）。

### 🧠 ROCm 堆栈

| 组件 | 版本 |
|-----------|---------|
| ROCm | **7.2.1**（`/opt/rocm → /opt/rocm-7.2.1`） |
| hipconfig | 7.2.53211 |
| 内核驱动 | ROck 模块 6.16.13 已加载 |
| HSA 运行时 | 1.18 |

### ⚙️ 系统规格

- **CPU：** AMD EPYC 9334（2× 32 核 = 128 线程）
- **内存：** 503 GiB
- **交换空间：** 无

### 📍 如何使用 PyTorch 配合 ROCm

PyTorch 位于系统虚拟环境中——激活它：

```bash
source /opt/venv/bin/activate
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.device_count())"
# → True, 8
```

如果你当前 shell 无法 `import torch`，很可能你不在虚拟环境中。只需先执行 `source /opt/venv/bin/activate` 即可。