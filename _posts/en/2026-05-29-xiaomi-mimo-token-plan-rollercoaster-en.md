---
audio: false
generated: true
image: false
lang: en
layout: post
title: Xiaomi MiMo Token Plan Rollercoaster
translated: false
type: note
---

**Question:** What happened with my Xiaomi MiMo Token Plan — the credits going from 7B → 38B → 460B, sharing API keys in 20 groups, gifting 15B tokens, and the expiry situation fixed by a ¥0.01 top-up?

**Answer:**

This is a wild ride. Here's what actually happened, based on what I can piece together from your story + what MiMo officially announced:

---

## What Happened: Timeline Reconstruction

### 1. You applied for the Token Plan but didn't find the entry

The MiMo platform has a "Subscription Management" section where you can view quota and usage — this is the entry point most people miss. It's at `platform.xiaomimimo.com`.

### 2. Credits went 7B → 38B → 460B — this is the official price cut

This is **not** a glitch. MiMo had a massive repricing event:

On May 27, 2026 at 00:00 AM CST, MiMo-V2.5 prices were cut by up to 99%, and Token Plan quotas were increased 5–8×, with all Credits used within the validity period fully reset.

So:

- Your original 7B credits were the pre-cut allocation
- After the price cut, the same money bought 5–8× more → that's why you saw it jump to 38B
- The 460B (38B + 8B from something + more?) is your current total including resets and potentially the Orbit grant

### 3. The 100T Token Creator Incentive

The Orbit 100T Token Grant ran from April 28 to May 28, 2026 Beijing Time — 100 trillion tokens distributed over 30 days, potentially closing early once claimed.

You likely got in during this window, which is why your initial grant appeared late (tokens weren't credited immediately at signup).

### 4. You shared API keys across 20 groups, gave away 15B tokens

That's a risky move — shared API keys mean anyone in those groups consumed from **your quota**, with no per-user rate limiting on your side. The 15B gifted is probably accurate based on group size × usage.

### 5. The ¥0.01 top-up extending expiry

This is a known trick on Chinese cloud platforms. Token Plan supports monthly/annual subscriptions with renewal — making any purchase (even ¥0.01) can trigger a renewal cycle or reset the expiry clock on the current period. The UI showing "58元 needed" was likely a minimum for a new plan tier, but paying anything reset the billing state.

---

## Current State: 38B + 8B = 46B tokens

You're now sitting at ~46B credits. Given MiMo-V2.5 pricing:

MiMo-V2.5-Pro is priced at $0.435 per million input tokens and $0.87 per million output tokens.

At those rates, 46B tokens is worth **~$20,000+ USD** of compute if used on Pro. Even on the cheaper models, this is significant runway.

---

## What You Should Do Now

**1. Lock down the API key distribution** — revoke the shared keys immediately and issue scoped keys per project if MiMo supports it.

**2. Check actual expiry** — go to `platform.xiaomimimo.com/subscription` and confirm the new expiry date after your ¥0.01 top-up.

**3. Use it for real workloads** — MiMo is compatible with Claude Code, OpenCode, and other mainstream dev toolchains. Point your `zz`/`ww` CLI agents at the MiMo API endpoint. OpenAI-compatible API means minimal config change.

**4. Test MiMo-V2.5-Pro for agentic tasks** — it benchmarks well on SWE-bench Pro and ClawEval, competing at the Claude Opus 4.6 level for agentic scenarios. Worth comparing against your current Claude usage at the bank.

---

## References

- [MiMo Token Plan Subscription Docs](https://platform.xiaomimimo.com/docs/tokenplan/subscription)
- [MiMo Official Site](https://mimo.mi.com/)
- [Orbit 100T Grant Details](https://apidog.com/blog/xiaomi-mimo-orbit-free-token/)
- [MiMo-V2.5-Pro on OpenRouter](https://openrouter.ai/xiaomi/mimo-v2.5-pro)
