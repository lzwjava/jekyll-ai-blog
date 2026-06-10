---
audio: false
generated: true
image: false
lang: en
layout: post
title: Symbols and Baud Rate
translated: false
type: note
---

Question: What are "signal changes (symbols)" in baud rate?

Answer:

A **symbol** is a distinct signal state sent over a communication channel during a fixed time interval.

Think of it this way:

* **Bit** = information (0 or 1)
* **Symbol** = physical signal transmitted on the wire, fiber, or radio wave

A symbol may represent **one bit or multiple bits**.

### Simple Example: Binary Signaling

Suppose the transmitter uses:

* Low voltage = 0
* High voltage = 1

```
Voltage

High ────┐      ┌──────
         │      │
Low  ────┴──────┴──────→ Time
         0      1
```

Each symbol carries 1 bit.

| Symbol | Bit |
| ------ | --- |
| Low    | 0   |
| High   | 1   |

Thus:

* 1000 symbols/sec = 1000 baud
* 1000 bits/sec = 1000 bps

---

### Multi-Level Signaling

Instead of only two voltage levels, suppose we use four:

| Voltage Level | Bits |
| ------------- | ---- |
| -3V           | 00   |
| -1V           | 01   |
| +1V           | 10   |
| +3V           | 11   |

Now one symbol carries **2 bits**.

Example:

```
00  11  01  10
↓   ↓   ↓   ↓

-3V +3V -1V +1V
```

If we send:

* 1000 symbols/sec (1000 baud)

then:

[
1000 \times 2 = 2000 \text{ bps}
]

So:

* Baud rate = 1000
* Bit rate = 2000

---

### Why "Signal Changes"?

Historically, engineers observed the signal physically changing on the line:

```
Voltage

+3V ──────┐
          │
+1V ──┐   └──────
      │
-1V ──┘
      └─────────→ Time
```

Each symbol interval corresponds to a chosen signal state.

A **baud** is essentially:

> "How many symbol intervals per second are transmitted?"

Not every symbol must actually change level from the previous one, but historically baud rate referred to the rate at which symbols are sent.

---

### Real Modems Example

Early telephone modems:

* 2400 baud
* 9600 bps

How?

Each symbol encoded:

[
9600/2400 = 4 \text{ bits per symbol}
]

using modulation schemes such as QAM.

Thus:

* Symbol rate = 2400 baud
* Information rate = 9600 bits/sec

---

### Connection to Nyquist

Nyquist says:

[
\text{Maximum Baud Rate} = 2B
]

where (B) is channel bandwidth.

For a 3000 Hz telephone line:

[
2 \times 3000 = 6000 \text{ baud}
]

If each symbol carries:

* 1 bit → 6000 bps
* 2 bits → 12000 bps
* 4 bits → 24000 bps

This is why communication systems try to pack multiple bits into each symbol.

### Intuition

Imagine shipping information with trucks:

* **Baud rate** = trucks per second
* **Bits per symbol** = boxes carried by each truck
* **Bit rate** = boxes delivered per second

Formula:

[
\text{Bit Rate} = \text{Baud Rate} \times \text{Bits per Symbol}
]

So a **symbol** is the actual physical signal state transmitted during one signaling interval, while **bits** are the information encoded into that symbol.
