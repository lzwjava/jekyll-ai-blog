---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Trunk-Based Development Benefits
translated: false
type: note
---

Question: Is the case against using multiple Git branches (like Git Flow) and instead using a single main branch with feature flags strong, especially the claim that teams can go from days-long release cycles to 20+ deploys per day with zero incidents?

Answer:

The case is very strong in modern software engineering — especially for teams building web services, SaaS products, or any continuously delivered system. This approach is often called "Trunk-Based Development" (TBD) + Feature Flags, and it’s the backbone of how companies like Google, Facebook, Netflix, and most of the “high-scale” tech world operate today.

### Why the anti-branching argument holds up

| Problem with long-lived feature branches (Git Flow style) | How Trunk-Based Development + Feature Flags solves it |
|-------------------------------------------------------------|----------------------------------------------------------------|
| “Nobody knows what’s actually in prod” (merge hell, integration debt) | Everyone works on `main`. The commit that’s in production is literally the same commit (or a very recent one) that every developer has locally. |
| Constant merge conflicts and integration surprises             | Continuous integration is real — you integrate multiple times per day instead of once every few weeks. |
| Releases are big, risky, and slow (days/weeks)                  | You deploy the exact same commit to all environments. New code is hidden behind feature flags until ready → you can deploy 20–100 times per day safely. |
| Hotfixes require cherry-picking and special branches           | Hotfix = commit to `main` + deploy + toggle the flag (or revert the flag). No special branch needed. |
| Rollbacks are terrifying (undoing a 2-week batch of features)  | Rollback = toggle flags off or deploy previous commit. Takes seconds, not hours/days. |

### Real-world evidence
- Google, Facebook, and Microsoft have been doing trunk-based development for 15+ years and publish papers showing near-zero deployment incidents despite thousands of deploys per day.
- The 2023 State of DevOps reports (Accelerate / DORA) continue to show that elite performers (the ones with >100 deploys/day and <1-hour lead time) overwhelmingly use trunk-based development and feature flags.
- Netflix famously went from quarterly releases to thousands of deploys per day after adopting this pattern.
- Shopify, Etsy, and many fintech companies publicly credit 20–100 deploys/day with zero downtime to this exact shift.

### The “20+ deploys/day with zero incidents” claim
It’s not marketing hype — it’s routine for mature teams using this pattern. Once you stop batching features into big releases and instead ship every commit behind flags, deployment becomes a complete non-event. The only thing that can break production is a bad flag toggle (which is instantly reversible) or a data-migration issue, and those are far rarer than integration bugs from long-lived branches.

### When branches are still useful
- Open-source projects with many external contributors (pull-request model is fine).
- Very large monoliths without good feature-flag infrastructure (but even then, most teams eventually invest in flags and move to trunk).
- Regulated environments that legally require “release packages” (healthcare, aerospace) — though even many of those are moving to flag-based continuous deployment with audit trails.

Bottom line
Yes, the case is extremely solid. For almost all product/development teams today, long-lived feature branches are an anti-pattern that directly causes slow, risky, painful releases. Switching to one main branch + feature flags routinely delivers the 10–100× improvement in deployment frequency and stability that the poster claims.

References:
- [Accelerate: State of DevOps Reports (multiple years](https://www.devops-research.com/research.html)
- [Trunk Based Development website and case studies](https://trunkbaseddevelopment.com)
- [Google’s paper on >100 deploys/day (2016, still relevant)](https://cloud.google.com/architecture/devops/devops-measurement-monitoring-and-observation)
- [Feature Flags at scale — LaunchDarkly / Optimizely case studies]
