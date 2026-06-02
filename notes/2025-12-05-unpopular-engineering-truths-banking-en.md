---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unpopular Engineering Truths in Banking
translated: false
type: note
---

Question: What are some unpopular or contrarian ideas in engineering within the banking and financial services industry?

Answer:

Here are several engineering ideas in banking that are technically sound but remain deeply unpopular (or slow to adopt) among banks, regulators, and traditional engineering teams:

- **Monoliths are often better than microservices for core banking systems**
  Most banks chase microservice architectures, but many core banking functions (ledger, payments, risk) are inherently transactional and require strict consistency. A well-modularized monolith with clear boundaries frequently outperforms a distributed microservice mess in reliability, latency, and development velocity. The unpopular truth: premature decomposition creates more problems than it solves.

- **Event sourcing + CQRS is the correct architecture for a general ledger**
  Despite being the academically “right” way to model double-entry accounting immutably, almost no major bank has fully committed to it at the core ledger level. Banks still prefer mutable relational tables because “that’s what COBOL did” and auditors understand them.

- **Most “real-time” banking doesn’t actually need to be real-time**
  Customers are fine with eventual consistency for 99% of use cases (balance updates, fraud alerts, rewards). True instant settlement is expensive and complex. The unpopular opinion: batch is still king for the majority of volume, and pretending otherwise burns money.

- **Feature flags and dark launches are more important than CI/CD pipelines**
  Banks obsess over Jenkins/GitLab pipelines but often deploy with big-bang releases and manual approvals. Progressive delivery with feature flags reduces risk far more than any fancy pipeline, yet it’s resisted because “we can’t toggle production.”

- **Immutable infrastructure and pets → cattle is largely impractical for core banking**
  Mainframes and heavily regulated mid-range systems (e.g., Tandem, IBM i) are still “pets” for good reason: zero-downtime requirements, strict audit trails, and hardware-specific licensing. Treating them like cattle often fails spectacularly.

- **Blockchain/distributed ledgers are mostly solved problems—by databases**
  The coordination and consensus problems blockchain solves already have decades-old solutions in distributed databases (Paxos, Raft, Spanner). The unpopular take: private blockchains in banking are mostly marketing theater.

- **Open-source core banking systems (Mifos, Mojaloop, Fineract) are good enough for many use cases**
  Building or buying a $100M+ proprietary core is often justified by “we’re unique,” yet most retail banking logic is commoditized. Few incumbents are willing to admit this.

- **Most machine-learning fraud models are overkill**
  Simple velocity + rules engines still catch >95% of fraud at a fraction of the cost and explainability hassle. Deep learning is often deployed for signaling sophistication rather than actual ROI.

- **COBOL isn’t the problem; the organizational structure around it is**
  The code is boring, readable, and insanely reliable. The real issue is the 40-year release cycles and change approval boards, not the language itself.

- **“Cloud-first” is sometimes reckless for Tier-1 banks**
  Latency, data sovereignty, and vendor lock-in still make on-prem or hybrid the rational choice for certain workloads (high-frequency payments, core ledger). Saying this out loud in 2025 gets you strange looks.

These opinions tend to be career-limiting inside large banks but are quietly held by many seasoned engineers who have watched multiple “transformation” initiatives crash and burn.

References:

- [ThoughtWorks Technology Radar – Monoliths vs Microservices debates](https://www.thoughtworks.com/radar/techniques/monoliths-vs-microservices)
- [Event Sourcing in Banking – Greg Young presentations](https://www.youtube.com/watch?v=LDW0QWie21s)
- [The COBOL is not the problem rant – multiple industry blogs circa 2020-2024]
