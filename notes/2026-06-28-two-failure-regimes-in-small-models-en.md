---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two Failure Regimes in Small Models
translated: false
type: note
---

Right. Your read is correct, and the diagnosis is cleaner than "the model is just too small."

What you're seeing has two distinct failure regimes, and they have different causes:

**1. The first ~20 tokens (garbled but Java-shaped)**

`return new.Invalid(this.nameOf.Value)`, `public String get(String source)`, `this.tree.GetAttribute(...)` — this is the model's actual learned distribution. It knows Java *texture*: capitalized method names, `this.` chains, `public void`, brace nesting. What it lacks is the long-range coherence to bind `search(int key)` to a tree-traversal body. At 124M params with GPT-2's context handling, the induction heads can copy local syntactic patterns but can't hold "I'm inside a BST.search method that should compare key against root.key and recurse." That's the expected small-model ceiling — not a bug.

**2. The `S.S.S.S` loop (the actual interesting part)**

This is **not** a capability failure. This is a sampling/repetition collapse, and it's distinct from the first regime. Once the model emits `.S.S.S`, each `.S` makes the next `.S` overwhelmingly probable — a classic self-reinforcing attractor. `top_k=200` doesn't save you because the degenerate token's probability mass has already collapsed onto one path; the other 199 candidates are negligible. `temp=0.8` is high enough to *enter* a weird region but not high enough to *escape* the basin once you're in it.

The `S` itself is almost certainly a BPE artifact — `S` as a frequent capitalized-identifier-prefix token (`.S`, `.Set`, `.String`, `.Size`) that the model learned as a high-frequency continuation and now loops on without semantic grounding.

So your summary line should really split it:

> Continuation degrades in two phases: (1) ~20 tokens of locally-plausible but globally-incoherent Java (model's genuine ceiling), then (2) a BPE-token repetition attractor (`.S.S.S`) — a sampling collapse, not a knowledge gap.

**On your actual thesis** — "don't underestimate 124M, add a compiler + a loop, maybe you get runnable code" — that instinct is right and it's exactly the lever that makes small models punch up. The model alone can't self-correct, but it doesn't need to if you wrap it. Three concrete moves, cheapest first:

```python
# 1. Kill the degeneration loop directly — this alone fixes your output
out = model.generate(
    ids,
    repetition_penalty=1.3,      # penalize already-emitted tokens
    no_repeat_ngram_size=3,      # hard-ban any repeated trigram → ".S.S.S" impossible
    temperature=0.8, top_k=200,
)
```

`no_repeat_ngram_size=3` would have *prevented your entire failure case* — the moment `.S.S.S` tries to become `.S.S.S.S` it's a banned trigram. Try just this first; it's a one-line test in your REPL.

The compiler-in-the-loop idea is the real win, and it's a tiny reject-sample loop:

```python
def gen_compilable(model, prompt, k=8):
    for _ in range(k):
        code = prompt + model.generate(prompt, no_repeat_ngram_size=3)
        if javac_ok(code):           # shell out to javac, check returncode
            return code
    return None  # fall back

def javac_ok(src):
    import subprocess, tempfile, os
    d = tempfile.mkdtemp()
    p = os.path.join(d, "BinarySearchTree.java")
    open(p, "w").write(src)
    r = subprocess.run(["javac", p], capture_output=True)
    return r.returncode == 0
```

This is best-of-N against a *free, perfect verifier*. You're not asking 124M to be right — you're asking it to be right *once in N tries*, and letting `javac` filter. For something as templated as BST methods, even a degenerate base model gets surprising mileage once you stop it from collapsing.

The deeper version of this is what makes it a genuine research-y direction rather than a hack: the compiler's binary signal is a reward, and you can close the loop. Compile-pass as a filter for rejection-sampled SFT data (keep only the runs that compile, fine-tune on them) is the cheapest version. The expensive version is GRPO with `compiles → +1, runs+passes_test → +2` as reward — which is exactly the RLVR (RL with verifiable rewards) setup that's eating code-model training right now. A 124M model with a `javac` reward signal on a narrow domain (single-file algorithmic Java) is a legitimately fun experiment that fits on your 4070.

One thing to verify before you over-attribute: paste the prompt back as a `generate` continuation with `do_sample=False` (greedy). If greedy *also* collapses into a repetition loop (just a different token), that confirms it's an architectural/training-coverage issue rather than a sampling temperature artifact — and tells you the repetition penalty is load-bearing, not optional.
