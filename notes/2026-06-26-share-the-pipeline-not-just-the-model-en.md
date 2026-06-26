---
audio: false
generated: true
image: false
lang: en
layout: post
title: Share the pipeline, not just the model
translated: false
type: note
---

**Question:** Should I publish this SEC-EDGAR GPT-2 124M training run internally at the bank (e.g. ping the big AI channel)? And should I run evals/benchmarks first, or move fast and show it quickly?

**Answer:**

Short version: yes, share it — but reframe what you're sharing, and spend 2-3 hours on a minimal eval first. Not because eval is virtuous, but because in a *bank* context, a raw `val_loss=3.2` number is meaningless to 95% of the channel and actively risky with the other 5% who'll ask "compared to what?"

**The reframe that matters**

A 124M model that hits val_loss ~3.2 on SEC filings is, by itself, not impressive to a banking AI audience — they have GPT-4 access. If you post "I trained GPT-2 from scratch on 10-Ks, loss 3.2," the likely internal reaction is polite silence or "why not just prompt Claude?" That undersells you badly, because the *actual* impressive thing is the capability you've demonstrated: you can take a domain corpus → tokenize → train a model end-to-end on your own GPU in 9 hours. That's a reusable pipeline, not a one-off model.

So lead with the capability, not the artifact:

> "Built an end-to-end pretraining pipeline (raw SEC EDGAR → tokenized 1.55B tokens → trained 124M GPT-2 in 9.2h on a single 4070). Pipeline is corpus-agnostic — point it at any internal text corpus and get a domain LM. Here's what a from-scratch financial LM learns, and where the cost/quality line sits vs fine-tuning."

That framing converts "small toy model" into "I can build domain models for us cheaply."

**Minimal eval — fast, high-signal, ~2-3 hours**

Skip formal benchmarks (HellaSwag etc. are irrelevant for a domain LM and will score poorly, hurting you). Do three things instead, all of which produce screenshots that *show*, not tell:

1. **Qualitative generation samples (30 min).** Generate completions from real 10-K prompt prefixes — a risk-factor opening, an MD&A sentence, a balance-sheet line. Put base GPT-2 124M side-by-side with your SEC model on the *same* prompts. The contrast (generic web text vs. fluent SEC boilerplate) is the single most persuasive artifact you can produce. This is your headline image.

```python
prompts = [
    "Item 1A. Risk Factors. Our business is subject to",
    "The following table sets forth our consolidated",
    "Management's Discussion and Analysis of Financial Condition",
]
# generate with both ckpts, temp=0.8, 100 tokens, show side by side
```

2. **Domain-vs-base loss delta (20 min).** Compute val_loss of *stock* GPT-2 124M on your SEC val shard vs. your trained model. If stock GPT-2 is ~4.5+ and yours is ~3.2, that delta *is* your benchmark — it's interpretable ("28% lower perplexity on financial text") and self-contained, no external leaderboard needed.

3. **One concrete downstream hook (1 hr, optional but strong).** A bank audience cares about *use*, not perplexity. Pick one: zero-shot next-section prediction, or extract the model's hidden states as features for a tiny financial-text classifier (e.g. risk-factor vs MD&A section ID). Even a crude 80% accuracy on a real task lands far harder than any loss curve.

That's it. Don't build a full harness — you'll lose the speed advantage that's your whole point.

**On posting to the big AI channel — yes, but tactically**

Three caveats specific to your situation as a contractor:

- **Data/compliance check first.** SEC EDGAR is fully public, so the *data* is clean. But confirm you trained on *your own* hardware (192.168.x.x workstation / AMD cloud), not bank infra, and say so explicitly. "Trained on personal GPU, public SEC data" preempts the one question that could turn this from a win into a problem.
- **Don't frame it as "look what I did on the side."** Frame it as "here's a capability that could be useful for us" — domain LMs for internal corpora, cheap fine-tuning bases, embeddings for financial retrieval. This aligns with your playbook point 3 (use bank problems as learning ground) and converts personal work into perceived value-add.
- **Big channel vs. targeted DM.** A cold post to a 500-person AI channel often gets less traction than DMing the 3-4 people who actually run ML there, *then* posting once one of them engages. Warm the signal first. This also serves your point 1 (prune for people who make you sharper / could matter later).

**Speed vs. polish — your instinct is right**

You've been learning AI for 3 years and training for months; the bottleneck now isn't more training, it's *visible output*. Ship the share this week. The 2-3 hour eval is the minimum that makes the share credible rather than dismissible — past that, more polish has sharply diminishing returns. Generation samples + loss delta + one downstream demo + the pipeline framing = a 30-minute writeup that punches well above a 124M model's weight.

One last thing: package the pipeline as a clean repo (or internal gist) with a one-command reproduce. "Here's the model" is forgettable; "here's the tool that makes models, run it yourself" is what gets you remembered and pinged later when someone needs exactly this.
