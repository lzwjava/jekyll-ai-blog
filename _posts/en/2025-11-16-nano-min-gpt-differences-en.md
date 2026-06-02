---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: nanoGPT vs minGPT Key Differences
translated: false
type: note
---

I'll search for information about the differences between nanoGPT and minGPT by Andrej Karpathy.
Based on the search results, here are the key differences between Andrej Karpathy's nanoGPT and minGPT:

## Core Philosophy and Purpose

**minGPT** was designed primarily as an **educational tool** - it was Karpathy's first implementation focused on making GPT architecture understandable and accessible for learning purposes [1].

**nanoGPT** represents a **practical evolution** that Karpathy describes as "the simplest, fastest repository for training/finetuning medium-sized GPTs" that "prioritizes teeth over education" [1]. This means it's optimized for actual training performance rather than just educational clarity.

## Technical Differences

### Codebase and Implementation
nanoGPT is essentially a **rewrite of minGPT** with significant optimizations and improvements [1]. While minGPT served as the foundation, nanoGPT was rebuilt from the ground up with performance as the primary goal.

### Performance Focus
The search results highlight that nanoGPT is specifically designed for **speed and efficiency** in training medium-sized GPT models [1]. This represents a shift from minGPT's educational focus to a more production-oriented approach.

### Training Capabilities
nanoGPT is positioned as a repository that can handle **actual training and fine-tuning** of GPT models at scale, whereas minGPT was more of a demonstration and learning tool [1].

## Development Timeline

The evolution appears to be:
1. **minGPT** → Original educational implementation
2. **nanoGPT** → Rewritten version prioritizing performance and practical training
3. **llm.c** → Karpathy's even more optimized C implementation mentioned in the search results [2]

## Community Reception

The search results indicate that nanoGPT has been widely adopted as a **reasonably accessible and easy-to-run** implementation [3], suggesting it strikes a good balance between educational value and practical utility.

In summary, while both projects come from Andrej Karpathy, minGPT was his educational GPT implementation, and nanoGPT is its optimized successor focused on actual training performance rather than just educational clarity.

Citations:
[1] https://github.com/karpathy/nanoGPT
[2] https://www.lesswrong.com/posts/j3gp8tebQiFJqzBgg/how-the-nanogpt-speedrun-wr-dropped-by-20-in-3-months
[3] https://www.libhunt.com/compare-minGPT-vs-nanoGPT
