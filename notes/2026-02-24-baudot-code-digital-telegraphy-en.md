---
audio: false
generated: true
image: false
lang: en
layout: post
title: Baudot Code and Digital Telegraphy
translated: false
type: note
---

Question: Who was Émile Baudot, and what was his contribution to telecommunications?

Answer: **Jean-Maurice-Émile Baudot** (1845–1903) was a French telegraph engineer and inventor who revolutionized digital communication. He is best known for inventing the **Baudot code**, the first truly digital character code, and for developing a multiplexed telegraph system that allowed multiple messages to be sent over a single wire simultaneously.

---

### 1. The Baudot Code (Digital Foundation)

Before Baudot, telegraphy relied largely on Morse code, which used variable-length signals (dots and dashes). Baudot’s breakthrough was the creation of a **5-bit binary code**.

* **Fixed Length:** Every character was exactly five bits long.
* **Binary Nature:** Each bit was either "on" or "off" (current or no current).
* **Capacity:** $2^5 = 32$ possible combinations. To handle the full alphabet plus numbers and symbols, he introduced "Letter" and "Figure" shift keys—a concept still used in modern keyboards.

### 2. The Multiplex System

Baudot’s system was designed for efficiency. Using a synchronized **distributor** (a rotating mechanical switch), he enabled up to six operators to share a single telegraph line.

* **Synchronous Timing:** The sending and receiving machines had to spin at the exact same speed.
* **Time-Division Multiplexing (TDM):** This was a primitive version of TDM, a cornerstone of modern fiber-optic and cellular communications.

### 3. The Baudot Keyboard

Unlike the Morse key, Baudot’s interface looked like a piano with five keys.

* Operators pressed combinations of keys with their left and right hands.
* The operator had to maintain a steady rhythm to stay in sync with the rotating distributor, often cued by a "click" sound from the machine.

### 4. Legacy and the "Baud" Unit

Baudot’s influence is so fundamental that his name was immortalized in the SI unit for communication speed:

* **The Baud (Bd):** This unit measures the number of symbol changes (events) per second in a communication channel. While often confused with "bits per second," the Baud specifically honors his work in pulse-based signaling.

---

### Summary Table: Morse vs. Baudot

| Feature | Morse Code | Baudot Code |
| --- | --- | --- |
| **Length** | Variable (dots/dashes) | Fixed (5-bit) |
| **Timing** | Asynchronous | Synchronous |
| **Automation** | Difficult to automate | Ideal for machine printing |
| **Usage** | Human-to-human | Machine-to-machine (Telex) |

Would you like me to explain how the "shift" characters allowed Baudot to squeeze more than 32 characters out of a 5-bit system?