---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: CRC 编码效率详解
translated: true
type: note
---

Question: In cyclic redundancy check (CRC), if the codeword has k information bits and r redundancy bits are added during encoding, what is the encoding efficiency?

Answer:

正确答案是 **D. k/(k+r)**。

**Explanation:**

Encoding efficiency（编码效率，也称为 code rate 或 information rate）衡量的是在传输的总位（bits）中，实际携带有效信息的比例。

- Information bits (payload): **k** bits
- Redundancy bits (check bits, parity bits): **r** bits
- Total codeword length: **k + r** bits

因此，encoding efficiency 的定义为：

**Efficiency = (number of information bits) / (total number of bits in the codeword) = k / (k + r)**

这与选项 **D** 相符。

**Quick memory tip:**
"信息位 k，总长 k + r，效率 k / (k + r)"

**为什么其他选项是错误的：**

- A. r/(r+k) → 这是 redundancy ratio（冗余率），而不是效率。
- B. 1/(k+r) → 在此语境下没有实际意义。
- C. r/k → 这是相对冗余度，与效率的概念相反。

因此，正确的选择确实是 **D**。

References:

- None (standard coding theory definition, no external reference required)
