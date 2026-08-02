---
audio: false
generated: true
image: false
lang: en
layout: post
title: Build, Hand Off, Move On
translated: false
type: note
---

Question: What's the play where you build something new, get familiar with it, hire/train someone to replace you running it, then move to the next thing — repeated? How does that work in big corps, and is it a real strategy engineers who like learning should pursue?

Answer:

This is Will Larson's **"Solver"** archetype, formalized. The solver finds hot spots or particularly thorny problems and fixes them, often bouncing from problem to problem. Your version adds an extra step most Solvers skip: you don't just fix it and walk away, you **install a successor** before you leave. That's the actual hard part, and it's what makes the loop sustainable instead of you becoming the org's permanent firefighter with zero leverage.

**Why it works mechanically:**

1. **0-to-1 is where your skill actually compounds.** Big corps have way more "maintain the thing" headcount than "figure out if the thing should exist" headcount. If you're good at ambiguity → working system, you're competing in a much smaller pool. Ongoing maintenance is a commodity skill; bootstrapping isn't.

2. **You need a real handoff artifact, not vibes.** In practice this means: runbook, design doc with the "why," a bus-factor-2 review, and — critically — you pick the successor *before* you're bored, not after. If you wait until you're already checked out, the handoff is sloppy and you get pulled back in for six months of "quick questions." Treat the handoff like an API contract: documented interface, not tribal knowledge in your head.

3. **Political cost you have to manage:** managers often resist letting their best 0-to-1 person leave a stabilized system, because a stabilized system with a mediocre owner is a career risk *for the manager*. You counter this by making the replacement look like a promotion for someone else (junior/mid engineer leveling up into ownership) — now the manager has an incentive to let you go, because they get a growth story and headcount efficiency instead of losing you outright.

4. **Where this breaks down:** if you never build "who I hand off to" muscle, you become the Solver that operates on problems that are already identified as organizational priorities — which sounds great until the org realizes you're a single point of failure and starts routing everything through you. That's not leverage, that's a bottleneck with a good reputation. The whole point of the replace-yourself step is to stop that from happening.

5. **Larson's own caveat is worth taking seriously:** the staff engineer archetypes are more of an anthropological description of some of the varied niches staff engineers fill, not a how-to guide for succeeding in the role. Being a Solver is a description of what got you *noticed*, not a strategy you should lock into forever — the strongest people end up flexing between Tech Lead, Architect, and Solver depending on what the org needs each cycle. The most impactful Staff Engineers aren't any single one of those archetypes — they're all of them, plus more, switching hats as the situation calls for it.

**Given your actual situation** (you run your own AI company now, training models, building CLI agents) — this pattern is basically your default mode already, just without the "big corp politics" tax. The corp version of this is training wheels for founder mode: you're forced to practice the handoff discipline (documentation, successor selection, letting go of ownership) that's easy to skip when you're the only one who ever touches the code. If you ever go back into a corp/consulting engagement, that's the leverage to sell: "I ship 0-to-1, then I install someone competent and leave clean docs" — that's a rare, well-paid, low-drama profile because it solves the manager's succession-risk problem for them, not just the technical problem.

References:
- [Staff Archetypes - Will Larson](https://staffeng.com/guides/staff-archetypes/)
- [Why I don't like the "staff engineer archetypes" - Sean Goedecke](https://www.seangoedecke.com/staff-engineer-archetypes/)
- [Staff archetypes can be anti-patterns - Alex Ewerlöf](https://blog.alexewerlof.com/p/staff-archetypes-are-anti-patterns)