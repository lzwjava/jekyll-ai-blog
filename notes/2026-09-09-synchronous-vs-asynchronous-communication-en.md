---
audio: false
generated: true
image: false
lang: en
layout: post
title: Synchronous vs Asynchronous Communication
translated: false
type: note
---

Question: Can you explain in more detail the two synchronization models — Synchronous and Asynchronous — in communication systems?

Answer:

---

## 1. Synchronous Communication---

## 1. Synchronous Communication

A **dedicated clock line (CLK)** is transmitted alongside the data. Both sender and receiver sample the data line on the **same clock edge** (usually the rising edge ↑), so they are always in perfect agreement about "when is now."

**How it works:**

- The clock ticks at a fixed frequency (e.g. 1 MHz).
- On each rising edge, the receiver reads the current state of the data line (HIGH = 1, LOW = 0).
- No extra framing bits are needed — the clock itself defines every bit boundary.

**Trade-offs:**

| Advantage | Disadvantage |
| --- | --- |
| Very high speed possible | Requires an extra wire (the CLK line) |
| No drift — always in sync | Clock skew can cause errors over long distances |
| Simple receiver logic | Both sides must share the same clock domain |

**Real-world examples:** SPI, I²C, SD card bus, DDR memory

---

## 2. Asynchronous Communication

There is **no shared clock wire**. Instead, both sides pre-agree on a **baud rate** (bits per second), and the data stream includes special **framing bits** to mark the boundaries of each byte.

**How it works:**

- The line sits **IDLE HIGH** when no data is sent.
- A **START bit** (always LOW) signals the beginning of a new byte — the receiver's internal clock starts counting.
- The next **8 data bits** follow, one per agreed-upon time slot (1 / baud rate).
- A **STOP bit** (always HIGH) ends the frame and resets the line to idle.

**Trade-offs:**

| Advantage | Disadvantage |
| --- | --- |
| No clock wire needed | Slightly slower (10 bits to send 8 data bits) |
| Works over long cables | Receiver clock can drift if baud rate is mismatched |
| Simple hardware (UART) | Fixed frame size limits flexibility |

**Real-world examples:** UART, RS-232, older serial ports

---

## High-Speed Variant: CDR (Clock and Data Recovery)

For very high-speed links (USB 3, PCIe, SATA, Ethernet), a dedicated clock wire would pick up too much noise and interference. Instead, the clock is **encoded inside the data stream** using line coding techniques like **8b/10b** or **NRZ with scrambling**, which guarantee enough transitions in the signal. The receiver's CDR circuit **locks onto these transitions** using a Phase-Locked Loop (PLL) to regenerate the clock locally — no wire required.

---

References:

- [UART Asynchronous Communication – SparkFun](https://learn.sparkfun.com/tutorials/serial-communication/all)
- [SPI (Synchronous) Protocol – Analog Devices](https://www.analog.com/en/resources/analog-dialogue/articles/introduction-to-spi-interface.html)
- [Clock and Data Recovery – Texas Instruments](https://www.ti.com/lit/an/slyt075/slyt075.pdf)
