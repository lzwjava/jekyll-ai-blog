---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 FinGPT Execution Plan
translated: false
type: note
---

Question: Expand the "Ship the FinGPT-style experiment on your RTX 4070" task into a concrete, runnable plan.

Answer:

Here's the expanded version — a full day-of execution plan, structured so you can copy-paste and iterate in the REPL.

## 1. Ship the FinGPT-style experiment on your RTX 4070 (Highest Priority)

**Why this one first:** It's the single artifact that fuses your three assets — banking domain knowledge, GPU training skill, and AI-native tooling — into one demonstrable portfolio piece. A QLoRA financial-sentiment adapter trained on your own 4070, served via SGLang, with eval numbers, is more persuasive to a hiring manager (or your family) than any résumé line.

### Hardware reality check first

The 4070 has **12 GB VRAM**. That rules out full fine-tuning of an 8B model (needs ~60+ GB). QLoRA (4-bit base + LoRA adapters) on an 8B fits, but it's tight — expect to drop batch size to 1 and lean on gradient accumulation. If you hit OOM, fall back to a 3B (Qwen2.5-3B / Llama-3.2-3B), which trains comfortably and iterates 3–4x faster. For a first end-to-end run, **start at 3B to validate the pipeline, then scale to 8B once it's green.**

### Step 0 — Environment

```bash
ssh lzw@192.168.1.36
mkdir -p ~/fin-sft && cd ~/fin-sft
python -m venv .venv && source .venv/bin/activate
pip install -U "transformers>=4.44" "peft>=0.13" "trl>=0.11" \
    "bitsandbytes>=0.43" "datasets" "accelerate" "scikit-learn"
nvidia-smi   # confirm the 4070 is free before you start
```

### Step 1 — Build the instruction dataset

Skip cloning FinGPT's full repo — their pipeline carries a lot of legacy plumbing you don't need. The valuable part is the *data recipe*. Use the public `financial_phrasebank` set (~4.8K labeled headlines, positive/negative/neutral) as your base and reshape it into instruction format.

```python
# make_dataset.py
from datasets import load_dataset
import json, random

ds = load_dataset("financial_phrasebank", "sentences_50agree", split="train")
label_map = {0: "negative", 1: "neutral", 2: "positive"}

INSTR = "Classify the sentiment of this financial news headline as positive, negative, or neutral."

rows = []
for ex in ds:
    rows.append({
        "messages": [
            {"role": "user", "content": f"{INSTR}\n\nHeadline: {ex['sentence']}"},
            {"role": "assistant", "content": label_map[ex["label"]]},
        ]
    })

random.seed(0)
random.shuffle(rows)
split = int(len(rows) * 0.9)
with open("train.jsonl", "w") as f:
    for r in rows[:split]: f.write(json.dumps(r) + "\n")
with open("eval.jsonl", "w") as f:
    for r in rows[split:]: f.write(json.dumps(r) + "\n")

print(f"train={split} eval={len(rows)-split}")
```

If you want the *real* domain edge: augment this with a few hundred headlines pulled from your bank's actual problem space (earnings, rate moves, credit events) and label them with an LLM call — that's your AI-native dataset-engineering move and what makes the adapter yours rather than a tutorial repro.

### Step 2 — QLoRA training script

```python
# train.py
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

MODEL = "Qwen/Qwen2.5-3B-Instruct"   # bump to 8B after green run

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(
    MODEL, quantization_config=bnb, device_map="auto",
    attn_implementation="sdpa",
)

peft_cfg = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj","k_proj","v_proj","o_proj",
                    "gate_proj","up_proj","down_proj"],
)

train_ds = load_dataset("json", data_files="train.jsonl", split="train")

cfg = SFTConfig(
    output_dir="out",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,   # effective batch 16
    num_train_epochs=3,
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    bf16=True,
    gradient_checkpointing=True,
    logging_steps=10,
    save_strategy="epoch",
    max_seq_length=512,
    packing=False,
)

trainer = SFTTrainer(model=model, args=cfg,
                     train_dataset=train_ds, peft_config=peft_cfg)
trainer.train()
trainer.save_model("out/adapter")
```

```bash
python make_dataset.py
python train.py     # 3B/3 epochs on a 4070 ≈ 15–30 min
watch -n2 nvidia-smi   # in a second pane, confirm you're not OOM-ing
```

**OOM knobs in order:** drop `max_seq_length` to 256 → confirm `gradient_checkpointing=True` → lower `r` to 8 → drop to a 3B if you started at 8B.

### Step 3 — Eval (this is what makes it a portfolio piece, not a toy)

Numbers are the deliverable. Run accuracy + per-class F1 against your held-out set, and compare adapter vs. base to prove the tuning did something.

```python
# eval.py
import json, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from sklearn.metrics import accuracy_score, classification_report

BASE = "Qwen/Qwen2.5-3B-Instruct"
tok = AutoTokenizer.from_pretrained(BASE)
model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16, device_map="auto")
model = PeftModel.from_pretrained(model, "out/adapter").eval()

LABELS = ["positive","negative","neutral"]
def predict(text):
    msgs = [{"role":"user","content":text}]
    ids = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt").to(model.device)
    out = model.generate(ids, max_new_tokens=5, do_sample=False)
    resp = tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True).lower()
    return next((l for l in LABELS if l in resp), "neutral")

rows = [json.loads(l) for l in open("eval.jsonl")]
y_true = [r["messages"][1]["content"] for r in rows]
y_pred = [predict(r["messages"][0]["content"]) for r in rows]

print("acc:", accuracy_score(y_true, y_pred))
print(classification_report(y_true, y_pred, labels=LABELS))
```

### Step 4 — Serve via your existing SGLang setup

SGLang supports LoRA adapters directly, so you don't need to merge first for testing:

```bash
python -m sglang.launch_server \
    --model-path Qwen/Qwen2.5-3B-Instruct \
    --lora-paths fin=out/adapter \
    --port 30000

curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"fin","messages":[{"role":"user",
       "content":"Classify: Bank reports record quarterly losses amid loan defaults"}]}'
```

For deployment (not just testing), merge the adapter into the base weights with `model.merge_and_unload()` and serve the merged checkpoint — slightly faster inference, no adapter-switching overhead.

### Step 5 — Write it up (30 min, compounds forever)

A short post on lzwjava.github.io: dataset recipe, the OOM tuning you actually hit on 12 GB, base-vs-adapter F1 table, SGLang serving snippet. That's the public artifact that does your marketing/credibility work per your own playbook.

### Realistic timeline for today

- 0:00–0:30 env + dataset
- 0:30–1:15 first 3B training run + watch for OOM
- 1:15–1:45 eval, get the numbers
- 1:45–2:15 SGLang serve + sanity prompts
- 2:15–3:00 (optional) scale to 8B if VRAM held, else write-up

That's a full closed loop — train → eval → serve → publish — inside your 3-hour window.

References:

- [FinGPT (AI4Finance)](https://github.com/AI4Finance-Foundation/FinGPT)
- [financial_phrasebank dataset](https://huggingface.co/datasets/financial_phrasebank)
- [TRL SFTTrainer docs](https://huggingface.co/docs/trl/en/sft_trainer)
- [PEFT QLoRA guide](https://huggingface.co/docs/peft/en/developer_guides/quantization)
- [SGLang LoRA serving](https://docs.sglang.ai/backend/lora.html)
