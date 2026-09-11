---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing "Card Not Recognized" in VRAM Testing
translated: false
type: note
---

I read the manual fully (《显存测试软件使用手册》— VRAM Testing Software Manual, 25 pages, covering the HDD/USB edition of MODS+MATS). Let me correct a few things about how it works first, then explain why you're hitting "card not recognized at startup".

## First, understand the relationship between MODS and MATS

Both are NVIDIA internal tools leaked into the repair community, and they work together:

| Tool | What it does | Analogy |
| --- | --- | --- |
| **MODS** | Loads a low-level driver, initializes the GPU, runs JS test scripts (`gputest.js`) — this is the "build the environment" step | A mini driver + test framework that bypasses the OS |
| **MATS** | Memory Access Test System — reads/writes VRAM bit by bit, generates `report.txt`, reporting errors by FBPA/channel | Depends on MODS having initialized the GPU first |

So the correct flow is two steps, **and the order cannot be reversed**:

```bash
cd /home/400.250                      # pick the version matching your card
./mods gputest.js -skip_rm_state_init -notest   # ① build environment — you MUST see PASS
./mats -n 1 -e 10                     # ② actually test VRAM (-n 1 = 2nd GPU, i.e., the dGPU)
less report.txt                       # ③ read results: numbers after FBI0A0 = bad VRAM chip
```

When the card can display on its own, `./mats -e 10` runs automatically. But **when you use the iGPU to test a dead dGPU, you must run step ① first**. Otherwise you get exactly what you described — "not recognized" / the "GPU register invalid" error (that's the error shown in step 17 of the manual).

## Common causes of "not recognized at startup" (by likelihood)

1. **Running mats before building the environment** — in the iGPU-hosts-dGPU setup, skipping `./mods gputest.js -skip_rm_state_init -notest` and going straight to `./mats -e 10` will always fail with "GPU register invalid".
2. **MODS version doesn't match the GPU** — the three versions map to different card generations (roughly: 367 → GTX9xx and below, 400 → 10xx/16xx/20xx, 455 → RTX 30 series). Wrong version = GPU can't be enumerated.
3. **Card is too new** — this 2021 image supports up to RTX 3090 only. RTX 40 series, Intel GPUs, and mining variants (P106 etc.) are **out of scope** — no amount of testing will make them recognizable.
4. **Wrong boot mode** — menu item 1 is Legacy-only; only items 2/3 support UEFI. Under UEFI you can only test NVIDIA cards. Picking the wrong mode means it won't boot or won't detect anything.
5. **The card's core/power rails are already dead** — if even `./mods gputest.js -skip_rm_state_init -notest` never shows PASS, the card's power delivery or core is faulty. **MODS cannot initialize such a card at all; there's no software fix.** Check external power (6/8-pin), PCIe edge contacts, and BIOS Primary Display settings first.
6. **Dual-GPU setup missing steps** — you must enable Multi-GPU in BIOS, and add `-n 1` to target the dGPU (otherwise it tests the iGPU by default, which of course "shows nothing").
7. **Not enough RAM** — the manual requires system RAM ≥ VRAM (an 8GB card needs 8GB+ RAM), otherwise tests won't run.

## Traps in the manual itself (don't copy its formatting literally)

- `./MATS`, `. /mats`, and `–e` (long dash) in the text are all typos. The real command is **lowercase `mats` + ASCII hyphen**: `./mats -e 10`, and every space matters.
- Version directory names: it's `cd /home/400.281.2` — the manual's "cd /home/ 400.281.2" has a misplaced space.
- AMD cards use a different flow: RX580 and below use `./model` to test + `./modelg` to view results; RX5700 and above use `./tserver -boardtest=memfa`, results in `memfa.log`.

## Suggested next steps

You said the test hasn't succeeded yet — to help me pinpoint the issue, tell me:

1. What environment are you running? (Which menu item of this disk image? Or something you set up yourself?)
2. Which card exactly? (Specific model, and is it an ex-mining card?)
3. Where exactly does it fail: **can't even get into the boot menu** / **error when running mods from the directory** / **mods never shows PASS** / **mats reports invalid register**?

Each failure point points to a completely different cause. If it errors out right after running a command from the menu, paste the exact on-screen error text — I can usually tell at a glance whether it's a wrong version choice or the card itself failing to initialize.
