---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GeForce上的混合GPU训练
translated: true
type: note
---

问题：如何在混合了 RTX 3060/3090/4090 卡的 10 GPU 机器上训练模型？

答案：

**核心问题不在于算力，而在于三点：GeForce 上无 P2P/NVLink、异构显存（12GB/24GB/24GB）以及 PCIe 带宽。** 处理好这些问题，DDP/DeepSpeed 就能正常工作。

### 1. 首先检查 P2P 的实际情况

NVIDIA 在驱动层面上对 GeForce（30/40 系列）禁用了 P2P，这被证实是故意的产品差异化策略。NVIDIA 纯粹为了推动用户购买专业级显卡，在消费级 90 系列卡上阻止了 P2P，尽管硬件是支持的。具体到 4090，除了人为的限制外，还存在一个真正的 bug——多 GPU RTX 4090 设置的 CUDA UVA 实现存在缺陷，P2P 传输报告成功但会静默损坏数据（目标全零或 NaN），该问题仅在驱动 525.105.17+ 中修复。底线：**在 GeForce 卡上始终使用 `NCCL_P2P_DISABLE=1` 运行，不要与它对抗。**

```bash
export NCCL_P2P_DISABLE=1
export NCCL_IB_DISABLE=1      # 消费级机器上没有 infiniband
export NCCL_SHM_DISABLE=0     # 共享内存传输是你的后备方案，保持启用
export NCCL_DEBUG=WARN
```

有一个驱动补丁 (`aikitoria/open-gpu-kernel-modules`) 可以通过 BAR1/DMA 强制启用 P2P，如果你想挣扎一下的话，但对于一个 10 卡混合机器来说，不值得为此引入不稳定性——在 P2P 成为瓶颈之前，PCIe 通道数早就成为瓶颈了。

### 2. 拓扑结构比显卡本身更重要

单主板上 10 块 GPU 意味着大多数插槽运行在 x4 或 x1（使用转接卡）。检查你实际的路数分配：

```bash
nvidia-smi topo -m
lspci -vv | grep -A2 "LnkSta:"    # 每张卡实际协商的带宽/速度
```

如果带宽不足，不要在所有 10 张卡上做张量并行或朴素的 DDP all-reduce——你将被网络（PCIe）限制。相反：

### 3. 使用 DeepSpeed ZeRO-3 配合每 GPU 异构批量大小

由于显存是 12/24/24GB，不要在 ranks 之间使用完全相同的微批次大小。DeepSpeed 本身不能完美支持每个 rank 覆盖批次大小，所以实际的操作是**按 rank 分组混合**：在不同显存层之间使用流水线并行，在同一显存组内使用数据并行。

```python
# launch.py — 根据显存大小对 rank 进行分组
import os, torch.distributed as dist

RANK = int(os.environ["RANK"])
GPU_TIERS = {
    # rank: vram_gb
    0: 12, 1: 12, 2: 12,      # 3060 卡
    3: 24, 4: 24, 5: 24, 6: 24,  # 3090 卡
    7: 24, 8: 24, 9: 24,      # 4090 卡
}
# 微批次大小与显存余量成比例
MICRO_BATCH = {12: 4, 24: 8}
micro_bs = MICRO_BATCH[GPU_TIERS[RANK]]
```

`deepspeed_config.json`:
```json
{
  "train_micro_batch_size_per_gpu": "auto",
  "gradient_accumulation_steps": "auto",
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {"device": "cpu", "pin_memory": true},
    "overlap_comm": true,
    "contiguous_gradients": true,
    "reduce_bucket_size": 5e7,
    "stage3_prefetch_bucket_size": 5e7
  },
  "bf16": {"enabled": true},
  "comms_config": {
    "nccl_p2p_disable": true
  }
}
```

"auto" 让 DeepSpeed 的自动调优器选择每个 rank 的微批次大小，但老实说，面对 3 种不同的显存层级，我宁愿通过一个封装脚本，为不同的 rank 组传递不同的 `--per_device_train_batch_size` 来硬编码，而不是相信自动调优器——它是为同构集群优化的。

### 4. 对于混合机器，更简单且通常更好的方法：完全按层级分开

不要强行把全部 10 张卡塞进一个训练任务。两种配置能让你走得更远：

- **3090+4090 组（7 张卡，每张 24GB）**：标准的 FSDP/DDP，同构，没有批次大小的烦恼。
```bash
NCCL_P2P_DISABLE=1 torchrun --nproc_per_node=7 --nnodes=1 train.py \
  --fsdp full_shard --bf16 --gradient_checkpointing
```
- **3060 组（3 张卡，每张 12GB）**：用于评估/推理服务、数据预处理或小型消融实验，而不是主要的训练任务。试图将一张 12GB 的卡塞进与 24GB 卡相同的 ZeRO-3 分片组，意味着整个组的分片大小将被最小的卡限制——你会损失掉大卡上大部分额外的 24GB 显存余量。

这与你在 MI300X 集群上的做法一致——同构分组胜过通过软件强行处理异构。

### 5. 单机 10 卡的实际陷阱

- **功耗**：3×170W (3060) + 4×350W (3090) + 3×450W (4090) ≈ 3260W 仅 GPU。必须使用多电源，通过 `nvidia-smi -pl <瓦数>` 对每张卡交错设置功耗限制，否则你会跳闸。
- **PCIe 转接卡**：挖矿风格的转接卡（x1）会严重拖慢 all-reduce 吞吐量。如果认真想搞，建议使用每个插槽都有真正 x8 电气连接的板子（WRX80/EPYC）。
- **驱动版本**：对于混用中的任何 4090，最低驱动版本必须是 525.105.17+——根据已确认的 NVIDIA 论坛帖子，早期驱动在多 4090 的 P2P 场景下，即使设置了 `NCCL_P2P_DISABLE`，也会静默损坏数据。

参考资料：
- [Cannot enable P2P communication in RTX3090 server · NVIDIA/nccl#1127](https://github.com/NVIDIA/nccl/issues/1127)
- [Standard nVidia CUDA tests fail with dual RTX 4090 Linux box](https://forums.developer.nvidia.com/t/standard-nvidia-cuda-tests-fail-with-dual-rtx-4090-linux-box/233202)
- [Patching NVIDIA's driver and vLLM to enable P2P on consumer GPUs](https://smcleod.net/2026/02/patching-nvidias-driver-and-vllm-to-enable-p2p-on-consumer-gpus/)
- [Problems With RTX4090 MultiGPU — Puget Systems](https://www.pugetsystems.com/labs/hpc/problems-with-rtx4090-multigpu-and-amd-vs-intel-vs-rtx6000ada-or-rtx3090/)
- [DeepSpeed ZeRO config docs](https://www.deepspeed.ai/docs/config-json/#zero-optimizations-for-fp16-training)