---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: CPU与GPU训练性能对比
translated: true
type: note
---

在笔记本电脑上运行 NanoGPT 训练时出现的低 MFU（0.01%）源于命令中的 `--device=cpu` 标志，该标志强制整个工作负载在 CPU 上运行，而未利用任何 GPU 加速。以下是原因分析及与 4070 Ti 配置的对比：

### 笔记本电脑低 MFU 的关键原因

- **CPU 与 GPU 架构不匹配**：像 NanoGPT 中的 Transformer（即使是此微型配置：4 层、128 嵌入维度、批量大小 12）这类模型，其高度可并行的矩阵运算（如注意力机制、前馈网络）正是 GPU 通过数千核心和高带宽内存所擅长的。而 CPU（即使是现代笔记本电脑的 CPU，根据内核/平台信息推测应为 Intel Alder Lake-P 系列）则按顺序或有限并行方式处理这些运算。PyTorch 在 CPU 上使用优化的 BLAS（如 OpenBLAS），但对此类模型而言，其计算吞吐量仍不及 GPU 的 1%。MFU 衡量的是*相对于理论峰值 FLOPs 的利用率*，因此以 CPU 为主的运行自然会显示如 0.01% 的极低值——这并非“故障”，只是对该任务效率低下。

- **此处未启用 GPU 卸载**：您笔记本电脑的硬件（来自 Alder Lake-P 的 Intel UHD Graphics）不兼容 CUDA，因此未经调整的情况下 PyTorch 默认使用 CPU。`get_gpu_info.py` 的输出显示了一个集成 Intel iGPU 被错误标记为“AMD”（可能是解析 `lspci` 的脚本错误），但即使该 iGPU 可用，标准 PyTorch 也无法开箱即用地在 Intel/AMD iGPU 上加速训练。您需要额外配置如 Intel 的 oneAPI（通过 `torch.backends.mps` 或扩展）或适用于 AMD 的 ROCm，但这仍处于实验阶段且性能无法与 NVIDIA 匹敌。

- **模型/工作负载规模**：这是一个在小型数据集（Shakespeare 字符，block_size=64）上运行的微型模型。在 CPU 上，数据加载、Python 循环和非 FLOP 操作的开销占主导，进一步拉低了 MFU。您的 max_iters=2000 和 log_interval=1 意味着频繁的检查点/评估，放大了 CPU 瓶颈。

### 与 4070 Ti（10% MFU）的对比

- **硬件吞吐量差距**：4070 Ti（RTX 40 系列，约 29 TFLOPs FP16）处理此模型的速度比笔记本电脑 CPU（对 ML 有效的约 0.5-1 TFLOPs）快 10-20 倍。对于小型模型上的 NanoGPT，10% 的 MFU 是合理的——它未达到 100% 是由于内核启动开销、内存带宽限制和非理想批量大小。提高 batch_size（例如至 128+）或使用 FP16/bfloat16 可将其提升至 15-20%，但您的配置较为保守。

- **隐式 GPU 模式**：在 4070 Ti 配置上，您可能正在运行 `--device=cuda`（NanoGPT 在可用时的默认设置），从而启用了完整的张量并行性和 cuBLAS/cuDNN 内核。仅此一项即可通过针对硬件优化来提升 MFU。

| 方面 | 笔记本电脑 (CPU) | 4070 Ti (GPU) |
| ------ | ------------------ | --------------- |
| **设备** | CPU（强制） | CUDA GPU |
| **峰值 FLOPs** | 约 0.5-1 TFLOPs（ML 优化） | 约 29 TFLOPs (FP16) |
| **实现的 MFU** | 0.01%（CPU 开销主导） | 10%（并行优势显现） |
| **训练时间估计（2000 次迭代）** | 10-30+ 分钟（I/O 缓慢） | <1 分钟（极快） |
| **瓶颈** | 串行执行、RAM 限制 | 内存带宽、内核效率 |

### 改进笔记本电脑训练的快速修复

- **如可能，切换到 GPU**：如果您可以通过 SSH + `torchrun` 远程访问 4070 Ti，直接在那里运行即可。对于本地 Intel iGPU，可尝试：

  ```
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu  # 确保 CPU 回退
  # 或对于 Intel oneAPI（实验性）：
  conda install intel-extension-for-pytorch -c intel
  ```

  然后测试 `--device=cuda`（会报错）或在启用 IPEX 时使用 `device='xpu'`。预计最佳情况下 MFU 为 1-5%——仍不理想。

- **优化 CPU 运行**：
  - 如果 RAM 允许，将 `batch_size` 增加至 24-48（您的 Ubuntu 24.04 配置在 glibc2.39 下资源充足）。
  - 添加 `--compile=True`（PyTorch 2.0+ dynamo 可加速 CPU，约快 20-50%）。
  - 在数据加载器中使用 `num_workers=4` 实现 I/O 并行。
  - 使用 `taskset -c 0-7` 运行以绑定到性能核心（通过 `lscpu` 检查）。

- **进行基准测试**：在 4070 Ti 机器上使用 `--device=cuda` 重新运行以进行直接对比（应达到约 10% MFU）。如果您分享确切的 NanoGPT 仓库/版本，我可以建议配置调整。

这是预期行为——CPU 不适用于生产环境的 ML 训练。如果问题依旧，请提供完整的训练日志以便深入调试！
