---
audio: false
generated: true
image: false
lang: en
layout: post
title: HDLC Normal Response Mode Basics
translated: false
type: note
---

Question: In HDLC, the operation mode where the transmission process is initiated by the primary station, and a secondary station can only transmit information to the primary station as a response after receiving a command frame from the primary station is called what?

A. Normal Response Mode (NRM)
B. Asynchronous Response Mode (ARM)
C. Asynchronous Balanced Mode (ABM)
D. Synchronous Balanced Mode

Your answer: B
Correct answer: A

Answer:

The correct answer is **A. 正常响应方式 (Normal Response Mode, NRM)**.

### Explanation:

HDLC defines three main operational modes:

- **Normal Response Mode (NRM)**
  This is a **master-slave** (unbalanced) configuration.
  - Only the **primary station** can initiate transmission.
  - The **secondary station** is not allowed to transmit anything until it receives a command frame (usually with the P/F bit set to poll) from the primary station.
  - After being polled, the secondary may send one or more response frames (with the last frame having the F bit set).
  - The primary station is fully responsible for link management, polling, timeouts, retransmissions, and error recovery.
  → This exactly matches the description in the question.

- **Asynchronous Response Mode (ARM)**
  This is still unbalanced (primary + secondary), but the **secondary station** can send frames at any time without waiting for permission from the primary (i.e., it can initiate transmission asynchronously).
  → This is **not** the mode described in the question.

- **Asynchronous Balanced Mode (ABM)**
  This is a **balanced** configuration (both sides are combined stations).
  Either station can initiate transmission at any time without needing permission from the other side.
  → Clearly different from the described behavior.

- **Synchronous Balanced Mode**
  This term is not a standard HDLC mode (it does not exist in the official HDLC standard).

Therefore, the scenario described — **transmission started only by the primary station**, and **secondary station can only respond after receiving a command** — is the definition of **Normal Response Mode (NRM)**.

Your mistake: You chose **B (Asynchronous Response Mode)**, which is the opposite case — the secondary is allowed to initiate transmission without being polled first.

References:

- HDLC protocol specification (ISO 13239 / ITU-T Recommendation X.25 LAPB documentation)
- Most computer networking textbooks covering Data Link Layer protocols (e.g., Tanenbaum, Kurose & Ross, Forouzan)
