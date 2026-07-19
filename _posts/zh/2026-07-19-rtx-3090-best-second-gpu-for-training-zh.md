---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 3090：最佳第二GPU用于训练
translated: true
type: note
---

问题：RTX 4070（12GB）+ 第二块 GPU 用于本地多卡/分布式训练，预算约 5000 元二手（闲鱼/京东）——选 NVIDIA 还是 AMD？如何选择？

答案：

**NVIDIA，没有悬念。** 混用厂商会破坏你想要的真正用途（联合训练）。NCCL 只支持 CUDA 到 CUDA 通信。RCCL 虽然存在，但并没有 CUDA↔ROCm 的集合通信后端——你无法在同一个 `torch.distributed` 进程组中横跨 4070 和 7900 XTX 执行 `all_reduce`。混用厂商的最佳情况：两个独立的单 GPU 进程，它们之间没有张量/数据并行。这不算“第二块 GPU 用于训练”，而是“两台独立的电脑”。

ROCm 开源对于驱动考古确实不错，但对你这里没有帮助——互操作问题出在集合通信层，而不是驱动层。

```
联合训练（DDP/FSDP/流水线并行）跨多卡 → 需要同一厂商 → NVIDIA
两个独立的单 GPU 任务并行运行      → 厂商无所谓
```

既然你明确想要分布式/双 GPU，那答案就是：NVIDIA。

**5000 元买什么：二手 RTX 3090 24GB。** 被公认在 2026 年仍是性价比之王——二手市场 RTX 3090 已跌至约 600-800 美元（约 4500-6000 元），仅为原发布价 1500 美元的一小部分，而二手 RTX 4090/5090 均超过 2000 美元。它拥有 24GB GDDR6X 显存、384-bit 位宽、936GB/s 带宽，加上成熟的 CUDA 支持，使其在本地 LLM/边缘 AI 工作中领先于同类价位显卡——对你来说，显存容量比原始算力更重要。

**具体在闲鱼上：** 避免购买矿卡（风扇/导热垫磨损），除非价格极低；优先选择带包装/发票或支持验货平台的商品。非公版型号（如华硕猛禽、技嘉魔鹰）散热更好但体积更大——请检查机箱空间，并确保你的电源有额外的 12V 接口支持 350W 显卡。

**这里无需追求 NVLink**——你的 4070 本来就不支持 NVLink（消费级 Ampere 中仅 3090/3090 Ti 支持），所以不要去找 NVLink 桥接套件。你只能用 PCIe P2P 通信。

**异构显存（12GB + 24GB）处理**——不要使用简单的 DDP（会浪费 3090 额外的 12GB，批次大小受限于小显存显卡）。可选方案：

```python
# 方案 1：按层显存预算进行模型并行（transformers）
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "your-model",
    device_map={
        "model.layers.0-19": 0,   # 4070，层数较少
        "model.layers.20-39": 1,  # 3090，层数较多
        "lm_head": 1,
    },
    torch_dtype=torch.bfloat16,
)

# 方案 2：使用 FSDP 并按 rank 感知显存进行分片（deepspeed）
# deepspeed 配置：为 rank0（4070）设置更小的 "reduce_bucket_size"
# 或者干脆在 rank0 上更积极地使用梯度检查点

# 方案 3 — 最简单，也是我实际会用的：
# 用 3090（rank0）作为主要训练卡，4070 用于推理/评估
# 或者运行另一个并发的实验，不需要跨卡通信
torchrun --nproc_per_node=1 --node_rank=0 train.py --gpu 1  # 3090 负责实际训练
```

对于你的 GPT-2 规模训练工作，实际上只用 3090（24GB，~936GB/s 带宽，完整 BF16/TF32 张量核心）就能完成比强行让两块不匹配的卡跑 DDP 更有用的工作。把 4070 当作第二个独立的工作节点（数据预处理、评估、小实验），而不是费力让两块卡在同一个任务上保持同步。

参考资料：

- [A卡没人买！五年前的N卡又火了：二手RTX 3090成性价比之王 - 快科技](https://news.mydrivers.com/1/1109/1109956.htm)
- [二手RTX3090：2026年边缘AI领域的性价比之王 - Kaiyun](https://www.yhkjgroup.com/news/1196.html)
- [3090显卡多少钱 目前3090价格及参数一览 - 驱动人生](https://www.160.com/article/9337.html)
