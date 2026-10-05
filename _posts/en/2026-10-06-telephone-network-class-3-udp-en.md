---
audio: false
generated: true
image: false
lang: en
layout: post
title: Telephone Network Class 3 UDP
translated: false
type: note
---

Question: What does “电话网络 3 类 UDP” mean?

Answer:

If you mean **telephone network Class 3 UDP**, the phrase is ambiguous. It is not a standard Internet term. It may refer to one of these:

### 1. Telephone network traffic classification (VoIP)

Modern phone calls often use:

* **Signaling**

  * SIP (call setup, hangup, registration)
  * Usually TCP or UDP (SIP commonly uses UDP port 5060)

* **Media**

  * Voice packets (RTP)
  * Usually **UDP**
  * Example:

    ```
    Voice → RTP packets → UDP → IP
    ```

Why UDP?

A voice call needs low latency:

```
TCP:
packet lost → retransmit → delay → voice gap

UDP:
packet lost → ignore → continue speaking
```

For human conversation, a 100 ms delay is usually worse than losing a tiny audio fragment.

---

### 2. OSI / computer networking “3类”?

If you mean **network layer classification**, UDP is not a network layer protocol.

Stack:

```
Application
   SIP
   RTP
      |
Transport
   UDP  ← here
      |
Internet
   IP
      |
Link
   Ethernet / WiFi / 5G
```

UDP is a **Layer 4 transport protocol**.

---

### 3. “三类电话网” (Class 3 telephone network)

In traditional telecom, “class” can mean telephone switches:

* Class 5: local telephone office
* Class 4: toll/intercity switch
* Class 3/2/1: higher-level carrier switching hierarchy

Those are from the old PSTN telephone system and unrelated to UDP.

---

Most likely, if you saw “电话网络 + UDP”, it means:

> Voice/VoIP calls use UDP because real-time communication prefers low latency over guaranteed delivery.
