---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 马克·肯普夫发明以太网桥
translated: true
type: note
---

问题：Mark Kempf 的生平是怎样的？作为 Ethernet 网桥的作者/发明者，他是如何参与到网络领域的？

回答：

Mark Kempf 是一名网络工程师，最著名的是他在 1983 年在数字设备公司 (DEC) 工作期间发明了第一个 Ethernet MAC bridge（也称为 learning bridge 或 Layer 2 switch）。

1983 年，工程师 Alan Kirby 向 Kempf 提出一个想法，即通过使用存储转发交换来连接独立的 Ethernet 网段，从而消除 Ethernet 中的共享介质限制。Kempf 是 DEC 网络高级开发组的首席工程师，第二天就迅速开发出了“learning bridge”的概念。这个设备能够自动学习 MAC 地址，并且只将数据包转发到相关的网段，显著提高了传统共享 Ethernet（在大型网络中会遭遇冲突）的性能和可扩展性。

结果就是 LANBridge 100，DEC 的第一个商用双端口 Ethernet 网桥产品，不久后推出。这项创新通过允许更大、分段的网络而无需完整的路由开销，帮助 Ethernet 击败了 Token Ring 和 FDDI 等竞争对手。Kempf 拥有与这项技术相关的专利，DEC 免版税许可了 MAC bridge 专利，从而实现了 IEEE 标准化和其他供应商（例如 Kalpana 的多端口交换机）的广泛采用。

Kempf 还为 DEC 的其他网络进步做出了贡献，包括终端服务器、主机安全软件、光网络以及 GigaSwitch 等高性能交换机。他后来在 Raptor、Okena、Cisco 和 BitSight Technologies 等公司担任高管职务（例如工程副总裁）。他是近 20 项网络和安全专利的共同发明人，技术论文和书籍章节的共同作者，并继续进行研究和咨询，包括与麻省理工学院的合作。

除了他在 20 世纪 80 年代到 90 年代在 DEC 的职业成就之外，关于他的早年生活、教育或个人细节的公开信息很少。

注意：有多个名为 Mark Kempf 的人（例如，一名退役的美国海军上尉在国防科技领域，另一些在金融或软件领域），但与 Ethernet 网桥相关联的是 DEC 工程师。

参考文献：

- [IEEE Spectrum: How DEC Engineers Saved Ethernet](https://spectrum.ieee.org/how-dec-engineers-saved-ethernet)
- [Hackaday: How DEC’s LANBridge 100 Gave Ethernet A Fighting Chance](https://hackaday.com/2024/04/09/how-decs-lanbridge-100-gave-ethernet-a-fighting-chance/)
- [Packet Pushers Podcast: History of Networking: How Bridging Saved Ethernet](https://packetpushers.net/podcasts/heavy-networking/hn741-history-of-networking-how-bridging-saved-ethernet/)
- [Wikiwand: Network Switch (citing invention)](https://www.wikiwand.com/en/Network_switch)
