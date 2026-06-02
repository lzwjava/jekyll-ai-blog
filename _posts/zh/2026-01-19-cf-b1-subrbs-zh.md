---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5.2
title: Codeforces 题目 B1 Sub-RBS 初级版解题报告
translated: true
type: note
---

Question: How to solve the Codeforces problem “B1. Sub-RBS (Easy Version)”?

Answer:

这道题目要求在给定的 regular bracket sequence (RBS) `s` 中，找出一个其它的 **longest regular bracket subsequence** `t`，使得根据自定义定义，`t` 的 **lexicographically better** 比 `s` 更好。

让我们逐步分解。

---

## 1. 理解 “better than”

一个 bracket sequence `t` 比 `s` **better**，如果：

1. `s` 是 `t` 的前缀且 `t ≠ s`，**或者**
2. 在第一个不同的位置上，`t[i] = '('` 且 `s[i] = ')'`。

由于 `t` 是 `s` 的 **subsequence**，第一种情况是不可能的（subsequence 长度不可能更长且同时保持 `s` 为其前缀）。

所以只有 **第二条规则有效**：

> 在第一个不同的位置，`t` 必须是 `'('` 而 `s` 是 `')'`。

---

## 2. 关键观察

为了比 `s` 更好，subsequence `t` 必须：

* 与 `s` 的某个前缀匹配，
* 然后 **跳过 `s` 中的一个 `')'`，转而使用后面出现的一个 `'('`**。

这意味着：
👉 必须存在一个位置，使得 `s[i] = ')'`，但在字符串后面的部分存在一个未使用的 `'('` 供我们选择。

---

## 3. 策略

我们希望得到 **maximum length** 的有效 subsequence `t`。

为了实现这一点：

1. **移除 `s` 的一个以 `')'` 结尾的前缀**。
2. 从剩余的后缀中，获取 **longest possible regular bracket subsequence**。

最优选择是：

* 移除 **最短的以 `')'` 结尾的前缀**，使得剩余的后缀仍然包含一个 regular bracket sequence。

为什么？

* 移除的部分越短 → 剩余的 subsequence 越长。
* 立即跳过一个 `')'` 可以保证 `t` 比 `s` 更好。

---

## 4. 什么时候不可能？

如果 **每一个以 `')'` 结尾的前缀都会导致剩余后缀无效**，那么：

* 没有 subsequence 能比 `s` 更好。
* 输出 `-1`。

这发生在 `s` 已经是 lexicographically minimal 的情况下，例如：

* `()`
* `(())()`

---

## 5. 实际解题方法

对于每个 test case：

1. 从左到右遍历字符串。
2. 追踪 brackets 的 balance。
3. 找到 **第一个位置 `i` 使得 `s[i] = ')'`** 且满足：

   * 后缀 `s[i+1 ... n]` 包含至少一个有效的 RBS。
4. 计算该后缀中 **longest RBS subsequence** 的长度：

   * 长度等于 `2 × min(number of '(' , number of ')')`。
5. 输出该长度。
6. 如果不存在这样的位置 → 输出 `-1`。

---

## 6. 示例演示

### 示例 1

```
s = ()
```

* 唯一的有效 subsequence 是它本身。
* 无法变得更好。
  ✅ 输出：`-1`

---

### 示例 2

```
s = (()(()))
```

* 跳过位置 3 的 `')'`。
* 剩余字符串可以组成 `((()))`。
* Length = 6。
  ✅ 输出：`6`

---

### 示例 3

```
s = (())()
```

* 任何跳过的 `')'` 都会破坏后缀的有效性。
* 没有更好的 subsequence。
  ✅ 输出：`-1`

---

## 7. Time complexity

* 每个 test case 在 **O(n)** 时间内处理。
* 所有 test cases 的总复杂度为 **O(Σn)** ≤ 2 × 10⁵。
* 在限制条件下完全可以接受。

---

## 8. 总结

✔ 你不需要显式地构建 subsequence。
✔ 你是在寻找跳过一个关键的 `')'` 后 **最佳的可能后缀**。
✔ 如果存在这样的后缀 → 计算其最大的 RBS 长度。
✔ 否则 → 输出 `-1`。

这种 greedy 观察是高效解决该问题的核心思路。
