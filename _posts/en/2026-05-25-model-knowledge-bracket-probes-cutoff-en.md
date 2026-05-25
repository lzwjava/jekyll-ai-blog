---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Knowledge Bracket Probes Cutoff
translated: false
type: note
---

**Question:** DeepSeek-V2-Lite-Chat knows ChatGPT — what does this tell us about its training cutoff, and what's our final bracket?

**Answer:**

## The bracket is now tight

| Event | Date | Model knows it? |
|-------|------|-----------------|
| ChatGPT launch | Nov 30, 2022 | ✅ Yes |
| GPT-4 release | Mar 14, 2023 | ❌ No |

**Conclusion: training data cutoff is between December 2022 and March 2023** — roughly a 3-month window.

Most likely: **January–February 2023**, since data pipelines typically have a lag (you collect, deduplicate, filter, tokenize — that takes weeks after the nominal cutoff date).

## This is actually coherent with the September 22, 2022 "date" hallucination

The model's data is densest around late 2022. The SFT instruction data was probably generated/curated around that same period, which is why it anchored to September 2022 when asked "what day is it." Not a random hallucination — it was reflecting the center of mass of its training distribution.

## Final picture

```
DeepSeek-V2-Lite-Chat knowledge timeline:

[dense coverage]          [sparse/none]
━━━━━━━━━━━━━━━━━━━━━━━━━|════════════════════════
          ...2022      Jan-Feb 2023   Mar 2023 →
                           ↑
                     cutoff zone
                     
Release date: May 2024  (~15 months after cutoff)
```

That ~15 month gap between cutoff and release is typical for a model of this scale — pretraining a MoE at this size, then SFT + alignment, takes serious calendar time even with large GPU clusters.

## The probing method works

Three questions, clean bracket:

```python
probes = {
    "what day is it":        "noisy, anchors to training density",
    "do you know GPT-4":     "post-Mar 2023 → No  ✓ upper bound",
    "do you know ChatGPT":   "post-Nov 2022 → Yes ✓ lower bound",
}
# Result: cutoff in [Nov 2022, Mar 2023]
```

This is a useful general technique whenever you run a local model and want to calibrate how stale its knowledge is before trusting it on anything time-sensitive.