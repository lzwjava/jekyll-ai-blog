---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FFN作为键值记忆
translated: true
type: note
---

**问题：** 如何理解 Transformer 中的 FFN 作为 Key-Value Memory？

**答案：**

让我们逐步建立直觉。

---

## 步骤 1: 回顾 FFN 数学

FFN(x) = ReLU( x · W₁ᵀ ) · W₂

- `x` = input token vector (dim: `d_model`)
- `W₁` = first weight matrix (dim: `d_hidden × d_model`)
- `W₂` = second weight matrix (dim: `d_model × d_hidden`)

---

## 步骤 2: 将 W₁ 视为一组 "keys"

**W₁ 的每一 row** 都是一个与 `x` 在同一空间的 vector。

操作 `x · W₁ᵀ` 只是在计算 input `x` 与 W₁ 每一 row 之间的 **dot product**。

```
x · W₁ᵀ = [x·k₁, x·k₂, x·k₃, ..., x·kₙ]
```

这字面意思是在问：**"我的 input x 与每个 key kᵢ 有多相似？"**

大的 dot product = key 匹配。小的 dot product = key 不匹配。

经过 ReLU 后，只有 **匹配的 keys 激活** (negative = 0, positive = kept)。

---

## 步骤 3: 将 W₂ 视为一组 "values"

**W₂ 的每一 column** 都是一个 value vector `vᵢ`。

ReLU 给出 activation scores `[a₁, a₂, ..., aₙ]` 后，第二步：

```
output = a₁·v₁ + a₂·v₂ + ... + aₙ·vₙ
```

这是一个 value vectors 的 **weighted sum** — 完全像一个 soft lookup table。

---

## 步骤 4: 具体类比

想象模型内部有一本 dictionary：

```
"The Eiffel Tower is in ___"
        ↓
Key pattern: [city after landmark, French context, ...]
        ↓ matches neuron #4721
Value vector #4721: points toward "Paris" in vocab space
        ↓
Output: adds "Paris" signal to the prediction
```

每个 key 与 training examples 中的 textual patterns 相关联，每个 value 在 output vocabulary 上产生一个 distribution。

在一个以 '...no substitutes' 结尾的句子中，一个特定的 FFN key 激活。如果我们不知道这个 key 与 pattern 'substitutes at end of sentence' 相关，并且它的 value 预测 next likely token，我们就无法解释为什么模型接下来 output 一个 specific word。

---

## 步骤 5: 它是 "soft" 查找，而非 hard lookup

与 hash map 不同（你要么找到 key，要么没有），这是 **differentiable / soft**：

| Hard dictionary | FFN (soft) |
| --- | --- |
| Exact key match | Dot product similarity |
| Returns one value | Returns weighted mix of many values |
| Fixed entries | Learned during training |

activation `m = f(x · Kᵀ)` 可被视为一个 vector，包含 FFN block 中每个 memory entry 的 unnormalized coefficient。结果，FFN block 的 output 是一个 memory values 的 **weighted mixture**。

---

## 总结图

```
Input x
   │
   ▼
x · W₁ᵀ  ←── "Which keys match my input?"
   │           (W₁ rows = keys)
   ▼
ReLU       ←── "Suppress non-matches"
   │
   ▼
scores · W₂ ←── "Retrieve weighted values"
   │             (W₂ columns = values)
   ▼
Output     ←── "Knowledge retrieved"
```

W₁ 的每一 row 是一个 key (pattern detector)，而 W₂ 的每一 column 是一个用于组成 output 的 value。第二投影作为相应的 "values" — 每一 column 是一个 contribution，根据其 key 激活的强度按比例添加到 output 中。

---

## 为什么这一点很重要？

feed-forward layer 的 output 是其 memories 的 **composition**，随后通过 residual connections 在整个 model 的 layers 中 refine，以产生最终 output distribution。

这意味着 factual knowledge（例如，"capital of France = Paris"）实际上被 **encoded in the weights of W₁ and W₂** — 这就是为什么有时你可以通过修改特定的 FFN weight entries 来 "edit" 一个 model 的 factual knowledge。

**参考文献：**

- [Geva et al. (2021) — Transformer Feed-Forward Layers Are Key-Value Memories](https://arxiv.org/abs/2012.14913)
- [ZeroEntropy — Feedforward Network explainer](https://www.zeroentropy.dev/concepts/feedforward-network/)
- [Geva et al. (2022) — Transformer Feed-Forward Layers Build Predictions by Promoting Concepts](https://arxiv.org/abs/2203.14680)
