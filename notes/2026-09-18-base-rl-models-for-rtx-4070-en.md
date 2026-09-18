---
audio: false
generated: true
image: false
lang: en
layout: post
title: Base RL Models for RTX 4070
translated: false
type: note
---

**Question:** Can you give me a base (non-instruct) model recommendation for this RL experiment on an RTX 4070?

**Answer:**

Yes — for GRPO/RL experiments you **always want a base model**, not an instruct model. Here's why and what to use:

---

## Why Base Model for RL?

- **Instruct models** are already RLHF-tuned — you're fighting against existing alignment, reward hacking is harder to observe
- **Base models** are a blank slate — the RL reward signal has full control, you can clearly see the policy learning
- This is exactly how DeepSeek-R1 and Qwen's thinking mode were built: **base → RL directly** (no SFT warmup needed for small experiments)

---

## Best Base Models for RTX 4070 (12 GB)

| Model | VRAM (4-bit) | Speed | RL Suitability |
| --- | --- | --- | --- |
| `Qwen/Qwen2.5-1.5B` | ~1.1 GB | Very fast | ⭐⭐⭐ Best for quick iteration |
| `Qwen/Qwen2.5-3B` | ~2.0 GB | Fast | ⭐⭐⭐ Good balance |
| `Qwen/Qwen2.5-7B` | ~4.5 GB | Moderate | ⭐⭐⭐ Strongest results |
| `microsoft/Phi-4-mini` | ~2.5 GB | Fast | ⭐⭐ Good reasoning base |
| `google/gemma-3-1b-pt` | ~0.9 GB | Fastest | ⭐ Weaker but tiny |

**Recommended: `Qwen/Qwen2.5-1.5B`** for first experiments, then scale to `Qwen/Qwen2.5-7B` once your reward function is validated.

---

## Updated Full Script with Base Model

