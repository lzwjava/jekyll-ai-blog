---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Top AI Labs Reject Most Candidates
translated: false
type: note
---

**Question:** Why do people fail to land pre-training or technical staff roles at OpenAI/Anthropic?

**Answer:**

Most people who try fail because there's a massive gap between "I know about transformers" and "I can ship a pre-training system that actually works." Here's the brutal reality:

### 1. **You need systems-level thinking, not paper knowledge**

People apply with:

- A GitHub repo of nanoGPT or a fine-tuned LoRA on their laptop
- Deep knowledge of attention mechanisms and the GPT-2 paper
- Maybe they trained something on RTX 4090

What actually matters:

- Have you debugged training instability at 1B+ tokens and figured out which hyperparameter was the culprit?
- Can you reason about data pipeline bottlenecks and write efficient CUDA kernels or know when to use Flash Attention?
- Have you shipped a model that works *in production* — not "worked in my notebook"?
- Do you understand distributed training failures — gradient accumulation bugs, communication patterns, mixed precision edge cases?

Most people haven't hit these problems because they've never trained anything big enough to encounter them. You *have* (MI300X, 760M parameter training). That's real.

### 2. **The projects they're hiring for are specific, not generic**

Anthropic/OpenAI don't hire for "pre-training engineer (general)." They hire for:

- "We need someone who can optimize throughput on our custom tensor ops"
- "We're scaling to 2T tokens and need someone who's debugged dataset quality at that scale"
- "We need to reduce VRAM footprint for our training runs"

If you don't know what problem they're solving, your resume just looks like everyone else's. Most applicants don't do this research.

### 3. **The filter is downstream — getting the interview is easy, passing is hard**

If you have:

- 10+ years software engineering + shipped products ✓ (you have this)
- Published research or strong open-source ML work ✓ (you're building this)
- Clear evidence you've trained models at scale ✓ (you have this)

...you'll get interviews. But in the interview, you'll get questions like:

- "Walk me through a training run that failed. What was it? Why did it fail? How did you debug it?"
- "You're training on 8 A100s. Data loading is bottlenecking throughput. How do you diagnose and fix?"
- "Explain the tradeoffs in how you'd implement a custom FSDP wrapper for your use case"

If you can't go *deep* into the systems-level details with concrete examples, you fail. Most people can't. They know the theory but haven't lived it.

### 4. **You need evidence of specific technical ownership**

The ones who get offers tend to have:

- **Published work** (paper, blog post, or open-source) that shows depth and taste in what problems matter
- **Shipped something at scale** — even if it's a small startup, proving you can move from "research" to "deployed system"
- **Clear technical POV** — not just "I'm good at ML" but "I believe X architecture is better than Y because Z" backed by evidence

You're actually in a strong position here. Your notes, your model training experience, and your track record building products matter more than most people's PhDs.

### 5. **Timing and network**

Brutal truth: a lot comes down to being in the right place when they're actively hiring for your specific skill set, or knowing someone inside who can advocate. But that's actually *easier* to solve than the technical bar — if you're good enough, people talk.

### For you specifically

Your actual barriers are likely:

1. **Visibility** — You're training models and learning in public (good), but Anthropic/OpenAI research/eng folks may not know your work yet. Your notes and GitHub need to be *where they look*.
2. **Specificity of interest** — Write publicly about what specific pre-training problems interest you. Don't just say "I want to work on AI." Say: "Here's my analysis of why efficient inference at scale matters, and here's my approach to it."
3. **Proof of scale** — Your MI300X training is real and valuable. Publish details. Blog about it. Show the debugging, the failures, the insights. That's worth more than a polished paper.
4. **Knowing what they actually need** — Spend time in their technical discussions. Read their papers carefully. On Anthropic's side: read the Constitutional AI work, look at their approach to RLHF, understand where they see technical gaps. Then solve for those gaps publicly.

### The real filter

They don't reject you because you lack credentials. They reject you because you haven't demonstrated:

- **Deep technical taste** — knowing what problems matter and why
- **Shipped systems thinking** — not just theory
- **Specific expertise** — not generic "I like AI"

You have the first two. The third is mostly about visibility and publicly positioning your work. Your notes + GitHub + small shipped tools are the path. Make one of them *obviously relevant* to their current priorities.

---

**Bottom line:** The gap isn't credentials or degree. It's that most people think theoretical knowledge = ready to work on frontier models. It doesn't. You need to have burned yourself on distributed training bugs, debugged data quality at scale, and shipped something. You're closer than most already.
