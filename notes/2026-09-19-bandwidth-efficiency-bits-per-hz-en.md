---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Bandwidth Efficiency: Bits per Hz"
translated: false
type: note
---

Question: What is **频带利用率 (bandwidth efficiency)**?

Answer:

**频带利用率 = how efficiently a communication system uses its available bandwidth to transmit information.**

The most common formula is:

$$
\boxed{\eta = \frac{R_b}{B}}
$$

where:

* \\(R_b\\) = bit rate, in **bit/s**
* \\(B\\) = occupied bandwidth, in **Hz**
* \\(\eta\\) = bandwidth efficiency, in **bit/(s·Hz)**

### Example

Suppose a communication system:

$$
R_b = 10\text{ Mbps}
$$

and occupies:

$$
B = 2\text{ MHz}
$$

Then:

$$
\eta = \frac{10\times10^6}{2\times10^6}
=5\text{ bit/(s·Hz)}
$$

So the system transmits **5 bits per second for every 1 Hz of bandwidth**.

### Intuition

Think of bandwidth as the width of a pipe:

```text
Bandwidth B
<------------------------>

Information
██████████████████████████  Rb
```

Higher \\(\eta\\) means **more bits squeezed into each Hz**.

This is why modulation schemes such as **QPSK, 16-QAM, 64-QAM, 256-QAM** matter: higher-order modulation can transmit more bits per symbol, potentially increasing spectral efficiency.

For an ideal \\(M\\)-ary modulation:

$$
\boxed{\eta \approx \log_2 M\quad \text{bit/(s·Hz)}}
$$

before accounting for things like pulse-shaping roll-off, coding overhead, guard bands, etc.

For example:

$$
\text{QPSK}: \log_2 4=2
$$

$$
16\text{-QAM}: \log_2 16=4
$$

$$
64\text{-QAM}: \log_2 64=6
$$

So **频带利用率 is essentially "bits per second per Hz."**
