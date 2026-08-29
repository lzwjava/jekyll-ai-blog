---
audio: false
generated: true
image: false
lang: en
layout: post
title: Treat Knowledge Like Source Code
translated: false
type: note
---

Question: Is cloning a course/book into local text and then exploring it interactively with a Pi agent a good way to learn?

Answer: **Yes. And I think this is a very powerful AI-native learning loop.**

The key idea is:

> **Don't "read" the course. Turn the course into a codebase and debug it with an agent.**

For example:

```bash
course/
├── 01-introduction.md
├── 02-transformer.md
├── 03-attention.md
├── 04-training.md
├── exercises/
└── notes/
```

Then use your Pi agent:

```text
$ pi

> Explain 03-transformer.md, but don't summarize it.
> Walk through every important claim.

> Why does this equation work?

> What assumption is being made here?

> Give me a tiny PyTorch implementation.

> Let's verify it numerically.

> What would break if I removed this term?

> Find anything in this chapter that is ambiguous or potentially wrong.

> Connect this section to the actual Transformer source code.
```

That changes the learning process from:

```text
book → read → understand? → forget
```

into:

```text
source material
      ↓
local corpus
      ↓
agent interrogation
      ↓
questions
      ↓
implementation
      ↓
experiment
      ↓
failure
      ↓
debugging
      ↓
understanding
```

### The important part: treat knowledge like source code

Your analogy is exactly right.

When you clone a GitHub repo, you don't necessarily trust the README. You can inspect:

```bash
grep -R "attention" .
```

open the implementation:

```python
Q = x @ Wq
K = x @ Wk
V = x @ Wv

scores = Q @ K.T / sqrt(d)
probs = softmax(scores)
out = probs @ V
```

Then ask:

> Why exactly is `sqrt(d)` here?

Then derive it.

Then run an experiment.

Then deliberately break it.

Learning from a technical book can work the same way.

### Even better: make the agent your "pair programmer"

Instead of:

```text
Agent: Here's a summary of Chapter 3.
You: 👍
```

use:

```text
You: I don't understand this paragraph.

Agent: Let's isolate the claim.

You: Why?

Agent: Because ...

You: Prove it.

Agent: Here's the derivation.

You: Implement it.

Agent: Here's 20 lines of PyTorch.

You: Test it.

Agent: Result ...

You: Now remove the normalization.

Agent: Here's what changes.

You: Why?

...
```

That's much closer to **learning by doing**.

And because the source is local, you can give the agent very strong constraints:

```text
Only answer using the course material and experiments
unless you explicitly say you are introducing outside knowledge.
Always give the exact source section.
Never hide uncertainty.
When there is an equation, derive it.
When there is code, execute or reproduce a minimal version.
When possible, propose an experiment.
```

This is especially good for subjects like:

* Transformer architecture
* CUDA
* GPU hardware
* distributed training
* operating systems
* compilers
* mathematics
* papers
* electronics

For something like a GPU board, you can literally do:

```text
board/
├── schematic.pdf
├── boardview/
├── datasheets/
├── photos/
├── measurements/
├── repair-log.md
└── questions.md
```

Then the "textbook" becomes **the actual object you're studying**.

You can ask:

```text
What is R47?

Why is it placed next to this capacitor?

Trace the power path.

What voltage should exist on both sides?

What failure modes would make this component relevant?

Which datasheet claim supports this?

What measurement should I make next?
```

That's essentially **debugging reality itself**.

So I wouldn't think of this merely as "using AI to read books."

I'd call it:

> **Turning learning material into an interactive executable knowledge base.**

And the deepest part is that **questions become the unit of learning**, rather than pages or chapters.

A good course in this model isn't:

```text
100 hours of video
```

It's:

```text
1000 questions
500 experiments
100 implementations
50 failures
10 mental models
```

That is much closer to how you already learn engineering by taking apart GPUs, models, code, and hardware.
