---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KV缓存预填充与重用
translated: true
type: note
---

问题：在LLM推理中，KV缓存预填充是如何工作的？这是否意味着无论输入如何，KV缓存始终相同？

回答：

并非如此——让我澄清一下**预填充**（阶段）和**KV缓存复用**（优化）之间的区别。

---

**预填充阶段（它通常的含义）**

在LLM推理中，每个请求都经历两个阶段：

1. **预填充**——模型并行处理整个输入提示，为每个token计算注意力键和值。这产生了初始的KV缓存。
2. **解码**——模型逐个生成token，并逐步将新token的KV对追加到缓存中。

因此，“预填充”仅指**提前处理提示**，并不意味着缓存是固定的。

---

**KV缓存复用（你想到的概念）**

你可以跨请求复用KV缓存，但前提是**前缀完全相同**。这称为**前缀缓存**（或提示缓存）：

```
共享前缀：  [系统提示token] → KV只计算一次，缓存 ✅
请求A：     [系统提示] + [用户查询A] → 只预填充查询A
请求B：     [系统提示] + [用户查询B] → 只预填充查询B
```

缓存的KV块是**内容相关的**——它们与特定的token序列绑定。不同的输入会产生不同的KV值，因为注意力键/值是从token嵌入计算得出的。

---

**为什么KV不能是“输入无关的”**

K和V矩阵为：

```
K = W_k · x
V = W_v · x
```

其中`x`是token嵌入。不同的token → 不同的`x` → 不同的K/V值。因此，KV缓存**始终是特定输入token的函数**。

---

**像RadixAttention / SGLang这样的系统做了什么**

它们将KV缓存存储在**前缀树（radix树）**中，因此任何共享公共前缀的请求都可以复用这些缓存的块。这是你直觉的实际实现——你可以跳过对共享部分重新计算预填充。

```
"You are a helpful assistant. Today is..."
        ↑ 在1000个请求中相同 → 只计算一次，复用KV缓存
```

---

参考文献：
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180)
- [SGLang: Efficient Execution of Structured Language Model Programs](https://arxiv.org/abs/2312.07104)
- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)