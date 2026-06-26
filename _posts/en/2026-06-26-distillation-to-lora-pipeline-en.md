---
audio: false
generated: true
image: false
lang: en
layout: post
title: Distillation to LoRA Pipeline
translated: false
type: note
---

**Question:** How do I actually build the distillation → LoRA pipeline — frontier model generates instruction data from my SEC corpus, then LoRA a small model on it, with a downstream-task benchmark?

**Answer:**

Here's the full pipeline, build-first. Four stages: **slice corpus → distill instructions → LoRA train → eval against zero-shot baseline**. I'll give you runnable code for each. Targets your 4070 first (fast iteration), MI300X for scale-up.

The core insight driving the design: you're not teaching the model *finance* (frontier models know it). You're teaching it your *task format* — turning a strong generalist into a reliable, cheap, structured-output specialist. That's distillation: big teacher → small student on a narrow task.

---

## Stage 0: Architecture

```
SEC .npy tokens  ──(detokenize)──>  raw 10-K text sections
                                          │
                                          ▼
                          ┌─────────────────────────────┐
                          │ TEACHER (V4-Pro / Opus API)  │
                          │ section → instruction pair   │
                          └─────────────────────────────┘
                                          │  ~5k JSONL pairs
                                          ▼
                          ┌─────────────────────────────┐
                          │ STUDENT (Qwen3-8B + LoRA)    │
                          │ trained on pairs, 4070       │
                          └─────────────────────────────┘
                                          │
                                          ▼
                   EVAL: student-LoRA vs student-zeroshot vs teacher
                          on held-out tasks (exact-match / F1)
```

You picked the goal in the picker — I'll write Stage 1 to support both **extraction** and **QA/summarization** since those were the live options; you just flip a flag.

---

## Stage 1: Recover text from your .npy shards

You tokenized with GPT-2 BPE, so detokenize back to clean section text. Don't feed raw token IDs to the teacher — feed readable filings.

```python
# detok.py — recover 10-K text sections from your tokenized shards
import numpy as np, tiktoken, re, json

enc = tiktoken.get_encoding("gpt2")
shard = np.load("/mnt/data/zz/datasets/sec-edgar-tok/val_000000.npy")  # use val to avoid train leakage later

text = enc.decode(shard[:5_000_000].tolist())  # decode a chunk; full shard is huge

# 10-Ks have natural section markers — split on them
SECTION_RE = re.compile(r"(Item\s+\d+[A-Z]?\.\s)", re.IGNORECASE)
parts = SECTION_RE.split(text)
# stitch marker+body back together, keep sections 800-6000 chars (fits teacher context, non-trivial)
sections = []
for i in range(1, len(parts)-1, 2):
    sec = (parts[i] + parts[i+1]).strip()
    if 800 <= len(sec) <= 6000:
        sections.append(sec)

print(f"{len(sections)} usable sections")
with open("sections.jsonl", "w") as f:
    for s in sections[:6000]:           # cap — you only need a few thousand
        f.write(json.dumps({"text": s}) + "\n")
```

Why val shard: you'll hold some of these out for eval, and you want zero overlap with anything the student might later see. Keep train shards reserved if you scale up.

---

## Stage 2: Distill — teacher generates instruction pairs

This is the heart of it. The teacher reads a section and emits a `(instruction, input, output)` triple. Structured output = your eval is mechanical later.

{% raw %}

