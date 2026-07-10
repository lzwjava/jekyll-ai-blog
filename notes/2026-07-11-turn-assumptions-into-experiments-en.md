---
audio: false
generated: true
image: false
lang: en
layout: post
title: Turn Assumptions Into Experiments
translated: false
type: note
---

**Question: Your friend said “your biggest problem is assuming things.” Is that right?**

Answer: **partially right, but the wording is too broad.**

From your recent discussions (MI50, ROCm, CUDA, AI training, agents, hardware choices), your strength is that you build strong mental models quickly. You often connect patterns:

* Apple ecosystem → CUDA ecosystem
* Android openness → ROCm openness
* More GPU experiments → faster learning
* Open source code → easier debugging

Those analogies are useful. Many engineers operate exactly this way: abstract from known systems, form hypotheses, test.

The risk is the **jump from analogy → conclusion without measurement**.

Example:

> "ROCm source is open, so debugging GPU problems will be much easier."

Maybe. But reality:

* A huge codebase ≠ easy debugging.
* Kernel/compiler/runtime issues may require deep hardware knowledge.
* CUDA has closed parts but decades of documentation, examples, StackOverflow answers, profiling tools, and production users.

Another example:

> "MI50 is cheap, so it is a good AI training card."

True in some dimensions:

* 16GB HBM2
* ECC
* lots of bandwidth
* cheap second-hand

But assumptions:

* ROCm version support
* PyTorch compatibility
* kernel support
* power consumption
* software friction

Need actual experiments.

A more scientific version of your thinking:

```
Hypothesis:
MI50 + ROCm can train small LLMs effectively.

Experiment:
- install ROCm
- run PyTorch benchmark
- train GPT-2 124M
- compare throughput vs RTX 4070
- measure debugging time

Conclusion:
keep or sell
```

That is not "stop assuming". It is **turn assumptions into experiments faster**.

Your friend probably sees a pattern: you sometimes spend a lot of time building a beautiful theory before running the simplest test.

For engineering, especially AI infrastructure:

```
intuition → hypothesis → experiment → data → updated intuition
```

is the loop.

Your intuition is actually an advantage. The adjustment is: **don't let the first mental model become the final answer.**
