---
audio: false
generated: true
image: false
lang: en
layout: post
title: "RS-232: Negative Voltage for Logic 1"
translated: false
type: note
---

Question: **Is RS-232 logic 1 electrically −15 V to −5 V?**

Answer: **Yes, roughly — but the formal RS-232C limits are a little more precise.**

For the RS-232 receiver:

| RS-232 signal voltage | Meaning                       |
| --------------------: | ----------------------------- |
|     **+3 V to +15 V** | Logic **0** (SPACE)           |
|     **−3 V to −15 V** | Logic **1** (MARK)            |
|      **−3 V to +3 V** | Undefined / transition region |

So:

```text
Voltage

 +15V ───────────── maximum
       │
       │  Logic 0
 +3V  ─────────────
       │
       │  UNDEFINED
  0V  ─────────────
       │
       │  UNDEFINED
 -3V  ─────────────
       │
       │  Logic 1
 -15V ───────────── minimum
```

The important thing is:

```text
RS-232:

1  → negative voltage
0  → positive voltage
```

This is **opposite to the intuition you may have from normal digital logic**, where:

```text
CMOS:
1 → +3.3 V
0 → 0 V
```

### One subtle point

Don't think of it as requiring exactly `-15 V` for a `1`.

For example, a transmitter might actually output:

```text
Logic 1 → -8 V
Logic 0 → +8 V
```

and that's perfectly valid.

The standard specifies the **voltage ranges**, not that every device must output ±15 V.

Also, the region:

```text
-3 V < V < +3 V
```

is intentionally a **dead/undefined zone** that gives the receiver noise margin.
