---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 Codeforces 2190A 中的运行时错误
translated: true
type: note
---

**Question:** 为什么这段代码在 Codeforces problem 2190A 的 test 1 中出现了 Runtime Error？

**Answer:**

你的代码在 test 1 出现 **Runtime Error** 主要是因为这个关键的逻辑错误：

```java
for (i = 0; i < n; i++) {
    char target;
    if (i < zero) {
        target = '0';
    } else {
        target = '1';
    }
    if (s.charAt(i) != target) {
        positions.add(i);
    }
}
```

这个逻辑假设在排序后，字符串应该变为：

- 前 `zero` 个字符 = '0'
- 剩余的 `one` 个字符 = '1'

但这**不是**题目所要求的。

该题目要求的是通过**最多一次**交换两个字符，能够获得的**lexicographically smallest**（字典序最小）的字符串。

这意味着目标排序字符串**始终**是：

所有的 '0' 都在所有的 '1' **之前**
→ `000...0111...1`（恰好是 `zero` 个 0 后面跟着 `one` 个 1）

但你的代码是将**当前**字符串与这个理想的排序字符串进行比较，并收集**所有**不匹配的位置。

这对于该问题的目的来说是完全错误的，因为：

- 题目只允许**最多一次交换**（0 次或 1 次交换）
- 你应该输出以下内容之一：
  - "Bob"（如果已经排序 / 不需要交换 / 仅靠 1 次交换无法完成）
  - "Alice" + **恰好两个交换位置**（从 1 开始计数）

你的代码几乎总是输出**超过两个位置**（或者零个），这导致：

- 错误的输出格式 → 评测系统期望的是：
  - 单行 "Bob"
  - 或者两行："Alice" 后面跟着**恰好两个数字**
- 当它打印了过多数字或错误的数量时 → 就会触发 **Runtime Error** 或 **Wrong Answer**

### test 1 出现 Runtime Error 的真实原因

很可能 test 1 是以下这些简单情况之一：

```
1
3
010
```

或

```
1
4
1100
```

或

```
1
1
0
```

在这些情况下，你的代码：

- 统计了 `zero` 和 `one` 的数量
- 如果字符全部相同 → 打印 "Bob"（没问题）
- 否则 → 进入 `positions` 集合逻辑
- 打印 "Alice" 然后打印出**许多位置**（或者没有位置）
- 评测系统期望 "Bob" 或 "Alice\nx y" → 你的输出格式无效 → **Runtime Error**

### 正确思路（简述）

你只需要找到**最多一个位置错误的、在 '0' 之前的 '1'**。

如果字符串是非递减的（所有的 0 都在 1 之前），那么字符串已经符合要求（Bob）。

否则，你通常需要将**一个出现得太早的 '1'** 与**一个出现得太晚的 '0'** 进行交换。

最常见的模式：找到应该为 '0' 的**最左边的 '1'**，以及应该为 '1' 的**最右边的 '0'**，然后交换它们。

但你必须检查在进行这一次交换后，字符串是否变得有序。

### 快速正确的方案

```java
Read t
For each test:
    Read n, s
    Count zeros = count of '0'

    // 检查是否已经有序 (non-decreasing)
    boolean sorted = true;
    for (int i = 1; i < n; i++) {
        if (s.charAt(i) < s.charAt(i-1)) {
            sorted = false;
            break;
        }
    }

    if (sorted) {
        out.println("Bob");
        continue;
    }

    // 寻找我们拥有 '1' 但在 target 中应该是 '0' 的最左侧位置
    int left = -1;
    for (int i = 0; i < zeros; i++) {
        if (s.charAt(i) == '1') {
            left = i;
            break;
        }
    }

    // 寻找我们拥有 '0' 但在 target 中应该是 '1' 的最右侧位置
    int right = -1;
    for (int i = n-1; i >= zeros; i--) {
        if (s.charAt(i) == '0') {
            right = i;
            break;
        }
    }

    // 如果两个都找到了 → 一次交换即可修复
    if (left != -1 && right != -1) {
        out.println("Alice");
        out.println((left+1) + " " + (right+1));
    } else {
        out.println("Bob");  // 一次交换无法完成
    }
```

这并不是 100% 完整的代码（某些边界情况需要仔细检查），但它解释了解决方向。

你当前的代码正在尝试做一些与题目要求完全不同的事情，这就是它很早就失败（test 1）的原因。

**References:**

- [https://codeforces.com/contest/2190/problem/A](https://codeforces.com/contest/2190/problem/A)
