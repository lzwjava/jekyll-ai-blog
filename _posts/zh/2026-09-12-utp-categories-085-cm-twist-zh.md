---
audio: false
generated: true
image: false
lang: zh
layout: post
title: UTP类别：0.85厘米绞距
translated: true
type: note
---

问题：**关于UTP的五种类别介绍——以及“0.85厘米”与什么有关？是长度限制吗？**

答案：

如果你指的是经典的**UTP电缆类别**，核心概念如下：

| 类别       | 频率      | 典型以太网              | 最大信道长度 |
| ---------- | --------- | ----------------------- | ----------- |
| **Cat 3**  | 16 MHz    | 10 Mbps                 | 100 m       |
| **Cat 5**  | 100 MHz   | 100 Mbps                | 100 m       |
| **Cat 5e** | 100 MHz   | 1 Gbps                  | 100 m       |
| **Cat 6**  | 250 MHz   | 1 Gbps；10 Gbps（短距） | 100 m       |
| **Cat 6A** | 500 MHz   | 10 Gbps                 | 100 m       |

这里的 **100 m** 是以太网信道的限制；通常由 **90 m 永久链路 + 最多 10 m 跳线**组成。Cat 6 仅支持较短距离的 10 GbE，通常约为 55 m。([Network Startup Resource Center][1])

### 那么 **0.85 cm** 是什么？

**0.85 cm 并非电缆长度限制。**

它指的是旧 Cat 5 术语中铜线对的**绞距**：

> Cat 5：绞距 ≈ **0.6–0.85 cm**。([WashU CSE][2])

可以将一对线想象为：

```text
────╲╱────╲╱────╲╱────╲╱────
      ↑
   绞距（twist pitch）
   ~0.6–0.85 cm
```

导体通过扭绞来减少**串扰/电磁干扰**。不同类别采用不同的几何结构和更严格的性能要求，从而支持更高的信号频率。

因此不要混淆：

```text
0.85 cm  → 绞距 / 扭绞长度
100 m    → 以太网最大信道长度
100 MHz  → Cat 5 带宽/频率等级
```

此外，**UTP** 本身代表**非屏蔽双绞线**（Unshielded Twisted Pair）。“Cat 5 / 5e / 6 / 6A”描述**性能类别**，而 UTP 描述**屏蔽结构**。([TME][3])

如果你所说的 **“5 类 UTP”**特指 **Cat 5**，而非“五种 UTP 类别”，那么 0.85 cm 这个数字几乎可以肯定就是你看到的**绞距**。([WashU CSE][2])

参考文献：

* [Washington University UTP lecture notes](https://www.cse.wustl.edu/~jain/cse473-22/ftp/i_1cni.pdf?utm_source=chatgpt.com)
* [NSRC Layer 1 Cabling Standards](https://nsrc.org/activities/agendas/en/cndo/networking/cndo/en/presentations/Layer1-Cabling-Standards.pdf?utm_source=chatgpt.com)
* [Eaton Ethernet cable length guide](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/network-connectivity/ethernet-cables-explained.html?utm_source=chatgpt.com)

[1]: https://nsrc.org/activities/agendas/en/cndo/networking/cndo/en/presentations/Layer1-Cabling-Standards.pdf?utm_source=chatgpt.com "Slide 1"
[2]: https://www.cse.wustl.edu/~jain/cse473-22/ftp/i_1cni.pdf?utm_source=chatgpt.com "Student Questions"
[3]: https://www.tme.com/us/en-us/news/library-articles/page/78420/how-to-choose-the-length-and-type-of-network-cable-cat5e-cat6-cat6a-cat7-differences-and-applications/?utm_source=chatgpt.com "How to choose the length and type of network cable? CAT5e, CAT6, CAT6A, CAT7 – differences and applications | TME US"
