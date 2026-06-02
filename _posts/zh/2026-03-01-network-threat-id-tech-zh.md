---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络威胁识别技术
translated: true
type: note
---

问题：为了准确识别和辨识网络中的各种不安全因素，并进而进行相应的预防、消除和修复，使用的是哪种计算机网络安全技术？

A. Encryption technology
B. Monitoring and auditing technology
C. Authentication technology (鉴别技术)
D. Access control technology

给出的正确答案是 C。

**答案：**

正确答案是 **C. 鉴别技术** (authentication/identification technology)。

**解释：**

问题描述了一种技术，其主要目的是**及时准确地检测、判断和识别**网络中的各种不安全因素——如攻击、窃取、篡改、viruses、worms、trojans 和其他 malicious code——从而采取相应的预防、消除和修复措施。

让我们分析每个选项：

- **A. Encryption technology**：主要通过使数据对未经授权方不可读来保护数据的**confidentiality**。它不专注于检测或识别 attacks/malware。
- **B. Monitoring and auditing technology**：专注于**recording**和**tracking**用户/network 活动和系统事件，通常用于后续分析或 compliance。它更被动（logging），而非主动实时识别和判断 threats。
- **C. 鉴别技术 (Authentication / Identification / Detection technology)**：在本问题语境中（以及根据提供的解释），这指的是主动**识别和辨识** security threats、异常行为、malicious code、intrusions 等的技术。这与问题描述非常吻合——及时准确判断和识别不安全因素 → 预防、消除、修复。
- **D. Access control technology**：主要决定**谁被允许**访问哪些资源（authorization）。它防止 unauthorized access，但不是主要负责检测/识别正在进行的 attacks 或 malicious code。

虽然在现代英语术语中“鉴别技术”最常翻译为**authentication**（verifying identity），但在许多中文计算机安全教材和考试语境中（尤其是较旧材料或特定考试题库），“鉴别技术”被更广泛地用于包括**threat detection**、**intrusion detection**、**malicious code identification** 等。

根据问题的措辞和提供的官方解释，在此特定考试语境中，**C** 是预期的正确答案。

**参考文献：**

- 无（基于提供的题目解释）
