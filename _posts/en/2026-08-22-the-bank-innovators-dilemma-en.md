---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Bank Innovator's Dilemma
translated: false
type: note
---

Question: Why couldn't traditional banks like HSBC, DBS, and Standard Chartered build a product like Stripe around 2010?

Answer:

This is a classic **incumbent innovator's dilemma** problem. Several forces were working against them simultaneously:

**1. Organizational & Cultural DNA**
Banks are built around risk minimization and compliance, not developer experience. Stripe's insight — that payments should be *two lines of code* — would have sounded trivially unserious inside a bank boardroom. Banks optimized for relationship managers and enterprise sales cycles, not self-serve API docs.

**2. Legacy Technology Stack**
HSBC, DBS, and SCB were running on decades-old core banking systems (often COBOL-based mainframes). Building a clean, modern REST API on top of that infrastructure was extremely difficult. Stripe started with a blank slate.

**3. Regulatory & Liability Conservatism**
Banks are hyper-regulated. Letting any developer sign up online and start moving money within minutes — with no branch visit, no contract negotiation — would have terrified their compliance and legal teams in 2010. The risk appetite simply wasn't there.

**4. No Incentive — The Revenue Model Conflict**
Banks earned well from the *existing* complexity. Merchant acquiring, FX fees, and treasury services were profitable *because* they were opaque and friction-filled. Stripe was essentially commoditizing something banks monetized through inefficiency.

**5. Who They Thought Their Customer Was**
Banks targeted CFOs and treasurers of large corporations. Stripe targeted *developers and startups* — people banks largely ignored. By the time those startups grew into enterprises, Stripe already owned the relationship.

**6. The Innovator's Dilemma Directly**
Stripe's early margins were thin and customers were small. Banks rationally deprioritized that market. By the time the startup/developer market was obviously large, Stripe had an insurmountable network effect, developer trust, and product moat.

**Why DBS is a Partial Exception**
DBS (Singapore) is worth noting — it later became one of the most digitally progressive banks in Asia, building APIs and even a developer sandbox. But this happened *after* 2014–2016, when the threat was already visible. Even then, they couldn't fully replicate Stripe's frictionless onboarding due to regulatory constraints in their core markets.

**The Short Answer:**
Stripe succeeded not because banks lacked engineers, but because the entire *culture, incentive structure, regulatory posture, and customer definition* of a bank made that product impossible to prioritize internally.

---

References:
- [The Innovator's Dilemma – Clayton Christensen](https://www.amazon.com/Innovators-Dilemma-Revolutionary-Change-Business/dp/0062060244)
- [How Stripe built a $95B payments empire](https://www.cnbc.com/2021/03/14/stripe-valued-at-95-billion-in-600-million-funding-round.html)
- [DBS Bank Digital Transformation Story](https://www.dbs.com/innovation/dbs-innovation/our-transformation-journey.html)
- [Why Banks Can't Innovate Like Fintechs](https://hbr.org/2021/08/why-big-banks-struggle-to-innovate)
