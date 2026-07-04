---
audio: false
generated: true
image: false
lang: en
layout: post
title: "50K Steps: Code Fails, Finance Works"
translated: false
type: note
---

Here's the analysis:

---

## Results assessment: d12 step 50K, temp=0.8

**Training curve (val_bpb across checkpoints)**:

```
step  5000: 1.6798  train_loss=1.3968
step 10000: 1.6399  train_loss=1.3723
step 15000: 1.6256  train_loss=1.4654
step 20000: 1.5952  train_loss=1.3630
step 25000: 1.5680  train_loss=1.1359
step 30000: 1.5363  train_loss=1.1988
step 35000: 1.5101  train_loss=1.2288
step 40000: 1.4683  train_loss=1.1691
step 45000: 1.4463  train_loss=1.0767
step 50000: 1.4176  train_loss=1.0616
```

Curve is still descending at step 50K (no plateau), so the model hasn't converged yet. Tokens seen: 50K * 65,536 = ~3.3B.

### Qualitative breakdown by domain

**Code prompts — all failing**

| Prompt | What it does |
| -------- | ------------- |
| **code_go** | Repeats prompt constraints verbatim ("The client should gracefully handle SIGINT..."), then drifts into unrelated `os.environ['PORT']` config boilerplate. Never generates a single line of Go code. |
| **code_python** | Echoes the prompt back: "The function does not take any additional arguments. To add a new value to the list you must do so the function returns a list." Zero code generation. |
| **code_quicksort** | This is the **best** code output. Generates a syntactically valid quicksort with one bug: `return quicksort(left) + middle + quicksort(right) - 1` (the `- 1` is wrong). Then invents `sort_2`, `sort_3`, ..., `sort_5` that all call `arr.sort(quicksort)` — syntactically valid but semantically broken (passing a function as key). The model has learned *code shape* but not *code semantics*. |
| **code_react** | Starts with a legitimate DataFetcher component (possibly memorized from training data), then defines `fetch()` as a React component (shadowing the browser API), then enters a self-referential loop copying the same component structure. |
| **code_sql** | Lists raw column names instead of writing a GROUP BY aggregation. Generates `WHERE id = 1 ORDER BY name` — no SUM, no COUNT, no top-5. |

**General knowledge prompts — word salad**

All four (autonomic, compound, photosynthesis, water) follow the same pattern: faithfully reproduce the prompt for the first ~40 tokens, then undergo **semantic collapse**:

- "fight-or-flight response" → "the warm, as opposed to the pitty"
- "photosynthesis" → "photometry phototechnique" / "the following photographs"
- "compound interest" → just repeats the prompt text as its own output
- "oceans, lakes, and rivers" → "the continuous oceans, not the flows over land"

The model associates words by surface co-occurrence, not meaning. "Photosynthesis" → "photo" → "photographs". "Autonomic" → "automatic system" → "pitty" (??). This is characteristic of a model that has learned token-level statistics but hasn't formed proper latent representations for conceptual reasoning.

**SEC/financial prompts — the one bright spot**

| Prompt | Assessment |
| -------- | ----------- |
| **sec_revenue** | **Genuinely plausible**. The 80-tok output continues the financial narrative coherently: "The effective growth was $5.42% in the prior year, including $4.7 million." The 200-tok version generates a full second paragraph of revenue analysis with reasonable-looking numbers. This is the only domain where the output could pass as human-written to a casual reader. |
| **sec_risk** | Starts okay copying the prompt, then fixates on "ecosystem" and repeats it 12+ times. The 200-tok version invents "Item 1B. Sustainable Risks" — a hallucinated SEC section header. |
| **sec_financial_analysis** | Degrades into "Sinh-Deutschmans algorithm" (nonsense) and lists of "1.8, 1.5, 1.6" — the model latched onto the ratio numbers and kept generating them. |
| **sec_ifrs** | References "APLT" (hallucination), then "15,200, 172, 200" — numbers picked up from surface pattern matching. No actual IFRS/GAAP analysis. |

### Root cause

At 1.42 val_bpb with 32K vocab, the model's byte-level perplexity is ~2^1.42 ≈ 2.68. This means at every byte position, the model is roughly as uncertain as picking among 3 possibilities. For code generation (high-entropy, exact syntax required), this is fatal — even one wrong token breaks the program. For formulaic text like SEC revenue filings (low-entropy templates), it works because the next token is heavily constrained by nearby context.

The model has learned local n-gram patterns well enough to mimic the *shape* of financial reporting, but lacks the global coherence to produce correct code or reason about concepts. It's behaving like a high-order character-level Markov model — good at local pattern completion, zero understanding.

### What would help

- **More steps**: curve still descending at 50K. Running to 100K+ would drop val_bpb toward ~1.3, which would reduce the garbage tail.
- **Larger model**: d12 (768 dim) is GPT-2 Small scale. A d24 (1536 dim) would have more capacity to internalize the structure of code and concepts from the same data.
- **Lower temperature**: 0.8 is quite high for sampling. At 0.4-0.5 the model would stay closer to the learned distribution and produce less hallucination (but also less variety). The code_quicksort and sec_revenue outputs would likely tighten up.
- **The val_bpb of 1.42 needs to reach ~1.0-1.1 for reliable code generation** — that's the threshold where the model has enough bits to encode syntax constraints.
