---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 逐步解析确定性有限自动机
translated: true
type: note
---

**Question:** Explain more detailedly, step by step, what a deterministic finite automaton (DFA) is

**Answer:**

让我们非常缓慢地、一步一步地深入了解 **Deterministic Finite Automaton (DFA)** 的概念，就像我们要从零开始构建它一样。

### Step 1: 我们想要构建什么？

我们需要一个机器，它可以读取一个 string（例如 "10110" 或 "hello123"）并只回答一个问题：

**这个 string 是否属于某个特定的 language / pattern？**

Yes → accept（接受）
No → reject（拒绝）

而且这个机器应该非常简单：
- 它只有有限数量的“记忆位置”（称为 states）
- 它在输入中永远不会回退（从左到右只读取一次）
- 它的行为是完全可预测的（没有猜测，没有运气成份）

这正是 DFA 被设计出来的目的。

### Step 2: 每个 DFA 的五个组成要素

每个 DFA 都是由这五个要素精确定义的：

1. **Q** = set of states
   → 将其视为机器可能处于的不同“心情”或“情境”。
   例如：“我看到了偶数个 1”、“我看到了一个数字”、“我处于注释块内部”等。
   → 必须是一个有限列表：q₀, q₁, q₂, …, qₙ

2. **Σ** = input alphabet
   → 机器允许读取的符号/字母。
   例如：
   - {0, 1} → binary
   - {a, b, c, ..., z} → 小写英文字母
   - {0, 1, 2, 3, 4, 5, 6, 7, 8, 9} → 仅数字

3. **δ** = transition function（最重要的部分！）
   → 告诉机器：
     “如果我处于 state X 并且读取了符号 a，那么我必须进入 state Y”
   → 非常严格的规则：**对于每一个 state 和每一个可能的符号，有且仅有一个对应的 next state**
     → 没有选择，没有“也许”，没有“两种可能性” → 这就是为什么它被称为 **deterministic**（确定性）

4. **q₀** = starting state
   → 机器允许开始读取 string 的唯一起点。

5. **F** = set of accepting (final) states
   → 如果读取完整个 string 后，机器处于属于 F 的任何 state → “Yes, good string!”
   → 如果结束时处于不属于 F 的 state → “No, bad string!”

### Step 3: 逐步演示 —— DFA 如何在 string 上运行？

示例 DFA：
Language = 所有以 **01 结尾** 的 binary strings

States:
- q₀ = start / 还没看到任何有用的东西
- q₁ = 最后一个符号是 0
- q₂ = 最后两个符号是 01 ← accepting state

Transitions:

| Current | Input | → Next |
| :--- | :--- | :--- |
| q₀ | 0 | → q₁ |
| q₀ | 1 | → q₀ |
| q₁ | 0 | → q₁ |
| q₁ | 1 | → q₂ |
| q₂ | 0 | → q₁ |
| q₂ | 1 | → q₀ |

Start state = q₀
Accepting states = {q₂}

现在让我们逐步运行一些 strings：

**String: 01**

| Position | Read | Current state → New state |
| :--- | :--- | :--- |
| 0 | — | q₀ (start) |
| 1 | 0 | q₀ → q₁ |
| 2 | 1 | q₁ → q₂ |
| End | — | at q₂ → **accept** ✓ |

**String: 001**

| Position | Read | Current → New |
| :--- | :--- | :--- |
| 0 | — | q₀ |
| 1 | 0 | q₀ → q₁ |
| 2 | 0 | q₁ → q₁ |
| 3 | 1 | q₁ → q₂ |
| End | — | q₂ → **accept** ✓ |

**String: 011**

| Position | Read | Current → New |
| :--- | :--- | :--- |
| 0 | — | q₀ |
| 1 | 0 | q₀ → q₁ |
| 2 | 1 | q₁ → q₂ |
| 3 | 1 | q₂ → q₀ |
| End | — | q₀ → **reject** ✗ |

**String: 1010**

| Position | Read | Current → New |
| :--- | :--- | :--- |
| 0 | — | q₀ |
| 1 | 1 | q₀ → q₀ |
| 2 | 0 | q₀ → q₁ |
| 3 | 1 | q₁ → q₂ |
| 4 | 0 | q₂ → q₁ |
| End | — | q₁ → **reject** ✗ |

### Step 4: 最重要的属性 —— 逐一说明

- **Deterministic**
  → 在任何时刻，**有且仅有一个可能的下一步动作**。
  → 没有分支，没有“可能是这个，或者是那个”。

- **Finite**
  → 你可以在一张纸上写下所有的 states（即使是很长的一张纸）。

- **No ε-moves** (epsilon = empty move)
  → 每次 transition 必须消耗输入中的恰好一个字符。

- **Total / complete function**
  → 对于 Σ 中的每一个 state 和每一个符号，**必须**定义一个 transition。
  → 不会出现“未定义”或“卡住”的情况。

### Step 5: 总结表格 —— DFA 能做什么和不能做什么

| Can recognize | Cannot recognize |
| :--- | :--- |
| 所有以 “01” 结尾的 strings | 所有 0 和 1 数量相等的 strings |
| 任何固定的 pattern / keyword | 正确匹配的括号 ()()(()()) |
| 所有包含偶数个 1 的 strings | 形如 aⁿbⁿ 的 strings (相同数量的 a 和 b) |
| 大多数编程语言中合法的变量名 | 具有任意嵌套深度的 HTML/XML |
| 能被 3 整除的 binary numbers | 大多数自然语言 (English, Chinese…) |

所有“能做”的例子都是 **regular languages**。
所有“不能做”的例子都是 **not regular**（它们需要更强大的机器：pushdown automata，Turing machines…）。

### Step 6: 快速视觉类比

把 DFA 想象成一张地铁线路图：
- 车站 (Stations) = states
- 彩色箭头 (Colored arrows) = 标有符号的 transitions
- 你从一个特定的车站出发
- 你每读到一个字母就严格遵循一个箭头移动
- 结束时：如果你在一个“绿色”（accepting）车站 → 成功

这基本上就是 DFA 的全部内容。

您想再看一个具体的案例演练吗（例如：偶数个 0，或者包含子串 “101”，或其他示例）？

**References:**

- None (core automata theory concept – standard textbook material)
