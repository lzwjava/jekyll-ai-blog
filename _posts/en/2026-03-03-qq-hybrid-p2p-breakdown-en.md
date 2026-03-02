---
audio: false
generated: true
image: false
lang: en
layout: post
title: QQ Hybrid P2P Communication Breakdown
translated: false
type: note
---

Question: How does QQ use P2P technology to communicate?

Answer: 

QQ (Tencent's instant messaging application) employs a **hybrid architecture** that combines centralized servers with **P2P (peer-to-peer)** connections. It does not use pure P2P for all communication but selectively applies P2P to reduce server load, lower latency, and save bandwidth, especially for media-heavy features.

### Main Scenarios Where QQ Uses P2P

- **Video calls and audio calls**  
  QQ adopts a classic VoIP-style design:  
  - Call setup and signaling (invitation, negotiation of parameters, session establishment) always go through Tencent's servers.  
  - Once the session is established and codec/parameter agreement is reached, the actual **audio/video media stream** is transmitted directly between the two clients using P2P whenever possible.  
  This significantly reduces server bandwidth consumption for real-time media.

- **File transfer (especially between online friends)**  
  When both users are online, QQ attempts to establish a direct P2P connection for transferring files.  
  - If successful → data flows directly between the two clients (faster and saves server traffic).  
  - If it fails (strict NAT/firewall, incompatible network environments) → falls back to relay through Tencent servers.

- **Text messages**  
  Text messages usually travel through Tencent servers rather than pure P2P, especially:  
  - When the recipient is offline (messages are stored on the server).  
  - In many everyday scenarios (historical behavior of QQ clients).  
  However, when both parties are online and under favorable network conditions, some implementations may send small messages directly via P2P.

### How QQ Achieves P2P Connectivity (NAT Traversal)

Most users are behind NAT routers, so QQ must solve the NAT traversal problem to enable direct connections. It uses techniques very similar to those in Skype, WebRTC, etc.:

1. **Both clients periodically maintain UDP connections** to QQ login servers (commonly on ports 8000/8001). This creates NAT mappings.
2. **Discovery phase**  
   - Each client learns its own public IP:port (via QQ servers acting like STUN servers).  
   - When user A wants to call/user B or send a large file, A asks the server for B's public IP:port mapping(s).
3. **Hole punching (P2P打洞)**  
   - Both clients simultaneously send UDP packets to each other's predicted public IP:port.  
   - This "punches holes" in their respective NAT devices.  
   - After a short time, the NAT mappings allow incoming packets from the peer, establishing a direct UDP channel.
4. **Fallback relay**  
   If hole punching fails (e.g., symmetric NAT on one or both sides), media/data is relayed through Tencent's high-bandwidth servers.

QQ primarily uses **UDP** for media P2P channels (better for real-time and hole punching), but can fall back to **TCP** in difficult network environments.

### Summary of QQ's P2P Strategy

| Feature              | Signaling / Control | Media / Data Transfer       | Primary Method          |
|----------------------|---------------------|-----------------------------|-------------------------|
| Text chat            | Server              | Usually server, sometimes P2P | Server → hybrid        |
| Voice/video call     | Server              | P2P when possible           | Hybrid (P2P preferred) |
| File transfer (online) | Server            | P2P when possible           | Hybrid (P2P preferred) |
| NAT traversal        | —                   | UDP hole punching + relay   | STUN-like + relay      |

In short, QQ uses P2P mainly for **high-bandwidth real-time media** (video/voice) and **large file transfers** between online users, while relying on servers for signaling, offline messages, and fallback when direct P2P cannot be established.

References:  

- [The Mechanism of Tencent QQ Video Communication](https://www.researchgate.net/publication/266643063_The_Mechanism_of_Tencent_QQ_Video_Communication)
- [Forensic Analysis of Popular Chinese Internet Applications](https://opendl.ifip-tc6.org/db/conf/ifip11-9/df2010/YangCHWCCC10.pdf)
- [QQ通信原理及QQ是怎么穿透内网进行通信的？](https://blog.csdn.net/tanqiuwei/article/details/27198983)
- [P2P通信原理与实现 - 腾讯云开发者社区](https://cloud.tencent.com/developer/article/2215777)