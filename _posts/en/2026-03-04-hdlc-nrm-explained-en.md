---
audio: false
generated: true
image: false
lang: en
layout: post
title: HDLC Normal Response Mode Explained
translated: false
type: note
---

Question: In HDLC, the operation mode where the transmission process is initiated by the primary station, and the secondary station can only transmit information to the primary station as a response after receiving a command frame from the primary station is called

A. Normal Response Mode  
B. Asynchronous Response Mode  
C. Asynchronous Balanced Mode  
D. Synchronous Balanced Mode  

Your answer: B  
Correct answer: A  

Answer: 

The correct answer is **A. Normal Response Mode (NRM)**.

### Explanation:

HDLC (High-level Data Link Control) defines three main operational modes:

- **Normal Response Mode (NRM)**  
  - The primary station (主站) has complete control over the link.  
  - Only the primary station can initiate data transmission.  
  - The secondary station (从站) is not allowed to transmit anything unless it is explicitly polled or commanded by the primary station.  
  - After receiving a command frame (especially with the poll bit set), the secondary may respond with one or more frames.  
  - If multiple frames are sent in response, the last frame must have the final bit (F-bit) set.  
  - This mode matches **exactly** the description in the question:  
    > “传输过程由主站启动，从站只有收到主站某个命令帧后，才能作为响应向主站传输信息。”

- **Asynchronous Response Mode (ARM)**  
  - The secondary station can initiate transmission at any time without waiting for permission from the primary (asynchronous means no constant polling is required).  
  - This is the opposite of the behavior described in the question.

- **Asynchronous Balanced Mode (ABM)**  
  - Both stations are equal (balanced configuration).  
  - Either station can initiate transmission at any time.  
  - Commonly used in point-to-point full-duplex links (e.g., modem connections, LAPB in X.25).  
  - Clearly not matching the question.

- **Synchronous Balanced Mode**  
  - This is not a standard HDLC mode name.

Therefore, the description given in the question is the textbook definition of **Normal Response Mode (NRM)**.

Your choice of B (Asynchronous Response Mode) is incorrect because in ARM the secondary is allowed to send data spontaneously, without needing a command frame from the primary first.

References:  

- HDLC protocol standards (ISO 13239 / ITU-T Recommendation)  
- Most computer network textbooks (e.g., Tanenbaum, Kurose & Ross, Forouzan) describe NRM exactly as quoted in the question.