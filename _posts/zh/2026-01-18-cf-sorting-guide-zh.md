---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-pro-preview
title: Codeforces 排序游戏解题指南
translated: true
type: note
---

Question: 如何解决 Codeforces 题目 "Sorting Game"？在该题目中，Alice 和 Bob 轮流将 binary string 的 non-increasing subsequence 重新排列为 non-decreasing order。

Answer:

### **Problem Analysis**

游戏在长度为 $n$ 的 binary string 上进行。

1. **Valid Move**：玩家选择一个 **non-increasing** subsequence（例如 `1, 1, 0, 0`）并将其排序为 **non-decreasing** order（例如 `0, 0, 1, 1`）。该操作必须严格改变字符串。
2. **Losing Condition**：无法进行有效移动的玩家输掉比赛（Normal Play Convention）。
3. **Terminal State**：当且仅当字符串已经 **sorted**（所有的 `0` 都在 `1` 之前）时，字符串处于 terminal state（无法移动）。如果字符串已排序，任何 non-increasing subsequence 都将只包含全 `0` 或全 `1`，对其排序不会改变字符串。

### **Winning Strategy**

如果 Alice 能够在一步移动中将字符串转变为排序状态，她就赢了。因为游戏在玩家面对已排序字符串时立即结束，如果 Alice 在她的第一回合就能完成排序，Bob 将立即输掉。

**Alice 总能一步完成排序吗？**
是的，只要字符串尚未排序。为此，Alice 需要识别出与最终排序版本相比，所有“位置不对”的字符。

1. 设 $z$ 为字符串 $s$ 中 `0` 的总数。
2. 在长度为 $n$ 且包含 $z$ 个 `0` 的已排序字符串中，前 $z$ 个字符必须是 `0`，其余 $n-z$ 个字符必须是 `1`。
3. Alice 可以选择当前字符不正确的索引集合 $I$：
* 任何满足 $i \le z$ 且 $s[i] = '1'$ 的索引 $i$。
* 任何满足 $i > z$ 且 $s[i] = '0'$ 的索引 $i$。

4. **Validity Check**：
* 索引 $i \le z$（对应 $s[i] = '1'$）处的字符总是出现在索引 $i > z$（对应 $s[i] = '0'$）处的字符之前。
* 因此，所选的 subsequence 总是由一系列 `1` 后跟一系列 `0` 组成，这是 **non-increasing** 的。
* 对该 subsequence 进行排序会将 `1` 移到后面，将 `0` 移到前面，从而使整个字符串变得有序。
* 如果字符串未排序，此集合 $I$ 将包含至少一个 `1` 和一个 `0`，从而使该移动有效。

### **Algorithm**

1. 统计字符串中 `0` 的总数 ($z$)。
2. 检查字符串是否已经排序（即从索引 $1$ 到 $z$ 的所有字符是否都是 `'0'`）。
3. 如果字符串已经排序，输出 **Bob**。
4. 否则，输出 **Alice**。
5. 提供移动方案：
* 找到所有满足 $i \le z$ 且 $s[i] = '1'$ 的索引 $i$。
* 找到所有满足 $i > z$ 且 $s[i] = '0'$ 的索引 $i$。
* 合并这些索引，对其排序，并作为 Alice 的第一步移动输出。

### **Complexity**

* **Time**：每个 test case 为 $O(n)$，用于统计 `0` 的数量和识别索引。
* **Space**：$O(n)$，用于存储移动的索引。

References:

* [Codeforces Problem 2190A - Sorting Game](https://codeforces.com/contest/2190/problem/A)（注：请根据您的来源确保 contest ID 正确。）