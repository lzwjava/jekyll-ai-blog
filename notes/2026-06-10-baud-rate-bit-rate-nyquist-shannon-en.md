---
audio: false
generated: true
image: false
lang: en
layout: post
title: Baud Rate, Bit Rate, Nyquist, Shannon
translated: false
type: note
---

Question: What is the difference between baud rate and bit rate, and how do the Nyquist and Shannon formulas relate to them?

Answer:

**1. Definitions**

* **Bit Rate (bps, bits per second):**
  The number of **bits transmitted per second** over a communication channel. For example, if a channel sends 1000 bits in 1 second, the bit rate is 1000 bps.

* **Baud Rate (Bd, symbols per second):**
  The number of **signal changes (symbols) per second** on the channel. A symbol may encode one or more bits depending on the modulation scheme.

  **Key relation:**
  [
  \text{Bit rate} = \text{Baud rate} \times \text{Bits per symbol}
  ]

  Example:

  * Binary signal (2 levels): 1 bit/symbol → bit rate = baud rate
  * QPSK (4 levels): 2 bits/symbol → bit rate = 2 × baud rate

---

**2. Nyquist Formula (Ideal Maximum Bit Rate without Noise)**

Nyquist considered a **noiseless channel** of bandwidth (B) Hz. If the channel uses (M) discrete signal levels, the maximum bit rate is:

[
\text{Bit rate}_{\text{max}} = 2B \log_2 M
]

* (B) = channel bandwidth in Hz
* (M) = number of signal levels (e.g., 2 for binary, 4 for QPSK)
* Assumes ideal, noiseless transmission

**Interpretation:**

* Doubling (M) allows one to transmit more bits per symbol, increasing the bit rate without increasing bandwidth.

---

**3. Shannon Formula (Maximum Bit Rate with Noise)**

Shannon accounted for **channel noise**, giving the theoretical maximum **channel capacity** (C) in bits per second:

[
C = B \log_2 (1 + \text{SNR})
]

* (B) = bandwidth in Hz
* SNR = signal-to-noise ratio (linear, not dB)

**Interpretation:**

* Even with infinite signal levels, noise limits how much information can be reliably transmitted.
* Shows that increasing bandwidth or improving SNR increases channel capacity.

---

**4. Summary Table**

| Concept   | Formula                                | Notes                                             |
| --------- | -------------------------------------- | ------------------------------------------------- |
| Bit rate  | (R = \text{Baud rate} \times \log_2 M) | Depends on symbols per second and bits per symbol |
| Baud rate | Symbols per second                     | Signal changes per second                         |
| Nyquist   | (R_{\max} = 2B \log_2 M)               | Ideal noiseless case                              |
| Shannon   | (C = B \log_2(1 + \text{SNR}))         | Noisy channel capacity                            |

---

**5. Example**

* Channel bandwidth (B = 3000) Hz

* Binary signaling ((M=2))

* Nyquist:
  [
  R_{\max} = 2 \times 3000 \times \log_2 2 = 6000 \text{ bps}
  ]

* If SNR = 30 (linear), Shannon:
  [
  C = 3000 \log_2 (1 + 30) \approx 3000 \times 4.954 \approx 14,862 \text{ bps}
  ]

This shows that with noise, Shannon gives the **true maximum bit rate**, whereas Nyquist shows the **ideal maximum** assuming noiseless conditions.

---

References:

* [Baud rate vs Bit rate - Wikipedia](https://en.wikipedia.org/wiki/Baud)
* [Nyquist formula - Wikipedia](https://en.wikipedia.org/wiki/Nyquist_rate)
* [Shannon–Hartley theorem - Wikipedia](https://en.wikipedia.org/wiki/Shannon%E2%80%93Hartley_theorem)
