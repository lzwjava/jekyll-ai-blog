---
audio: false
generated: true
image: false
lang: en
layout: post
title: CMP 90HX Unlock Economics
translated: false
type: note
---

I've explored the repo. Here's what it is and the economics question.

## What this project actually is

`cmp90hx-unlock` is a hacking/research effort to **undo NVIDIA's deliberate crippling of the CMP 90HX**. That card is:

- A **GA102 die — the exact same silicon as the RTX 3080** (sm_86, 50 SMs), not a special chip.
- Physically crippled by NVIDIA for "mining compliance": compute throughput throttled via **eFuse-set SM issue-rate registers**, plus the PCIe link **hardware-fused to Gen1 x16**, and graphics **(3D/PGRAPH) permanently power-gated**.
- Shipping as a near-useless coin-miner card that, when mining died, became e-waste.

This project develops an exploit chain that walks a GSP Falcon coprocessor vulnerability (originally from Jon Pry's "A Canary in the Crypto Mine") to open the **PLM** privilege lock and write the compute override registers (SS0/SS1), restoring full LLM prefill/decode throughput.

## So: will the price go up?

**Short answer: likely yes for an unlocked, working unit — but the ceiling is low and well below an RTX 3080.** Here's the reasoning.

### Upward pressure
- The card is in bins as borderline e-waste right now. Unlocking converts it from "coin miner, compute disabled" into an **actual Hall infra/larga-param compute card** (AI/LLM inference). Utility jumps, so the resale value jumps.
- Supply is **fixed** (a handful of these cards in the channel — NVIDIA didn't keep producing it). Fixed supply + a new demand segment (AI/LLM tinkerers wanting cheap compute) → per-unit price rises. This is the classic "handicapped-hardware unlock" effect (e.g., GTX 1080's coincidence LHR, or RX 5800 resurfaces).

### Why the upside is capped
- **PCIe is hardware-locked to Gen1 x16** (2.5 GT/s). The project's own roadmap/research spends a whole section on this — no software path moves it. That is a real bandwidth bottleneck for large models / model sharding.
- **10 GB VRAM** only — too small to hold many current LLMs.
- **Graphics/3D remain fully locked** — no display, no gaming. The card is compute-only forever.
- It's still crypto-mining-refugee hardware in a flush market niche; buyers who want RTX 3080 performance just buy a real, cheap 3080 **with** full PCIe, display, and VRAM.

### So what does the unlock really buy?
- It converts the CMP 90HX from de-priced to near-zero to a **budget AI-inference card with caveats** — Gen1 PCIe, 10 GB, no video. That's a "budget LLM box" capacity, not a real 3080 substitute.

## Bottom line
The unlock should **raise the floor** relative to the crippled "mining trash" price it currently trades at. But it does **not** create a supply-constrained, RTX-3080-grade card — Gen1 + 10 GB + no graphics cap the ceiling. If you're asking "should I sell / buy now?", midterm the unlocked units will fetch a premium, but don't expect a dramatic run-up — expect it to price somewhere between "crippled mining card" and "budget Gen1 compute card."

*(One caveat per the repo itself: the unlock is a security-hole exploit on one specific driver stack, requires Secure Boot off, and NVIDIA could patch/relock via driver or firmware update — the value premium depends on how long that stays viable, and it does not exist in every 90HX sample.)*
