---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 异或操作简单解释
translated: true
type: note
---

## XOR 操作 — 全面介绍

---

### 1. 什么是 XOR？

XOR（Exclusive OR）是一种逻辑运算符，其输出**仅当输入不同时为 true**——一个为 true，另一个为 false。对于多个输入，XOR 仅当 true 输入的数量为**奇数**时为 true。

在大多数编程语言中使用符号 `^` 表示，在数学记号中使用 `⊕`，XOR 广泛用于 cryptography、data structures 和 algorithms。

---

### 2. 真值表

理解 XOR 的最基本方法是通过其真值表：


| A | B | A XOR B |
|---|---|---------|
| 0 | 0 | **0** |
| 0 | 1 | **1** |
| 1 | 0 | **1** |
| 1 | 1 | **0** |

XOR 操作仅当输入不相等时产生 true 输出（1）。否则，产生 false 输出（0）。这就是为什么它被称为 *exclusive* OR——它排除了两个输入均为 true 的情况。

---

### 3. 按位 XOR — 工作原理

XOR 对两个操作数的单个位执行按位操作。如果两个操作数中对应的位**不同**，则返回 `1`；如果**相同**，则返回 `0`。

**示例 — 12 XOR 10：**

```
  12 = 1100  (binary)
  10 = 1010  (binary)
  ----------------
  XOR= 0110  =  6 (decimal)
```

每个位对逐一分析：`A = 1101`，`B = 1011`，因此 `A XOR B = 0110`。

---

### 4. XOR 的关键属性


| Property | Rule | Meaning |
|---|---|---|
| **Commutativity** | A ⊕ B = B ⊕ A | 顺序无关 |
| **Associativity** | (A ⊕ B) ⊕ C = A ⊕ (B ⊕ C) | 分组无关 |
| **Identity** | A ⊕ 0 = A | 与 0 进行 XOR 返回相同值 |
| **Self-inverse** | A ⊕ A = 0 | 与自身 XOR 得到 0 |
| **Nilpotency** | A ⊕ 1 = NOT A | 与 1 进行 XOR 翻转位 |

这些属性——自逆和单位元——被用于各种计算任务。

---

### 5. XOR 与 OR 的关键区别

XOR 操作仅当输入**不同**时输出 true，而常规 OR 操作只要**至少一个**输入为 true 就输出 true。XOR 用于需要翻转位的按位操作，而 OR 用于至少一个 true 条件即可满足的设置。

---

### 6. 硬件实现

在硬件级别，XOR 使用 5 个门实现：2 个 AND 门、2 个 NOT 门和 1 个 OR 门。第一个输入馈送到一个 NOT 门，其输出与第二个输入流向一个 AND 门。第二个输入同样馈送到另一个 NOT 门，其输出与第一个输入流向另一个 AND 门。两个 AND 门的输出然后馈送到 OR 门以产生最终结果。

XOR 也可以视为**模 2 加法**。因此，XOR 门用于在计算机中实现二进制加法。半加器由一个 XOR 门和一个 AND 门组成。

---

### 7. 实际应用

#### a) 无临时存储交换两个变量
使用 XOR，可以在不使用任何辅助存储的情况下交换值：
```
a = a XOR b
b = b XOR a
a = a XOR b
```

#### b) 加密 / 解密
XOR 在 cryptography 中被广泛用于将 plaintext 与 key 组合产生 ciphertext。由于 XOR 是可逆的——`(A ⊕ B) ⊕ B = A`——它确保了对称加密和解密。

#### c) 在数组中查找唯一元素
编程中 XOR 的最常见用途之一是，在每个其他元素出现两次的数组中查找唯一元素。对所有元素进行 XOR 会导致重复项抵消（因为 `x ⊕ x = 0`），仅留下唯一数字。

```python
result = 0
for num in nums:
    result ^= num
# result holds the unique number
```

#### d) 错误检测（奇偶校验）
XOR 操作用于奇偶校验，以确定二进制字中设置为 1 的位数是奇数还是偶数。这通常用于计算机内存系统中的错误检测。

#### e) RAID 存储系统
XOR 用于 RAID 3–6 中创建 parity 信息。如果三个硬盘中的任何一个丢失，可以通过对剩余硬盘中的字节进行 XOR 来重建丢失的字节。

#### f) 位翻转 / 掩码
XOR 可用于在字节中切换特定位。使用带有 XOR 的 mask 仅翻转目标位，同时保持其他位不变。

#### g) 随机数生成
XOR 用于为硬件随机数生成器生成 entropy pools。XOR 操作保留随机性，即随机位与非随机位进行 XOR 将产生随机位。可以使用 XOR 组合多个潜在随机数据源，并且输出的不可预测性保证至少与最佳单个源一样好。

---

### 8. 与负数的 XOR

对负数执行 XOR 时，必须先将数字转换为其 two's complement（二进制补码）形式。然后逐位应用 XOR 操作，其中最高有效位（MSB）表示结果的符号。

**XOR 的符号规则：**


| X | Y | X ^ Y |
|---|---|-------|
| + | + | + |
| + | - | - |
| - | + | - |
| - | - | + |

---

### 9. 总结

XOR 是一种看似简单但用途极广的操作。其核心规则——**“仅当输入不同时输出 1”**——支持了广泛的高效算法和硬件设计。无论您是在加密数据、检测错误、交换值还是设计逻辑电路，XOR 都是计算机科学中最基本且强大的工具之一。

References:

- [GeeksforGeeks – Bitwise XOR Operator](https://www.geeksforgeeks.org/software-engineering/bitwise-xor-operator-in-programming/)
- [Baeldung – The XOR Operation](https://www.baeldung.com/cs/exclusive-or)
- [Wikipedia – Exclusive OR](https://en.wikipedia.org/wiki/Exclusive_or)
- [Wikipedia – XOR Gate](https://en.wikipedia.org/wiki/XOR_gate)
- [DEV Community – Understanding the XOR Operator](https://dev.to/mspilari/understanding-the-xor-operator-a-powerful-tool-in-computing-1517)
- [LoginRadius – How Does Bitwise XOR Work](https://www.loginradius.com/blog/engineering/how-does-bitwise-xor-work)
- [Vaia – Exclusive Or Operation](https://www.vaia.com/en-us/explanations/computer-science/computer-programming/exclusive-or-operation/)
