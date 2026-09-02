---
audio: false
generated: true
image: false
lang: en
layout: post
title: "DC vs AC: Current, Not Charge"
translated: false
type: note
---

Question: Does DC mean “direct charge” and AC mean “alternating charge”?

Answer: Almost — the correct terms are:

* **DC = Direct Current**
* **AC = Alternating Current**

Not “direct charge.”

### DC

Current flows primarily in **one direction**:

```text
DC:

+ ───────────────→ ─────────────── -
       current
```

A battery is a typical DC source:

```text
Battery
+  ───────────→  -
```

A PC motherboard mostly operates internally with **DC voltages** such as 12 V, 5 V, 3.3 V, 1.8 V, ~1.5 V, ~1 V, etc.

### AC

The current periodically **changes direction**:

```text
AC:

→ → → →
← ← ← ←
→ → → →
← ← ← ←
```

The electricity coming from a normal wall outlet is AC. In many countries it's around **50 or 60 Hz**, meaning the voltage alternates periodically.

You can visualize the voltage like:

```text
Voltage
  +
  │      /‾\      /‾\
  │     /   \    /   \
0 ├────/─────\──/─────\──── time
  │   /       \/       \
  │  /        /\        \
  -
```

So when using your multimeter:

**`V⎓` / DC voltage** → motherboard, battery, USB, PSU output, etc.

**`V~` / AC voltage** → wall outlet / mains AC.

One subtle point: **AC/DC describes current/voltage behavior, not “charge.”** Charge is a different physical concept.
