---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SM120 Blackwell Ultra 推理优化
translated: true
type: note
---

**问题：** “工作流中使用 AI Agent 进行推理优化” 中的 “SM120” 是什么意思？

**回答：**

**SM120** 指的是 **NVIDIA 的 SM（流式多处理器）第 120 代**——这是 CUDA/PTX 内部使用的计算架构代际标识符。

具体来说，SM120 对应的是 2024 年发布、2025 年出货的 **Blackwell** 架构（GB200/B200/B100 GPU）。

SM 编号遵循 NVIDIA 的架构代际关系：

| SM 版本 | 架构 | GPU |
|---|---|---|
| SM80 | Ampere | A100, A10 |
| SM86 | Ampere | RTX 3090 |
| SM89 | Ada Lovelace | RTX 4090 |
| SM90 | Hopper | H100, H200 |
| SM100 | Blackwell（第一代） | B100, B200 |
| **SM120** | **Blackwell Ultra** | **GB300, B300** |

因此，“工作流中使用 AI Agent 的 SM120 推理优化”很可能是 **GTC 2025 或类似 NVIDIA 活动的演讲或论文标题**，具体是关于使用代理工作流在 **Blackwell Ultra** GPU 上优化 LLM 推理。

在 CUDA 术语中，可以通过以下方式指定此目标：

```bash
nvcc --gpu-architecture=sm_120 ...
```

或在 PyTorch 中：

```python
torch.cuda.get_device_capability()  # 对于 SM120 返回 (12, 0)
```

你有该具体演讲或论文的链接吗？如果有，我可以深入了解其实际内容。
