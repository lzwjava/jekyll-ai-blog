---
audio: false
generated: true
image: false
lang: en
layout: post
title: User Count Isn't Economic Scale
translated: false
type: note
---

Question: In large corporations, internal tools and platforms aren't marketed externally, meaning they only have thousands of users — so isn't their economic scale inherently small?

Answer:

This is a common intuition, but **user count ≠ economic scale** in the enterprise context. Here's why:

**Value is measured differently internally**

| Metric | Consumer app | Internal platform |
|---|---|---|
| Scale signal | MAU / DAU | Hours saved × headcount × salary |
| Revenue model | Direct monetization | Productivity / error reduction |
| User count | Millions | Thousands |
| Value per user | Low (~$/month) | Very high (~$10k-$100k+/year) |

If an internal tool saves 2 hours/week per engineer at a company with 10,000 engineers earning $200k/year, that's roughly **~$200M/year in recovered productivity** — from "only thousands of users."

**Other scaling factors that matter more than user count:**

- **Process criticality** — An internal CI/CD platform, data pipeline, or risk system can gate *billions* in business operations. Downtime = direct revenue loss.
- **Leverage on core business** — Amazon's internal logistics tools, Google's Borg (cluster scheduler), or Goldman Sachs' trading infrastructure don't need millions of users to justify enormous investment.
- **Build cost amortized over time** — Once built, a 10,000-user internal platform can run for a decade, compounding its ROI.
- **Switching cost** — Internal platforms often become so embedded that replacing them costs more than the original build.

**Where you *are* right:**

The small user base *does* create real problems:
- Harder to justify headcount for dedicated teams
- Feedback loops are slower and less diverse
- No network effects
- Features get cut because "it's internal, good enough"

This tension is why many companies eventually **open-source or commercialize** their internal tools (e.g., Google → Kubernetes, Facebook → React, Netflix → various OSS projects) — to escape exactly the economic trap you're describing.

References:
- [Why Big Tech Companies Build Internal Tools (and Why It Matters)](https://medium.com/swlh/why-big-tech-companies-build-internal-tools-and-why-it-matters-2e3d2b9bf2e3)
- [The Economics of Internal Developer Platforms — Thoughtworks](https://www.thoughtworks.com/insights/blog/platform-engineering/economics-of-internal-developer-platforms)
- [From Internal Tool to Open Source: The Google Kubernetes Story](https://kubernetes.io/blog/2018/07/20/the-history-of-kubernetes-the-community-behind-it/)
