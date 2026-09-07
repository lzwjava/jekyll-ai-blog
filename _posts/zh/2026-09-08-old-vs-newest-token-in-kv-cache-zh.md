---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KV缓存中的旧令牌与最新令牌
translated: true
type: note
---

问题：KV 缓存中的“old tokens”和“newest token”是什么意思？

答案：**“old”和“newest”仅仅指已经处理过的 token 与当前正在生成的 token。**

举个例子：

```text
The cat sat
```

假设 LLM 已经处理了这 3 个 token：

```text
Token 1: The
Token 2: cat
Token 3: sat
```

现在它要生成 **token 4**。

### 1. “old tokens”

已经存在于上下文中的 token 就是 **old tokens**：

```text
The   cat   sat
 ↑     ↑     ↑
old   old   old
```

Transformer 已经计算了它们的：

```text
K1, V1
K2, V2
K3, V3
```

并存储在 KV 缓存中：

```text
KV Cache:

K1 V1   ← "The"
K2 V2   ← "cat"
K3 V3   ← "sat"
```

这些不需要重新计算。

---

### 2. “newest token”

现在模型生成下一个 token，例如：

```text
"The cat sat on"
              ↑
          newest token
```

`on` 就是 **newest token**，因为它刚刚被生成。

对于这个 token，模型计算：

```text
Q4
K4
V4
```

然后：

```text
KV Cache:

K1 V1   ← The
K2 V2   ← cat
K3 V3   ← sat
K4 V4   ← on       ← 新添加
```

接着在生成 token 5 时：

```text
The cat sat on the
                  ↑
              newest token
```

此时：

```text
The cat sat on
 ↑   ↑   ↑   ↑
old old old old

the
 ↑
newest
```

缓存中已经包含：

```text
K1 V1
K2 V2
K3 V3
K4 V4
```

所以我们只计算：

```text
Q5 K5 V5
```

并将 `K5、V5` 追加进去。

---

### 重要的区分

在每一个解码步骤中，**只有一个新处理的 token**：

```text
┌──────────────────── 已经处理 ────────────────────┐
│                                                   │
The   cat   sat   on   the   mat
 ↑     ↑     ↑    ↑    ↑
 old   old   old  old  old
                         │
                         └── 此步骤中的 newest
```

生成 `mat` 后，情况变为：

```text
The   cat   sat   on   the   mat
 ↑     ↑     ↑    ↑    ↑     ↑
 old   old   old  old  old  newest
```

在**下一个**步骤中，新生成的 token 成为 newest，而 `mat` 变为 old。

因此，“old”并不是 token 的永久属性，它是相对于当前生成步骤而言的。

---

### 一个微妙但重要的点

在生成 token 6 时，模型仍然需要**关注所有先前的 token**：

```text
Q6  ×  [K1 K2 K3 K4 K5]
       ↓  ↓  ↓  ↓  ↓
      所有先前的 token
```

但它不需要**重新计算** `K1...K5` 和 `V1...V5`。

这正是 KV 缓存的全部意义：

```text
                OLD TOKENS
                   │
             K/V 已缓存
                   │
                   ▼
新 token → Q ──→ attention → 下一个 token 的概率
       └────→ K,V → 追加到缓存
```

这也是为什么**KV 缓存在每个解码步骤中会增长一个 token**。