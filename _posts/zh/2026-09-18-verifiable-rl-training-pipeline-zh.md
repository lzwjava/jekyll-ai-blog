---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 可验证强化学习训练流水线
translated: true
type: note
---

是的，你的理解基本正确。

**问题：**
RL 使用生成的数据 + 奖励分数 + 可验证规则（Lean/代码执行）来引导模型朝向期望行为？

**答案：**

一个简化的 RL 流程如下：

```
LLM policy πθ
    |
    | generate output y
    v
Environment / Verifier
    |
    | compute reward r
    v
RL algorithm updates θ
    |
    v
Better future outputs
```

关键思想：

> 模型并不直接学习“正确答案”。它学习的是增加期望奖励的策略。

数学上：

$$
J(\theta)=E_{y\sim \pi_\theta}[R(y)]
$$

RL 尝试调整模型参数：

$$
\theta \leftarrow \theta + \alpha \nabla_\theta J(\theta)
$$

使得更高奖励的输出变得更有可能。

---

## 示例 1：代码生成

提示：

```
Write a Python function to sort a list
```

模型生成：

```python
def sort(x):
    return x[::-1]
```

验证器运行：

```bash
pytest tests.py
```

结果：

```
失败
```

奖励：

```
r = 0
```

另一个样本：

```python
def sort(x):
    return sorted(x)
```

测试：

```
通过
```

奖励：

```
r = 1
```

RL 学到：

```
通过测试的输出
↑ 概率
```

---

## 示例 2：Lean 定理证明

模型生成：

```lean
theorem add_zero (n : Nat) :
  n + 0 = n := by
  rfl
```

Lean 编译器：

```
成功
```

奖励：

```
+1
```

错误证明：

```lean
by
  sorry
```

Lean 拒绝：

```
失败
```

奖励：

```
0
```

验证器成为一台**事实检验机**。

---

## 为什么这很强大

传统的 RLHF：

```
人类：
"这个答案感觉更好"
        |
        v
Reward model
        |
        v
RL
```

问题：

* 主观
* 昂贵
* reward hacking

---

可验证的 RL：

```
计算机：
"它编译通过吗？"
"定理证明成功吗？"
"模拟器成功吗？"
        |
        v
精确奖励
```

示例：

| 领域            | 验证器                  |
| --------------- | ----------------------- |
| 编程            | unit tests/compiler     |
| 数学            | Lean/Coq/Isabelle       |
| 机器人学        | simulator               |
| 游戏            | game score              |
| SQL             | database execution      |
| 硬件设计        | EDA tools               |

奖励几乎是二元的：

```
正确 = 1
错误 = 0
```

---

这是近期**推理模型**背后的核心思想：

```
基础模型
    +
大规模生成的问题
    +
可验证奖励
    +
RL 优化
    =
更强的推理模型
```

例如，数学：

```
生成 1000 个解决方案

解决方案 A：
证明检查器通过
奖励 = 1

解决方案 B：
错误代数
奖励 = 0

RL 将概率推向类似 A 的推理模式
```

有趣的是，模型可以发现**新的内部策略**，因为 RL 只告诉：

> “这个输出成功了。”

它并没有明确地教授每一步推理。

这就是为什么可验证的环境（Lean、代码执行、游戏、模拟器）对训练推理模型变得越来越重要。