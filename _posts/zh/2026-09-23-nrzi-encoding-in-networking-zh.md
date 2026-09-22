---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络中的NRZI编码
translated: true
type: note
---

问：什么是 networking 中的 NRZI？

答：**NRZI（Non-Return-to-Zero Inverted）** 是一种 **line encoding** 方案：它将 bits 映射为 wire 上的 physical signal transitions。

关键思想是：

> **一个 transition 表示一个 bit 值；no transition 表示另一个。**

一个常见约定是：

* `1` → **transition**
* `0` → **no transition**

因此，如果当前 signal level 为 `LOW`：

```text
bits:    1  0  0  1  1  0
signal:  └─┐───┐└─┐───
           ↑       ↑ ↑
        transition
```

更精确地说，从 `LOW` 开始：

```text
bit:      1   0   0   1   1   0
level:   LOW HIGH HIGH LOW HIGH HIGH
           └───┘     └──┘
            no       transition
```

### 为什么使用 NRZI？

传输原始 `0/1` voltage levels 的问题在于 **clock recovery**。

假设你传输：

```text
000000000000
```

接收端看到恒定 signal，难以确定 individual bits 的位置。

NRZI 可以让 transitions 对信息进行编码，从而让 synchronization 更容易。

但有一个重要的注意点：

```text
111111111111
```

在上述约定下产生 **continuous transitions**，而：

```text
000000000000
```

产生 **no transitions**。

因此，长串有问题的 bit 仍然会导致 synchronization 问题。所以 protocols 通常将 NRZI 与 **bit stuffing** 或另一个 coding layer 结合使用。

### NRZ 与 NRZI

最简单的记忆方式是：

```text
NRZ:
    bit value → signal level

NRZI:
    bit value → whether signal changes
```

例如，对于 `1 = transition`：

```text
bits:   1 0 1 1 0 0 1
        ↓ ↓ ↓ ↓ ↓ ↓ ↓

NRZI:   ↑ ─ ↑ ↑ ─ ─ ↑
```

绝对 voltage 并不直接承载 bit；真正起作用的是 **change/no-change relationship**。

### 你会在哪里遇到它

NRZI 出现在多个 networking/storage protocols 和 standards 中，特别是 **USB**（历史上，USB 1.x/2.0 在 physical layer 使用 NRZI 并配合 bit stuffing）。

一个微妙的点是：**NRZI 的约定并不是通用的**。有些描述使用 `1 = no transition` 和 `0 = transition`，所以请务必查看具体 protocol 的定义，而不要死记哪个 bit 表示 transition。

我还可以用约 20 行 Python 逐步讲解 **USB 的 NRZI + bit-stuffing encoder/decoder**，这样会让机制非常具体。