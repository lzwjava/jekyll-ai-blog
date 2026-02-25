---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ATM 与 IP 网络对比
translated: true
type: note
---

Question: 比较 ATM 和 IP 网络

Answer:

以下是 **ATM (Asynchronous Transfer Mode)** 和 **IP (Internet Protocol) networks** 的清晰比较：

| 方面                          | ATM (Asynchronous Transfer Mode)                          | IP (Internet Protocol) networks                          |
|-------------------------------|------------------------------------------------------------|----------------------------------------------------------|
| **交换范式**                  | 面向连接（virtual circuits）                               | 无连接（datagram）                                       |
| **基本数据单元**              | 固定大小信元（53 bytes: 5-byte header + 48-byte payload）  | 可变大小数据包（通常 576–1500 bytes，上至 ~64 KB）       |
| **开销**                      | 高（53-byte 信元 ≈10%）                                    | 较低（取决于数据包大小，通常 2–5%）                      |
| **保证 QoS**                  | 原生支持优秀（CBR、VBR-rt、VBR-nrt、ABR、UBR 类）          | 最初无；后通过 IntServ、DiffServ、MPLS 添加               |
| **带宽效率**                  | 差（信元税 + 有效载荷 < 48 bytes 时填充）                  | 好（尤其是大包）                                         |
| **延迟抖动 (jitter)**         | 非常低且可预测                                             | 可变 / 高（取决于拥塞）                                  |
| **典型分组化延迟**            | 非常低（小固定信元）                                       | 较高（尤其是语音/视频的大 MTU）                          |
| **主要部署时代**              | 1990 年代中期 – 2000 年代初（峰值 ~1998–2005）             | 1980 年代 – 至今（~2005 年起主导）                       |
| **主要应用**                  | 电信骨干网、早期宽带接入 (ADSL)、视频、VoATM               | 通用互联网、如今的一切                                    |
| **流量管理**                  | 强大（CAC、UPC、每个 VC 的流量整形、监管）                 | 原生较弱（主要是尽力而为）；依赖上层或 MPLS               |
| **每个有效载荷字节的头部**    | 高（5/53 ≈ 9.4%）                                          | 低（TCP/IP 为 20/1500 ≈ 1.3%，巨型帧更低）               |
| **复用粒度**                  | 非常细（每个接口最多 65,535 个 VC）                        | 粗（取决于 5 元组流）                                    |
| **当前状态 (2025–2026)**      | 运营商网络中几乎完全淘汰                                    | 普遍（IPv4 + IPv6）                                      |
| **替代技术**                  | 主要被 IP/MPLS + Ethernet 取代                             | —（当前主导技术）                                        |
| **典型链路速度 (峰值时代)**   | OC-3 (155 Mbps)、OC-12 (622 Mbps)、OC-48 (2.5 Gbps)        | 1 Gbps → 400 Gbps+（仍在增长）                           |

### 关键总结 – 为什么 ATM 输了，IP 赢了

- **ATM 优势**（1990 年代–2000 年代初）  
  - 实时应用（语音、视频）的优秀 QoS  
  - 非常低的抖动和可预测延迟  
  - 细粒度流量工程和准入控制

- **ATM 劣势**（长期致命）  
  - 高信元税 / 带宽低效  
  - 昂贵硬件（专用 ATM 交换机）  
  - 复杂网络管理  
  - 不适应突发性互联网流量

- **取代 ATM 的 IP/MPLS/Ethernet 优势**  
  - 更好的带宽效率  
  - 廉价硬件（商用 Ethernet + 路由器）  
  - 更简单架构  
  - MPLS 后来提供了 ATM 的大多数流量工程和 QoS 功能  
  - 极好扩展至 100/400/800 Gbps 链路

**结论（2026 年视角）**  
ATM 是一项非常复杂的技术，在保证 QoS 和实时流量方面表现出色——但它最终对突发性、尽力而为主导的互联网流量模型来说太昂贵且太低效。如今，几乎没有生产运营商或企业网络再使用原生 ATM；它已被 IP/MPLS/Ethernet 组合几乎完全取代。

References:  

- None (based on established telecommunications and networking knowledge)