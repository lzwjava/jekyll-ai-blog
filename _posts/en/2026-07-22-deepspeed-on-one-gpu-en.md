---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSpeed on One GPU
translated: false
type: note
---

Question: Can an RTX 4070 (single GPU) use DeepSpeed?

Answer:

Yes. A single RTX 4070 can absolutely use DeepSpeed. In fact, many of DeepSpeed's optimizations work even when `world_size=1`.

However, **not every DeepSpeed feature is useful on a single 12 GB GPU**.

| Feature                     | Single RTX 4070 | Worth using?             |
| --------------------------- | --------------- | ------------------------ |
| Fused Adam                  | ✅               | Yes                      |
| CPU Adam                    | ✅               | Sometimes                |
| Mixed Precision (BF16/FP16) | ✅               | Yes                      |
| Gradient Accumulation       | ✅               | Yes                      |
| Activation Checkpointing    | ✅               | Yes                      |
| ZeRO Stage 1                | ✅               | Small benefit            |
| ZeRO Stage 2                | ✅               | Sometimes                |
| ZeRO Stage 3                | ✅               | Yes if model barely fits |
| Pipeline Parallel           | ❌               | Needs multiple GPUs      |
| Tensor Parallel             | ❌               | Needs multiple GPUs      |
| Communication overlap       | Mostly useless  | No                       |

### What DeepSpeed actually gives you on one GPU

For a single GPU, DeepSpeed is mostly a **memory optimizer**, not a speed optimizer.

Normal PyTorch stores

```
parameters
gradients
optimizer states
```

For Adam:

```
weights        1x
gradients      1x
m              1x
v              1x

≈4× parameter memory
```

DeepSpeed can

* offload optimizer states to CPU
* offload parameters to CPU/NVMe
* checkpoint activations
* use fused CUDA kernels

That lets you train models that otherwise OOM.

---

### Example

Without DeepSpeed

```
python train.py
```

With DeepSpeed

```
deepspeed train.py \
    --deepspeed ds_config.json
```

Example config:

```json
{
  "train_micro_batch_size_per_gpu": 1,

  "gradient_accumulation_steps": 16,

  "bf16": {
    "enabled": true
  },

  "zero_optimization": {
    "stage": 2
  }
}
```

---

### For a 12 GB RTX 4070

I'd roughly rank the options like this:

```
1. bf16
2. Flash Attention
3. gradient checkpointing
4. gradient accumulation
5. DeepSpeed ZeRO
6. CPU offload
7. QLoRA
```

If you're training full models, ZeRO helps.

If you're doing LoRA/QLoRA, DeepSpeed often provides little benefit because PEFT already reduces memory dramatically.

---

### Compared to FSDP

Nowadays many projects choose:

```
PyTorch FSDP
    +
torch.compile
    +
Flash Attention
```

instead of DeepSpeed.

DeepSpeed remains strongest when you need:

* ZeRO-3
* CPU/NVMe offload
* very large models
* Microsoft's training stack

---

### For your workload

From your recent experiments (GPT-2 training on an RTX 4070 and running FLUX on 12 GB VRAM), I'd use:

* **GPT-2 / transformer pretraining (<1B params):** Plain PyTorch + Flash Attention + gradient checkpointing. DeepSpeed is optional.
* **7B–14B full finetuning:** DeepSpeed ZeRO-2/3 becomes valuable.
* **LoRA / QLoRA:** Skip DeepSpeed unless you hit memory limits.
* **FLUX / diffusion training:** Prefer Hugging Face Accelerate (optionally with DeepSpeed backend) over using DeepSpeed directly.

References:

* [DeepSpeed GitHub repository](https://github.com/deepspeedai/deepspeed?utm_source=chatgpt.com)
* [DeepSpeed documentation](https://deepspeed.readthedocs.io/en/latest/?utm_source=chatgpt.com)
