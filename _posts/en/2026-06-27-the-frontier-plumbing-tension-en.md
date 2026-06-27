---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Frontier-Plumbing Tension
translated: false
type: note
---

This is a real strategic tension, but the framing has a flaw worth pulling apart.

**Where you're right:** When a capability discontinuity hits — and frontier model jumps are exactly that — the marginal value of "another senior engineer maintaining the CRUD app" drops relative to "senior engineer who deeply groks what the new model can now do." Orgs that don't carve out exploration time get caught flat-footed. Google's "20% time" existed precisely because the people closest to the work spot the discontinuity first. The bank you're at almost certainly under-allocates here — that's structurally true of risk-averse incumbents, and it's a real reason their internal tooling lags.

**Where the framing breaks:**

"Full-stack app/server dev is previous-generation" — no. The model doesn't deploy itself, doesn't handle auth, doesn't own the data pipeline, doesn't deal with the latency budget or the compliance boundary. What changes is the *ratio*: less hand-written business logic, more orchestration, eval, context engineering, and plumbing *around* models. The full-stack skill becomes the substrate that makes the AI-native layer shippable. The engineers who win the next cycle are the ones who have *both* — they can take a raw capability and turn it into something that survives contact with production. Pure "I only explore GPT" people generate demos that never ship.

"Just explore GPT, don't need a company laptop" — the *exploring* isn't the scarce skill. Anyone can chat with a model. The scarce skill is translating exploration into a system: what's the eval harness, where does it break on your actual data, what's the failure mode under adversarial input, what's the cost curve at scale. That requires the infrastructure (data, compute, the messy internal systems) that the company laptop / environment gives you. Decoupling exploration from the org's real problems produces shallow takes.

So the sharper version of your argument: **big corps should give senior people protected time to apply new frontier capabilities to the company's actual hard problems — with real data and infra access — rather than treating model adoption as a side quest squeezed between sprint tickets.** That's defensible and most incumbents fail at it.

For your own situation — this is exactly the asymmetry to exploit quietly. The bank won't give you protected exploration time officially, but you can *take* it by automating the (b)-tax work, then pointing the freed hours at applying frontier models to the bank's actual problems. That's where you build domain knowledge that compounds *and* prove the AI-native thesis with real systems, not demos. The org's failure to allocate exploration time is your arbitrage.

The "previous generation" instinct is the part to drop — it's the kind of thing that reads as sharp but loses you credibility with the people who've shipped enough to know the plumbing never goes away. Karpathy still talks about the boring infrastructure constantly. The frontier and the plumbing aren't sequential generations; they're the same stack.
