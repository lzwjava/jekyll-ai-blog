---
audio: false
generated: true
image: false
lang: en
layout: post
title: DES Encryption Mechanism
translated: false
type: note
---

**Question: What is the DES encryption mechanism?**

**Answer:**

DES (**Data Encryption Standard**) is a **symmetric block cipher**. It means:

* The **same secret key** is used for encryption and decryption.
* It encrypts data in fixed-size blocks.
* It uses a series of transformations to scramble plaintext into ciphertext.

DES basics:

```
Plaintext (64 bits)
        |
        v
 Initial Permutation (IP)
        |
        v
 16 rounds of Feistel network
        |
        v
 Final Permutation (IP^-1)
        |
        v
Ciphertext (64 bits)
```

## 1. Key structure

DES uses:

* Effective key size: **56 bits**
* Stored key size: **64 bits**

  * 56 bits are actual key bits
  * 8 bits are parity check bits

Example:

```
64-bit key
+--------------------------------+
| 56-bit secret | 8-bit parity   |
+--------------------------------+
```

Because 56 bits became too small, DES is now considered insecure.

---

## 2. Feistel network

The core idea of DES is the **Feistel structure**.

Split the 64-bit block:

```
Input:

+-------------+-------------+
| Left 32 bit | Right 32bit |
+-------------+-------------+

L0            R0
```

Each round:

```
L(i+1) = R(i)

R(i+1) = L(i) XOR F(R(i), K(i))
```

Where:

* `K(i)` = round key
* `F()` = DES round function

After 16 rounds:

```
L16 + R16

= ciphertext
```

The advantage of Feistel:

Encryption and decryption use almost the same hardware.

Only the order of keys changes:

Encryption:

```
K1 K2 K3 ... K16
```

Decryption:

```
K16 K15 K14 ... K1
```

---

## 3. DES round function F()

The main scrambling happens here:

```
32-bit R
   |
   v
Expansion E
(32 bits -> 48 bits)

   |
   XOR

48-bit round key

   |
   v

S-box substitution
(48 bits -> 32 bits)

   |
   v

Permutation P

   |
   v

32-bit output
```

Detailed:

### Expansion

The right half:

```
32 bits
```

is expanded to:

```
48 bits
```

so it matches the round key.

---

### XOR with key

Example:

```
101010...
XOR
110011...
---------
011001...
```

---

### S-box

The S-box is the security heart of DES.

It maps:

```
6 bits -> 4 bits
```

There are 8 S-boxes:

```
48 bits

S1 S2 S3 S4 S5 S6 S7 S8

8 × 6 bits

       |

       v

32 bits
```

The S-box introduces **non-linearity**, preventing simple mathematical attacks.

---

## 4. Key schedule

DES creates 16 round keys.

Process:

```
56-bit key

      |
      v

Split:

C0 (28 bits)
D0 (28 bits)


      |
      v

Rotate left each round

      |
      v

Compression permutation

      |
      v

48-bit K1 ... K16
```

So:

```
K1
K2
...
K16
```

are generated.

---

## 5. Example

Encryption:

```
Plaintext:

"HELLO123"

64 bits

        |
        v

DES with key

        |
        v

Ciphertext:

8 bytes random-looking data
```

Decryption:

```
Ciphertext

        |
        v

DES with same key

        |
        v

"HELLO123"
```

---

## 6. Why DES became insecure

The problem:

```
56-bit key
```

has only:

```
2^56 ≈ 72 quadrillion
```

possibilities.

Modern GPUs/ASICs can brute force this.

A famous example:

* In 1998, EFF built a machine that cracked DES in about 56 hours.
* Today, large-scale hardware can do it much faster.

So DES was replaced by:

```
DES
 |
 v
3DES (Triple DES)
 |
 v
AES
```

Modern standard:

```
AES-128
AES-256
```

---

## 7. DES vs AES

|            | DES     | AES                              |
| ---------- | ------- | -------------------------------- |
| Year       | 1977    | 2001                             |
| Block size | 64 bits | 128 bits                         |
| Key size   | 56 bits | 128/192/256 bits                 |
| Structure  | Feistel | Substitution-Permutation Network |
| Rounds     | 16      | 10/12/14                         |
| Security   | Broken  | Current standard                 |

---

In short:

**DES works by repeatedly mixing a 64-bit data block with 16 generated keys using a Feistel network. Its security comes mainly from S-box nonlinear substitution and repeated permutations. The mechanism was historically important, but the 56-bit key is too small today, so AES replaced it.**
