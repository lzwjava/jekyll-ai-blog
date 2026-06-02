---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CRC 零追加规则详解
translated: true
type: note
---

Question: 使用 generator polynomial 位串 11001 的 CRC校验 (Cyclic Redundancy Check) 时，在对信息位串执行 GF(2) 上的多项式除法以计算 CRC 冗余位之前，必须在信息位串末尾附加多少个零？

Answer:

正确答案是 **C (4)**。

### 解释

1. **理解 Generator Polynomial**：
    问题指出，对应 generator polynomial 的位串是 `11001`。
    - 在二进制表示中，这对应从最高次到最低次的多项式系数（$x^4, x^3, x^2, x^1, x^0$）。
    - 因此，多项式是 $G(x) = 1\cdot x^4 + 1\cdot x^3 + 0\cdot x^2 + 0\cdot x^1 + 1\cdot x^0 = x^4 + x^3 + 1$。

2. **确定多项式的次数**：
    - $G(x)$ 中 $x$ 的最高次是 4。
    - 或者，可以通过计算 generator string 的位数并减 1 来确定次数。
    - `11001` 的长度 = 5 位。
    - 次数 ($r$) = $5 - 1 = 4$。

3. **CRC 计算规则**：
    - 要计算 CRC 冗余位（也称为 Frame Check Sequence 或 FCS），必须在原始消息（信息位）末尾附加 $r$ 个零，其中 $r$ 是 generator polynomial 的次数。
    - 由于次数是 4，因此必须在信息位串末尾附加 **4** 个零，然后执行模 2 除法。

4. **为什么选项 B 不正确**：
    - 选项 B 建议添加 3 个零。如果 generator polynomial 的次数是 3（例如，像 `1101` 这样的 4 位串），这将是正确的。但是，由于串 `11001` 有 5 位，次数是 4，需要 4 个零。

**结论**：
由于 generator polynomial `11001` 的次数是 4，因此必须在信息位末尾附加 **4** 个零。
