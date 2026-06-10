---
audio: false
generated: true
image: false
lang: en
layout: post
title: Real Exam Questions 02141 Sample
translated: false
type: note
---

**Question:** Show me real exam questions from recent 02141 papers (applicable to the Guangdong April 2026 sitting).

**Answer:**

I pulled the April 2025 national paper (the most recent published set — papers with the same course code are usable across provinces). Below is a representative sample, translated to English with the correct answer and a one-line reason for each, so it doubles as drill material. The full original Chinese paper with answer links is at the source.

## Section 1 — Single choice (单选, 1 pt each)

These are real questions from the 2025-04 paper, paraphrased into English:

1. **In asynchronous transmission, the unit of data sent is:** byte / character / word / field → **Character (字符)**. Async framing wraps each character with start/stop bits — this is the textbook ch.2 definition.
2. **RS-232 is a typical protocol of which layer?** → **Physical layer**. It specifies voltages, pins, connectors — mechanical/electrical characteristics = physical layer.
3. **Which option lists only internet-layer (网络互连层) protocols?** → **IP, ICMP, IGMP** together (the distractors smuggle in UDP/TCP/FTP, which are transport/application layer). Train yourself to layer-classify every protocol acronym instantly.
4. **In the LAN reference model, everything related to attaching to different transmission media lives in:** → **the MAC sublayer**. LLC is media-independent; MAC is media-dependent. Classic 802 model question.
5. **The topology of traditional (classic coax) Ethernet is:** → **Bus (总线型)**. "Traditional" is the trap word — modern switched Ethernet is star, but the textbook's 传统以太网 means 10BASE-2/5.
6. **The VLAN standard is:** → **IEEE 802.1Q**. Distractors are 802.1D (STP), 802.1p (priority), 802.1s (MSTP). Pure memorization.
7. **CSMA/CD in traditional Ethernet aims to avoid:** → **Collisions (冲突)**. The CD literally stands for collision detection.
8. **A routing table's basic structure contains destination network, next hop, interface, and:** → **Subnet mask**. Needed to do the longest-prefix match.
9. **With symmetric encryption among n users where each pair shares a key, total keys needed:** → **n(n−1)/2**. It's just C(n,2) — and the follow-up they love: public-key crypto reduces this to 2n keys (n key pairs).
10. **Common Internet security protocols are:** → **IPsec, SSL, TLS** (distractor sets mix in IGMP/ICMP/TTL, which aren't security protocols at all).

## Section 2 — Fill in the blank (填空, 1 pt each)

Real 2025-04 items, translated. You must produce the exact Chinese term:

11. The metric for the amount of data passing through a network per unit time → **吞吐量 (throughput)**.
12. Adjacent layers in a layered architecture exchange data through → **接口/服务访问点 (interface / SAP)**.
13. The application-layer protocol of the WWW service → **HTTP**.
14. The connectionless transport-layer protocol in TCP/IP → **UDP**.
15. A transport-layer port number is a binary integer of → **16** bits.

## Sections 3–4 — Short answer & application (from adjacent years' papers)

The back half of papers recycles heavily. Verified recurring examples:

- Explain synchronization in a communication system; name the two synchronization methods used in data transmission and give the pros and cons of each (异步: simple/cheap but ~20–30% overhead from start/stop bits; 同步: efficient for large blocks but needs clock recovery and more complex hardware).
- Compare circuit switching, message switching, and packet switching (3-way comparison table is the expected answer shape).
- State the CSMA/CD working procedure (the four-phrase Chinese mnemonic: 先听后发，边听边发，冲突停发，随机延迟后重发).
- List the OSI seven layers in order and state the main function of each.
- Application question archetype: given a class C network like 192.168.1.0/24, divide into N subnets — write the mask, each subnet's network address, broadcast address, and usable host range.
- Application question archetype: CRC — given a bit string and generator polynomial, compute the transmitted frame by XOR division.

## What this tells you about the 23

Look at the pattern: every single-choice answer above is a one-hop fact lookup, and the fill-ins demand exact Chinese terminology. There's no systems reasoning anywhere — your production networking knowledge literally cannot express itself in this format unless you've loaded the textbook's vocabulary table into memory. The fix is mechanical: scrape the 真题 pages above into a JSONL of (question, answer, chapter) and drill with a tiny CLI quizzer until single-choice + fill-in (~35 pts) is near-perfect, then bank the two application archetypes (~20 pts) — that alone clears 60 before you write a single 简答.

Want me to write that scraper + spaced-repetition drill script (Python, runs on your Air, feeds from these zikaosw pages)?

**References:**

- [2025年4月 自考02141 真题及答案 — 自考生网](https://www.zikaosw.cn/news/27006520.html)
- [02141 历年真题及答案汇总（2007–2025） — 自考生网](https://www.zikaosw.cn/lnzt/subject-791.html)
- [2023年4月 自考02141 真题及答案 — 自考生网](https://www.zikaosw.cn/news/18018883.html)
