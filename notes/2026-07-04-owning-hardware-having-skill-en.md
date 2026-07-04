---
audio: false
generated: true
image: false
lang: en
layout: post
title: Owning Hardware ≠ Having Skill
translated: false
type: note
---

**Question:** Reflecting on a friend's story about owning a GTX 1060 since 2016 but never doing hands-on work with it — what's the real lesson about hardware, practice, and career positioning?

**Answer:**

Your friend's 1060 story is a good specimen of a general failure mode: *owning the tool ≠ having the skill, and proximity ≠ practice*. A few threads worth pulling on.

**The Yin Wang point is about variation, not equipment.** His myopia/tennis argument is that people repeat one fixed configuration (one pair of glasses for every distance, one coached stroke) and never run experiments on themselves. The 1060 owner made the same mistake in reverse: he had the hardware for variation — could have written a CUDA kernel, trained a tiny net, profiled a game — but ran zero experiments. The hardware sat there as a static configuration. The lesson isn't "buy GPUs," it's "whatever you own, generate variations and observe."

**The counterfactual is real but overstated.** Yes, someone who wrote CUDA in 2016–2018 had a head start when GPT hit in 2022. But you're living proof that the gap was closable: you went from no GPU practice to training GPT-2 760M on an MI300X. The people who *couldn't* close the gap weren't missing the 1060 — they were missing the invariant layer underneath: memory hierarchy, parallelism models, how compilers lower code to hardware. That's why "computer software/hardware 精通 → fast GPT learner" is the correct causal story. DirectX experience circa 2010 would have helped only insofar as it taught the invariants (pipelines, shaders as SIMT programs, host↔device transfer costs).

**What actually doesn't change**, and is worth deliberately practicing now:

1. The memory hierarchy (registers → shared/LDS → HBM → host RAM) and why arithmetic intensity determines everything. This is the same on your 4070, the MI300X, and whatever ships in 2030.
2. SIMT execution — warps/wavefronts, divergence, occupancy. CUDA and HIP are dialects of the same idea.
3. Compilation — how `torch.compile` / Triton / XLA lower Python to kernels. This is the modern 编译原理, and it's where the leverage is.

**Concrete practice suggestion**, since you have both machines: write one naive matmul kernel and one tiled version, benchmark against cuBLAS/rocBLAS, and write up why the gap exists. On the 4070 in CUDA, then port to HIP on the MI300X (`hipify-perl` does 90% of it). That single exercise touches all three invariants above and takes a weekend. It's the exact "实操" your friend skipped for eight years — and it directly compounds into your DeepSeek MoE / inference-optimization goals, since MoE performance is mostly a memory-bandwidth story.

The VR analogy in your message has one flaw worth noting: not every cool device is worth deep study. VR *hardware* ownership without practice was mostly fine, because VR didn't become the platform shift — GPUs did. The filter isn't "cool electronics I own" but "does this device expose an invariant layer of computing?" GPUs did (parallel compute). VR headsets mostly exposed application-layer APIs. So the refined rule: **practice hands-on with devices that sit close to the fundamentals; skim the rest.**
