---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 消息摘要中的单向哈希函数
translated: true
type: note
---

问题：**单向哈希函数 (one-way hash function)** 在 **报文摘要算法 (message digest algorithms)** 中是什么意思？

答案：

**单向哈希函数**是一种将任意长度的消息映射为**固定长度摘要**的函数：

```text
消息 M
   │
   ▼
H(M)
   │
   ▼
固定大小的摘要
```

例如 SHA-256：

```text
"hello"
   │
   ▼ SHA-256
2cf24dba5fb0a30e26e83b2ac5b9e29e...
   └── 256 位 = 32 字节
```

### 为什么叫“单向”？

因为：

```text
M ──H──> 摘要
```

在计算上很容易，但：

```text
摘要 ──???──> M
```

在计算上不可行。

**不存在实用的逆函数**：

```python
摘要 = sha256(消息)

# 你不能这样做：
消息 = sha256_inverse(摘要)
```

你只能尝试候选消息：

```python
for candidate in candidates:
    if sha256(candidate) == 摘要:
        print("找到它了")
```

这就是为什么密码系统存储的是类似：

```text
SHA-256(密码)
```

而不是明文密码——尽管在实际密码存储中，应该使用 **Argon2id/bcrypt/scrypt** 而不是原始 SHA-256。

### 加密哈希有什么用途？

通常这些属性很重要：

**1. 确定性**

```text
H("hello") == H("hello")
```

**2. 固定输出大小**

```text
H("a")                 -> 256 位
H("一条很长的消息...") -> 256 位
```

**3. 原像抗性**

给定：

```text
y = H(x)
```

找到一个 `x` 使得 `H(x) = y` 应该是不可行的。

**4. 碰撞抗性**

很难找到：

```text
x != y
```

使得：

```text
H(x) == H(y)
```

### 为什么叫“报文摘要”？

可以把摘要看作消息的**指纹**：

```text
             SHA-256
消息 ─────────────────> 摘要
                            ↓
                         指纹
```

只要一个比特发生变化：

```text
"hello"
   ↓
2cf24dba...

"Hello"
   ↓
185f8db3...
```

摘要就会彻底改变。

这就是为什么报文摘要被用于**数字签名、完整性校验、证书、Git、TLS**等场景。

一个微妙但重要的点是：**“单向”并不意味着数学上不可逆**。它意味着对于设计良好的加密哈希，目前没有已知的计算上可行的方法来恢复原像。
