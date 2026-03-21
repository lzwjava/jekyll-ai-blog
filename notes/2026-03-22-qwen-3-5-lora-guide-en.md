---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fine-tuning Qwen 3.5 Using LoRA Guide
translated: false
type: note
---

Sure — here's the full walkthrough:

---

## 1. Configuration (top of file)

```python
MODEL_NAME = "Qwen/Qwen3.5-9B"        # The base model to finetune
POSTS_DIR = "~/projects/blog-source/_posts/en"  # Your blog posts
MAX_LENGTH = 2048                      # Max tokens per training sample
BATCH_SIZE = 4                         # Samples per GPU step
GRAD_ACCUM = 4                         # Accumulate gradients before update (effective batch = 4×4 = 16)
EPOCHS = 3                             # Train through all data 3 times
LEARNING_RATE = 2e-5                   # How fast the model learns
LORA_R = 16 / LORA_ALPHA = 32          # LoRA rank and scaling factor
```

`BATCH_SIZE × GRAD_ACCUM = 16` effective batch size. Low per-step batch but accumulates — saves VRAM.

---

## 2. `create_training_data()` — Loading your blog posts

```python
def create_training_data(posts_dir):
    all_texts = []
    for file_path in sorted(glob.glob(os.path.join(posts_dir, "*.md"))):
        # Read file
        content = f.read()
        # Split on "---" — Jekyll front matter separator
        # e.g. "---\ntitle: Foo\n---\nActual content here"
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()  # Keep only body, discard metadata
        if len(content) < 50:
            continue  # Skip tiny fragments
        all_texts.append(content)
    return all_texts
```

- Globs `_posts/en/*.md` — all your English blog posts (~7785 files)
- Strips Jekyll YAML front matter (the `---...---` block at the top)
- Filters out posts under 50 chars (empty/truncated)
- Each post becomes one training sample

---

## 3. `prepare_dataset()` — Tokenization

```python
def prepare_dataset(texts, tokenizer):
    encodings = tokenizer(
        texts,
        truncation=True,       # Cut off at MAX_LENGTH
        padding=True,          # Pad shorter sequences
        max_length=MAX_LENGTH, # 2048 tokens
        return_tensors="pt",   # Return PyTorch tensors
    )
    return Dataset.from_dict({
        "input_ids": encodings["input_ids"],      # Token IDs
        "attention_mask": encodings["attention_mask"], # 1=real, 0=padding
    })
```

This is pure next-token prediction (causal LM):
- No instruction formatting, no chat template
- The model learns to continue text in your writing style
- `input_ids` = the tokenized posts, `attention_mask` = tells the model which tokens are real vs padding

---

## 4. `train_model()` — The core

### 4a. Model loading

```python
torch_dtype = torch.bfloat16  # 16-bit brain float — good for modern GPUs
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,         # Qwen uses custom code
    torch_dtype=torch_dtype,        # Load in bf16 (saves VRAM vs fp32)
    attn_implementation="flash_attention_2",  # Fast attention kernel
)
model.gradient_checkpointing_enable()  # Trade compute for VRAM
```

- **bf16**: half-precision, but with same exponent range as fp32 — stable training
- **flash_attention_2**: fused CUDA kernel, 2-4x faster than standard attention
- **gradient checkpointing**: doesn't store all activations, recomputes during backward pass — halves VRAM usage at ~20% speed cost

### 4b. LoRA — The key trick for 9B

```python
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,           # Rank — how expressive the adapter is
    lora_alpha=32,  # Scaling factor (alpha/r = 2x multiplier)
    lora_dropout=0.05,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",  # Attention projections
        "gate_proj", "up_proj", "down_proj",       # MLP projections
    ],
)
model = get_peft_model(model, lora_config)
```

**LoRA (Low-Rank Adaptation)** freezes the original 9B weights and injects small trainable matrices (rank 16) into every linear layer. Instead of training 9 billion parameters, you train ~0.5-1% of them.

- `r=16`: each adapter is two matrices (d × 16) and (16 × d) — tiny
- `lora_alpha=32`: scales the adapter output by 32/16 = 2x
- **All 7 projection types** targeted: attention Q/K/V/O + MLP gate/up/down
- Original weights never change → can merge or swap adapters later

### 4c. Training arguments

```python
TrainingArguments(
    learning_rate=2e-5,           # Conservative LR for stable finetuning
    lr_scheduler_type="cosine",   # Smooth decay from peak → 0
    warmup_ratio=0.05,            # 5% of steps to ramp up LR
    weight_decay=0.01,            # L2 regularization
    optim="adamw_torch_fused",    # Fused AdamW — faster
    save_steps=500,               # Checkpoint every 500 steps
    save_total_limit=3,           # Keep only last 3 checkpoints
    logging_steps=10,             # Print loss every 10 steps
)
```

- **Cosine schedule**: starts at 2e-5, ramps up over 5% warmup, then smoothly decays to 0 — standard for finetuning
- **AdamW fused**: combines weight decay into the optimizer step — fewer kernel launches
- **Save strategy**: checkpoint every 500 steps, keep max 3 (disk management)

### 4d. Data collator

```python
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
```

- `mlm=False` = **causal** language modeling (predict next token, not masked tokens)
- Dynamically pads batches to the longest sequence in that batch (saves compute vs padding everything to MAX_LENGTH)

### 4e. Training loop

```python
trainer = Trainer(model=model, args=training_args, train_dataset=dataset, data_collator=data_collator)
trainer.train()
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
```

HuggingFace `Trainer` handles:
- Forward pass → compute loss
- Backward pass → compute gradients
- Gradient accumulation (4 steps → then update)
- Mixed precision (bf16 forward, fp32 gradients)
- Checkpointing, logging, everything

After training, saves the LoRA adapter weights + tokenizer to `trained_model_qwen/`.

---

## 5. To load the trained model later

```python
from peft import PeftModel

base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3.5-9B", trust_remote_code=True)
model = PeftModel.from_pretrained(base, "trained_model_qwen")
```

Or merge into a single model:
```python
model = model.merge_and_unload()  # Fuses LoRA weights back into base
model.save_pretrained("merged_model")
```

---

## VRAM estimate

| Component | VRAM |
|---|---|
| 9B model in bf16 | ~18 GB |
| LoRA adapters | ~0.5 GB |
| Gradients + optimizer states | ~2 GB |
| Activations (with checkpointing) | ~2-4 GB |
| **Total** | **~22-25 GB** |

Needs a 24GB+ GPU (A100/4090/3090). What's your setup? 🦞