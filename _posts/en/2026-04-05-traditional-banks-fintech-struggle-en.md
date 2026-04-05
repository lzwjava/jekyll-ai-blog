---
audio: false
generated: true
image: false
lang: en
layout: post
title: Traditional Banks Struggle Against Global Fintech
translated: false
type: note
---

Question:
Are traditional foreign banks with fragmented regional apps less efficient than global AI-driven platforms like Revolut and Stripe, and is this why engineers in Chinese big tech often earn more?

Answer:

Yes — your reasoning is broadly correct, but it needs a nuanced breakdown. The difference comes from **architecture, scale model, and engineering leverage**, not just “AI” alone.

---

# 1. Traditional multinational banks: fragmented + manpower-heavy

Banks like Standard Chartered and DBS Bank typically operate like this:

* Each **country/region has its own app**
* Separate compliance, KYC, payment rails
* Separate engineering teams
* Legacy core banking systems
* Heavy vendor outsourcing
* Slow release cycles

This creates:

* duplicated engineering effort
* inconsistent user experience
* slow feature rollout
* high operational cost
* low engineering leverage

Example structure:

```
UK App  -> UK team
HK App  -> HK team
SG App  -> SG team
IN App  -> India team
AE App  -> Middle East team
```

This is **human scaling**, not **software scaling**.

So even with **tens of millions of high-end customers**, profit per engineer is relatively low.

---

# 2. Global fintech platforms: software + platform scaling

Companies like Revolut and Stripe use a **single global platform**:

* one core ledger
* one API platform
* one risk engine
* one AI fraud model
* one UX
* config per region

Structure:

```
Global Core Platform
     ↓
 Region configs (currency, compliance)
     ↓
 Same app everywhere
```

This gives:

* 10x engineer leverage
* unified data → better AI
* faster iteration
* lower marginal cost
* global network effects

This is **software scaling**.

---

# 3. Why Chinese big tech engineers often earn more

Companies like:

* Tencent
* Alibaba
* ByteDance

operate closer to **platform model**, not bank model:

* unified super apps
* huge scale users
* fast iteration
* AI everywhere
* infra reuse
* small teams with big impact

So:

* engineer output higher
* profit per engineer higher
* salaries higher
* but also more competitive (“卷”)

---

# 4. Banks are structurally disadvantaged

Traditional banks face:

* regulatory fragmentation
* country licenses
* legacy cores (COBOL, mainframes)
* risk-averse culture
* vendor dependency

Even if they want to be global, they **can't easily unify**.

That’s why fintechs often out-innovate banks.

---

# 5. AI makes the gap even larger

AI benefits **unified data platforms**:

Revolut / Stripe:

* global fraud model
* global credit model
* unified behavior data
* automated ops

Traditional banks:

* siloed data
* local models
* manual review

So AI **amplifies** platform advantage.

---

# Final conclusion

Your intuition is mostly right:

* Regional bank apps → low efficiency
* Global fintech platform → high efficiency
* AI increases platform advantage
* Higher leverage → higher engineer salary
* Chinese big tech closer to platform model → higher pay but more intense

But one caveat:

Banks optimize for **safety + regulation**, not **efficiency**.
Fintechs optimize for **scale + speed**.

Different goals → different architectures.