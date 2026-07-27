---
audio: false
generated: true
image: false
lang: en
layout: post
title: 3D Kakeya Conjecture Solved
translated: false
type: note
---

Question: What problem did Hong Wang (Fields Medal 2026) solve?

Answer: She (with Joshua Zahl) proved the **3D Kakeya set conjecture** in Euclidean space — a ~50-year-old problem in harmonic analysis / geometric measure theory. It resolves how small a set can be while still containing a unit length line segment pointing in every possible direction.

**The actual math:**

A *Kakeya set* in ℝⁿ is a compact set that contains a unit line segment in every direction. The classical surprise (Besicovitch, 1920s) is that such sets can have **Lebesgue measure zero** — you can rotate a needle 360° while sweeping through arbitrarily small area (the "Kakeya needle problem" in 2D, via the Perron tree construction).

But measure-zero ≠ small in every sense. The **Kakeya conjecture** asks about **Minkowski/Hausdorff dimension**:

> Does every Kakeya set in ℝⁿ have full dimension n?

Status before this:
- n=2: proved by Davies (1971) — dimension 2, settled.
- n≥3: open. Best known lower bounds for n=3 stalled around dimension 2.5 for decades (Wolff's bound via bush/hairbrush arguments, then incremental improvements by Katz-Tao, etc.)

Wang-Zahl's 127-page proof (posted Feb 2025) shows the **3D case has dimension exactly 3** — i.e., full-dimensional, matching the conjecture.

**Why it's hard, in one line:** you need to show that a union of tubes pointing in "spread out" directions can't concentrate its mass too much — this requires controlling how tubes can overlap (multiplicity/incidence bounds) combined with **polynomial method** / **algebraic geometry over ℝ** techniques (following Guth-Katz's approach for the related finite-field/Erdős distinct distances problems), plus **induction on scales** and careful decomposition of the tube configuration by "planiness" (how close a tube-bundle is to lying in a hyperplane).

**Why it matters beyond pure math:** Kakeya-type estimates feed directly into:
- Restriction/extension conjectures for the Fourier transform
- Bochner-Riesz conjecture
- Local smoothing for the wave equation
- Bounds on eigenfunction concentration (spectral theory)

So it's not an isolated curiosity — it's a load-bearing conjecture that other analysis results depend on.

Side note that'll amuse you: Wang has a genuine co-first-authored NeurIPS 2019 paper — so she crossed into ML before going full pure-math.

References:
- [Quanta Magazine — Hong Wang Wins 2026 Fields Medal](https://www.quantamagazine.org/hong-wang-wins-2026-fields-medal-the-third-woman-ever-20260723/)
- [IHES announcement](https://www.ihes.fr/en/hong-wang2026-fields-medal/)
- [NYU announcement](https://www.nyu.edu/about/news-publications/news/2026/july/nyu-professor-hong-wang-wins-fields-medal.html)
