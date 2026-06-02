---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Implementing Trunk-Based Development with Feature Flags
translated: false
type: note
---

Question: What are the practical, step-by-step instructions to successfully implement Trunk-Based Development with feature flags in a real team?

Answer:

Here is a battle-tested, phased rollout plan that most teams use to move from Git Flow (or chaos) to true Trunk-Based Development with 20–100+ deploys per day.

### Phase 0 – Prerequisites (1–2 weeks)
1. Ensure you have real CI that runs on every commit (tests, lint, security scans).
2. Make the CI pipeline fast (<10 minutes for the critical path). If it’s slower, fix it first.
3. Achieve 80%+ unit test coverage and reasonable integration/e2e coverage.
4. Set up automated deployments to a staging environment on every merge to `main`.

### Phase 1 – Enforce “short-lived branches” (1–2 weeks)
- Maximum branch lifetime: 48 hours (many teams start with 24h).
- Enforce via CI policy: branch age >48h → pipeline fails.
- No more `develop`, `release/*`, or long-lived feature branches.
- Developers still create feature branches, but they must merge daily (or multiple times/day).
- Goal: Get the team used to small, frequent commits and continuous integration.

### Phase 2 – Introduce feature flags (2–6 weeks)

| Step | Action |
|------|--------|
| 1    | Choose a feature-flag system (LaunchDarkly, Unleash, ConfigCat, Split.io, or in-house). |
| 2    | Create a “Hello World” flag and toggle something trivial in production. |
| 3    | Define flag lifecycle rules: every flag must have an owner + removal date (max 30–90 days). |
| 4    | Add automated cleanup job: fail CI if dead flags exist. |
| 5    | Start wrapping every new feature in a flag. Old code can stay unflagged for now. |

### Phase 3 – Go fully trunk-based (the big switch)
1. Declare `main` as the only branch. Delete `develop` and all old release branches.
2. All work now happens either:
   - Directly on `main` (for very small changes), or
   - In extremely short-lived branches (<4 hours ideal, <24h absolute max).
3. Mandate “pair/mob programming” or mandatory code review within hours (not days).
4. Enforce “merge to main multiple times per day” as a cultural norm (track it in standups).

### Phase 4 – Continuous Deployment (the payoff)
1. Promote the exact same commit from staging → production automatically (or with one-click approval).
2. Deploy every merge to `main` to production (code is always behind flags or 100% safe).
3. Start removing old flags aggressively once features are fully rolled out.
4. Add canary deployments or ring deployments if you want extra safety.

### Phase 5 – Optimize & scale
- Move to commit-level deployments (some teams deploy every single commit).
- Implement “flag debt” dashboard and fail builds if >X stale flags.
- Add automated rollback on error-rate increase (PagerDuty + Spinnaker/Argocd rollbacks).
- Celebrate when you hit 10 deploys/day → 20 → 50 → 100.

### Typical timeline for a 10–50 person team

| Week | Milestone |
|------|----------|
| 1–2  | Fast CI + short-lived branch policy |
| 3–8  | Feature flags on all new work |
| 9–12 | Full trunk-only + continuous deployment to production |
| 12+  | 20+ deploys/day, near-zero incidents |

### Common pitfalls & how to avoid them

| Pitfall                        | Fix                                                                 |
|--------------------------------|---------------------------------------------------------------------|
| “My feature is too big for a flag” | Break it into 10 small flags (UI flag, API flag, DB migration flag, etc.) |
| Database schema changes         | Use expandable migrations + rollback scripts + feature-flagged code |
| Fear of breaking prod           | Start with dark launches and percentage rollouts (0.01% → 100%)    |
| Flag sprawl                    | Enforce 30-day max lifetime + automated cleanup                     |

Once you reach Phase 4, deployment truly becomes boring — exactly what you want.

References:
- [Trunk Based Development – Full implementation guide](https://trunkbaseddevelopment.com)
- [Paul Hammant’s TBD short-lived branches page](https://paulhammant.com/2013/05/22/trunk-based-development-in-pictures)
- [Google’s Site Reliability Engineering book – Chapter 27: Continuous Deployment](https://sre.google/sre-book/release-engineering)
- [Feature Flag Driven Development – Martin Fowler](https://martinfowler.com/articles/feature-toggles.html)
- [Accelerate – 2023 State of DevOps Report (trunk-based development correlation)](https://cloud.google.com/devops/state-of-devops)
