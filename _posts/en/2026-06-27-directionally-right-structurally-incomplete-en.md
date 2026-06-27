---
audio: false
generated: true
image: false
lang: en
layout: post
title: Directionally Right, Structurally Incomplete
translated: false
type: note
---

You're directionally right, but let me sharpen where the argument holds and where it breaks.

**Where you're correct:**

The "one digital bank per region, 1000-person team each" model is genuinely structurally inefficient. The core IT insight you're invoking — marginal cost of software approaches zero, so duplicating teams across regions to rebuild the same KYC/onboarding/ledger/payments stack is the opposite of the scaling effect software should give you. Wise and Revolut prove the alternative: one codebase, one core platform, ~tens of millions of users, where each new market is a config/compliance layer on top of shared infrastructure rather than a fresh 1000-person rebuild. Revolut hit ~50M+ users with a fraction of the headcount-per-user of any incumbent regional bank. That's the compounding you're pointing at.

The "大锅饭" critique also has teeth: in a per-region cost center, individual leverage is low, comp is capped, there's no equity, and your output doesn't compound into anything you own. For *you specifically* — contractor, no promotion path — this is exactly the (b)-tax to minimize.

**Where the argument is incomplete:**

1. **Regulation is the actual reason, not stupidity.** Banks fragment by region because banking licenses, capital requirements, data residency, and regulators are per-jurisdiction. A global bank legally *cannot* run one ledger across all markets the way Wise does — and even Wise/Revolut aren't doing what they look like. Revolut operated for years on an EMI (e-money) license, not a full banking license, which is precisely why it could centralize. It struggled for *years* to get a UK banking license (finally granted 2024) and still doesn't have one in many markets it operates in. The "几千万用户 one app" model partly works because they avoided being a real bank for as long as possible.

2. **Scope is different.** Wise/Revolut do consumer payments, FX, cards, some savings. They do *not* do corporate lending, securities settlement, custody, trade finance, or the 对公 business that's a huge chunk of a global bank's actual revenue and where the margins and moats are. "几千万 consumer users" is a great *product* business but not obviously a bigger *enterprise* than corporate banking. The fintech disrupts the thin retail layer; the boring institutional core is harder to unbundle.

3. **The fintechs are less profitable than they look.** Revolut turned its first meaningful profit recently; many neobanks (Monzo, N26, Chime) burned enormous capital for thin or negative margins per user. Acquiring 几千万 users who hold small balances and pay near-zero fees is a real-business problem, not a free win. The incumbents' "wasteful" regional teams are sitting on deposit franchises and lending spreads that the apps don't have.

**The synthesis that's actually useful to you:**

The future isn't "one app beats regional banks." It's that the *infrastructure layer* gets unbundled and commoditized — BaaS, embedded finance, shared core platforms (Thought Machine, Mambu, Marqeta) — so that the 1000-person regional rebuild becomes a 50-person integration. The incumbents that survive will be the ones that internally adopt this and kill their own duplication. The fintechs win the retail UX and the platform vendors win the rails.

So your instinct — *don't tie your compounding to a per-region cost center* — is right. But the lesson for your trajectory isn't "go build a Revolut." It's: the leverage is in the **horizontal platform/tooling layer**, not in any single regional vertical. That's also exactly where AI-native single-operator businesses now have an edge — the thing you're already building toward. One person with agents replacing what regional integration teams do is a far more defensible wedge than competing with Revolut on consumer acquisition.

Is your read that the bank's internal tooling/platform fragmentation is the specific inefficiency you'd want to attack, or are you thinking more about the consumer-app end?
