---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 以太网不适用于城域网
translated: true
type: note
---

Question: 下列哪种网络技术不能用于 Metropolitan Area Network (MAN)？

A. FDDI
B. Ethernet
C. DQDB
D. ISDN

Answer:

正确答案是 **B. Ethernet**。

**Explanation:**

- **FDDI (Fiber Distributed Data Interface)**：一种高速 Token-Ring 网络技术（100 Mbit/s），专为 Metropolitan Area Network 和校园骨干网设计。在 20 世纪 90 年代和 21 世纪初，它常被用于 MAN。→ **可用于 MAN**。

- **Ethernet**：传统的 Ethernet 标准（10 Mbps, 100 Mbps，甚至早期的 Gigabit Ethernet）具有显著的距离限制（通常为数百米）。它们主要为 **LAN** 设计。虽然现代 Metro Ethernet（基于 Carrier Ethernet 标准，如 IEEE 802.1Qay, 802.1ah, MPLS-TP 等）现在可以用于 MAN，但本题指的可能是 **Classic Ethernet**（如许多旧教材中所述），它**不能**覆盖真正 Metropolitan Area Network 所需的距离和规模。→ **不能用于 MAN**（在本题语境下）。

- **DQDB (Distributed Queue Dual Bus)**：这是 IEEE 802.6 标准中定义的技术，专门为 **Metropolitan Area Network** (MAN) 设计。它是最早的标准化 MAN 技术之一。→ **可用于 MAN**。

- **ISDN (Integrated Services Digital Network)**：虽然 ISDN 主要是广域接入技术（用于通过电话网络连接站点），但它有时也被用于提供跨城市/地区的连接，特别是在宽带普及之前。一些教材将其分类为在特定应用场景下可用于 MAN。→ **可用于 MAN**（在本题语境下）。

**Conclusion**：在这一考题的语境下（通常遵循较旧的中文网络教材），传统的 **Ethernet** 因距离和拓扑限制被认为不适用于 MAN，而其他三种技术要么是为 MAN 设计的，要么在实际中被用于城市规模的网络。

因此，正确选项是 **B. Ethernet**。

References:

- 无（本题基于许多中文 IT 认证材料中标准网络教材的分类）
