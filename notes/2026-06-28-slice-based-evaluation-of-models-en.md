---
audio: false
generated: true
image: false
lang: en
layout: post
title: Slice-Based Evaluation of Models
translated: false
type: note
---

Question: I've figured out how to evaluate a trained model — categorize inputs by prompt length, programming language, and topic, then pick representative examples for a lightweight eval. This kind of hands-on, exploratory understanding of training/inference/eval is genuinely pleasurable to the mind, and with an agent helping run experiments, nothing is hard. Right?

Answer:

Right — and the instinct you arrived at (stratified sampling across input dimensions) is exactly what serious eval harnesses formalize. You discovered it by building, which is the durable way. Let me push it one layer deeper so the intuition compounds.

What you described is **slice-based evaluation**. The core idea: a single aggregate score (perplexity, mean accuracy) hides failure modes. You decompose the input distribution into slices and measure per-slice, because a model can be great on short English prompts and collapse on long multi-turn Rust ones — the average lies.

Your three axes are good. The thing to internalize is *why* each one matters mechanistically:

- **Prompt length** → tests positional generalization and KV-cache/attention behavior at lengths beyond what dominated training. A GPT-2-scale model trained mostly on short sequences degrades past its effective context. This is where you catch length extrapolation failures.
- **Programming language** → tests tokenizer efficiency and data-mix coverage. Languages with sparse training representation tokenize worse (more tokens per semantic unit) and have higher loss. This directly reflects your dataset composition.
- **Topic** → tests domain coverage and is where you'll see the long tail of knowledge gaps.

The piece your description is missing: **a scoring function per slice**. "Pick some examples" gives you inputs; you still need a metric. For a base LM, options ranked by build-cost:

```python
# Cheapest, no labels needed: per-slice loss/perplexity
import torch, torch.nn.functional as F

@torch.no_grad()
def slice_perplexity(model, tokenizer, prompts, device="cuda"):
    losses = []
    for p in prompts:
        ids = tokenizer.encode(p, return_tensors="pt").to(device)
        logits = model(ids).logits
        # shift: predict token t from tokens <t
        loss = F.cross_entropy(
            logits[:, :-1].reshape(-1, logits.size(-1)),
            ids[:, 1:].reshape(-1),
        )
        losses.append(loss.item())
    mean = sum(losses) / len(losses)
    return {"ppl": float(torch.exp(torch.tensor(mean))), "n": len(prompts)}

slices = {
    "short_python":  [...],
    "long_python":   [...],
    "short_rust":    [...],
    "long_prose_en": [...],
}
report = {name: slice_perplexity(model, tok, ps) for name, ps in slices.items()}
```

Perplexity is free (no labels) and catches a lot. But it measures *next-token surprise*, not *task success*. For code specifically, the gold-standard eval is **functional correctness**, not loss — pass@k on executable tests (HumanEval-style), because a model can have low loss and still emit code that doesn't run.

```python
# pass@1 sketch: generate, execute against a test, count passes
def pass_at_1(model, problems):  # problems: [{"prompt", "test", "entry_point"}]
    passed = 0
    for prob in problems:
        code = generate(model, prob["prompt"])          # your sampling fn
        ns = {}
        try:
            exec(code + "\n" + prob["test"], ns)         # run in a sandbox in practice
            ns["check"](ns[prob["entry_point"]])
            passed += 1
        except Exception:
            pass
    return passed / len(problems)
```

Three principles that separate a toy eval from one you'll trust:

1. **Lock the eval set and version it.** The moment your eval set drifts, scores across checkpoints aren't comparable. A frozen 200-example set beats a fresh 2000-example one for tracking training progress.
2. **Watch contamination.** If eval prompts leaked into training data, your numbers are fiction. With nanoGPT-scale data you control this; keep a held-out split that never touches training.
3. **Sampling settings are part of the eval.** pass@k at temperature 0 vs 0.8 are different measurements. Pin temperature, top-p, and max tokens, or you're measuring noise.

On the "with an agent, nothing is hard" feeling — mostly true, and the joy is real. The one caution: agents make it cheap to *generate* evals and easy to *not notice when the eval itself is broken*. The hard part was never running the experiment; it's trusting the number. A green pass@1 of 0.9 means nothing if the test harness silently swallowed exceptions. So the discipline that compounds isn't "run more experiments" — it's "be suspicious of every metric until I've seen it move in the direction physics says it should" (e.g., loss must drop as you train; pass@k on contaminated data is a smell, not a win).

You've got the right loop. Add a scoring function, freeze the set, and treat your eval harness with the same suspicion you'd treat a model's output.
