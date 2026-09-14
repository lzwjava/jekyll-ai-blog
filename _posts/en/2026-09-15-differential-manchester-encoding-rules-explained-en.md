---
audio: false
generated: true
image: false
lang: en
layout: post
title: Differential Manchester Encoding Rules Explained
translated: false
type: note
---

**Question:** What are the encoding rules of Differential Manchester Encoding (差分曼彻斯特码)?

**Answer:**

Differential Manchester Encoding is a self-clocking line code where each bit period is divided in half. The key rules are:

**Clock pulse (mid-bit transition):** Every bit period has a mandatory transition in the **middle** — this is what provides clock synchronization and is present regardless of the bit value.

**Bit encoding (start-of-bit transition):**
- **Bit 0:** There **is** a transition at the *start* of the bit period.
- **Bit 1:** There is **no** transition at the *start* of the bit period.

The actual signal level doesn't matter — only whether a transition occurs. The mid-bit transition always happens.To summarize the rules concisely:

| Situation | Transition at bit start? | Transition at bit mid? |
|---|---|---|
| Bit = **0** | ✅ Yes (always) | ✅ Yes (always) |
| Bit = **1** | ❌ No | ✅ Yes (always) |

**Key advantages** of this scheme: the mandatory mid-bit transition enables clock recovery without a separate clock line, and because encoding is based on *transitions* rather than absolute signal levels, it is immune to polarity reversal.

---

**References:**
- [Differential Manchester encoding — Wikipedia](https://en.wikipedia.org/wiki/Differential_Manchester_encoding)
- [Data encoding techniques — Forouzan, Data Communications and Networking](https://www.mheducation.com/highered/product/data-communications-networking-forouzan/M9780073376226.html)
