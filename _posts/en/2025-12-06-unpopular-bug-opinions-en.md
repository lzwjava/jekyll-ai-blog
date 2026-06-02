---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Why Bugs Persist Unpopular Opinions
translated: false
type: note
---

Question: What are some unpopular opinions about why developers or teams fail to solve software problems or fix bugs?

Answer:

Here are some genuinely unpopular (and often uncomfortable) opinions about why bugs persist or problems remain unsolved, based on real-world observation rather than feel-good narratives:

- **Most bugs aren’t hard technically—they’re hard socially.** The code is obvious to fix, but someone’s ego, politics, or fear of blame keeps it unfixed. Teams would rather live with a known bug for years than admit the original author (or architect) was wrong.

- **“We don’t have time to fix it properly” actually means “We don’t have the skill to fix it properly.”** Experienced engineers fix root causes quickly. Incompetent or junior-heavy teams turn one-line fixes into multi-month sagas and then blame “technical debt.”

- **Many persistent bugs are features in disguise.** Users have adapted their workflow around the bug. Fixing it “correctly” would break muscle memory or third-party tools, so the bug quietly becomes spec.

- **Code reviews don’t prevent bugs—they just spread the blame.** A bad design gets six “LGTM” approvals because no one wants to be the jerk who blocks the PR or admits they don’t fully understand it.

- **“It works on my machine” is a moral failing, not a valid excuse.** If your team says this unironically in 2025, you’ve already lost.

- **The worst bugs are the ones no one reports because the users assume “that’s just how software is.”** Silent suffering is the default user experience; the bugs you know about are the easy ones.

- **Pair programming and TDD are overrated for bug prevention in most codebases.** They help juniors level up and make code look clean, but the majority of production bugs come from requirements misunderstandings, race conditions, and external changes—things that tests and pairing rarely catch.

- **Some bugs should stay unfixed.** The cost-benefit math on a bug that affects 0.001% of users once a year, requires a risky refactor, and has a solid workaround is obvious—but saying it out loud gets you accused of “not caring about quality.”

- **Blaming “legacy code” is a cop-out 90% of the time.** The real reason nothing gets fixed is that the people who understand the old system have left, and the new team is scared to touch it. “Legacy” just means “we fired everyone who knew how it worked.”

- **Senior engineers cause more unfixed bugs than juniors.** Juniors write sloppy code that’s easy to spot and fix. Seniors write “clever” abstractions that look beautiful but collapse under real-world load, and no one dares question them.

These opinions tend to be unpopular because they shift blame from “the code” or “management” to the actual humans and incentives in the room—and most people would rather keep the comfortable myths.

References:
- [The “Works on My Machine” Excuse](https://blog.codinghorror.com/the-works-on-my-machine-problem/)
- [On Being a Senior Engineer](https://www.kitchensoap.com/2012/10/25/on-being-a-senior-engineer/)
- [The Law of Leaky Abstractions](https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/)
