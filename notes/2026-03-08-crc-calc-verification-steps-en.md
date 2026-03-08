---
audio: false
generated: true
image: false
lang: en
layout: post
title: CRC Calculation and Verification Steps
translated: false
type: note
---

**Question:** After appending 4 zeros to the information bit string (using generator polynomial `11001`), how do you perform the CRC calculation and verify it at the receiver?

**Answer:**

---

## Complete CRC Workflow: Calculation & Verification

Let's use a concrete example throughout:

- **Message (D):** `10110110`
- **Generator (G):** `11001` (degree r = 4)

---

## STEP 1 — Append r Zeros to the Message

Since G has degree 4, append **4 zeros** to D:

```
Original message:    10110110
After appending:     101101100000   ← this is D × 2^r
```

---

## STEP 2 — Perform Modulo-2 Division (XOR Long Division)

The process of modulo-2 binary division works just like familiar long division, except that instead of subtraction, XOR is used at each step.

**Rules:**
- If the current leading bit is `1` → XOR with the generator `11001`
- If the current leading bit is `0` → XOR with `00000` (i.e., just shift/bring down)
- The result of each XOR becomes the next working value; bring down the next bit

```
Dividend: 101101100000
Divisor:  11001

Step-by-step XOR long division:

  101101100000
  11001
  ---------
   10111           ← XOR result (drop leading 0)
   
  101110           ← bring down next bit
  11001
  ---------
   10111           ← XOR result

  101110           ← bring down next bit
  11001
  ---------
   10111

  101110           ← bring down next bit
  11001
  ---------
   10111

  101110           ← bring down next bit
  11001
  ---------
   10111

  ...continue until no bits remain...

Final Remainder (R) = 1110   ← 4 bits (= degree of G)
```

> **Note:** The remainder always has exactly **r bits** (4 bits here). If the raw remainder has fewer than r bits, pad leading zeros.

---

## STEP 3 — Form the Transmitted Frame

The CRC bits (remainder R) are appended to the end of the original data to form the transmitted frame, making the complete frame exactly divisible by the generator G.

```
Transmitted Frame T = Original Message + CRC bits
T = 10110110 + 1110
T = 101101101110
```

---

## STEP 4 — Receiver Verification

The validity of a received message can be verified by performing the same division again, this time with the CRC check value appended (instead of zeros). If there are no detectable errors, the remainder will equal zero.

**At the receiver**, divide the entire received frame `T` by G:

```
Received frame:  101101101110
Divisor:         11001

Perform modulo-2 division...

Final Remainder = 0000  ✅  ← No error detected
```

**If a bit error occurred**, e.g., frame becomes `111101101110`:

```
Received frame:  111101101110
Divisor:         11001

Final Remainder = some nonzero value ❌ ← Error detected!
```

If the remainder is zero, the data unit is assumed to be intact and accepted. A non-zero remainder indicates an error has occurred.

---

## Summary Table

| Step | Action | Example |
|------|--------|---------|
| 1 | Append r zeros to message | `10110110` → `101101100000` |
| 2 | Divide by G using XOR (mod-2) | `101101100000 ÷ 11001` |
| 3 | Remainder R = CRC bits | R = `1110` |
| 4 | Transmit: Message + R | `101101101110` |
| 5 (Receiver) | Divide received frame by G | Remainder = `0000` → No error |

---

## Key Properties

- The transmitted frame T(x) has the key property that it is exactly divisible by G(x) — meaning G(x) is a factor of T(x).
- The r-bit remainder (k−1 bits where k = length of generator) is appended at the sender side. At the receiver, if the remainder of division is 0, the data has no errors.
- CRC detects **all burst errors** of length ≤ r bits (the degree of the generator polynomial).

**References:**

- [GeeksforGeeks – Modulo-2 Binary Division](https://www.geeksforgeeks.org/dsa/modulo-2-binary-division/)
- [Wikipedia – Cyclic Redundancy Check](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)
- [CS Williams – CRC Lecture Notes](https://www.cs.williams.edu/~tom/courses/336/outlines/lect7_2.html)
- [UMass Interactive CRC Problems](https://gaia.cs.umass.edu/kurose_ross/interactive/CRC.php)