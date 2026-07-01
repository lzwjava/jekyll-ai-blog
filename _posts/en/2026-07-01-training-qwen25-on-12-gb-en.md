---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Qwen2.5 on 12 GB
translated: false
type: note
---

Question: Beyond inference, can I actually *train* (or fine-tune) Qwen2.5-1.5B-Instruct on an RTX 4070 (12 GB)? SGLang is inference-only, so what are the real training options on this card?

Answer:

Yes — but let's be precise about what "train" means on 12 GB. SGLang is an inference/serving engine (RadixAttention, continuous batching); it does no gradient computation. For training you need PyTorch + an optimizer, and the memory math is brutal.

The 12 GB memory wall

A 1.5B model in bf16 weights alone is ~3 GB. The killer is the optimizer state. Full fine-tuning with AdamW needs, per parameter:

- weights (bf16): 2 bytes
- gradient (bf16): 2 bytes
- Adam m + v (fp32): 8 bytes
- fp32 master copy: 4 bytes

That's ~16 bytes/param → 1.5B × 16 ≈ **24 GB** just for static state, before activations. Full fine-tuning is dead on a 4070. So the real options are LoRA/QLoRA.

QLoRA memory math (this is what fits)

QLoRA quantizes the frozen base to 4-bit (NF4) and only trains small low-rank adapters:

- base weights (4-bit): 1.5B × 0.5 bytes ≈ 0.75 GB
- LoRA adapters (r=16, ~0.3% of params): a few MB of trainable params
- optimizer state only on adapters: negligible
- activations + gradient checkpointing: the variable cost

Total lands around **4–7 GB** depending on seq length and batch size. Very comfortable on 12 GB. Plain LoRA (base in bf16, ~3 GB) also fits with headroom.

Minimal QLoRA training script

This is the build-first path — `trl` + `peft` + `bitsandbytes`:

```python
# pip install -U trl peft bitsandbytes transformers datasets accelerate
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer
from datasets import load_dataset

model_id = "Qwen/Qwen2.5-1.5B-Instruct"

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,   # saves another ~0.4 GB
)

model = AutoModelForCausalLM.from_pretrained(
    model_id, quantization_config=bnb, device_map={"": 0},
    attn_implementation="flash_attention_2",  # or "sdpa" if FA2 unbuilt
)
tok = AutoTokenizer.from_pretrained(model_id)

peft_cfg = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj","k_proj","v_proj","o_proj",
                    "gate_proj","up_proj","down_proj"],  # attn + MLP
)

ds = load_dataset("trl-lib/Capybara", split="train[:2000]")

cfg = SFTConfig(
    output_dir="qwen-qlora",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,        # effective batch 16
    gradient_checkpointing=True,          # biggest activation saver
    bf16=True,
    max_length=1024,
    learning_rate=2e-4,
    num_train_epochs=1,
    logging_steps=10,
    optim="paged_adamw_8bit",             # paged = survives VRAM spikes
)

trainer = SFTTrainer(model=model, args=cfg, train_dataset=ds, peft_config=peft_cfg)
trainer.train()
trainer.save_model("qwen-qlora/adapter")
```

The levers that actually control whether it OOMs, in order of impact: `gradient_checkpointing=True` (trades ~30% compute for large activation savings), `max_length` (activations scale linearly — drop to 512 if tight), `per_device_train_batch_size`, and `paged_adamw_8bit` (the paged optimizer offloads to CPU RAM on spikes instead of crashing).

Knowledge → memory map

| Method | Base dtype | Fits 12 GB? | Trains |
| --- | --- | --- | --- |
| Full FT | bf16 | ❌ ~24 GB | all params |
| LoRA | bf16 (~3 GB) | ✅ ~6–9 GB | adapters |
| QLoRA | 4-bit (~0.75 GB) | ✅ ~4–7 GB | adapters |

Where your two GPUs split the work

Prototype the QLoRA loop on the 4070 — get the data pipeline, chat template, and adapter config correct at `max_length=512`, batch 1–2. When you want full fine-tuning, longer context, or a real sweep, push it to the MI300X (192 GB), where full bf16 FT of a 1.5B sits in well under 30 GB and you can crank batch size and sequence length. The 4070 is your correctness-checking environment; the MI300X is your scale environment.

After training, merge and serve back through SGLang:

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM
base = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="bfloat16")
merged = PeftModel.from_pretrained(base, "qwen-qlora/adapter").merge_and_unload()
merged.save_pretrained("qwen-merged")
# then: python -m sglang.launch_server --model-path qwen-merged
```

One caveat on flash-attention-2: prebuilt wheels for the 4070 (Ada, sm_89) can be finicky — if `flash_attention_2` errors at load, switch to `attn_implementation="sdpa"`, which uses PyTorch's built-in fused attention and is nearly as fast at this scale.

References:

- [QLoRA paper (Dettmers et al.)](https://arxiv.org/abs/2305.14314)
- [PEFT LoRA docs](https://huggingface.co/docs/peft/main/en/developer_guides/lora)
- [TRL SFTTrainer docs](https://huggingface.co/docs/trl/main/en/sft_trainer)
- [bitsandbytes (paged optimizers)](https://huggingface.co/docs/bitsandbytes/main/en/index)
- [Qwen2.5 models](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct)
