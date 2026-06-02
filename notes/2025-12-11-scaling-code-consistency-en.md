---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Scaling Code Consistency Beyond Single Gatekeepers
translated: false
type: note
---

Question: In large companies, should every team have a single main gatekeeper for the Git repository, overall project architecture, code quality, and code style to ensure long-term consistency? And why is code consistency so hard to maintain—why do most large projects end up messy?

Answer:

Having **one single gatekeeper** (a “tech lead” or “architect czar”) can work well in small-to-medium teams or in the early stages of a project, but it almost always fails or becomes a bottleneck in big corporations and long-lived large codebases. Here’s why most companies deliberately avoid the “one supreme gatekeeper” model and why consistency is still so hard:

### Why a single gatekeeper doesn’t scale in big corps

| Problem | What happens with one gatekeeper | What actually happens in practice |
|---------|----------------------------------|-----------------------------------|
| Bottleneck | All non-trivial changes wait for that one person’s review | Velocity drops, teams get frustrated, people start working around the gatekeeper |
| Bus factor = 1 | Person goes on vacation, gets sick, or leaves → everything stops | Knowledge silos form, onboarding new architects takes months |
| False sense of consistency | One person enforces their personal taste | Taste changes over time, or the person wasn’t actually consistent themselves |
| Slow decision making | Every new library, pattern, or refactoring needs their blessing | Teams either wait forever or just YOLO it (creating more mess) |

Successful big-tech companies (Google, Meta, Amazon, Microsoft, etc.) use a very different model:

### What actually works at scale

| Mechanism | Purpose | Examples |
|-----------|--------|--------|
| Small set of owners per area (usually 2–5 senior engineers) | Redundancy + faster reviews | Google’s OWNERS files, GitHub CODEOWNERS |
| Strong automated enforcement | Linters, formatters, static analysis, presubmit checks | clang-format, ktlint, ESLint + Prettier, ErrorProne, etc. run on every CL |
| Architecture Decision Records (ADRs) and RFC processes | Written, searchable decisions instead of tribal knowledge | Amazon’s 6-pagers, Google’s design docs |
| Style guides that are enforced by tools, not humans | Humans only handle the hard cases | Airbnb JavaScript Style Guide + ESLint, Google Java/C++ Style Guides |
| Periodic “consistency sprints” or tech debt weeks | Fix accumulated mess in bulk instead of preventing every tiny deviation | Meta’s “Hackathons for cleanup, Google’s Fixits |

### Why consistency is inherently hard (even with the above)

1. **Team turnover** – People who made the original decisions leave; new people don’t know the old context.
2. **Local optima vs global optima** – A pattern that is slightly worse globally can be much faster locally, so teams pick it under deadline pressure.
3. **Feature urgency always beats tech debt** – Business says “ship by Christmas or we lose $10 M”, nobody cares about perfect naming.
4. **Gradual accretion** – 5 % inconsistency per year compounds. After 8 years you have ~50 % mess even if every single change was reasonable.
5. **Different sub-teams have legitimately different needs** – The ads backend and the mobile client don’t need the same patterns.
6. **Tooling and language evolution** – The “correct” way in 2018 becomes legacy in 2024 (callback → Promise → async/await → React Server Components…).

### Bottom line

No, you do **not** want one supreme gatekeeper in a big corp. You want:

- Clear written standards
- Ruthless automation of those standards
- A small, rotating set of owners per component (not one hero)
- Cultural acceptance that paying down tech debt is real work

Companies that rely on a single heroic architect eventually hit a wall around ~50–100 engineers on the codebase. Companies that invest in automation and distributed ownership can keep 1,000+ engineers moving fast with surprisingly decent consistency.

References:

- [Google Engineering Practices – Code Review](https://google.github.io/eng-practices/)
- [ThoughtWorks Tech Radar – Centralized vs Decentralized Ownership](https://www.thoughtworks.com/radar/techniques)
- [The Architecture Bottleneck (Stripe engineering blog)](https://stripe.com/blog/scaling-engineering)
