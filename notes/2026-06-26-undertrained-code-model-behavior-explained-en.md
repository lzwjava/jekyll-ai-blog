---
audio: false
generated: true
image: false
lang: en
layout: post
title: Undertrained Code Model Behavior Explained
translated: false
type: note
---

**Question:** Now that I've prompted with a real 57-token code prefix, the output is no longer pure whitespace — it's code-like tokens (`case`, `data_type`, `static`, `return 1;`, `p_count = 0`, C/C++ fragments) but still incoherent. How do I explain this?

**Answer:**

This output tells a completely different and much more reassuring story than the first one. Read what changed:

- Context went from `seq_len=3` → `seq_len=57`.
- Output went from "pure whitespace + `<div>`" → **actual code morphology**: `case`, `data_type`, `static_p__p`, `return 1;`, `p_count = 0`, `<< "name"`, `0x[0x]`, `%2.first`, `@v`.

**The model is conditioning on context now.** It is not collapsing to the unigram prior anymore. So your earlier garbage was *primarily* the short-context / sampling problem, not dead weights. The model learned real things. Three concrete pieces of evidence:

1. **It picked up the language.** The prompt is Python (`for _ in range(...)`), but the continuation drifts into **C/C++** (`static`, `return 1;`, `case`, `<<` stream operators, `0x` hex literals). That's not random — it's the model recognizing low-level/syntactic code tokens and generating *plausible-looking* C. github-code is C/C++/Java-heavy, so the model's strongest priors are there. It's generating the most-trained language, which is exactly what an undertrained code model does.

2. **Local syntax is correct, global structure is not.** `return 1; }`, `static ... (p_count = 0, p_len)`, `case ...:` — these are individually well-formed C fragments. The model has learned **token-level and short-span syntax** (what follows `return`, that `case` wants a `:`, that `<<` chains in C++ streams). What it *hasn't* learned is **long-range coherence** — matching braces across lines, keeping a function semantically consistent, staying in one language. That's the expected capability profile of a 124M model at PPL ~32: good local statistics, no global plan.

3. **The `_` and mangled-identifier explosion** (`static_p__p`, `_INT_id_R_REp_d`, `p___p_p`) is your **tokenizer** showing through. GPT-2 BPE shreds identifiers like `p_count`, `data_type`, `__init__` into fragments around underscores, so the model emits underscore-soup because that's how the corpus *looks* in token space. This is the single clearest argument for switching to the StarCoder tokenizer — it has proper handling for code identifiers and whitespace runs, and would clean up a large fraction of this visual garbage immediately.

### So what's the actual diagnosis now?

You can **retire** the earlier "Problem 2: space domination" and "Problem 3: can't learn patterns" conclusions. Neither holds. The corrected picture:

| Earlier claim | Revised verdict |
|---|---|
| Space token domination is pathological | No — was an artifact of 3-token context. Real cause was the generation loop, now fixed. |
| Model can't learn patterns (underfitting) | Wrong. It learned local C/C++ syntax. It's *undertrained*, not incapable. |
| Data is too dirty | Still true, and now the *main* remaining lever. |
| (new) Tokenizer is shredding identifiers | This is now visibly the second-biggest lever. |

What you're looking at is a **normally undertrained small code model with a code-hostile tokenizer**. This is the expected output of nanoGPT-124M on raw github-code at this loss. Nothing is broken. It's just not good *yet*.

### Why exactly this much incoherence at PPL 32

Perplexity 32 means: on average, at each position the model is as uncertain as if choosing uniformly among ~32 tokens. For local syntax (after `return`, after `case`) the true distribution is sharp, so it gets those right. For "what's the next *meaningful* identifier 40 tokens into a function," the distribution is genuinely wide and the model has no idea — so it samples plausible-looking-but-meaningless tokens. The result is locally-grammatical, globally-nonsensical code. That's textbook for this loss level. CodeParrot-small at PPL ~20 still produces semi-broken functions; you're 1.6× worse in perplexity, which is the visible gap.

### What moves the needle now, ranked

1. **Tokenizer → StarCoder/StarCoder2 tokenizer.** Kills the `__p__p` identifier soup, handles whitespace runs as single tokens (frees context, lowers loss). Biggest visible-quality win per unit effort. This alone will make outputs look dramatically more like real code.
2. **Data → `the-stack-dedup`, restricted to 2–3 languages** (say Python + C). Fewer languages at 124M = denser signal = the model stops code-switching mid-function. Dedup + license filtering drops the noise floor.
3. **Then train longer.** Loss was still falling; with cleaner data + better tokenizer the asymptote is lower, so more steps actually pay off now.

Don't add natural-language mixing — still irrelevant at this stage and for this symptom.

### One quick confirmation worth running

Greedy-decode (argmax, temperature→0) the *same* 57-token prompt. If greedy gives you a run of more-coherent C than the sampled version above, that confirms the weights are fine and the remaining incoherence is just sampling entropy on top of an undertrained model — at which point tokenizer + data are unambiguously your whole roadmap.

```python
# argmax decode, no sampling noise
logits = model(idx_cond)[0][:, -1, :]
next_id = logits.argmax(dim=-1, keepdim=True)
idx = torch.cat([idx, next_id], dim=1)
```

Bottom line: the first output looked like a dead model; this output proves it's a **living, undertrained, badly-tokenized** model. That's a much better place to be — the fixes are tokenizer and data, both of which you already identified, and neither requires more GPU than you have.
