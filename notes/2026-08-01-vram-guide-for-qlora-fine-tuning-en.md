---
audio: false
generated: true
image: false
lang: en
layout: post
title: VRAM Guide for QLoRA Fine-Tuning
translated: false
type: note
---

Question: What GPU machine is needed for LoRA / QLoRA fine-tuning Qwen or DeepSeek models? Is 24GB VRAM enough?

Answer:

Yes, **24GB VRAM is enough for many LoRA/QLoRA fine-tuning tasks**, but the model size matters. The key difference:

* **LoRA**: base model weights stay in GPU memory (usually FP16/BF16), only adapters are trained.
* **QLoRA**: base model is quantized (usually 4-bit NF4), dramatically reducing VRAM usage.

The memory budget roughly:

```
VRAM ≈ model weights + activations + gradients + optimizer states + KV/cache + overhead
```

For QLoRA:

```
4-bit weights:
params × 0.5 bytes

LoRA adapters:
small (usually <1-2% of model)

optimizer:
only LoRA params, not full model
```

### Practical GPU requirements

| Model                        | Params | LoRA       | QLoRA    | 24GB GPU        |
| ---------------------------- | ------ | ---------- | -------- | --------------- |
| Qwen2.5-3B                   | 3B     | ~8GB       | ~5GB     | ✅ Easy          |
| Qwen2.5-7B                   | 7B     | ~16-20GB   | ~10-14GB | ✅ Easy          |
| Qwen2.5-14B                  | 14B    | ~30GB+     | ~18-22GB | ✅ Good          |
| Qwen2.5-32B                  | 32B    | ~70GB+     | ~22-30GB | ⚠️ Tight        |
| Qwen3-8B                     | 8B     | ~18GB      | ~12-16GB | ✅ Easy          |
| DeepSeek-R1-Distill-Qwen-7B  | 7B     | ~16-20GB   | ~10-14GB | ✅ Easy          |
| DeepSeek-R1-Distill-Qwen-14B | 14B    | ~30GB      | ~18-22GB | ✅ Good          |
| DeepSeek-R1-Distill-Qwen-32B | 32B    | impossible | ~24-32GB | ⚠️ Needs tricks |

A single:

* RTX 3090 24GB
* RTX 4090 24GB
* RTX A5000 24GB
* RTX 6000 Ada 48GB

is a very common QLoRA setup.

---

## Example: Qwen2.5-14B QLoRA on RTX 3090 24GB

Typical config:

```yaml
model: Qwen/Qwen2.5-14B-Instruct

quantization: 4bit
bnb_4bit_quant_type: nf4

lora:
  r: 16
  alpha: 32
  dropout: 0.05

training:
  batch_size: 1
  gradient_accumulation: 16
  max_seq_length: 4096
```

Memory:

```
Qwen 14B FP4:

14B params × 0.5 bytes
≈ 7GB

+
CUDA overhead
≈ 2GB

+
activations
≈ 8-10GB

+
LoRA
<1GB

-----------------
~18-20GB
```

Fits in 24GB.

---

## For DeepSeek models

Need to distinguish:

### DeepSeek-R1-Distill

These are normal dense Qwen/Llama-based models.

Example:

```
DeepSeek-R1-Distill-Qwen-14B
```

Easy.

A 24GB card works.

---

### DeepSeek-V3 / R1 full

Different beast.

```
DeepSeek-V3:
671B total params
37B activated params
```

Even QLoRA is not a normal single GPU job.

You need:

* multi-GPU
* distributed training
* large VRAM

Example:

```
8 × H100 80GB
or
8 × MI300X 192GB
```

---

## Your RTX 4070 12GB

Your current RTX 4070:

```
12GB VRAM
```

can do:

✅ Qwen2.5-3B
✅ Qwen2.5-7B QLoRA
✅ DeepSeek-R1-Distill-7B

Maybe:

⚠️ 14B with aggressive settings:

```
batch=1
seq_len=2048
gradient checkpointing
CPU offload
```

but not comfortable.

---

## Best home AI fine-tuning GPU choices in 2026

### Budget

Used RTX 3090 24GB

```
$600-800
24GB VRAM
great CUDA support
```

Probably the best price/performance.

### New

RTX 4090 24GB

```
24GB
fastest consumer card
```

### Serious local research

Used RTX A6000

```
48GB VRAM
ECC
```

Excellent for:

* Qwen 32B QLoRA
* larger context
* bigger batches

---

## Recommended stack

For QLoRA:

```bash
pip install transformers
pip install peft
pip install bitsandbytes
pip install trl
```

Minimal training:

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="bfloat16"
)

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-14B-Instruct",
    quantization_config=bnb,
    device_map="auto"
)

lora = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj"
    ]
)

model = get_peft_model(model, lora)
```

---

Given your setup (RTX 4070 + interest in training GPT/nanochat), the most useful upgrade path is:

1. Keep RTX 4070 for inference + small experiments.
2. Buy used RTX 3090 24GB.
3. Run:

   * Qwen3-8B full LoRA
   * Qwen2.5-14B QLoRA
   * DeepSeek-R1-Distill-14B QLoRA
4. Build datasets + evaluation pipeline.

For actual LLM engineering experience, a **single 24GB GPU is already enough to learn almost all LoRA/QLoRA workflows used in production.**