```python
# distill.py — frontier model turns raw sections into training pairs
import json, os, asyncio, aiohttp

TASK = os.environ.get("TASK", "extraction")   # "extraction" | "qa"

EXTRACTION_PROMPT = """You are building a training dataset. Given this 10-K section, output STRICT JSON only (no markdown fence):
{{"instruction": "Extract the structured fields from this SEC filing section.",
  "input": "<the section text, verbatim>",
  "output": {{"section_type": "...", "key_risks": ["..."], "financial_figures": [{{"label":"...","value":"..."}}], "fiscal_period": "..."}}}}
Only include fields actually present. Section:
---
{section}"""

QA_PROMPT = """Given this 10-K section, generate ONE high-quality question a financial analyst would ask, and its answer grounded ONLY in the text. Output STRICT JSON only:
{{"instruction":"Answer the question using only the filing section provided.",
  "input":"Question: <q>\\n\\nSection: {section}",
  "output":"<concise grounded answer>"}}
Section:
---
{section}"""

PROMPT = EXTRACTION_PROMPT if TASK == "extraction" else QA_PROMPT

async def call(session, section):
    body = {
        "model": "deepseek-v4-pro",          # your top model; swap to claude-opus if you prefer
        "max_tokens": 1500,
        "messages": [{"role": "user", "content": PROMPT.format(section=section)}],
    }
    headers = {"Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}",
               "Content-Type": "application/json"}
    async with session.post("https://api.deepseek.com/v1/chat/completions",
                            json=body, headers=headers) as r:
        data = await r.json()
        return data["choices"][0]["message"]["content"]

async def main():
    sections = [json.loads(l)["text"] for l in open("sections.jsonl")]
    sem = asyncio.Semaphore(16)              # concurrency — tune to your rate limit
    async def worker(sec, fout):
        async with sem:
            try:
                raw = await call(session, sec)
                pair = json.loads(raw.strip().removeprefix("```json").removesuffix("```").strip())
                if {"instruction","input","output"} <= pair.keys():
                    fout.write(json.dumps(pair) + "\n"); fout.flush()
            except Exception as e:
                print("skip:", e)
    async with aiohttp.ClientSession() as session, open(f"pairs_{TASK}.jsonl","w") as fout:
        await asyncio.gather(*[worker(s, fout) for s in sections])

asyncio.run(main())
```

{% endraw %}

Cost check: 5k sections × ~2k tokens in + ~500 out. At V4-Flash input $0.14/M, output $0.28/M, that's roughly **$1.50–3 total**. Even V4-Pro is under $15. Negligible for you. Run it on the Air — it's just API calls.

**Validate the dataset before training** (garbage pairs = garbage student):

```python
# inspect.py — sanity gate
import json
pairs = [json.loads(l) for l in open(f"pairs_extraction.jsonl")]
print(f"{len(pairs)} pairs")
# for extraction, check output parses as the expected schema
bad = sum(1 for p in pairs if not isinstance(p["output"], (dict,str)))
print(f"malformed outputs: {bad}")
print(json.dumps(pairs[0], indent=2)[:800])
```

Hold out 300 pairs as your eval set **now**, before training — `head -n 300 > eval.jsonl`, rest → `train.jsonl`.

---

## Stage 3: LoRA the student (Qwen3-8B on the 4070)

Use `unsloth` — it's the fastest path on a single consumer GPU, fits 8B + LoRA in 12GB via 4-bit, and the iteration speed matches your vibe-coding workflow. (TRL/PEFT is the more vanilla alternative if you want fewer abstractions.)

```python
# train_lora.py — QLoRA on the 4070
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig
import json

model, tok = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-8B-unsloth-bnb-4bit",   # 4-bit, fits 12GB
    max_seq_length=4096, load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=32, lora_dropout=0,
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
)

def fmt(ex):
    out = ex["output"] if isinstance(ex["output"], str) else json.dumps(ex["output"])
    msgs = [{"role":"user","content": ex["instruction"]+"\n\n"+ex["input"]},
            {"role":"assistant","content": out}]
    return {"text": tok.apply_chat_template(msgs, tokenize=False)}

ds = load_dataset("json", data_files="train.jsonl")["train"].map(fmt)

trainer = SFTTrainer(
    model=model, tokenizer=tok, train_dataset=ds,
    args=SFTConfig(
        per_device_train_batch_size=2, gradient_accumulation_steps=4,
        warmup_steps=20, num_train_epochs=3, learning_rate=2e-4,
        fp16=True, logging_steps=10, output_dir="out-sec-lora",
        optim="adamw_8bit", lr_scheduler_type="cosine",
    ),
)
trainer.train()
model.save_pretrained("out-sec-lora")   # adapter only, ~100MB
```

On the 4070, 5k pairs × 3 epochs ≈ **20–40 min**. This is the fast loop — iterate on data quality here. Once it works, optionally rerun the *same script* on the MI300X with V4-Flash or a 32B student for the "production" version; the code barely changes.

