---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fine-Tune on 10k Jekyll Notes
translated: false
type: note
---

**Question:** I have ~10k notes at lzwjava.github.io (Jekyll repo: github.com/lzwjava/jekyll-ai-blog). I want to fine-tune a model on them — what should I do?

**Answer:**

First, the honest framing: 10k notes ≈ **8–15M tokens**. That's far too small for pretraining, but it's a *very* good SFT dataset — especially because your notes-en corpus is literally already in Q&A format (title = question, body = answer). Fine-tuning will teach a model your **voice, format, and answer style**, not reliable factual recall of every note's content (for recall, RAG wins; weights are a lossy compressor at this data scale). The interesting project here is: **"a model that answers like lzwjava's notes"** — and that's exactly what SFT does well.

## Step 1 — Extract the dataset from Jekyll

Your posts are markdown with YAML front matter. Parse them into `{question, answer}` pairs:

```python
# build_dataset.py
import json, re
from pathlib import Path
import frontmatter  # pip install python-frontmatter

POSTS = Path("jekyll-ai-blog/_posts")  # or wherever notes live
out = open("notes_sft.jsonl", "w")

LIQUID = re.compile(r"{[%{].*?[%}]}", re.DOTALL)

n = 0
for f in sorted(POSTS.rglob("*.md")):
    post = frontmatter.load(f)
    if post.get("lang", "en") != "en":      # English only
        continue
    title = post.get("title", "").strip()
    body = LIQUID.sub("", post.content).strip()
    if not title or len(body) < 300:        # drop stubs
        continue
    out.write(json.dumps({
        "conversations": [
            {"role": "user", "content": title},
            {"role": "assistant", "content": body},
        ]
    }, ensure_ascii=False) + "\n")
    n += 1

print(f"{n} examples")
```

Then sanity-check token count and dedupe:

```bash
python -c "
import json, tiktoken
enc = tiktoken.get_encoding('cl100k_base')
tot = sum(len(enc.encode(json.loads(l)['conversations'][1]['content'])) for l in open('notes_sft.jsonl'))
print(f'{tot/1e6:.1f}M assistant tokens')"
```

Hold out ~200 examples as an eval set before training. Also filter aggressively — 7k clean examples beat 10k noisy ones. Drop notes that are pure link dumps, config snippets without prose, or duplicated answers.

## Step 2 — Pick model + machine

| Setup | Model | Method | Why |
|---|---|---|---|
| RTX 4070 (12GB) | Qwen3-4B / Llama-3.1-8B | QLoRA 4-bit | Fits in 12GB with Unsloth; free iteration |
| MI300X ($2/hr) | Qwen3-32B or Llama-3.3-70B | LoRA 16-bit | 192GB HBM3 lets you LoRA a 70B on one GPU |

Unsloth now officially supports AMD — its Triton kernels were ported to HIP/ROCm in collaboration with the ROCm team, verified on real MI300X hardware. Install on the MI300X box:

```bash
python3 -m venv unsloth_env && source unsloth_env/bin/activate
pip install torch torchvision torchao xformers --index-url https://download.pytorch.org/whl/rocm6.4
pip install --no-deps unsloth unsloth-zoo
pip install "unsloth[amd] @ git+https://github.com/unslothai/unsloth"
```

(ROCm systems need a pre-release bitsandbytes build — versions ≤ 0.49.2 have a 4-bit decode NaN bug on AMD GPUs — only matters if you go 4-bit; on MI300X just use 16-bit LoRA.)

## Step 3 — Train

```python
# train.py — works on both 4070 (CUDA) and MI300X (ROCm)
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig

model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-8B",          # 70B on MI300X if you want
    max_seq_length=4096,
    load_in_4bit=True,            # False on MI300X
)
model = FastLanguageModel.get_peft_model(
    model, r=32, lora_alpha=32,
    target_modules=["q_proj","k_proj","v_proj","o_proj",
                    "gate_proj","up_proj","down_proj"],
)

ds = load_dataset("json", data_files="notes_sft.jsonl", split="train")
ds = ds.map(lambda x: {"text": tokenizer.apply_chat_template(
    x["conversations"], tokenize=False)})

trainer = SFTTrainer(
    model=model, tokenizer=tokenizer, train_dataset=ds,
    args=SFTConfig(
        per_device_train_batch_size=2,   # 64+ on MI300X
        gradient_accumulation_steps=8,
        num_train_epochs=2,              # small data — don't go past 3
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        bf16=True, logging_steps=10,
        output_dir="lzw-notes-lora",
        packing=True,                    # critical for short Q&A pairs
    ),
)
trainer.train()
model.save_pretrained_merged("lzw-notes-merged", tokenizer)
```

With ~10M tokens, 2 epochs on an 8B QLoRA is a few hours on the 4070; on MI300X with batch 64+ it's well under an hour — one $2 droplet session covers many experiments. Watch eval loss; with data this small, **overfitting (memorized phrasing, repetition) shows up fast after epoch 2–3**.

## Step 4 — Eval and serve

Vibe-eval against the base model on your 200 held-out titles: generate both, diff the style. Then export for local use:

```bash
# GGUF for llama.cpp / ollama on the M2 Air
model.save_pretrained_gguf("lzw-notes-gguf", tokenizer, quantization_method="q4_k_m")
# Or serve on the 4070 box:
vllm serve ./lzw-notes-merged --max-model-len 4096
```

## Recommended path

1. **This weekend, 4070**: build dataset → QLoRA Qwen3-4B → see if the "lzwjava voice" emerges. Total cost: $0.
2. **Once the pipeline works, MI300X**: same script, LoRA a 32B/70B 16-bit, batch 64. This is also exactly the muscle memory that transfers to your nanochat/DeepSeek ambitions — the SFT stage of nanochat is this same loop, just hand-rolled.
3. **Stretch**: take the LoRA'd model + DPO pairs (your edited answers vs raw model answers) — that's a natural next step into the RLHF/DPO territory you want to learn.

**References:**

- [Unsloth — Fine-tuning LLMs on AMD GPUs (MI300X)](https://unsloth.ai/docs/new/fine-tuning-llms-on-amd-gpus-with-unsloth)
- [Unsloth AMD install guide](https://unsloth.ai/docs/get-started/install/amd)
- [AMD blog — fine-tuning Llama-3.3-70B LoRA on a single MI300X with Unsloth](https://www.amd.com/en/developer/resources/technical-articles/2025/10x-model-fine-tuning-using-synthetic-data-with-unsloth.html)
- [llm-tracker — AMD GPU training notes (torchtune vs axolotl vs unsloth)](https://llm-tracker.info/howto/AMD-GPUs)
