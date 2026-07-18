---
audio: false
generated: true
image: false
lang: en
layout: post
title: "RTX 3090: best second GPU for training"
translated: false
type: note
---

Question: RTX 4070 (12GB) + second GPU for local multi-GPU/distributed training, budget ~5000 CNY secondhand (Xianyu/JD) — NVIDIA or AMD, and how to pick?

Answer:

**NVIDIA. Not close.** Mixing vendors kills the actual use case you want (combined training). NCCL only talks CUDA-to-CUDA. RCCL exists but there's no CUDA↔ROCm collective backend — you can't `all_reduce` across a 4070 and a 7900 XTX in one `torch.distributed` process group. Best case with mixed vendors: two independent single-GPU processes, no tensor/data parallelism between them. That's not "second GPU for training," that's "two computers."

ROCm being open-source is genuinely nice for driver archaeology, but it doesn't help you here — the interop problem is at the collective-comm layer, not the driver.

```
Combined training (DDP/FSDP/pipeline) across cards → same vendor required → NVIDIA
Two isolated single-GPU jobs running side by side  → vendor doesn't matter
```
Since you explicitly want distributed/dual-GPU, that settles it: NVIDIA.

**What to buy at 5000 CNY: used RTX 3090 24GB.** Confirmed still the value king in 2026 — RTX 3090 has fallen to roughly 600-800 USD on the used market (about 4500-6000 CNY), a fraction of its original ~1500 USD launch price, while used RTX 4090/5090 both run over 2000 USD. Its 24GB GDDR6X on a 384-bit bus with 936GB/s bandwidth, plus mature CUDA support, keeps it ahead of similarly priced cards for local LLM/edge-AI work — VRAM headroom matters more than raw FLOPs for you.

**On Xianyu specifically:** avoid ex-mining cards with worn fans/thermal pads unless heavily discounted, prefer ones with box/invoice or a platform that offers inspection. Non-reference models (华硕猛禽, 技嘉魔鹰) cool better but are physically bigger — check case clearance and that your PSU has a spare 12V rail for a 350W card.

**No NVLink win here** — your 4070 doesn't support NVLink anyway (only 3090/3090 Ti among consumer Ampere do), so don't chase an NVLink-bridge pair. You're on PCIe P2P regardless.

**Heterogeneous VRAM (12GB + 24GB) handling** — don't use naive DDP (wastes 3090's extra 12GB, batch capped to the smaller card). Options:

```python
# Option 1: model-parallel split by layer VRAM budget (transformers)
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "your-model",
    device_map={
        "model.layers.0-19": 0,   # 4070, fewer layers
        "model.layers.20-39": 1,  # 3090, more layers
        "lm_head": 1,
    },
    torch_dtype=torch.bfloat16,
)

# Option 2: FSDP with per-rank memory-aware sharding (deepspeed)
# deepspeed config: set "reduce_bucket_size" smaller for rank0 (4070)
# or just run gradient checkpointing harder on rank0

# Option 3 — simplest, what I'd actually do:
# use the 3090 (rank0) as primary trainer, 4070 for eval/inference
# or a second concurrent experiment, no cross-GPU comm needed
torchrun --nproc_per_node=1 --node_rank=0 train.py --gpu 1  # 3090 does the real run
```

For your GPT-2-scale training work, realistically the 3090 alone (24GB, ~936GB/s BW, full BF16/TF32 tensor cores) will do more useful work than trying to force DDP across mismatched cards. Treat the 4070 as a second independent worker (data prep, eval, smaller experiments) rather than fighting to keep both cards in lockstep on one job.

References:
- [A卡没人买！五年前的N卡又火了：二手RTX 3090成性价比之王 - 快科技](https://news.mydrivers.com/1/1109/1109956.htm)
- [二手RTX3090：2026年边缘AI领域的性价比之王 - Kaiyun](https://www.yhkjgroup.com/news/1196.html)
- [3090显卡多少钱 目前3090价格及参数一览 - 驱动人生](https://www.160.com/article/9337.html)
