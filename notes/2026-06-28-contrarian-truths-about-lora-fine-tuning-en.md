---
audio: false
generated: true
image: false
lang: en
layout: post
title: Contrarian Truths About LoRA Fine-Tuning
translated: false
type: note
---

Question: What are unpopular or contrarian ideas about using LoRA to cheaply re-adapt a frozen open base model for fine-tuning?

Answer:

Here are the contrarian takes that survive scrutiny, ordered roughly by how much they cut against the consensus.

**1. LoRA doesn't just "learn less" — it learns *differently*, and that difference is often a downgrade.**

The popular framing is "LoRA ≈ full FT but cheaper, slightly worse." The sharper claim from the *intruder dimensions* work (Shuttleworth et al., 2024) is structural: LoRA introduces high-ranking singular vectors in the weight matrix that don't exist in the full-FT solution. Same task accuracy in-distribution, but the spectral structure is different, and those intruder dimensions correlate with worse OOD generalization and more forgetting of the pretraining distribution. So "LoRA matched full FT on my eval" can hide that you've built a more brittle model.

**2. "Frozen base + adapter" is a false economy when you're doing real domain adaptation.**

LoRA is parameter-efficient, not *knowledge*-efficient. A low-rank update to attention/MLP projections can re-style outputs and teach formats/tasks cheaply, but it's a poor vehicle for injecting genuinely *new* knowledge or shifting the base distribution hard. The "Tale of Tails" / continued-pretraining literature and the LIMA-style observations point the same way: if you need new facts or a different domain prior, you want full FT or continued pretraining, not a rank-16 patch. LoRA excels at *behavior*, underperforms at *knowledge*.

```python
# The honest decision rule
def should_use_lora(task):
    if task in ("format", "style", "tone", "task-following", "persona"):
        return True              # LoRA's sweet spot
    if task in ("new domain knowledge", "new language", "factual recall"):
        return False             # full FT / continued pretrain
    if task == "reasoning/math hard skill acquisition":
        return "maybe — rank matters, often disappointing"
```

**3. Rank is mostly a red herring; *which modules* you adapt matters far more.**

Folk wisdom obsesses over `r`. Empirically (QLoRA ablations, the original LoRA paper's own attention-only choice), going from r=8 to r=64 gives diminishing returns fast, while *applying LoRA to all linear layers including MLP* vs. attention-only is a much bigger lever. The unpopular consequence: most people are tuning the wrong knob. Adapt everything (`q,k,v,o,gate,up,down`) at low rank before you ever raise rank.

**4. QLoRA's quantized-base is a silent accuracy tax people pretend doesn't exist.**

QLoRA made LoRA *feel* free by training adapters on a 4-bit NF4 frozen base. The dequantize-at-inference story is clean, but you're optimizing adapters against a lossy base, and the merged/served model inherits that. For sensitive tasks the gap is real — it's just usually below the noise of a weak eval. "QLoRA = LoRA quality at 1/4 memory" is marketing, not a measured equivalence.

**5. Merging LoRA back into the base is lossy and often pointless.**

`W' = W + BA` is exact arithmetic, but the *appeal* of LoRA — swappable adapters, multi-tenant serving (S-LoRA), composability — vanishes the moment you merge. And merging multiple LoRAs is not additive in any principled way; interference between adapters is a known failure mode. Contrarian position: if you're going to merge and serve one model, you've thrown away LoRA's only structural advantage and should have just done full FT (or used the merge purely as a deployment convenience, knowing it's a one-way door).

**6. LoRA hyperparameter sensitivity is underrated and rarely reported.**

The α/r scaling, learning rate (LoRA wants ~10x higher LR than full FT), and init all interact non-trivially. Papers report the winning config; practitioners discover LoRA is *more* finicky to get to full-FT parity than the "just works" reputation suggests. rsLoRA (rank-stabilized scaling) exists precisely because the naive α/r scaling breaks at higher rank — evidence the default recipe was quietly wrong.

```python
# Defaults people copy that are often suboptimal:
LoraConfig(r=8, lora_alpha=16)   # alpha/r=2 scaling — fine at low r,
                                  # degenerates as r grows → use rsLoRA
# Practical: LoRA LR ~1e-4 to 3e-4, NOT the 1e-5/2e-5 you'd use for full FT
```

**7. The "1000 cheap experiments" promise is real but creates eval debt.**

LoRA's genuine win is iteration speed — you can run 50 adapter variants for the cost of one full FT. But cheap training with the same weak eval just lets you overfit to your eval faster. The bottleneck silently moves from compute to evaluation quality, and most LoRA pipelines never upgrade the eval to match. The cost didn't disappear; it moved somewhere you're not measuring.

**8. For very small models, LoRA's rationale partly collapses.**

The whole pitch is "the base is huge and expensive to fully tune." At nanoGPT/124M–760M scale on an MI300X with 192GB, you can full-FT trivially. LoRA there is mostly cargo-culted — you're paying the intruder-dimension / capacity penalty to save memory you have in surplus. Reserve LoRA for the regime where full FT genuinely won't fit (7B+ on a 4070), and just full-FT your GPT-2 760M experiments.

The synthesis: LoRA is a *behavioral re-styling* tool with a *knowledge-injection* ceiling, a *quantization* tax, a *spectral* side-effect, and a *serving* advantage you forfeit on merge. Treating it as "free full FT" is the popular error; treating it as "cheap format/task adaptation, full FT for knowledge" is the calibrated position.

References:

- [LoRA vs Full Fine-tuning: An Illusion of Equivalence (intruder dimensions)](https://arxiv.org/abs/2410.21228)
- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314)
- [A Rank Stabilization Scaling Factor for Fine-Tuning with LoRA (rsLoRA)](https://arxiv.org/abs/2312.03732)
- [S-LoRA: Serving Thousands of Concurrent LoRA Adapters](https://arxiv.org/abs/2311.03285)
- [LoRA Learns Less and Forgets Less](https://arxiv.org/abs/2405.09673)
