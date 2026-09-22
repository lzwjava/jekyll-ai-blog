---
audio: false
generated: true
image: false
lang: en
layout: post
title: NRZI Encoding in Networking
translated: false
type: note
---

Question: What is NRZI in networking?

Answer: **NRZI (Non-Return-to-Zero Inverted)** is a **line encoding** scheme: it maps bits to physical signal transitions on a wire.

The key idea is:

> **A transition represents one bit value; no transition represents the other.**

A common convention is:

* `1` → **transition**
* `0` → **no transition**

So if the current signal level is `LOW`:

```text
bits:    1  0  0  1  1  0
signal:  └─┐───┐└─┐───
           ↑       ↑ ↑
        transition
```

More precisely, starting at `LOW`:

```text
bit:      1   0   0   1   1   0
level:   LOW HIGH HIGH LOW HIGH HIGH
           └───┘     └──┘
            no       transition
```

### Why use NRZI?

The problem with transmitting raw `0/1` voltage levels is **clock recovery**.

Suppose you transmit:

```text
000000000000
```

The receiver sees a constant signal and has difficulty determining where individual bits are.

NRZI can make transitions encode information, which can make synchronization easier.

But there's an important catch:

```text
111111111111
```

under the convention above produces **continuous transitions**, while:

```text
000000000000
```

produces **no transitions**.

So long runs of the problematic bit still cause synchronization issues. Protocols therefore often combine NRZI with **bit stuffing** or another coding layer.

### NRZ vs NRZI

The easiest way to remember it:

```text
NRZ:
    bit value → signal level

NRZI:
    bit value → whether signal changes
```

For example, with `1 = transition`:

```text
bits:   1 0 1 1 0 0 1
        ↓ ↓ ↓ ↓ ↓ ↓ ↓

NRZI:   ↑ ─ ↑ ↑ ─ ─ ↑
```

The absolute voltage isn't what carries the bit directly; the **change/no-change relationship** does.

### Where you'll encounter it

NRZI appears in several networking/storage protocols and standards, notably **USB** (historically, USB 1.x/2.0 uses NRZI plus bit stuffing at the physical layer).

One subtle point: **NRZI's convention isn't universal**. Some descriptions use `1 = no transition` and `0 = transition`, so always check the protocol's definition rather than memorizing which bit means transition.

I can also walk through **USB's NRZI + bit-stuffing encoder/decoder with ~20 lines of Python**, which makes the mechanism very concrete.
