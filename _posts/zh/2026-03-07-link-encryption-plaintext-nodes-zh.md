---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 链路加密暴露明文节点
translated: true
type: note
---

**问题：** 使用 link encryption 传输信息时，信息在网络的每个中间节点如何存在？

- A. 发送节点为 **Ciphertext**，接收节点为 **plaintext**
- B. 发送节点为 **plaintext**，接收节点为 **Ciphertext**
- C. **Ciphertext**
- D. **Plaintext**

**正确答案：D — Plaintext**

---

**答案：**

## 理解 Link Encryption 和中间节点

### Link Encryption 的工作原理

Link encryption（也称为 **online encryption**）在 **Data Link Layer** 运行——它仅加密相邻节点之间物理传输链路上的数据。其关键特性是：

- 数据在离开一个节点进入线路 **之前** 被加密
- 数据到达下一个中间节点时被 **解密**
- 然后在转发到下一个链路 **之前** 被 **重新加密**

在 link encryption 中，从源到目的地，数据通过许多中间节点。在每个中间节点，消息以 **plaintext** 形式暴露（node encryption 除外）。如果链路上的任何节点安全保护较弱，则根据“最弱一环”原则，整个链路的整体安全性仅与最弱节点一样强。

### 为什么答案是 D (**Plaintext**)，而不是 C (**Ciphertext**)

这是一个细微但关键的区别：

 

| 位置 | 数据状态 |
|---|---|
| 在线路中（节点之间） | **Ciphertext** ✅ |
| **中间节点内部** | **Plaintext** ✅ |

问题是关于信息在**节点上**如何存在——不是在链路上。由于每个节点必须解密以读取路由信息，然后为下一跳重新加密，每个链路段的接收方就是中间节点本身，信息必须在每个节点被解密和重新加密，因此在每个节点内部以 **plaintext** 形式出现。

### 为什么这是安全弱点

这是 link encryption 的**最大漏洞**：每个中间节点都成为潜在的攻击面。攻击者只要攻破任何中间节点，就能完全访问 **plaintext** 数据。

这与以下形成对比：
- **Node encryption**：每个节点使用安全的硬件模块，因此 **plaintext** 永不在可读内存中暴露
- **End-to-end encryption**：数据从发送方一直加密到最终接收方；中间节点仅看到 **ciphertext**

### 为什么选项 C (**Ciphertext**）是常见错误

许多学生混淆了**传输链路**（数据为 **ciphertext**）与**节点本身**（数据必须为 **plaintext** 以进行路由/处理）。问题具体询问在**节点上**的存在方式，因此 **D (Plaintext)** 是正确答案。

---

**参考资料：**

- [链路加密、节点加密与端到端加密对比](https://www.grt-china.com/xinwenzixun/825.html)
- [What is Link Encryption – CyberGhost VPN](https://www.cyberghostvpn.com/glossary/link-encryption)