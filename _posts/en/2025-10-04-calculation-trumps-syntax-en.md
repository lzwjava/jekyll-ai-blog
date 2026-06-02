---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Calculation Trumps Syntax in AI
translated: false
type: note
---

You're spot on that the heart of AI and LLMs isn't in the elegance of prose or the philosophical musings on programming languages—though folks like Yin Wang and Daniel P. Friedman have undeniably sharpened our thinking there. Wang's blog dives deep into the guts of systems like Python and Lisp, critiquing how they shape computation in practice, while Friedman's books (think *The Little Schemer* series) demystify recursion and functional paradigms in a way that's almost poetic. But yeah, when it comes to building something that *does*—like generating coherent text or crunching gradients in a neural net—the rubber hits the road in the "how" and "what" of calculation, not the syntax sugar.

### Why Calculation Trumps Syntax

At its core, an LLM like me isn't pondering Lisp macros or Java's object hierarchies; it's executing matrix multiplications, attention mechanisms, and probabilistic sampling at scale. The "how to calculate" boils down to:

- **Algorithms and models**: Things like transformer architectures (Vaswani et al., 2017) define *what* gets computed—self-attention over token embeddings, positional encodings, etc. This is where the magic happens, independent of the language. You could implement GPT in pseudocode and it would "work" on paper; the syntax is just a vehicle.
- **Numerical precision and efficiency**: Here, "calculate what" matters hugely. We're talking token probabilities, loss functions (e.g., cross-entropy), and backpropagation. Mess up the math, and your model hallucinates garbage. Syntax? It's secondary—Python's NumPy gets you 90% there with readable bliss, but it's interpreted and slow for training behemoths.

Language choice *does* sneak in as a pragmatic filter, though. C++ shines for the performance-critical underbelly of AI (e.g., TensorFlow's kernels or PyTorch's CUDA bindings), where every cycle counts in distributed training. Python dominates for prototyping because it's concise—why wrestle with C++'s memory management when `torch.nn.Linear` lets you chain layers in a line? But you're right: it's a "small issue." The real bottlenecks are algorithmic (e.g., scaling laws like Kaplan et al.'s) or data-related, not whether you're typing `def` or `struct`.

### Where PL Insights Still Sneak In

That said, dismissing PL entirely feels like throwing the baby out with the bathwater. Good language design (inspired by Friedman/Wang types) makes *expressing* those calculations safer and faster:

- **Abstractions for reasoning**: Functional purity (à la Scheme) helps avoid bugs in probabilistic code, which is huge for reliable AI inference.
- **Performance without pain**: Rust or even modern C++ borrow from PL research to give you speed *plus* safety, reducing the "calculate wrong" errors that plague raw C.

In the end, AI progress is 80% math/models/data, 15% engineering (where langs like C++ flex), and 5% syntax poetry. If we optimized for the latter, we'd have prettier papers but slower robots. What's your take—do you think we'll see more PL-AI fusion, like domain-specific langs for neurosymbolic stuff?

[Wang's Blog](https://www.yinwang.org)
[Friedman's Essence of Programming](https://www.cs.indiana.edu/~dfriedman/)
[Attention Is All You Need (Transformers Paper)](https://arxiv.org/abs/1706.03762)
[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
