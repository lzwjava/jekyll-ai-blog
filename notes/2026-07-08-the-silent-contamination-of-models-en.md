---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Silent Contamination of Models
translated: false
type: note
---

Question: Cooking analogy — you don't need to wash yesterday's pan if it's a salty environment (bacteria won't grow much), and similarly, if a model checkpoint has no "dirty data," you can resume training mid-way, even continue from someone else's public checkpoint, instead of always starting from a fresh pot/new model. Is this reasoning valid?

Answer:

The analogy is directionally right but the salt case and the checkpoint case have different failure modes, and conflating them will bite you in one specific way: **contamination in ML compounds and is silent, while contamination in food is usually visible/detectable (smell, color, growth).**

## The cooking side (quick, not your main interest but worth being precise)

Salt lowers water activity (a_w), which is what actually inhibits most bacterial growth — not "salt kills bacteria" directly. But:
- Halophiles and some spore formers (notably *Clostridium botulinum*, *Staphylococcus aureus* toxin) tolerate salt fine.
- A "salty pan" isn't a sterile pan — it's a pan with reduced growth rate for *most* organisms, for a *bounded* time window.

So "don't wash it" is a bet on (a) low initial contamination, (b) short reuse window, (c) high salt/low a_w. It's a legitimate risk-reduction heuristic, not sterilization. Same logic, different domain.

## The model checkpoint side — this is the part that matters for you

Your instinct maps to a real, well-established practice: **continued/continual pretraining** instead of retraining from scratch. The research consensus:

- Continued training's learning rate schedule and data distribution are what actually determine whether you get catastrophic forgetting — not just "was the checkpoint clean."
- The standard recipe when resuming a checkpoint on new data (Gupta et al. / "reuse don't retrain" line of work): re-warm the learning rate then cosine re-decay it, which lets the model adapt quickly to new data while improving downstream performance versus just continuing at the old decayed rate.
- Cheap insurance against forgetting: a replay fraction of just 1–5% of the original pretraining data, mixed into the new data, effectively mitigates forgetting. This is the ML equivalent of "the salt is still active" — you're not starting from zero, you're preserving the prior environment while introducing new stuff.
- Important nuance for MoE specifically: forgetting isn't uniform across layers. Earlier layers retain ~100–104% of original probe accuracy and can even improve on subsequent tasks, while degradation concentrates almost entirely in the final layer and readout head. So if you're doing DeepSeek v4 MoE work, your router + late layers are the "surface of the pan that touches new food" — that's where contamination/drift shows up first, not the backbone.
- Bottom line from the literature: no method guarantees perfect retention of all old tasks without sacrificing new learning — it's mitigation, not elimination.

## Where the analogy breaks

Salt contamination is local and detectable — you can smell a bad pan. Model contamination is **not locally detectable**:

```python
# The "smell test" doesn't exist for models — you have to build one.
# Minimal contamination/eval-leak check before you trust a public checkpoint
# or resume training on scraped data:

import hashlib
from datasets import load_dataset

def ngram_fingerprint(text, n=13):
    tokens = text.split()
    return {hashlib.md5(' '.join(tokens[i:i+n]).encode()).hexdigest()
             for i in range(len(tokens)-n+1)}

def contamination_rate(train_texts, eval_texts, n=13):
    eval_grams = set()
    for t in eval_texts:
        eval_grams |= ngram_fingerprint(t, n)
    hits = 0
    for t in train_texts:
        if ngram_fingerprint(t, n) & eval_grams:
            hits += 1
    return hits / len(train_texts)
```

If you're pulling a checkpoint off HF and continuing training, run this against your eval sets (or your target domain's held-out set) first. That's the actual analog of "checking if the pan smells bad" — except for models the check has to be *computational*, because your own senses give zero signal until eval scores mysteriously look too good (train/test leak) or the model degrades on something you didn't test (silent forgetting on a capability you didn't probe).

## Practical rule for your workflow

Don't reload from scratch when:
- You control the data pipeline and can verify no eval-set leakage
- You're doing domain-adaptive continued pretraining (your own nanochat-scale runs, MI300X sessions)
- You use LR re-warm + small replay buffer as default hygiene, not an afterthought

Do start fresh (new pot) when:
- The checkpoint's provenance/data mix is unknown or unverifiable (random HF upload, no data card)
- You're about to publish/ship it and haven't run a contamination check
- The checkpoint already shows anomalous eval behavior you can't explain

So: yes, "don't always use a new pot" is correct engineering instinct — checkpoint reuse and continual pretraining are standard practice and save enormous compute. But the safety mechanism isn't "trust it because nothing looks dirty" (that's the food analogy's weak point too) — it's LR re-warming, replay ratios, and an explicit contamination check, because unlike a bad-smelling pan, a contaminated checkpoint gives you no sensory warning.

References:

- [Domain-Adaptive Continued Pre-Training of Small Language Models](https://arxiv.org/pdf/2504.09687)
- [Reuse, Don't Retrain: A Recipe for Continued Pretraining of Language Models](https://arxiv.org/html/2407.07263v1)
- [Catastrophic Forgetting as Accessibility Collapse: A Three-Level Framework](https://arxiv.org/pdf/2606.06032)
