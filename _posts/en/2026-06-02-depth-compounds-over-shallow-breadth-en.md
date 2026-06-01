---
audio: false
generated: true
image: false
lang: en
layout: post
title: Depth Compounds Over Shallow Breadth
translated: false
type: note
---

Question: Is it better to learn deeply in specialized fields like ML/DL, backend engineering, and cybersecurity by focusing intensely on one paper or open source project for a year, rather than spreading attention across many things?

Answer:

Yes. **One deep dive per year beats ten shallow passes.** This is especially true for you, and here's why.

## The Mechanism: Why Depth Compounds

In technical fields with high conceptual density, understanding works *exponentially*:

- **Month 1-2:** You're parsing syntax and fighting the tool. 50% effort, 5% understanding.
- **Month 3-4:** Patterns emerge. You're building mental models. Same effort, 30% understanding.
- **Month 6-9:** You've internalized trade-offs, debugged subtle bugs, read source code at 2am. You think in the domain. 70% understanding.
- **Month 10-12:** You're inventing. You spot optimizations the original author missed. You could teach it. 95% understanding.

If you jump to a new thing in month 4, you never reach the inflection point where understanding accelerates. You collect shallow pattern-matching instead of deep structure.

**Karpathy's nanoGPT era is the template here.** He didn't skim 10 papers on transformers. He implemented GPT from scratch, trained it, read the original Attention paper obsessively, understood the compute graph, tweaked sampling strategies. One year. That's why his teaching is so clear — he lived in the thing.

## Why Shallow Learning Fails in These Fields

Fields like ML/DL and distributed systems have **high context density**:

- A paper's real insight isn't in the abstract—it's in page 4 of the appendix, or in the code that reproduces Figure 3.
- The engineering is the research. Reading about distributed consensus is useless until you've debugged a multi-node system at 3am and understood consensus failure modes viscerally.
- Early optimization is *correct optimization.* In deep learning, the "premature optimization" warning doesn't apply—if you're doing inference optimization, you need to understand memory bandwidth, cache lines, and GPU compute ratios immediately.

Spreading thin optimizes for *talking about* the field, not building in it.

## Your Situation Specifically

You're at the perfect point for this:

- You've already shipped. You know the cost of spreading attention (you've lived it across iOS/Android/backend).
- You've got infrastructure (workstation + AMD cloud). You can run experiments that require weeks.
- You want to transition fully into AI engineering—this is the throttle.

**The right move:** Pick one deep domain per year. For the next 12 months, I'd suggest:

1. **Transformer internals + efficient inference** (3-4 months)
   - Deep dive: nanoGPT → llama.cpp source → FlashAttention paper + implementation
   - Build: a minimal inference engine with KV cache, quantization, maybe LoRA loading
   - Why: You use LLMs at 1.5B tokens/year. Understanding the compute graph directly impacts your work.

2. **Model training at scale** (4-5 months)
   - Deep dive: Distributed training (DDP, FSDP), gradient checkpointing, mixed precision, actual nanoGPT scaling experiments on your H100 access
   - Build: Train a small model end-to-end with profiling, understand throughput/memory/compute bottlenecks
   - Why: You have GPU access. Most engineers never train. This is a moat.

3. **Agent systems / tool use** (3-4 months)
   - Deep dive: ReAct/Plan & Execute, function calling, multi-agent patterns, actual agent code (not blog posts)
   - Build: A working agent that coordinates multiple tools, handles failures, does planning
   - Why: This is where the next layer of AI engineering lives.

You don't do these in parallel. You finish one, ship something, document it (your notes site), then move to the next.

## How to Structure the Deep Dive

When you commit to one paper/codebase:

1. **Read the paper actively**—implement as you read, line by line. Don't read passively.
2. **Rewrite the code from scratch** once you understand it. Teach it to Claude.
3. **Break it.** Modify hyperparameters, architecture, training procedure. See what fails and why.
4. **Profile it.** If it's code, measure memory, compute, latency. Understand the bottlenecks.
5. **Document publicly.** Post on your blog or notes. This forces clarity and cements learning.

**Yin Wang's approach** (whom you admire) is basically this: he goes very deep on one thing, writes essays about it with obsessive detail, then moves on. Not because he lost interest—because he *finished* understanding it. The depth is what lets him move fast.

## The Trap to Avoid

The temptation will be: "But I should also learn X because it's hot right now."

**Resist this.** Here's why:

- Hot trends in AI change every 6 months (LoRA → QLoRA → QLORA variants → dbrx → MoE → ...). If you chase novelty, you're always learning someone else's abstraction.
- Deep understanding makes you *faster* at adopting new things, not slower. Once you understand transformers deeply, a new efficient variant is a day to integrate, not a week to learn.
- Your competitive advantage isn't being first with the trend—it's understanding the *why* so deeply that you can evaluate if the trend matters.

## Concrete Timeline for You

**Next 12 months:**

- **Now → June 2026 (4 months):** Go very deep on inference optimization. Read llama.cpp, vLLM source. Build and ship something (quantized inference engine, maybe?). Document every optimization decision.
- **July → October (4 months):** Distributed training. Take a 7B or 13B model, train it on your AMD cloud or H100. Profile every bottleneck. Understand FSDP, gradient checkpointing, mixed precision viscerally.
- **November → December (2 months):** Solidify + explore. Ship one more thing. Maybe a training framework wrapper. Or agent systems (depending on what excites you).

Then reassess. But stick to the depth.

---

**TL;DR:** Yes, you're right. One paper/codebase per year beats ten shallow dives. You have the experience, the infrastructure, and the timeline to go deep. This is how Karpathy, Yin Wang, and the best engineers actually learned. Follow that path.