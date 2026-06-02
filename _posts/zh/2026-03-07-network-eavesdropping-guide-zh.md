---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络窃听详解
translated: true
type: note
---

**问题：** 在典型的网络系统威胁中，__________ 指的是非法拦截网络上传输的敏感信息。

**答案：**

正确答案是 **窃听 (Eavesdropping / Wiretapping)**。

---

## 解释

### 定义

**窃听 (Eavesdropping)** 是一种 **network security threat**，其中未经授权的一方秘密拦截并捕获穿越 **network** 传输的敏感数据。在 **cybersecurity** 中，**eavesdropping attack** 是一种恶意尝试，未经授权拦截并访问 **network** 上传输的数据，涉及 **cyber criminals** 秘密监控 **network traffic** 并捕获敏感信息，如 **login credentials**、**financial data** 或 **proprietary business intelligence**。

---

### **Eavesdropping (窃听)** 的关键特征

1. **被动与隐蔽性质** — 与其他形式的 **cyber attacks** 不同，听取设备或 **bug** 的存在可能不会对设备和 **network** 的性能产生不利影响，从而使其极难检测。

2. **目标：传输中的数据** — **Network eavesdropping** 发生在恶意行为者利用不安全或易受攻击的 **network** 来读取或窃取两个设备之间传输的数据时。

3. **利用不安全通道** — **Eavesdropping** 通常发生在用户连接到流量未加密或未保护的 **network** 并向同事发送敏感业务数据时。

---

### 常见窃听技术

| Technique | Description |
|---|---|
| **Packet Sniffing** | 捕获并读取穿越 **network** 的数据包 |
| **Wiretapping** | 物理或数字方式窃听通信线路 |
| **Man-in-the-Middle (MitM)** | 攻击者定位于发送方和接收方之间 |
| **Wi-Fi Eavesdropping** | 利用不安全的公共无线 **network** |

**Packet sniffing** 使用称为分析器的工具来拦截并捕获数据包。**Sniffers** 可以揭示用户访问的网站、数据包源和目的地，或电子邮件内容。

---

### 与其他网络威胁的区别

在典型的 **network threats** 背景下，重要的是将 **窃听** 与类似概念区分开来：

| Threat | Chinese Term | Description |
|---|---|---|
| **Eavesdropping** | 窃听 | 非法**拦截**传输中的数据 |
| **Tampering** | 篡改 | 修改传输中的数据 |
| **Spoofing** | 欺骗/伪装 | 冒充合法用户或系统 |
| **Denial of Service** | 拒绝服务 | 破坏服务的可用性 |
| **Repudiation** | 抵赖 | 否认已发送或接收数据 |

**窃听** 特别关注信息的**未经授权获取** — 数据被读取/复制，但通常**未被更改**，使其成为一种被动攻击。

---

### 预防方法

为了防止窃听，组织应首先对电子邮件、**network** 和通信进行加密，以及静态数据、使用中数据和传输中数据 — 这样，即使数据被拦截，黑客也无法在没有加密密钥的情况下解密它。

其他关键预防措施包括：

- 使用 **VPN** 进行安全隧道传输
- 避免公共/不安全的 **Wi-Fi network**
- 部署入侵检测系统 (**IDS**)
- **Network segmentation**
- 强认证机制

---

### 总结

> **窃听 (Eavesdropping)** = 非法拦截并获取网络上传输的敏感信息，而沟通各方不知情或未同意。这是一种专注于**机密性破坏**的**被动攻击**。

**参考文献：**

- [Fortinet: What Are Eavesdropping Attacks?](https://www.fortinet.com/resources/cyberglossary/eavesdropping)
- [Wikipedia: Network Eavesdropping](https://en.wikipedia.org/wiki/Network_eavesdropping)
- [Proofpoint: What Is an Eavesdropping Attack?](https://www.proofpoint.com/us/threat-reference/eavesdropping)
- [TechTarget: How to Prevent Network Eavesdropping Attacks](https://www.techtarget.com/searchsecurity/answer/How-to-prevent-network-sniffing-and-eavesdropping)
- [NordLayer: What Is Eavesdropping?](https://nordlayer.com/learn/threats/eavesdropping/)
