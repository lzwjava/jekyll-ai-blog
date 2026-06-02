---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 LoRA 微调 Qwen 3.5 指南
translated: true
type: note
---

当然——以下是完整指南：

---

## 1. 配置（文件顶部）

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

`BATCH_SIZE × GRAD_ACCUM = 16` 有效 batch size。每个步骤 batch 较小但累积——节省 VRAM。

---

## 2. `create_training_data()` —— 加载你的博客文章

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

- Globs `_posts/en/*.md` —— 所有英文博客文章（~7785 个文件）
- 剥离 Jekyll YAML front matter（顶部 `---...---` 块）
- 过滤掉少于 50 个字符的文章（空或截断）
- 每篇文章成为一个 training sample

---

## 3. `prepare_dataset()` —— Tokenization

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

这是纯 next-token prediction（causal LM）：
- 无 instruction formatting，无 chat template
- 模型学习以你的写作风格继续文本
- `input_ids` = tokenized 文章，`attention_mask` = 告知模型哪些 token 是真实 vs padding

---

## 4. `train_model()` —— 核心部分

### 4a. 模型加载

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

- **bf16**：半精度，但与 fp32 相同的指数范围——稳定 training
- **flash_attention_2**：融合 CUDA kernel，比标准 attention 快 2-4 倍
- **gradient checkpointing**：不存储所有 activations，在 backward pass 时重新计算——VRAM 使用减半，速度代价 ~20%

### 4b. LoRA —— 9B 模型的关键技巧

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

**LoRA (Low-Rank Adaptation)** 冻结原始 9B 权重，并在每个 linear layer 中注入小型可训练矩阵（rank 16）。不是训练 90 亿参数，而是训练 ~0.5-1%。

- `r=16`：每个 adapter 是两个矩阵 (d × 16) 和 (16 × d) —— 很小
- `lora_alpha=32`：将 adapter 输出缩放 32/16 = 2 倍
- **所有 7 种 projection 类型**：attention Q/K/V/O + MLP gate/up/down
- 原始权重永不变——稍后可 merge 或 swap adapters

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

- **Cosine schedule**：从 2e-5 开始，5% warmup 后平滑衰减到 0 —— finetuning 标准
- **AdamW fused**：将 weight decay 结合到 optimizer step —— 更少 kernel launches
- **Save strategy**：每 500 步 checkpoint，保留最多 3 个（磁盘管理）

### 4d. Data collator

```python
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
```

- `mlm=False` = **causal** language modeling（预测下一个 token，而不是 masked tokens）
- 动态将 batch 填充到该 batch 中最长序列（比填充到 MAX_LENGTH 节省计算）

### 4e. Training loop

```python
trainer = Trainer(model=model, args=training_args, train_dataset=dataset, data_collator=data_collator)
trainer.train()
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
```

Hugging Face `Trainer` 处理：
- Forward pass → 计算 loss
- Backward pass → 计算 gradients
- Gradient accumulation（4 步 → 然后 update）
- Mixed precision（bf16 forward，fp32 gradients）
- Checkpointing、logging 等一切

训练后，将 LoRA adapter 权重 + tokenizer 保存到 `trained_model_qwen/`。

---

## 5. 稍后加载训练好的模型

```python
from peft import PeftModel

base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3.5-9B", trust_remote_code=True)
model = PeftModel.from_pretrained(base, "trained_model_qwen")
```

或 merge 成单个模型：
```python
model = model.merge_and_unload()  # Fuses LoRA weights back into base
model.save_pretrained("merged_model")
```

---

## VRAM 估算



| 组件 | VRAM |
|---|---|
| bf16 中的 9B 模型 | ~18 GB |
| LoRA adapters | ~0.5 GB |
| Gradients + optimizer states | ~2 GB |
| Activations（带 checkpointing） | ~2-4 GB |
| **总计** | **~22-25 GB** |

需要 24GB+ GPU (A100/4090/3090)。你的配置是什么？🦞
