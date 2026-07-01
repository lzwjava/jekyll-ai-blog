---
audio: false
generated: true
image: false
lang: en
layout: post
title: CRC Explained Simply and Clearly
translated: false
type: note
---

Question: How does Cyclic Redundancy Check (CRC) work?

Answer:

## What is CRC?

A **Cyclic Redundancy Check (CRC)** is an error-detection technique used to determine whether data has been corrupted during transmission or storage. It works by treating data as a large binary number and performing a polynomial division — the remainder of that division becomes the **checksum** (also called the CRC value), which is appended to the data and verified at the receiving end.

---

## Core Concept

The fundamental idea is:

1. Both sender and receiver agree on a **generator polynomial** (the divisor).
2. The sender computes a CRC remainder from the data and appends it.
3. The receiver performs the same calculation. If the remainder is **zero**, the data is intact. If **non-zero**, an error occurred.

---

## Step-by-Step Process

### At the Sender Side

1. **Choose a generator polynomial** (e.g., `x³ + x + 1`, represented as binary `1011`).
2. **Append zeros** to the original data — the number of zeros equals the degree of the polynomial (i.e., if the polynomial is degree 3, append 3 zeros).
3. **Perform Modulo-2 division** (binary XOR-based division) of the padded data by the generator polynomial.
4. The **remainder** from this division is the CRC checksum.
5. **Replace the appended zeros** with the CRC remainder and transmit the full frame (original data + CRC).

### At the Receiver Side

1. Take the received data (including the CRC at the end).
2. Divide it by the **same generator polynomial** using Modulo-2 division.
3. If the **remainder is 0** → data is error-free ✅
4. If the **remainder is non-zero** → data is corrupted ❌ (request retransmission)

---

## Example (Simplified)

Suppose:

- Data bits: `1101011011`
- Generator polynomial (key): `10011` (represents CRC-4)

Steps:

1. Append 4 zeros: `11010110110000`
2. Perform XOR-based (Modulo-2) division by `10011`
3. Get remainder, e.g., `1110`
4. Transmit: `1101011011` + `1110` = `11010110111110`

Receiver divides `11010110111110` by `10011`. If remainder = `0000`, data is valid.

---

## Modulo-2 Division (XOR Division)

Unlike regular division, Modulo-2 division uses **XOR** instead of subtraction:

- `0 XOR 0 = 0`
- `1 XOR 1 = 0`
- `0 XOR 1 = 1`
- `1 XOR 0 = 1`

There are no borrows or carries — this makes it extremely fast and simple to implement in hardware.

---

## Common CRC Standards

| Standard | Bit Length | Common Use |
| ---------- | ----------- | ------------ |
| CRC-8 | 8 bits | Simple embedded systems |
| CRC-16 | 16 bits | USB, Modbus, storage |
| CRC-32 | 32 bits | Ethernet, ZIP, PNG, Wi-Fi |
| CRC-CCITT | 16 bits | Telecommunications |

Higher bit-length CRCs are more robust but require more computation. **CRC-32** can detect any single burst error up to 32 bits long and has a very low probability of missing longer errors.

---

## What CRC Can and Cannot Do

**CRC Can:**

- Detect single-bit errors
- Detect burst errors (contiguous corrupted bits) up to the polynomial's degree in length
- Detect most random error patterns

**CRC Cannot:**

- **Correct** errors — it only detects them
- Guarantee detection of all possible multi-bit errors (though very effective)
- Provide cryptographic security (it can be reverse-engineered)

---

## Where CRC is Used

- **Networking:** Ethernet frames, Wi-Fi packets, USB, Bluetooth, CAN bus
- **Storage:** Hard drives, SSDs, flash memory
- **File integrity:** ZIP, PNG, and other file formats
- **Communication protocols:** Modbus, A2B, Hamming codes

---

References:

- [Wikipedia – Cyclic Redundancy Check](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)
- [GeeksforGeeks – CRC and Modulo-2 Division](https://www.geeksforgeeks.org/dsa/modulo-2-binary-division/)
- [Lenovo – What is Cyclic Redundancy Check?](https://www.lenovo.com/us/en/glossary/cyclic-redundancy-check/)
- [Cardinal Peak – Understanding the CRC](https://www.cardinalpeak.com/blog/understanding-the-cyclic-redundancy-check)
- [Huawei – What Is Cyclic Redundancy Check?](https://info.support.huawei.com/info-finder/encyclopedia/en/CRC.html)
