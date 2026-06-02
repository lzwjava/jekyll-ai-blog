---
audio: false
generated: true
image: false
lang: en
layout: post
title: Smart Parallel Repo Update Optimization
translated: false
type: note
---

28s for 99 repos. Compare the three approaches:

```
Sequential (old):            ~99 × 4.4s ≈ 435s (7+ min)
Parallel pull (no check):    ~99 × 4.4s ÷ 8 ≈ 55s
Smart fetch-first (current): 28s  (98 up-to-date did fetch-only, 1 pulled)
```

The smart approach cut it roughly in half vs naive parallel pull. Here's why:

```
Repo that's up-to-date:
  Old:  git fetch (negotiate refs) + git merge (no-op) + verbose output parsing
  New:  git fetch (negotiate refs) → see 0 behind → skip

Repo that needs update:
  Old:  git fetch + git merge + verbose output
  New:  git fetch → see N behind → git pull (fetch again + merge)
```

The up-to-date repos save the merge step and verbose parsing. For 98/99 repos being current, that compounds.

To your original question about whether the initial pull is unnecessary because `gpa` handles pull on push-failure: `gpa` only runs on repos you're committing to. `projects update` covers all 99 repos — most are upstream projects you just track (pytorch, llama.cpp, dify, etc.). You need to pull those to get the latest code. The optimization is making that check cheap.
