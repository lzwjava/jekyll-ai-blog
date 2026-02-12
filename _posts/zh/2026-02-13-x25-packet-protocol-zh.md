---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: X.25 分组交换协议详解
translated: true
type: note
---

Question: What is X.25?

Answer: 

**X.25** 是一个由 **ITU-T 标准** 定义的协议套件（最初由 CCITT 开发），用于 **packet-switched data communication networks**。它是 20 世纪 70 年代末到 90 年代主流的宽带广域网协议，至今在某些特定领域仍有应用。

X.25 为公共数据网络（PDNs）上的可靠、面向连接的 packet switching 定义了完整的 **three-layer protocol stack**：

1. **Physical layer**  
   - 基于 X.21、X.21bis (兼容 V.24/RS-232) 或其他接口  
   - 规定了 DTE–DCE 连接的电气和机械特性

2. **Link layer** (Layer 2)  
   - **LAPB** (Link Access Procedure Balanced)  
   - 一种基于比特的 HDLC 衍生协议  
   - 通过编号、acknowledgments、retransmissions 和 error checking，在 DTE 和 DCE 之间提供可靠、无差错、按序列的 frame 传输

3. **Packet layer** (Layer 3)  
   - X.25 的核心  
   - 提供 **virtual circuit** 服务（包括交换虚拟电路 SVCs 和永久虚拟电路 PVCs）  
   - 主要功能：  
     - Call setup / call clearing  
     - 带有 sequencing 和 flow control 的数据传输  
     - 在单个物理链路上复用多个 logical channels  
     - 端到端的 error recovery 和 flow control (windowing)  
     - Packet 大小通常为 128, 256, 512, 或 1024 bytes (可协商)  
   - 使用 modulo-8 或 modulo-128 序列编号

**X.25 的主要特点：**

- **Connection-oriented** — 在数据传输前需要建立呼叫  
- **Reliable** — 保证按序、无差错交付（link layer 和 packet layer 共同保障）  
- **Slow** — 每一跳都有大量的 acknowledgments 和 retransmissions 开销  
- **在劣质线路上具有高可靠性** — 专为 20 世纪 70-80 年代多噪声的模拟线路设计  
- **Low throughput** — 典型速度为 9.6 kbit/s 至 64 kbit/s（极少更高）  
- **Expensive** — 在大多数公共网络中按 packet 数量和通话时长计费

**主要相关的 ITU-T 建议书 (X-series)：**

- X.25 — 运行在 packet mode 的终端在 DTE 和 DCE 之间的接口  
- X.3 — PAD 参数  
- X.28 — DTE–PAD 接口（异步终端到 PAD）  
- X.29 — PAD–host 通信协议  
- X.121 — 公共数据网络的国际编号计划  
- X.75 — packet-switched 网络之间的互联

**历史背景与衰落：**

- 在 20 世纪 80 年代至 90 年代初，广泛应用于金融交易（ATM、信用卡终端）、航空预订系统以及许多国家的早期互联网访问  
- 90 年代中期开始逐渐被以下技术取代：  
  - Frame Relay（开销更低，速度更高）  
  - ATM  
  - IP / MPLS / 基于 Internet 的 VPNs  
- 仍存在于某些遗留系统（如特定银行网络、SCADA、空中交通管制备份以及部分国家的公共 X.25 网络）

总结：  
X.25 是第一个被广泛部署的**分组交换国际标准**，在固有的不可靠线路上提供可靠的 virtual circuits，但由于其沉重的协议开销，使其在现代高速网络中显得效率低下。

References:  

- None (standard ITU-T X.25 recommendation and historical networking knowledge)