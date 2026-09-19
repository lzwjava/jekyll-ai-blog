---
audio: false
generated: true
image: false
lang: en
layout: post
title: QLoRA Fine-Tuning Qwen3-8B
translated: false
type: note
---

**Question:** How do I fine-tune Qwen3-8B on ~100MB of enterprise private text data?

**Answer:**

Here's a practical end-to-end guide for fine-tuning Qwen3-8B (8 billion parameters) on private enterprise data.

---

## 1. Environment Setup

```bash
# Recommended: Python 3.10+, CUDA 12.1+
pip install transformers==4.51.0 peft trl datasets accelerate bitsandbytes
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

**Hardware requirements:**

| Method | Min VRAM | Recommended |
| -------- | ---------- | ------------- |
| Full fine-tune | 80GB (A100) | 4× A100 |
| LoRA (4-bit QLoRA) | **16–24GB** | 1× A100/H100 |
| LoRA (8-bit) | 32GB | 2× A100 |

> For 100MB of text, **QLoRA (4-bit LoRA)** is the most practical enterprise approach — minimal GPU, fast iteration.

---

## 2. Prepare Your Data (~100MB text)

Your raw text needs to be converted into instruction-tuning or continued-pretraining format.

**Option A — Continued Pretraining (raw text, no labels)**

```python
# data/train.jsonl
{"text": "Your enterprise document content here..."}
{"text": "Another document or paragraph..."}
```

**Option B — Instruction Fine-tuning (Q&A pairs, recommended for enterprise)**

```python
# data/train.jsonl
{"instruction": "What is our refund policy?", "input": "", "output": "Our refund policy states..."}
{"instruction": "Summarize this contract clause", "input": "...", "output": "..."}
```

**Convert raw .txt files to JSONL:**

```python
import json, glob

records = []
for path in glob.glob("data/raw/*.txt"):
    with open(path) as f:
        text = f.read()
    # Chunk into ~512-token segments
    chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
    for chunk in chunks:
        records.append({"text": chunk})

with open("data/train.jsonl", "w") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
```

---

## 3. QLoRA Fine-tuning Script (Recommended)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
import torch

MODEL_ID = "Qwen/Qwen3-8B"  # or "Qwen/Qwen3-8B-Instruct"

# 1. 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# 2. Load model + tokenizer
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

# 3. LoRA config — target Qwen3 attention layers
lora_config = LoraConfig(
    r=16,                    # rank: 8-64, higher = more capacity
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# → trainable params: ~20M / 8B = ~0.25%

# 4. Load dataset
dataset = load_dataset("json", data_files={"train": "data/train.jsonl"})

# 5. Training config
sft_config = SFTConfig(
    output_dir="./qwen3-8b-finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,   # effective batch = 16
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    bf16=True,
    logging_steps=10,
    save_steps=100,
    max_seq_length=2048,
    dataset_text_field="text",       # or use "instruction"/"output" for chat
)

# 6. Train
trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=dataset["train"],
    tokenizer=tokenizer,
)
trainer.train()

# 7. Save LoRA adapter only (~100MB)
model.save_pretrained("./qwen3-8b-lora-adapter")
tokenizer.save_pretrained("./qwen3-8b-lora-adapter")
```

---

## 4. Use LLaMA-Factory (GUI Alternative, Easier)

If you prefer a no-code approach:

```bash
git clone https://github.com/hiyouga/LLaMA-Factory
cd LLaMA-Factory
pip install -e ".[torch,metrics]"

# Launch Web UI
llamafactory-cli webui
```

Then in the UI: select **Qwen3-8B** → upload your JSONL → choose **LoRA** → click Train.

---

## 5. Inference with Fine-tuned Adapter

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-8B", device_map="auto")
model = PeftModel.from_pretrained(base, "./qwen3-8b-lora-adapter")
tokenizer = AutoTokenizer.from_pretrained("./qwen3-8b-lora-adapter")

inputs = tokenizer("What is our enterprise refund policy?", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

---

## 6. Key Hyperparameters for 100MB Data

| Parameter | Suggested Value | Reason |
| ----------- | ---------------- | -------- |
| `r` (LoRA rank) | 16–32 | Balance capacity vs overfitting |
| `lora_alpha` | 2× rank | Standard scaling |
| `epochs` | 2–5 | 100MB is small; avoid overfitting |
| `learning_rate` | 1e-4 – 3e-4 | QLoRA sweet spot |
| `max_seq_length` | 1024–2048 | Match your doc length |
| `batch_size` (effective) | 16–32 | Via gradient accumulation |

---

## 7. Privacy / Enterprise Security Notes

- Run entirely **on-premise** — no data leaves your environment
- Use **Hugging Face offline mode**: `TRANSFORMERS_OFFLINE=1`
- Store adapters in your internal model registry (MLflow, Weights & Biases on-prem)
- Consider **data deduplication** before training to avoid memorization of sensitive records

---

**References:**

- [Qwen3 on Hugging Face](https://huggingface.co/Qwen/Qwen3-8B)
- [LLaMA-Factory (easiest fine-tune UI)](https://github.com/hiyouga/LLaMA-Factory)
- [TRL SFTTrainer Docs](https://huggingface.co/docs/trl/sft_trainer)
- [QLoRA Paper (Dettmers et al.)](https://arxiv.org/abs/2305.14314)
- [PEFT Library Docs](https://huggingface.co/docs/peft)
