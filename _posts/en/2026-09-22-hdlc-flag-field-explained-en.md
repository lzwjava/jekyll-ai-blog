---
audio: false
generated: true
image: false
lang: en
layout: post
title: HDLC Flag Field Explained
translated: false
type: note
---

Question: What is the **F frame** in HDLC networking?

Answer:

In **HDLC (High-Level Data Link Control)**, there isn't a standard frame type officially called an **“F frame.”** You may be referring to the **F (Flag) field** in an HDLC frame.

### HDLC frame structure

```text
+------+---------+------+-------------+-----+------+
| Flag | Address | Ctrl | Information | FCS | Flag |
+------+---------+------+-------------+-----+------+
  8b      8b       8b       variable    16/32b  8b
```

The **Flag field** is:

```text
01111110
```

or:

```text
0x7E
```

It appears at **both the beginning and end** of an HDLC frame.

### Why do we need the Flag?

The receiver uses `01111110` to identify **frame boundaries**:

```text
01111110 | Address | Control | Data | FCS | 01111110
   ↑                                          ↑
 start                                      end
```

So if the physical link is just a continuous stream of bits:

```text
...101100101101011111101011001011...
                  ↑
              frame boundary
```

the flag tells the receiver where a frame starts/ends.

### The interesting part: bit stuffing

Because the flag contains:

```text
01111110
```

HDLC must prevent the same pattern from accidentally appearing inside the data.

After **five consecutive `1`s**, the sender inserts a `0`:

```text
Data before stuffing:
01111110

Stuffing:
011111010
       ↑
   inserted 0
```

More precisely, for any data sequence:

```text
11111
```

the transmitter sends:

```text
111110
```

The receiver removes that stuffed `0`.

This means the flag sequence can remain unique:

```text
Flag:       01111110
Data:       011111010
                        ↑
              not interpreted as flag
```

### Minimal mental model

Think of HDLC as a **bit-oriented protocol**:

```text
          frame
    ┌───────────────────────┐
    ↓                       ↓
01111110  DATA + CONTROL  01111110
   flag                    flag
```

* **Flag** → frame delimiter
* **Address** → destination/station
* **Control** → frame type + sequencing/control
* **Information** → payload
* **FCS** → error detection
* **Bit stuffing** → prevents data from looking like a flag

One important distinction: **F in “F frame” is probably being used by your course/material to mean Flag**, rather than being one of the three standard HDLC frame types (**I, S, U**).

References:

* [HDLC — ITU-T Recommendation X.25](https://www.itu.int/rec/T-REC-X.25?utm_source=chatgpt.com)
* [HDLC — Wikipedia](https://en.wikipedia.org/wiki/High-Level_Data_Link_Control?utm_source=chatgpt.com)
