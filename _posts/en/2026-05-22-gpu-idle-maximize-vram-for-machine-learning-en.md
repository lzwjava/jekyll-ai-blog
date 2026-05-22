---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GPU Idle: Maximize VRAM for Machine Learning"
translated: false
type: note
---

The GPU is essentially idle right now. Here's the snapshot:

```
RTX 4070  |  VRAM: 168 MiB / 12,282 MiB (1.4%)
GPU Util: 0%  |  Memory Util: 0%  |  Temp: 43°C  |  Power: 10W / 215W
System RAM: 5.0 GiB used / 62 GiB total
```

Only Xorg (105 MiB) and gnome-shell (11 MiB) are on the GPU. The 12 GB VRAM is your primary bottleneck for ML. Here's how to squeeze the most out of it:

---

## 1. QLoRA — Your Default for Fine-Tuning

At 12 GB, you can't do full fine-tuning on 7B+ models. QLoRA (4-bit base + LoRA adapters) gets you there:

```python
from transformers import BitsAndBytesConfig
from peft import LoraConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

lora_config = LoraConfig(
    r=16,           # rank — 8-64, 16 is a good default
    lora_alpha=32,  # scaling — typically 2x rank
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
)
```

This puts a 7B model at ~4-5 GB VRAM, leaving room for gradients and activations.

## 2. Flash Attention 2 — Free VRAM

Saves 30-50% of attention memory with zero accuracy loss:

```bash
pip install flash-attn --no-build-isolation
```

```python
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-8B",
    attn_implementation="flash_attention_2",
    torch_dtype=torch.bfloat16,
)
```

## 3. Gradient Checkpointing — Trade Compute for Memory

Recomputes activations during backward pass instead of storing them:

```python
model.gradient_checkpointing_enable()
# With Unsloth:
model.gradient_checkpointing_enable({"use_reentrant": False})
```

Saves ~40-60% activation memory, 15-20% throughput penalty.

## 4. Unsloth — 2x Faster, 50% Less VRAM

Replace `transformers` + `peft` with Unsloth for free wins:

```bash
pip install unsloth
```

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(model, lora_config)
```

Unsloth's hand-written Triton kernels cut VRAM use dramatically. For a 7B QLoRA model, you can train with sequence length 4096 on 12 GB.

## 5. Micro-Batch + Gradient Accumulation

With 12 GB, batch_size=1 is often the limit. Simulate larger batches:

```python
training_args = TrainingArguments(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,  # effective batch = 16
    # ...
)
```

## 6. Optimizer Choice — 8-bit Adam

```python
# paged_adamw_8bit saves ~1-2 GB vs regular AdamW
training_args = TrainingArguments(
    optim="paged_adamw_8bit",
    # ...
)
```

## 7. When 12 GB Isn't Enough — CPU Offload

Your 62 GB system RAM is a massive buffer. For inference on larger models:

```bash
# llama.cpp with GPU offload layers
./llama-cli -m model.gguf -ngl 33  # offload 33 layers to GPU, rest on CPU
```

For training, DeepSpeed ZeRO-3 can offload optimizer states to CPU, letting you train models that would otherwise need 24+ GB.

## 8. Training from Scratch — nanoGPT Scale

On 12 GB, you can train a ~100M parameter GPT-2 from scratch (what you've done before). At that scale:

```python
# Key levers for 12 GB
batch_size = 64          # push as high as fits
block_size = 1024        # context length
gradient_accumulation_steps = 4
dtype = torch.bfloat16   # saves 50% memory vs fp32
compile = True            # torch.compile() for ~20% speedup
```

---

**Quick check — what are you trying to train or run right now?** Knowing the model size and task lets me give you exact config values instead of ranges.