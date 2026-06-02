---
audio: false
generated: true
image: false
lang: en
layout: post
title: XOR Operation Explained Simply
translated: false
type: note
---

Question: What is a comprehensive introduction to the XOR operation?

Answer:

## XOR Operation — Comprehensive Introduction

---

### 1. What is XOR?

XOR (Exclusive OR) is a logical operator whose output is **true if and only if the inputs differ** — one is true and one is false. With multiple inputs, XOR is true if and only if the number of true inputs is **odd**.

Represented by the symbol `^` in most programming languages and `⊕` in mathematical notation, XOR is widely used in cryptography, data structures, and algorithms.

---

### 2. Truth Table

The most fundamental way to understand XOR is through its truth table:

| A | B | A XOR B |
|---|---|---------|
| 0 | 0 | **0** |
| 0 | 1 | **1** |
| 1 | 0 | **1** |
| 1 | 1 | **0** |

The XOR operation produces a true output (1) **only when the inputs are unequal**. Otherwise, it yields a false output (0). This is why it is called an *exclusive* OR — it excludes the case where both inputs are true.

---

### 3. Bitwise XOR — How It Works

XOR performs a bitwise operation on the individual bits of two operands. It returns `1` if the corresponding bits in the two operands are **different**, and `0` if they are the **same**.

**Example — 12 XOR 10:**

```
  12 = 1100  (binary)
  10 = 1010  (binary)
  ----------------
  XOR= 0110  =  6 (decimal)
```

Each bit pair is analyzed one by one: `A = 1101`, `B = 1011`, so `A XOR B = 0110`.

---

### 4. Key Properties of XOR

| Property | Rule | Meaning |
|---|---|---|
| **Commutativity** | A ⊕ B = B ⊕ A | Order doesn't matter |
| **Associativity** | (A ⊕ B) ⊕ C = A ⊕ (B ⊕ C) | Grouping doesn't matter |
| **Identity** | A ⊕ 0 = A | XOR with 0 returns the same value |
| **Self-inverse** | A ⊕ A = 0 | XOR with itself gives 0 |
| **Nilpotency** | A ⊕ 1 = NOT A | XOR with 1 flips the bit |

These properties — self-inversion and identity — are exploited in various computational tasks.

---

### 5. XOR vs OR — Key Difference

The XOR operation outputs true only when inputs **differ**, while the regular OR outputs true if **at least one** input is true. XOR is used for bitwise operations where flipping bits is necessary, whereas OR is used for settings where at least one true condition suffices.

---

### 6. Hardware Implementation

At the hardware level, XOR is implemented using 5 gates: 2 AND gates, 2 NOT gates, and 1 OR gate. The first input is fed to one NOT gate, and its output flows with the second input to an AND gate. The second input is likewise fed to another NOT gate, and its output flows with the first input to another AND gate. Both AND gate outputs are then fed to the OR gate to produce the final result.

XOR can also be viewed as **addition modulo 2**. As a result, XOR gates are used to implement binary addition in computers. A half adder consists of an XOR gate and an AND gate.

---

### 7. Practical Applications

#### a) Swap Two Variables Without Temporary Storage

Using XOR, values can be swapped without any auxiliary storage:

```
a = a XOR b
b = b XOR a
a = a XOR b
```

#### b) Encryption / Decryption

XOR is heavily used in cryptography for combining plaintext with a key to produce ciphertext. Since XOR is reversible — `(A ⊕ B) ⊕ B = A` — it ensures symmetric encryption and decryption.

#### c) Finding the Unique Element in an Array

One of the most common uses of XOR in programming is finding the unique element in an array where every other element appears twice. XOR-ing all elements causes duplicates to cancel out (since `x ⊕ x = 0`), leaving only the unique number.

```python
result = 0
for num in nums:
    result ^= num
# result holds the unique number
```

#### d) Error Detection (Parity Checking)

XOR operations are used in parity checking to determine if the number of bits set to 1 in a binary word is odd or even. This is often used in computer memory systems to detect errors.

#### e) RAID Storage Systems

XOR is used in RAID 3–6 for creating parity information. If any one of three hard drives is lost, the lost byte can be reconstructed by XOR-ing bytes from the remaining drives.

#### f) Bit Flipping / Masking

XOR can be used to toggle specific bits in a byte. Using a mask with XOR flips only the targeted bits while leaving others unchanged.

#### g) Random Number Generation

XOR is used in generating entropy pools for hardware random number generators. The XOR operation preserves randomness, meaning a random bit XORed with a non-random bit will result in a random bit. Multiple sources of potentially random data can be combined using XOR, and the unpredictability of the output is guaranteed to be at least as good as the best individual source.

---

### 8. XOR with Negative Numbers

When performing XOR with negative numbers, the numbers must first be converted to their two's complement (binary complement) form. The XOR operation is then applied bit by bit, with the most significant bit (MSB) denoting the sign of the result.

**Sign rules for XOR:**

| X | Y | X ^ Y |
|---|---|-------|
| + | + | + |
| + | - | - |
| - | + | - |
| - | - | + |

---

### 9. Summary

XOR is a deceptively simple operation with extraordinarily broad utility. Its core rule — **"output 1 only when inputs differ"** — enables a wide range of efficient algorithms and hardware designs. Whether you're encrypting data, detecting errors, swapping values, or designing logic circuits, XOR is one of the most fundamental and powerful tools in computer science.

References:

- [GeeksforGeeks – Bitwise XOR Operator](https://www.geeksforgeeks.org/software-engineering/bitwise-xor-operator-in-programming/)
- [Baeldung – The XOR Operation](https://www.baeldung.com/cs/exclusive-or)
- [Wikipedia – Exclusive OR](https://en.wikipedia.org/wiki/Exclusive_or)
- [Wikipedia – XOR Gate](https://en.wikipedia.org/wiki/XOR_gate)
- [DEV Community – Understanding the XOR Operator](https://dev.to/mspilari/understanding-the-xor-operator-a-powerful-tool-in-computing-1517)
- [LoginRadius – How Does Bitwise XOR Work](https://www.loginradius.com/blog/engineering/how-does-bitwise-xor-work)
- [Vaia – Exclusive Or Operation](https://www.vaia.com/en-us/explanations/computer-science/computer-programming/exclusive-or-operation/)