---

## Stage 4: The eval that actually lands internally

This is what makes the difference between "I trained a thing" and "here's a measurable capability." Three-way comparison on your held-out 300 pairs: **teacher (ceiling) vs student-zeroshot (baseline) vs student-LoRA (your result)**.

```python
# eval.py — the money artifact
import json
from unsloth import FastLanguageModel

eval_set = [json.loads(l) for l in open("eval.jsonl")]

def score_extraction(pred, gold):
    # field-level F1 on extracted keys; robust to ordering
    try:
        p, g = json.loads(pred), gold if isinstance(gold,dict) else json.loads(gold)
    except: return 0.0
    pk, gk = set(map(str,_flatten(p))), set(map(str,_flatten(g)))
    if not gk: return 1.0 if not pk else 0.0
    tp = len(pk & gk)
    prec = tp/len(pk) if pk else 0; rec = tp/len(gk)
    return 2*prec*rec/(prec+rec) if (prec+rec) else 0.0

def _flatten(o, pre=""):
    if isinstance(o,dict):
        for k,v in o.items(): yield from _flatten(v, f"{pre}.{k}")
    elif isinstance(o,list):
        for v in o: yield from _flatten(v, pre)
    else: yield f"{pre}={o}"

def gen(model, tok, ex):
    msgs=[{"role":"user","content":ex["instruction"]+"\n\n"+ex["input"]}]
    ids=tok.apply_chat_template(msgs, return_tensors="pt", add_generation_prompt=True).to(model.device)
    out=model.generate(ids, max_new_tokens=512, do_sample=False)
    return tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True)

# load base (zero-shot) and LoRA versions, score both
for tag, adapter in [("zeroshot", None), ("lora", "out-sec-lora")]:
    model, tok = FastLanguageModel.from_pretrained("unsloth/Qwen3-8B-unsloth-bnb-4bit",
                    max_seq_length=4096, load_in_4bit=True)
    if adapter: model.load_adapter(adapter)
    FastLanguageModel.for_inference(model)
    scores=[score_extraction(gen(model,tok,ex), ex["output"]) for ex in eval_set]
    print(f"{tag}: mean F1 = {sum(scores)/len(scores):.3f}")
```

The headline becomes a single table:

| Model | Field-F1 | Cost/1k calls | Latency |
|---|---|---|---|
| V4-Pro (teacher) | 0.91 | $X | high |
| Qwen3-8B zero-shot | 0.58 | local | low |
| **Qwen3-8B + LoRA (yours)** | **0.84** | **local** | **low** |

*That* is the internal pitch: "I distilled a frontier model into an 8B that runs on-prem, hits 92% of teacher quality at zero API cost and no data leaving the bank." For a bank, the **on-prem + no-data-egress** angle is worth more than the F1 number — it's a compliance win, not just an ML win.

---

## Build order (fastest to signal)

1. **Today:** Stage 1+2 on the Air → get `pairs_extraction.jsonl`, eyeball 10 pairs. (~1hr, mostly API wait)
2. **Tomorrow:** Stage 3 on the 4070 → 30min train, confirm it generates valid JSON. (~2hr with debugging)
3. **Then:** Stage 4 → the three-way table. (~1hr)
4. **Optional scale-up:** rerun student as V4-Flash-LoRA on MI300X if the 8B shows signal and you want the bigger headline.

Total to a shareable artifact: ~1 weekend, and unlike the GPT-2 run, the output is a *measurable task win* plus a reusable distillation harness you can re-point at any internal corpus — which is the actual transferable asset.

Two gotchas to flag up front: (1) Qwen3 has thinking mode — disable it for structured extraction (`enable_thinking=False` in the chat template) or it'll wrap JSON in reasoning. (2) Greedy decode (`do_sample=False`) for eval reproducibility, but check the teacher didn't generate near-identical outputs across sections, or you're measuring memorization, not extraction.

Want me to write the MI300X scale-up variant (V4-Flash student, multi-GPU LoRA config) as a drop-in for Stage 3, or flesh out the QA-task eval (F1 over answer tokens instead of fields)?
