---
audio: false
generated: true
image: false
lang: en
layout: post
title: Retake Strategy for Network Exam
translated: false
type: note
---

**Question:** Give me a course guideline for 02141 Computer Network Technology (自考, Guangdong), which I'm retaking after scoring 23/100 in April 2026.

**Answer:**

First, the diagnosis. A 23 from someone with 12 years of engineering experience isn't a knowledge problem — you know more about real networks than this exam will ever test. It's a *format mismatch* problem. 自考 papers grade you on reproducing the textbook's exact Chinese terminology and chapter structure. Knowing how TCP actually behaves in production earns you zero points if you can't write 建立连接采用三次握手：SYN、SYN+ACK、ACK in the expected phrasing. So this guideline is about exam-game optimization, not learning networking.

## Course basics

Course 02141 uses the textbook 《计算机网络技术》, edited by 张海霞, 机械工业出版社, 2016 edition, which is the Guangdong Education Examination Authority's designated version. Closed-book written exam, 150 minutes, 100 points, 60 to pass. Typical paper structure across recent years: single-choice (~20×1), fill-in-the-blank (~10–15×1), short answer (简答, ~5×5–6), and application/calculation questions (综合应用, ~2×10) covering things like subnetting, CRC, or sliding window.

## Chapter map (张海霞 2016 edition)

1. **网络概述** — definitions, classification (LAN/MAN/WAN), topologies, network history. Pure memorization; heavy in 选择/填空.
2. **数据通信基础** — this is the exam's favorite chapter and probably where you bled points. Analog vs digital, baud rate vs bit rate (奈奎斯特/香农 formulas), encoding (NRZ, Manchester, 差分曼彻斯特), synchronization (异步/同步 — "what is synchronization, the two transmission sync methods, and pros/cons of each" is a literal past short-answer question), multiplexing (FDM/TDM/WDM/CDMA), switching (电路/报文/分组交换), error control (parity, CRC computation by hand).
3. **网络体系结构** — OSI 7层 vs TCP/IP 4层, what each layer does, in the textbook's exact wording. Guaranteed short-answer territory.
4. **局域网技术** — Ethernet, CSMA/CD (must be able to state the 先听后发、边听边发、冲突停发、随机延迟后重发 procedure), MAC addressing, VLANs, WLAN/802.11.
5. **网络互联** — IP addressing, classes A/B/C, subnet masks, CIDR, subnetting calculations (the big application question — practice dividing a /24 into N subnets by hand), routers/switches/gateways, ARP, ICMP.
6. **传输层与应用层** — TCP vs UDP, three-way handshake, port numbers, DNS, HTTP, FTP, SMTP/POP3, DHCP.
7. **网络安全与管理** — firewalls, encryption basics (对称/非对称), digital signatures, SNMP.

Weight roughly: ch.2 + ch.5 ≈ 45% of the paper; ch.3 + ch.4 ≈ 30%; the rest fills in.

## Study plan for the October 2026 sitting (~4 months)

Given your background, invert the normal order — past papers first, textbook second:

**Weeks 1–2: calibrate against real papers.** Download 5–8 sets of 真题 with answers (zikaosw.cn and hbzkjy.com host years from 2009–2023). Do one cold, grade it honestly. You'll find the gap is terminology recall, not concepts. Build an Anki deck (or a flat text file + a small spaced-repetition script — more your style) of every 名词解释 and 填空 answer phrased *exactly as the textbook phrases it, in Chinese*. This is the one course where your "English only" preference works against you: the answer sheet is graded in Chinese, so memorize the Chinese terms (报文交换, 差错控制, 信道复用) even though you think in English.

**Weeks 3–8: chapter passes, exam-first.** For each chapter: skim the textbook section, then immediately do every past-paper question tagged to that chapter. The 串讲小册子 bundled with the 自考通试卷 is genuinely the highest-ROI purchase here — it's a compressed list of exactly the testable sentences.

**Weeks 9–12: drill the two computation archetypes** until they're mechanical, ~15 minutes for both on exam day:
- Subnetting: given 192.168.10.0/24, split into 6 subnets → borrow 3 bits, mask 255.255.255.224, list network/broadcast/usable ranges.
- CRC: given message bits and generator polynomial, do the XOR long division by hand. Also Nyquist/Shannon plug-and-chug: C = 2H·log₂N and C = H·log₂(1+S/N).

**Final 2 weeks: closed-loop simulation.** Two full timed papers per week, handwritten in Chinese. Target ≥75 in simulation to bank margin for grading strictness.

**Tactical scoring math:** 20 choice + 12 fill-in gets you to 32 on recall alone; nail both application questions (+20) and you're at 52; you only need ~2 of 5 short answers to clear 60. Prioritize accordingly — short answers are the most expensive points to earn, so they're the buffer, not the foundation.

One AI-native tip that fits your workflow: feed the 真题 PDFs through an LLM pipeline to extract every Q/A pair into a JSONL drill set, then build a 20-line CLI quizzer (`zz`-style) that hits you with random 填空 in Chinese. You'll cover 10 years of papers in a fraction of the manual time.

**References:**

- [02141 计算机网络技术 考试资料/历年真题汇总 — 自考生网](https://www.zikaosw.cn/zkkm/791.html)
- [2022年广东自考《计算机网络技术02141》指定教材（机械工业出版社 张海霞 2016）](https://www.edu-edu.com/zikao/guangdong/jcdg/44629.html)
- [02141 历年真题下载 — 湖北自考网](http://www.hbzkjy.com/course/02141/)
- [02141 全套精讲+串讲视频 — bilibili](https://www.bilibili.com/video/BV1bV411s7pS/)
