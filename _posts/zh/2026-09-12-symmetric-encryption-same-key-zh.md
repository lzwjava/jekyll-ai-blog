---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 对称加密：相同密钥
translated: true
type: note
---

问题：**对称加密**是什么意思？

答案：**对称加密 = symmetric encryption**。

其核心思想很简单：

> **使用相同的密钥对数据进行加密和解密。**

```text
明文
   │
   │  加密 + 密钥
   ▼
密文
   │
   │  解密 + 相同密钥
   ▼
明文
```

例如：

```python
key = "my-secret-key"

ciphertext = encrypt("hello", key)
plaintext  = decrypt(ciphertext, key)

assert plaintext == "hello"
```

重要特性如下：

```text
加密(消息, K) → 密文
解密(密文, K) → 消息
```

双方都需要知道`K`。

### 为什么称为"对称"？

因为加密操作在通信双方使用**相同的共享密钥**：

```text
Alice                         Bob
  │                            │
  │      共享密钥 K             │
  ├────────────────────────────┤
  │                            │
  │ 加密(消息, K)              │
  │ ─────── 密文 ──────────>   │
  │                            │
  │              解密(密文, K) │
  │                            │
```

常见的对称加密算法包括**AES**和**ChaCha20**。

其主要问题是**密钥分发**：Alice和Bob最初如何安全地获得相同的密钥？这正是非对称加密（RSA/ECC）存在的原因之一。

一个有用的思维模型：

```text
对称加密   = 一个共享密钥
非对称加密 = 公钥 + 私钥
```

如果你愿意，接下来我可以详细讲解**AES在字节/块级别的工作原理，并展示一次加密轮次中发生的具体过程**。
