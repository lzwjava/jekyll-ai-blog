---
audio: false
generated: true
image: false
lang: en
layout: post
title: Error Control Methods in Data Communication
translated: false
type: note
---

**Question:** What are the error control methods (差错控制方式) in data communication systems (数据通信系统)?

---

**Answer:**

In data communication systems, errors are unavoidable — caused by thermal noise (random electronic interference) and impulse noise (sudden electromagnetic bursts). To address this, **error control coding** is used: redundant bits are appended to data before transmission so the receiver can detect or correct errors.

There are two types of error control codes:

- **Error-detecting codes** — detect errors but can't fix them (e.g., Parity Check, CRC)
- **Error-correcting codes** — detect and automatically fix errors (e.g., Hamming code, Convolutional code)

---

There are **3 main error control methods**, differing in implementation:

### 1. Forward Error Correction (FEC) — 前向纠错

The receiver not only detects errors but also uses coding techniques to **automatically correct** them without requesting retransmission. This requires error-correcting codes. The channel encoder adds redundancy at the sender, and the decoder at the receiver can correct most transmission errors.

- ✅ No return channel needed
- ✅ High channel utilization
- ❌ More complex coding; more redundant bits
- **Used in:** satellite communications, mobile networks, broadband data transmission

---

### 2. Automatic Repeat Request (ARQ) — 反馈重发检错

The receiver detects errors and notifies the sender via a **feedback channel** to **retransmit** the data, repeating until no error is found. Only error-detecting codes are needed. The simplest form is **stop-and-wait**: the sender sends one block, then waits for an acknowledgment before sending the next.

- ✅ Simpler coding; highly accurate
- ❌ Requires a feedback (return) channel
- ❌ Retransmissions reduce throughput in noisy channels

---

### 3. Hybrid ARQ (HEC) — 混合法

When channel interference is heavy, using ARQ alone causes excessive retransmissions (reducing throughput), while FEC alone may not guarantee sufficient accuracy. The hybrid method combines both: the decoder **corrects errors it can fix**, and only **requests retransmission for errors it can detect but not correct**. This greatly reduces retransmission frequency while maintaining high accuracy.

- ✅ Best balance of reliability and efficiency
- ✅ Strong error detection + partial correction
- **Used in:** modern wireless and cellular standards (e.g., LTE, 5G HARQ)

---

**References:**

- [差错控制技术，差错控制的三种方式 — C语言中文网](https://m.biancheng.net/view/atyjydp.html)
