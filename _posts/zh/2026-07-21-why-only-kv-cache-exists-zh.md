---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为何只有KV缓存存在
translated: true
type: note
---

**问题：为什么叫 KV 缓存 而不是 QKV 缓存？Q 不需要缓存吗？**

**答案：**

没错：**在自回归生成中，Q 不需要缓存**。只有 **K 和 V** 需要缓存。

原因来自注意力公式：

\[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt{d}})V
\]

对于每个新生成的 token，我们会创建一个新的 **Q**，但复用的是旧的 **K/V**。

---

## 逐步生成过程

假设提示词为：

```
The capital of France is
```

Tokens（词元）：

```
t1 t2 t3 t4 t5
```

在 L 层：

第一次前向传播：

```
Q:
q1 q2 q3 q4 q5

K:
k1 k2 k3 k4 k5

V:
v1 v2 v3 v4 v5
```

我们保存：

```
KV 缓存：

(k1,v1)
(k2,v2)
(k3,v3)
(k4,v4)
(k5,v5)
```

我们丢弃 Q。

为什么？

因为下一步只需要：

```
新 token t6
```

计算：

```
q6
k6
v6
```

然后注意力计算：

```
q6 关注于：

k1 k2 k3 k4 k5 k6
v1 v2 v3 v4 v5 v6
```

旧的查询：

```
q1 q2 q3 q4 q5
```

再也不会被使用。

---

## 为什么旧的 Q 是无用的

想象逐 token 解码的过程。

步骤 6：

```
Q = q6

K = [k1,k2,k3,k4,k5,k6]

V = [v1,v2,v3,v4,v5,v6]
```

注意力计算：

```
softmax(q6 · K^T)V
```

只有 `q6` 参与计算。

步骤 7：

```
Q = q7

K = [k1...k7]

V = [v1...v7]
```

同样：

```
只有 q7
```

没有任何操作需要：

```
q6
q5
q4
```

---

## 为什么 K 和 V 特殊

因为之前的 token 被用作 **记忆槽位**。

将注意力理解为：

```
查询：
"我需要什么信息？"

键：
"存在什么信息？"

值：
"实际的信息"
```

在生成过程中：

当前 token 询问：

```
Q(新 token)
       |
       v
搜索旧记忆

K 缓存
       |
       v
检索

V 缓存
```

旧的 token 变成了一个数据库：

```
        KV 缓存

token1 -> key1,value1
token2 -> key2,value2
token3 -> key3,value3
...
```

新的查询是搜索请求。

你不会存储旧的搜索请求。

---

## 训练时有所不同

在训练过程中，你会：

```
Q:
q1 q2 q3 q4 q5

K:
k1 k2 k3 k4 k5

V:
v1 v2 v3 v4 v5
```

一次性完成。

注意力矩阵：

```
        K

       1 2 3 4 5

Q 1    x
  2    x x
  3    x x x
  4    x x x x
  5    x x x x x
```

每个 Q 都被使用一次。

无需缓存。

---

## 一个细微之处：使用梯度检查点进行训练时

有时人们会提到"激活缓存"或"注意力缓存"，但这属于不同的概念。

* KV 缓存 → 推理优化
* 激活缓存 → 训练内存管理
* 优化器状态 → 训练状态

它们之间没有关联。

---

## 与 Flash Attention API 的联系

你的代码：

```python
flash_attn_with_kvcache(
    q,
    k_cache,
    v_cache,
    k,
    v
)
```

注意：

```python
q
```

是直接传递的：

```
q = 当前 token 的查询
```

而：

```python
k_cache
v_cache
```

是持久化的。

API 设计本身反映了数学原理：

```
新 Q
 +
旧 K,V 记忆
 =
下一个 token 的注意力
```

因此 **KV 缓存在数学上是正确的名称**。"QKV 缓存"会暗示存储旧的查询，但在自回归解码过程中，旧的查询没有未来用途。