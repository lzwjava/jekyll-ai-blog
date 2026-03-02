---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Skype 的混合 P2P 架构详解
translated: true
type: note
---

**问题：Skype 的 P2P 架构是什么？**

**答案：**

Skype 在 2003 年推出时最初使用了 **hybrid peer-to-peer (P2P) architecture**，这是由其创始人（之前创建了 Kazaa P2P 文件共享网络）开创的设计。这种设计使 Skype 区别于传统的 VoIP 服务，通过最小化对集中式服务器的依赖来降低成本，并实现更好的 NAT/firewall 穿越，用于语音、视频通话和文件传输。

Skype 原始 P2P 架构的关键元素包括：

- **普通节点 (clients)**：运行 Skype 应用的常规用户设备。这些节点在可能时处理直接连接。
- **Supernodes (SNs)**：具有公网 IP 地址、足够带宽、CPU 和 RAM 的强大客户端，自愿或被选为临时服务器。Supernodes 形成了分布式覆盖网络，并执行关键功能：
  - 在网络中维护分布式目录（用户位置和好友列表信息）。
  - 帮助登录、搜索和发现（没有单一中央服务器持有所有用户数据）。
  - 当直接 P2P 连接失败时（例如由于 symmetric NAT 或 firewalls），充当 NAT 穿越的中继。媒体流（语音/视频）优先使用直接 peer-to-peer，但会回退到通过 supernodes 或其他节点的中继路径。
- **Login servers、update servers 和 buddy-list servers**：一小组集中式服务器处理初始认证、软件更新和部分好友列表同步，但大多数操作是去中心化的。

这种混合模型允许：
- 对等节点之间直接媒体传输，实现低延迟并减少 Skype 方的带宽成本。
- 高效穿越 NAT 和 firewalls（当时优于许多基于 SIP 的系统）。
- 无需大规模服务器基础设施即可实现可扩展性。

该架构是专有的且有些不透明（早期论文如 2004 年的 Skype 协议分析通过逆向工程获得）。

Microsoft 在 2011 年收购 Skype 后：
- 出于可靠性、可扩展性、更易管理和集成原因，P2P 系统逐渐被淘汰。
- 2012 年，用户托管的 supernodes 被替换为 Microsoft 托管的 supernodes。
- 到大约 2017 年，Skype 完全过渡到基于 Microsoft Azure 的集中式云架构（通话使用 server-relay 模型，类似于大多数现代应用）。
- 原始 P2P 协议和 supernode 系统被弃用。

注意：截至 2025 年，Microsoft 已于 2025 年 5 月 5 日退役 Skype，并引导用户转向 Microsoft Teams（使用集中式基础设施）。Skype 的 P2P 方法影响了 WebRTC 等技术（许多现代视频应用使用它在可能时实现直接连接）。

总之，Skype 著名的 P2P 架构在其时代（2003–~2010 年代）具有创新性，但 Microsoft 为了解决稳定性、移动支持和运营挑战而用集中式服务器取代它——类似于 WeChat 从一开始就避免使用 P2P 的原因。

**参考文献：**

- [Skype protocol - Wikipedia](https://en.wikipedia.org/wiki/Skype_protocol)
- [Skype - Wikipedia (history and architecture changes)](https://en.wikipedia.org/wiki/Skype)
- [The Centralization of Skype - Matt Rickard](https://mattrickard.com/the-centralization-of-skype)
- [An Analysis of the Skype Peer-to-Peer Internet Telephony Protocol (2004 paper)](https://arxiv.org/pdf/cs/0412017v1.pdf)
- [ISO Consensus Paper: Skype (UT Austin)](https://security.utexas.edu/consensus/skype)