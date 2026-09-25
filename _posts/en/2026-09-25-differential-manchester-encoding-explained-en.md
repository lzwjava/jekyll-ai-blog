---
audio: false
generated: true
image: false
lang: en
layout: post
title: Differential Manchester Encoding Explained
translated: false
type: note
---

Question: What is differential Manchester encoding (差分曼彻斯特编码)?

Answer:

**Differential Manchester encoding** is a digital line encoding scheme where the **presence or absence of a transition at the beginning of each bit period** represents the bit value.

The key idea:

* There is **always a transition in the middle of every bit period** → provides clock synchronization.
* The **transition at the beginning** of the bit period carries the data.
* Depending on the convention:

  * **0** = transition at the beginning
  * **1** = no transition at the beginning

So unlike ordinary Manchester encoding, the **absolute voltage level doesn't matter**—only whether the signal changes.

### Example

Using the convention `0 = transition at bit boundary`:

```text
bits:       1     0     0     1
           |-----|-----|-----|-----|
signal:     ────┐ │┌───┐ │┌───┐ └──
                └─┘   └─┘   └─┘
                 ↑     ↑     ↑
              middle transitions
```

A cleaner way to think about one bit:

```text
             beginning       middle
                 ↓              ↓
bit = 0        ───┐             ┌───
                  └─────────────┘

bit = 1        ─────────────────┐
                                └────
```

The exact high/low orientation can be inverted without changing the decoded data, because the receiver cares about **transitions**, not voltage polarity.

### Why use it?

The major advantage is **clock recovery**.

For NRZ:

```text
111111111111
────────────
```

there may be no transitions for a long time, making clock synchronization difficult.

Differential Manchester guarantees:

```text
every bit:    |----transition----|
```

so the receiver can recover the bit clock from the signal itself.

It is also **polarity-insensitive**: swapping HIGH ↔ LOW everywhere doesn't change the decoded bits.

This is why it was used in systems such as **IEEE 802.5 Token Ring**.

### Manchester vs Differential Manchester

|                   | Manchester                     | Differential Manchester                  |
| ----------------- | ------------------------------ | ---------------------------------------- |
| Data encoded by   | Direction of middle transition | Transition/no-transition at bit boundary |
| Middle transition | Always                         | Always                                   |
| Polarity reversal | Changes interpretation         | Doesn't matter                           |
| Clock recovery    | Yes                            | Yes                                      |

The mental model I'd keep is:

> **Manchester:** “Which direction does the middle transition go?”
> **Differential Manchester:** “Did we transition at the boundary?”

That distinction is the whole thing.