---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 非对称密码学的主要特征
translated: true
type: note
---

**问题：** 非对称密钥密码学的主要特征是什么？

**答案：**

非对称密钥密码学（也称为公钥密码学）具有以下主要特征：

**1. 加密与解密密钥不同**
加密密钥和解密密钥不同，且从一个密钥推导出另一个密钥在计算上不可行。

**2. 密钥对**
每次生成密钥时，都会产生一对不同的密钥：

- **公钥** — 用于加密，公开发布并与任何人共享
- **私钥** — 用于解密，由所有者严格保密

**3. 算法公开**
加密算法和解密算法均为公开已知；安全性依赖于推导私钥的数学难度，而非算法的保密性。

**4. 简化的密钥管理（主要优势）**
由于加密密钥可以自由分发，用户只需保护自己的私钥。与对称系统相比，这极大地简化了密钥分发和管理——对称系统需要事先安全地交换共享密钥。

---

**参考来源：**

- [公钥密码学 — 维基百科](https://en.wikipedia.org/wiki/Public-key_cryptography)
- [非对称加密 — Cloudflare 学习中心](https://www.cloudflare.com/learning/ssl/what-is-asymmetric-encryption/)
