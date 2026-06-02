---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 逆向网络观点辩论
translated: true
type: note
---

问题：关于交换和路由技术有哪些不受欢迎的观点？

回答：

以下是网络社区中一些真正不受欢迎（或至少是逆向）的观点，它们通常会在 Reddit、思科论坛和厂商会议上引发激烈辩论：

- **厂商认证（尤其是 CCIE）对工程师来说大多是一种税，并且与实际技能不再相关。**
  许多自学成才或不依赖于特定厂商的工程师，他们运行着大型网络（云提供商、对冲基金、超大规模公司），其表现优于那些一辈子只接触 IOS/XE 的 CCIE。

- **SDN 被过分推销，并且在企业中大部分都失败了。**
  除了非常大的云提供商和少数小众电信用途之外，大多数“SDN”部署都只是集中管理+传统的分布式控制平面加上一个花哨的叠加层（ACI、NSX 等）。真正的 OpenFlow 风格 SDN 实际上已经消亡。

- **EVPN/VXLAN 对于 95% 的企业园区来说过于复杂。**
  一个设计良好的 Layer-3-to-the-access 模型，使用 OSPF/BGP 和传统的 802.1Q trunks，比仅仅因为“它是未来”就在到处运行 EVPN 更简单、更确定且更便宜。

- **白盒交换机 + 商业芯片（Broadcom Tomahawk/Jericho）已经获胜，而传统厂商只是在转售相同的芯片，并收取高昂的 NOS 税。**
  Cisco、Arista 和 Juniper 都运行在相同的 Broadcom/Intel/Marvell 芯片上。你为 Catalyst/NCS/QFX 支付的溢价主要是品牌和支持服务的门面。

- **IPv6 采用率在 25 年后仍然很低，因为大多数网络工程师都秘密地不想学习它。**
  NAT + 私有地址“就是好用”，并给人一种虚假的安全感。大多数 IPv6 部署都是半心半意的“双栈”，所有重要的事情仍然依赖于 IPv4。

- **TRILL、SPB 和 FabricPath 是比 VXLAN/EVPN 更好的想法，但因营销而非技术原因而失败了。**
  它们提供了真正的 Layer-2 多路径功能，而无需封装税和控制器依赖，但由于云的炒作，业界全力投入了 VXLAN。

- **组播（Multicast）正在消亡，不值得我们仍然投入的复杂性。**
  除了 IPTV 和金融领域，几乎没有人再需要 PIM。应用层组播（BitTorrent 风格）或任播 + 单播复制已经足够。

- **网络自动化未能实现承诺的 10 倍生产力提升，因为大多数团队在与 YAML 和 Jinja2 作斗争上花费的时间比他们使用 CLI 更多。**
  糟糕的抽象和不断的 Schema 变化（说的就是你，思科不断变化的 YANG 模型）使“基础设施即代码”成为一场噩梦。

- **Leaf-spine（Clos）拓扑结构经常在不理解流量矩阵的情况下被盲目崇拜。**
  许多组织部署了 3:1 过度订阅的 Leaf-spine 结构，而对于它们的 East-West 轻型工作负载来说，简单的两层设计会更便宜，性能也更好。

- **在 2025 年，硬件路由（ASIC）不再比软件路由好得多。**
  现代 x86/ARM 服务器结合 DPDK、VPP 或 eBPF/XDP，在考虑到许可和支持费用后，可以以比商业芯片交换机更低的成本实现每盒 100-400 Gbps 的路由吞吐量。

这些观点往往不受传统企业工程师、厂商 SE 和认证狂热者的欢迎，但在云原生、Web 规模和底层 Linux 网络圈子里却越来越被接受。

参考文献：

- [Reddit r/networking “你的网络死守阵地是什么？”帖子（多年）](https://www.reddit.com/r/networking/search/?q=hill%20to%20die%20on)
- [NANOG 邮件列表档案中关于 SDN/EVPN 的辩论](https://www.nanog.org/mailing-list/archives/)
- [Ivan Pepelnjak 关于 EVPN 复杂性的博客文章](https://blog.ipspace.net/tag/evpn/)
- [DPDK 和 FD.io 性能声明](https://www.fd.io/) / [eBPF/XDP 路由基准测试](https://cilium.io/blog/2023/03/21/ebpf-xdp-performance/)
