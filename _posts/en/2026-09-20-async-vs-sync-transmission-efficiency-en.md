---
audio: false
generated: true
image: false
lang: en
layout: post
title: Async vs Sync Transmission Efficiency
translated: false
type: note
---

Question: What’s the difference between **asynchronous transmission（异步传输）** and **synchronous transmission（同步传输）**, especially their transmission efficiency?

Answer:

The core difference is **how the receiver knows where each character/bit begins and ends**.

### 1. Asynchronous transmission

Each character is transmitted independently:

```text
       start   data        stop
         ↓      ↓           ↓
idle ── 0 ── 10110101 ── 1 ── idle
       ↑                    ↑
    start bit            stop bit
```

Usually:

```text
1 start bit + 8 data bits + 1 stop bit
```

So for 8 useful data bits:

$$
\eta = \frac{8}{1+8+1}=80\%
$$

If there are 2 stop bits:

$$
\eta = \frac{8}{1+8+2}=72.7\%
$$

The important point is that **every character carries synchronization overhead**.

Typical example: UART/serial communication.

---

### 2. Synchronous transmission

Instead of synchronizing every character, sender and receiver first establish/maintain synchronization, then transmit a **continuous block/frame**:

```text
sync/header       data data data data data data
   ↓                 ↓
[ synchronization ][        payload        ]
```

For example:

```text
| header | 10010110 10110101 01101001 ... |
```

The receiver uses the clock/synchronization mechanism to determine bit boundaries.

There is no need for:

```text
start + data + stop
start + data + stop
start + data + stop
...
```

for every character.

Therefore, for a large frame:

$$
\eta =
\frac{\text{payload bits}}
{\text{payload bits}+\text{sync/header overhead}}
$$

If you send 1000 bytes with only 10 bytes of overhead:

$$
\eta=\frac{1000}{1010}\approx99.0\%
$$

Much better than asynchronous transmission.

---

### 3. Why is synchronous more efficient?

Imagine transmitting 100 bytes.

#### Async

Suppose each byte has:

```text
1 start + 8 data + 1 stop
```

You actually transmit:

$$
100\times10=1000\text{ bits}
$$

Useful data:

$$
100\times8=800\text{ bits}
$$

Efficiency:

$$
\boxed{80\%}
$$

---

#### Sync

Suppose the whole 100-byte block has 2 bytes of synchronization/header overhead:

$$
100+2=102\text{ bytes}
$$

Efficiency:

$$
\frac{100}{102}\approx98.0\%
$$

So:

```text
Async:

S DDDDDDDD P | S DDDDDDDD P | S DDDDDDDD P
^^^^^^^^^^^^
overhead every byte


Sync:

SYNC | DDDDDDDD DDDDDDDD DDDDDDDD DDDDDDDD ...
^^^^
overhead once per frame
```

This is the key idea.

---

### 4. But async has an important advantage

Async is **simpler**.

You don't need to maintain continuous synchronization between sender and receiver.

For example, UART can simply say:

```text
idle
 ↓
START
 ↓
8 bits
 ↓
STOP
 ↓
idle
```

The receiver detects the start bit and samples the following bits according to the agreed baud rate.

So:

|                   | Asynchronous            | Synchronous                 |
| ----------------- | ----------------------- | --------------------------- |
| Synchronization   | Per character           | Per frame/continuous stream |
| Start/stop bits   | Usually yes             | Usually no per byte         |
| Efficiency        | Lower                   | Higher                      |
| Hardware/protocol | Simpler                 | More complex                |
| Good for          | Small/intermittent data | High-speed/bulk data        |
| Example           | UART                    | Ethernet, HDLC              |

### 5. One subtle point

**Synchronous does not automatically mean "higher bit rate."**

The distinction is primarily about **synchronization**, while efficiency comes from reducing synchronization overhead.

Think of it as:

```text
Async:
[SYNC][8 useful bits][SYNC][8 useful bits][SYNC][8 useful bits]

Sync:
[SYNC][many useful bits................................]
```

As the payload becomes larger, the fixed synchronization cost becomes negligible:

$$
\eta = \frac{L}{L+H}
$$

where \\(L\\) = payload length and \\(H\\) = synchronization overhead.

As \\(L\rightarrow\infty\\):

$$
\eta\rightarrow100\%
$$

That is why **synchronous transmission is generally more bandwidth-efficient for continuous/high-volume data**.