```python
# rl_grpo_base.py
# GRPO RL experiment using Qwen2.5-1.5B BASE model on RTX 4070
# Goal: teach chain-of-thought math reasoning from scratch via RL only

import re
import random
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model
from trl import GRPOConfig, GRPOTrainer

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_ID   = "Qwen/Qwen2.5-1.5B"   # BASE model, not instruct
OUTPUT_DIR = "./grpo_qwen1.5b_math"

# ── 1. Load model in 4-bit ────────────────────────────────────────────────────
bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,   # saves ~0.4 GB extra
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "left"      # important for generation

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb,
    device_map="cuda",
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",  # saves VRAM, faster
)

# ── 2. LoRA adapter — only train ~1% of weights ───────────────────────────────
lora_cfg = LoraConfig(
    r=16,                 # rank: 16 is a good default
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_cfg)
model.print_trainable_parameters()
# Expected output: trainable params: ~8M || all params: 1.54B || ~0.5%

# ── 3. Dataset — arithmetic with varying difficulty ───────────────────────────
SYSTEM = (
    "You are a math solver. Think step by step inside <think>...</think> "
    "tags, then give the final numeric answer after </think>."
)

def make_problem():
    level = random.choice(["easy", "medium", "hard"])
    if level == "easy":
        a, b = random.randint(1, 20), random.randint(1, 20)
        expr = f"{a} + {b}"
    elif level == "medium":
        a, b, c = random.randint(1, 15), random.randint(1, 10), random.randint(1, 5)
        expr = f"{a} * {b} + {c}"
    else:
        a, b, c = random.randint(2, 12), random.randint(2, 8), random.randint(1, 10)
        expr = f"({a} + {b}) * {c}"
    answer = str(eval(expr))
    prompt = f"{SYSTEM}\n\nProblem: {expr} = ?"
    return {"prompt": prompt, "answer": answer}

random.seed(42)
data = [make_problem() for _ in range(800)]
dataset = Dataset.from_list(data).train_test_split(test_size=0.1)

# ── 4. Reward function — multi-signal ─────────────────────────────────────────
def extract_answer(text: str) -> str | None:
    """Pull the last number after </think> tag."""
    after_think = text.split("</think>")[-1] if "</think>" in text else text
    nums = re.findall(r"-?\d+\.?\d*", after_think)
    return str(int(float(nums[-1]))) if nums else None

def reward_fn(completions, answer, **kwargs) -> list[float]:
    rewards = []
    for completion, gold in zip(completions, answer):
        # TRL passes completions as list-of-dicts or plain string
        text = completion[0]["content"] if isinstance(completion, list) else completion
        r = 0.0

        # Format reward: has <think> block?
        has_think = "<think>" in text and "</think>" in text
        if has_think:
            r += 0.2
            # Bonus for non-trivial reasoning (>20 chars inside tags)
            think_content = re.findall(r"<think>(.*?)</think>", text, re.DOTALL)
            if think_content and len(think_content[0].strip()) > 20:
                r += 0.1

        # Correctness reward
        pred = extract_answer(text)
        if pred is not None and pred == gold:
            r += 1.0           # correct answer
        elif pred is not None:
            r -= 0.3           # wrong answer (penalize, not harshly)
        else:
            r -= 0.5           # no answer extracted at all

        rewards.append(r)
    return rewards

# ── 5. GRPO config tuned for 12 GB ───────────────────────────────────────────
grpo_args = GRPOConfig(
    output_dir=OUTPUT_DIR,
    num_train_epochs=5,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,    # effective batch = 16
    learning_rate=5e-6,               # lower LR for base model stability
    warmup_ratio=0.05,
    num_generations=4,                # GRPO group size G=4
    max_prompt_length=256,
    max_completion_length=400,
    temperature=1.0,                  # high temp for exploration early on
    beta=0.02,                        # KL penalty — low for base model
    loss_type="grpo",
    optim="paged_adamw_8bit",
    bf16=True,
    fp16=False,
    gradient_checkpointing=True,      # trades compute for ~3 GB VRAM saving
    logging_steps=10,
    eval_steps=50,
    save_steps=100,
    report_to="none",                 # set "wandb" if you want tracking
    seed=42,
)

# ── 6. Train ──────────────────────────────────────────────────────────────────
trainer = GRPOTrainer(
    model=model,
    args=grpo_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    reward_funcs=reward_fn,
    processing_class=tokenizer,
)

print("=" * 60)
print(f"Model:     {MODEL_ID}")
print(f"Task:      Math reasoning via GRPO")
print(f"Train size:{len(dataset['train'])} | Eval: {len(dataset['test'])}")
print("=" * 60)

trainer.train()
trainer.save_model(f"{OUTPUT_DIR}/final")
tokenizer.save_pretrained(f"{OUTPUT_DIR}/final")
print("Done — LoRA adapter saved.")

# ── 7. Quick eval ─────────────────────────────────────────────────────────────
def test_model(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

print("\n── Test after training ──")
test_prompt = f"{SYSTEM}\n\nProblem: (7 + 5) * 3 = ?"
print(test_model(test_prompt))
```

---

## What to Watch During Training

```
Step  10 | reward: 0.12  ← model barely reasoning yet
Step  50 | reward: 0.45  ← starting to use <think> tags
Step 150 | reward: 0.78  ← answers mostly correct
Step 300 | reward: 1.05  ← solid reasoning chains forming
```

The reward climbing over steps is the RL signal working. If it plateaus early, lower `beta` (less KL penalty) or raise `temperature`.

---

## Install in One Command

```bash
pip install torch transformers trl peft bitsandbytes datasets flash-attn --upgrade
```

If `flash-attn` fails to build, just remove `attn_implementation="flash_attention_2"` from the model load — it's optional but saves ~1.5 GB VRAM.

**References:**

- [Qwen2.5-1.5B base on HuggingFace](https://huggingface.co/Qwen/Qwen2.5-1.5B)
- [TRL GRPOTrainer docs](https://huggingface.co/docs/trl/grpo_trainer)
- [DeepSeek-R1 paper (GRPO origin)](https://arxiv.org/abs/2501.12948)
- [PEFT LoRA docs](https://huggingface.co/docs/peft/conceptual_guides/lora)
