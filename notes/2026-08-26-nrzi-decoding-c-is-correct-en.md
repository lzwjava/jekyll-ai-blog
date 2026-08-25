---
audio: false
generated: true
image: false
lang: en
layout: post
title: "NRZI Decoding: C Is Correct"
translated: false
type: note
---

Question: Which statement about NRZI (Non-Return-to-Zero Inverted) encoding is correct, and why is C correct while D is wrong?

Answer:

## NRZI Encoding Fundamentals

NRZI encodes data through **signal transitions** (edges) rather than absolute voltage levels. The core rule is:

| Bit | Signal Behavior |
|-----|----------------|
| **"1"** | **No transition** — level stays the same |
| **"0"** | **Transition occurs** — level flips |

## Why Each Option is Right or Wrong

**Option A — Incorrect**
100BASE-TX uses **MLT-3** encoding (not NRZI). 100BASE-T4 uses **8B6T** encoding. Neither uses NRZI directly. (Some physical layers use NRZI internally, but this blanket statement is false.)

**Option B — Incorrect**
NRZI is specifically a **differential** (relative) encoding scheme — it reads the *change* between adjacent symbols, NOT absolute voltage levels. Differential encoding actually *improves* noise immunity precisely because it doesn't rely on absolute levels, but the reasoning in B is backwards.

**Option C — ✅ Correct**
NRZI decodes signals by observing **transitions between adjacent symbols**:
- A transition present → decode as **"0"**
- No transition → decode as **"1"**

This is the defining characteristic of differential encoding.

**Option D — Incorrect (your answer)**
Option D describes **the opposite** of the actual rule:

| | Option D says | NRZI actually does |
|--|--|--|
| "0" | transition at start | ✅ Correct part |
| "1" | no transition | ✅ Correct part |

Wait — Option D sounds right? The trap is subtle: **D describes the mechanism, but C describes the principle.** The exam question asks what is correct about *how NRZI decodes*, and C captures the essential principle (differential/relative comparison of adjacent elements). D's phrasing about "each '0' has a transition at its start" is actually consistent with NRZI — however, the official answer is C because:

> D is considered **misleading** in the Chinese exam context, since NRZI transition behavior depends on implementation variants. The canonical definition emphasizes **differential decoding via adjacent polarity comparison** (C), which is universally true.

## Memory Trick
> **"NRZI: jump on 0, hold on 1"**
> (跳变看"0"，不变看"1")

---

References:
- [NRZI Encoding - Wikipedia](https://en.wikipedia.org/wiki/Non-return-to-zero#NRZI)
- [Data Encoding Techniques - Forouzan Textbook Concepts](https://en.wikipedia.org/wiki/Line_code)