---
audio: false
generated: true
image: false
lang: en
layout: post
title: RM Skip Flag for Broken Cards
translated: false
type: note
---

Good question — this flag is the key to understanding how MODS/MATS work on partially broken cards.

## What "RM" means

**RM = Resource Manager** — it's the core of the NVIDIA driver (the part that lives in the kernel driver and handles GPU initialization: it enumerates the GPU, sets up memory mappings, allocates channels/FIFOs, programs registers, etc.). MODS contains its own copy of the RM and normally loads it as part of startup.

## What the flag does

Normally, `mods` startup sequence is roughly:

```
1. Probe/enumerate the GPU on PCIe
2. Run RM state init  ← program the GPU into a working state
3. Load test scripts (gputest.js etc.) and run tests
```

`-skip_rm_state_init` tells it to **skip step 2** — it detects the GPU but does *not* try to bring it into a fully initialized "healthy driver" state.

## Why you need it when testing broken cards

When a card is faulty, full RM init often **fails partway** (e.g., its VRAM is corrupted, or some power rail is marginal) and MODS bails out with an error before you can do anything. By skipping RM init:

- MODS gets access to the GPU at a **raw hardware level** instead
- MATS can then read/write the framebuffer directly, even though the card would never survive normal driver initialization
- That's exactly what you want — you're diagnosing, not using the card

That's also why the manual's flow pairs it with **`-notest`**:

```bash
./mods gputest.js -skip_rm_state_init -notest
```

- `-notest` → "don't actually run any tests, just load MODS and keep it resident"
- `-skip_rm_state_init` → "don't try to fully initialize the card"

Together, these two flags make MODS act as a **minimal bootstrap environment** so MATS can run afterward.

## The practical takeaway

| Command combination | Meaning |
|---|---|
| `./mods gputest.js -skip_rm_state_init -notest` → sees **PASS** | Card can at least be touched at hardware level — enough for MATS to test VRAM |
| Same command → **fails / no PASS** | The card isn't even reachable: dead core, no power rails, or wrong MODS version — MATS is useless here |

So if that command with `-skip_rm_state_init` fails on your card, it's not a flag problem — it's telling you the card can't be initialized at all (or you're using the wrong MODS version for that GPU generation).
