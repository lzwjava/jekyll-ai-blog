---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skype’s Hybrid P2P Architecture Explained
translated: false
type: note
---

**Question: What is Skype's P2P architecture?**

**Answer:**

Skype originally used a **hybrid peer-to-peer (P2P) architecture** when it launched in 2003, pioneered by its founders (who previously created the Kazaa P2P file-sharing network). This design made Skype stand out from traditional VoIP services by minimizing reliance on centralized servers, reducing costs, and enabling better NAT/firewall traversal for voice, video calls, and file transfers.

Key elements of Skype's original P2P architecture included:

- **Ordinary nodes (clients)**: Regular user devices running the Skype app. These handled direct connections when possible.
- **Supernodes (SNs)**: Powerful clients (with public IP addresses, sufficient bandwidth, CPU, and RAM) that volunteered or were selected to act as temporary servers. Supernodes formed a distributed overlay network and performed critical functions:
  - Maintained a distributed directory (user location and buddy list info) across the network.
  - Helped with login, search, and discovery (no single central server held all user data).
  - Acted as relays for NAT traversal when direct P2P connections failed (e.g., due to symmetric NAT or firewalls). Media streams (voice/video) preferred direct peer-to-peer but fell back to relayed paths via supernodes or other nodes.
- **Login servers, update servers, and buddy-list servers**: A small set of centralized servers handled initial authentication, software updates, and some buddy list synchronization, but most operations were decentralized.

This hybrid model allowed:
- Direct media transfer between peers for low latency and reduced bandwidth costs on Skype's side.
- Efficient traversal of NATs and firewalls (better than many SIP-based systems at the time).
- Scalability without massive server infrastructure.

The architecture was proprietary and somewhat opaque (reverse-engineered in early papers like the 2004 analysis of the Skype protocol).

After Microsoft acquired Skype in 2011:
- The P2P system was gradually phased out for reliability, scalability, easier management, and integration reasons.
- In 2012, user-hosted supernodes were replaced with Microsoft-hosted ones.
- By around 2017, Skype fully transitioned to a centralized, cloud-based architecture on Microsoft Azure (server-relay model for calls, similar to most modern apps).
- The original P2P protocol and supernode system were deprecated.

Note: As of 2025, Skype itself was retired by Microsoft on May 5, 2025, with users directed to Microsoft Teams (which uses centralized infrastructure). The legacy of Skype's P2P approach influenced technologies like WebRTC (used in many modern video apps for direct connections where possible).

In summary, Skype's famous P2P architecture was innovative for its time (2003–~2010s) but was replaced by centralized servers under Microsoft to address stability, mobile support, and operational challenges — similar to why apps like WeChat avoided P2P from the start.

**References:**

- [Skype protocol - Wikipedia](https://en.wikipedia.org/wiki/Skype_protocol)
- [Skype - Wikipedia (history and architecture changes)](https://en.wikipedia.org/wiki/Skype)
- [The Centralization of Skype - Matt Rickard](https://mattrickard.com/the-centralization-of-skype)
- [An Analysis of the Skype Peer-to-Peer Internet Telephony Protocol (2004 paper)](https://arxiv.org/pdf/cs/0412017v1.pdf)
- [ISO Consensus Paper: Skype (UT Austin)](https://security.utexas.edu/consensus/skype)