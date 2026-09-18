---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Lean：机器可验证的数学
translated: true
type: note
---

**问题：什么是 Lean 数学语言？**

**答案：**

**Lean** 是一种形式化编程语言和定理证明器，用于编写**机器可检查的数学**。它让人类能够用一种计算机可以通过小型可信内核验证的语言来表达数学定义、定理和证明。

可以这样理解：

> 数学 + 编程语言 + 证明检查器

核心思想：

普通数学证明：

```
定理：如果 a + b = b + a，则加法是可交换的。
证明：我们知道加法是可交换的。
```

Lean 证明：

```lean
theorem add_comm_example (a b : Nat) : a + b = b + a := by
  exact Nat.add_comm a b
```

Lean 会检查每一个逻辑步骤。

---

## 1. 为什么创建 Lean？

传统数学是为人类编写的：

```
设 x 为一个实数。
显然，x^2 >= 0。
因此...
```

人类凭直觉填补空白。

计算机无法做到这一点。它们需要：

```
定义
↓
公理
↓
逻辑推理规则
↓
证明对象
```

Lean 创建了一个可验证的**形式化证明对象**。

这对于以下方面很有用：

* 证明数学定理
* 验证软件
* 验证硬件
* AI 生成的推理评估

---

## 2. Lean 基于依赖类型理论

其基础是：

**归纳构造演算 (CIC)**

关键思想：

> 证明是一个程序，定理是一种类型。

示例：

```lean
theorem hello : 1 + 1 = 2 := by
  rfl
```

这里：

```
1 + 1 = 2
```

是一个**类型**。

证明：

```
rfl
```

是填充该类型的值。

类似于编程：

```python
def add(a,b):
    return a+b
```

在 Lean 中：

```
theorem proof_of_statement : Statement := proof
```

---

## 3. Lean 拥有一个微小的可信内核

这很重要。

Lean 本身有很多自动化工具：

* 策略 (tactics)
* AI 建议
* 搜索
* 简化器 (simplifiers)

但最终权威是内核。

流程：

```
人类 / AI
    |
    v
生成证明
    |
    v
Lean 内核
    |
    v
接受 / 拒绝
```

内核足够小，可以被审计。

---

## 4. 示例：证明算术

Lean：

```lean
example : 2 + 3 = 5 := by
  norm_num
```

策略：

```
norm_num
```

生成一个证明。

内核检查：

```
这个证明有效吗？
是
```

---

## 5. Lean 与普通编程的比较

Python：

```python
x = 5
print(x + 1)
```

问题：

“这个程序能运行吗？”

Lean：

```lean
theorem square_nonnegative (x : Int) :
  x*x >= 0 := ...
```

问题：

“这个数学命题被证明了吗？”

目标不同。

---

## 6. 为什么 AI 研究人员关注 Lean

现代推理模型使用 Lean，因为它提供了**可验证的奖励**。

普通 LLM 输出：

```
问题：
证明定理 X

LLM：
这是一个证明...
```

问题：

我们怎么知道它是正确的？

使用 Lean：

```
LLM 生成证明
        |
        v
Lean 编译器
        |
        +---- 有效 → 奖励 +1
        |
        +---- 无效 → 奖励 0
```

这创造了一个强化学习环境。

这就是为什么 Lean 对于以下方面很重要：

* AlphaProof
* DeepMind 数学推理研究
* OpenAI 定理证明实验
* 推理模型的强化学习

奖励是客观的。

---

## 7. Lean 生态系统

重要项目：

* Lean 4 — 当前 Lean 版本
* mathlib — 庞大的社区数学库

mathlib 包含了形式化的：

* 代数
* 拓扑
* 数论
* 分析
* 概率论
* 几何

示例：

```lean
import Mathlib

example (x : ℝ) : x^2 ≥ 0 := by
  positivity
```

---

## 8. 与 LLM 推理的关系

普通的思维链 (chain-of-thought)：

```
LLM：
步骤 1...
步骤 2...
步骤 3...
（答案）
```

无法被信任。

基于 Lean 的推理：

```
LLM：
生成 Lean 代码

        ↓

Lean 验证器

        ↓

正确 / 错误
```

因此，Lean 成为了一个**真实环境 (ground truth environment)**。

未来方向：

```
LLM
 |
 | 生成
 v
Lean 证明
 |
 | 验证
 v
数学真理
```

这类似于代码执行如何为 LLM 提供验证编程答案的方式。

---

一句话总结：

**Lean 是一种编程语言，其中数学命题成为类型，证明成为程序，从而让计算机能够机械地验证推理是否正确。**