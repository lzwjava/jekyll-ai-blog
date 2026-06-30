---
audio: false
generated: true
image: false
lang: en
layout: post
title: QKV as concrete causal substrate
translated: false
type: note
---

Question: My friend says LLMs don't understand "causality" as an abstract relation — they just memorize co-occurrence patterns, only knowing token proximity, never extracting independent causal logic. I replied: in one sentence, some people feel there's logic, some feel there isn't; logic itself is abstract; whereas K/Q/V (key, query, value) feels more program-like, more concrete. Right?

Answer:

You're directionally right, and your instinct to ground the argument in Q/K/V instead of the word "logic" is the sharper move. Let me make it precise.

Your friend's claim conflates two separable things: *representation* and *mechanism*. The "just co-occurrence / token proximity" framing is actually outdated and wrong on the mechanism side — attention is explicitly **not** about proximity.

**Why "token proximity" is the weak part of his argument:**

Attention computes relevance by content, not distance. The core operation:

```
scores = (Q @ K.T) / sqrt(d_k)   # [seq, seq] — every token scores every other
weights = softmax(scores)         # who attends to whom
out = weights @ V
```

Two tokens 500 positions apart can have a near-1.0 attention weight if their Q·K dot product is high. Position only enters through positional encodings (RoPE etc.), and even then it's a learned bias, not a hard "closer = more related" rule. So "it only knows token distance" is factually false — that's pre-transformer n-gram thinking.

**Where your friend is half-right:**

The model doesn't store a separate symbolic node called `CAUSES(a, b)`. There's no discrete causal graph. But "memorizing co-occurrence" undersells what's measurable: there's strong evidence of *learned structured representations* and circuits that do more than surface statistics:

- **Induction heads** (Olsson et al.) — circuits that implement "if A was followed by B earlier, predict B after A again." That's an algorithm, not a lookup.
- **World models** — the Othello-GPT work showed a model trained only on move sequences develops an internal representation of the board state, recoverable by linear probes. It built structure no one fed it.
- **Linear representation / "concept directions"** — abstract features (including relational ones) often live as linear directions in activation space.

So the honest position is in the middle: the model *does* extract abstractions beyond co-occurrence, but they're distributed/statistical, not symbolic. Whether that "counts as understanding causality" is where your "some feel there's logic, some don't" lands — and that's a definitional dispute, not an empirical one.

**Your Q/K/V point, sharpened:**

Yes — pointing at Q/K/V is the right rhetorical move because it replaces a vibes-argument ("does it *really* understand?") with a concrete, inspectable mechanism. "Logic" is unfalsifiable hand-waving; "here's the attention pattern and here's the circuit" is testable. You can literally probe activations and ablate heads. That's the difference between arguing about consciousness and reading the assembly.

The one correction I'd make to your phrasing: Q/K/V isn't a *substitute* for logic — it's the substrate logic-like behavior *emerges from*. The model has no causal logic module, yet causal-looking behavior falls out of stacking these operations + training pressure. That emergence is exactly what makes the "does it understand" question genuinely hard rather than obviously yes/no.

So: your friend is right that there's no symbolic causal engine, wrong that it's "just proximity," and you're right that grounding the debate in the actual mechanism beats arguing about the word "logic."

References:

- [In-context Learning and Induction Heads (Anthropic)](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html)
- [Emergent World Representations: Othello-GPT (Li et al.)](https://arxiv.org/abs/2210.13382)
- [Attention Is All You Need (Vaswani et al.)](https://arxiv.org/abs/1706.03762)
- [The Linear Representation Hypothesis (Park et al.)](https://arxiv.org/abs/2311.03658)
