---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Answers Change Fine-Tuning Strategy
translated: false
type: note
---

**Question:** Those 10k notes are AI-generated answers (I asked the questions, the AI wrote the responses) — not my own writing. Does that change the plan?

**Answer:**

Yes, it changes what fine-tuning gets you — and what the real asset is.

## What you'd actually be training

SFT on AI-written answers = **distillation**. The model doesn't learn "lzwjava's voice" — it learns to imitate whatever models wrote those answers (deepseek, gpt, etc.), compressed into a smaller student. That's still a legitimate and interesting project, but be clear-eyed about it:

- **Quality ceiling = the teacher models.** You're cloning their style and their mistakes from 2023–2026, frozen.
- **Inconsistent teacher.** 10k answers from different models/eras/styles → the student learns a muddy average. Mixed-teacher SFT data is measurably worse than single-teacher data.
- **License note:** OpenAI's ToS prohibits using outputs to train competing models; DeepSeek's outputs are permissively licensed. If your notes mix sources, that matters for anything public.

## The real asset: your 10k questions

The answers are commodity — any frontier model can regenerate them better today. The **questions are the irreplaceable part**: a curated curriculum of what a self-taught AI engineer actually asks, in order, across kernel internals → GPU compute → transformers. That's a high-quality prompt distribution that no public dataset has.

So the better pipeline is: **keep your questions, throw away the stale answers, regenerate with one consistent teacher.**

```python
# regen_answers.py — rebuild the dataset with a single, current teacher
import json, asyncio
from openai import AsyncOpenAI  # OpenRouter

client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1")
MODEL = "deepseek/deepseek-v4-pro"   # permissive outputs, one consistent style

SYSTEM = """You are a technical tutor for an experienced self-taught engineer.
Answer from first principles, code-first, minimal fluff, English."""

sem = asyncio.Semaphore(20)

async def regen(q):
    async with sem:
        r = await client.chat.completions.create(
            model=MODEL, max_tokens=2000,
            messages=[{"role": "system", "content": SYSTEM},
                      {"role": "user", "content": q}])
        return {"conversations": [
            {"role": "user", "content": q},
            {"role": "assistant", "content": r.choices[0].message.content}]}

async def main():
    qs = [json.loads(l)["conversations"][0]["content"]
          for l in open("notes_sft.jsonl")]
    results = await asyncio.gather(*[regen(q) for q in qs])
    with open("notes_sft_v2.jsonl", "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

asyncio.run(main())
```

Cost check: 10k questions × ~1.5k output tokens ≈ 15M tokens — pocket change on deepseek pricing, or just burn part of the free Xiaomi MiMo quota and distill mimo-2.5-pro instead. Then run the exact same Unsloth training from my previous answer on `notes_sft_v2.jsonl`. What you get: a 4B–8B local model distilled onto *your* question distribution — a personal offline tutor whose competence is concentrated exactly where your curiosity is. That's a genuinely useful artifact for the M2 Air via GGUF.

## If you want a model with *your* voice

Your ~400 blog posts are the only human-written corpus you have. That's maybe 0.5–2M tokens — too small for SFT alone, but two viable moves:

1. **Style LoRA on top of the distilled model**: low-LR (5e-5), 1 epoch of continued pretraining on raw blog text after the SFT stage. Enough to shift tone, not enough to teach knowledge.
2. **Mine your git history**: if you've ever hand-edited any AI answers in the repo, `git log -p` gives you (AI draft → your edit) pairs — that's free DPO data, and the most "you" signal that exists in the whole repo.

```bash
# find posts you've actually edited after initial commit (DPO candidates)
cd jekyll-ai-blog
git log --format= --name-only --diff-filter=M -- '_posts/*.md' | sort | uniq -c | sort -rn | head -50
```

## Bottom line

1. Don't SFT on the stale mixed-teacher answers — regenerate with one teacher using your questions.
2. Distill into Qwen3-4B/8B (4070 for iteration, MI300X for the big run).
3. Optionally layer a style LoRA from your 400 blog posts, and mine git edits for DPO pairs.

This version of the project is also strictly better résumé-wise: "built a distillation pipeline (prompt mining → synthetic regeneration → SFT → DPO)" is real dataset engineering, which is exactly the muscle you said you want to build.
