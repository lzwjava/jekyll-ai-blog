---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Choose arXiv License
translated: false
type: note
---

Question: How should I choose an arXiv license for my submission?

Answer:

Quick recommendation: **CC BY 4.0** for most cases. It's the most open, satisfies funder mandates (Plan S, NIH, ERC), and lets anyone reuse your work as long as they credit you. You retain copyright.

Here's the decision tree:

**CC BY 4.0** — Default choice. Anyone can share, remix, build on it (even commercially) with attribution. Maximizes reach and citations. Required by many open-access funders. Pick this unless you have a specific reason not to.

**CC BY-SA 4.0** — Same as CC BY, but derivatives must use the same license (copyleft). Choose if you want to prevent your work being absorbed into closed derivatives. Slightly more friction for reusers.

**CC BY-NC-SA 4.0** — Adds a non-commercial restriction. Avoid unless required — "non-commercial" is legally murky and blocks legitimate reuse (e.g., a startup training on your text, inclusion in some datasets/textbooks). Hurts reach.

**CC BY-NC-ND 4.0** — Non-commercial *and* no derivatives. The most restrictive CC option. Only the verbatim PDF can be redistributed. Bad for an ML paper you want built upon.

**arXiv non-exclusive license** — The old default. You grant arXiv the right to distribute; you keep everything else and grant no reuse rights to readers. Pick this if your target **journal forbids CC licensing on preprints** (some still do) or your publisher agreement requires it. Conservative, journal-safe.

**CC Zero (CC0)** — Public domain dedication, no rights reserved, no attribution required. Maximally open but you give up the attribution requirement. Most academics skip this since they want credit.

For your situation specifically (building in public, want maximum reuse and visibility, no journal/funder constraints on a self-published technical paper): **CC BY 4.0**. It's irrevocable per version, so if you later submit to a journal with restrictive preprint rules, you can apply a different license to that *version* — but CC BY rarely causes problems since most ML venues (NeurIPS, ICML, ICLR, ACL) accept CC BY preprints.

One caveat: if you're co-authoring with someone at an institution or under a grant, check their mandate first — some require CC BY, some forbid it.

References:

- [arXiv License Information](https://info.arxiv.org/help/license/index.html)
- [Creative Commons License Chooser](https://creativecommons.org/choose/)
