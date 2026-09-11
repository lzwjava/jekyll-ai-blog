---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skip RM State Initialization
translated: false
type: note
---

Question: What does `-skip_rm_state_init` mean in NVIDIA MODS?

Answer:

`-skip_rm_state_init` tells **MODS not to initialize/reset the NVIDIA Resource Manager (RM) state** during startup.

Conceptually:

```text
Normal:
MODS
  ↓
initialize RM
  ↓
initialize GPU state
  ↓
run test

-skip_rm_state_init:
MODS
  ↓
skip RM state initialization
  ↓
use the GPU's existing/boot-time state
  ↓
run test
```

### Why is it used here?

Your command is:

```bash
./mods gputest.js -skip_rm_state_init -notest
```

The important part is that this is **not yet the VRAM test**.

`gputest.js` is being used to get the GPU into a state where MATS can subsequently access it. `-notest` means essentially:

> initialize/enumerate the GPU, but don't actually execute the test.

And:

```text
-skip_rm_state_init
```

means:

> **Don't let MODS perform its normal RM state initialization.**

This is useful in the particular **iGPU-as-display + dGPU-under-test** setup because you don't want MODS' normal initialization sequence to interfere with the dGPU's existing PCIe/GPU state before MATS accesses it.

So the sequence is roughly:

```bash
./mods gputest.js -skip_rm_state_init -notest
#      ↑                 ↑
#      initialize        don't reset/init RM state
#      GPU environment

./mats -n 1 -e 10
#       ↑
#       target the second GPU
```

### `-skip_rm_state_init` vs `-notest`

They're doing **different things**:

| Flag                  | Meaning                      |
| --------------------- | ---------------------------- |
| `-skip_rm_state_init` | Skip RM state initialization |
| `-notest`             | Don't actually run the test  |

So:

```bash
./mods gputest.js -skip_rm_state_init -notest
```

roughly means:

> **Prepare/enumerate the GPU using `gputest.js`, but don't run the test and don't perform the normal RM state initialization.**

One important nuance: I would **not interpret `skip_rm_state_init` as "don't initialize the GPU at all."** MODS still has to enumerate/access enough of the GPU for the subsequent MATS workflow. It specifically skips the **RM state initialization phase**, not all GPU initialization.

If you want to understand why this avoids the `GPU register invalid` failure, the interesting part is the **MODS → RM → GPU BAR/register → MATS** initialization chain.
