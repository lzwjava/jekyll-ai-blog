---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Blackwell 消费计算能力
translated: true
type: note
---

问题：SM120 是什么意思？

答案：

`sm_120` = 计算能力 **12.0** = **Blackwell 消费级 GPU**（RTX 50xx 系列 — 5090、5080 等）。

编码方式与之前相同：`SM<主版本><次版本>` → `sm_120` = 12.0。

Blackwell 一代分为两个架构编号，与 Ampere 相同的消费/数据中心模式：

- `sm_100` → 10.0 → Blackwell **数据中心**（B100、B200、GB200）
- `sm_120` → 12.0 → Blackwell **消费级**（RTX 5090/5080/5070、RTX PRO 6000）

注意跳过了 11.x 整个系列——NVIDIA 将 10.x 留给了数据中心芯片（GB100），并将消费级提升到 12.x，而不是像 Ampere 那样使用次版本号（`sm_80` vs `sm_86`）。两个 Blackwell 芯片的硅片差异足够大，因此获得了独立的主版本号。

`sm_120` 相比 `sm_89`（你的 Ada 4070）新增的功能：

- **第五代 Tensor Core**，支持 `fp4`（NVFP4）和 `fp6`——亚字节量化推理。这是 LLM 推理的头号特性。
- **第二代 Transformer Engine**，具有更细粒度的 fp8/fp4 缩放。
- 更新的 `tcgen05` Tensor Core MMA 指令（数据中心版 `sm_100` 拥有完整的张量内存异步路径；`sm_120` 获得消费级子集）。

实际注意事项：**PyTorch/CUDA 工具包版本很重要。** `sm_120` 需要 **CUDA 12.8+** 和最新的 PyTorch 构建（2.7+）。旧版本 wheel 中 `TORCH_CUDA_ARCH_LIST` 最高只到 `9.0`，在 5090 上会失败或回退到慢速的 PTX JIT。如果你租用 5090 机器：

```bash
nvidia-smi --query-gpu=compute_cap --format=csv,noheader   # → 12.0
python -c "import torch; print(torch.cuda.get_device_capability())"  # (12, 0)
# 确保：torch.version.cuda >= '12.8'
```

对于你的技术栈，`fp4` 支持是最有趣的部分——它使得 Blackwell 在廉价本地推理大型量化模型时具有吸引力，而你的 4070 最高只支持 `fp8` Tensor Core 运算（即使在 Ada 消费级上 fp8 也受限）。
