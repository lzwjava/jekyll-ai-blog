---
audio: false
generated: true
image: false
lang: en
layout: post
title: Packet Switching Technologies Compared
translated: false
type: note
---

Question: Frame Relay is a data communication technology developed after X.25. From a principle perspective, Frame Relay, X.25, and ATM all belong to the same category of switching technology. Which of the following is correct?
A. Circuit switching
B. Packet switching
C. Message switching
D. Cell switching

Your answer: D
Correct answer: B

Answer:

The correct answer is **B. Packet switching** (分组交换).

**Detailed explanation:**

- **X.25**: This is a classic **packet-switched** network protocol (packet switching), widely used in the 1970s–1990s. It performs hop-by-hop error checking and retransmission at each node (link-layer retransmission), which results in high reliability but also high delay and low throughput.

- **Frame Relay**: Developed as a faster and more efficient successor to X.25, Frame Relay is still fundamentally **packet switching**. It uses variable-length frames and eliminates hop-by-hop error checking and flow control (end-to-end error control is left to higher layers). This makes it much faster and more suitable for modern digital lines.

- **ATM (Asynchronous Transfer Mode)**: ATM uses fixed-length **cells** (53 bytes) and is also a form of **packet switching**, but it is a special type often called **cell switching** or **cell-relay**. Despite being called "cell switching" in some textbooks, from the broader technical classification perspective, ATM still belongs to **packet switching** (分组交换), because it breaks user data into small packets (cells) and statistically multiplexes them.

**Key point for this question**:

Most Chinese certification exams (such as soft exam / Huawei / H3C / network engineer exams) and many textbooks classify **X.25, Frame Relay, and ATM** together under **分组交换 (packet switching)**.

The term "信元交换 (cell switching)" is sometimes used specifically for ATM, but in the context of this question, the intended and officially correct answer is **B. 分组交换**.

**Why D is incorrect in this context**:

Although ATM is indeed cell-based switching, the question uses the phrasing "帧中继、X.25及ATM都同属于" (all three belong to the same category). The common classification in Chinese teaching materials and exam standards groups them all under **分组交换**, not under the narrower term "信元交换" (which only applies to ATM).

Therefore, the standard answer is **B**.

References:

- None (based on standard network engineering teaching materials and certification exam patterns in China)
