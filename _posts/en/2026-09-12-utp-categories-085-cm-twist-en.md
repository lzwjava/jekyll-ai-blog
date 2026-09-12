---
audio: false
generated: true
image: false
lang: en
layout: post
title: "UTP Categories: 0.85 cm Twist"
translated: false
type: note
---

Question: **Intro to the 5 UTP categories — and what does “0.85 cm” relate to? Is it the length limit?**

Answer:

If you mean the classic **UTP cable categories**, the key idea is:

| Category   | Frequency |      Typical Ethernet | Max channel length |
| ---------- | --------: | --------------------: | -----------------: |
| **Cat 3**  |    16 MHz |               10 Mbps |              100 m |
| **Cat 5**  |   100 MHz |              100 Mbps |              100 m |
| **Cat 5e** |   100 MHz |                1 Gbps |              100 m |
| **Cat 6**  |   250 MHz | 1 Gbps; 10 Gbps short |              100 m |
| **Cat 6A** |   500 MHz |               10 Gbps |              100 m |

The **100 m** number is the Ethernet channel limit; typically this is **90 m permanent cable + up to 10 m patch cables**. Cat 6 only supports 10 GbE for a shorter distance, commonly around 55 m. ([Network Startup Resource Center][1])

### So what is **0.85 cm**?

**0.85 cm is NOT the cable-length limit.**

It refers to the **twist length** of the copper pair in old Cat 5 terminology:

> Cat 5: twist length ≈ **0.6–0.85 cm**. ([WashU CSE][2])

Think of one pair as:

```text
────╲╱────╲╱────╲╱────╲╱────
      ↑
   twist pitch
   ~0.6–0.85 cm
```

The conductors are twisted to reduce **crosstalk / electromagnetic interference**. Different categories use different geometries and tighter performance requirements, allowing higher signaling frequencies.

So don't confuse:

```text
0.85 cm  → twist pitch / twist length
100 m    → maximum Ethernet channel length
100 MHz  → Cat 5 bandwidth/frequency rating
```

Also, **UTP** itself means **Unshielded Twisted Pair**. “Cat 5 / 5e / 6 / 6A” describes the **performance category**, while UTP describes the **shielding construction**. ([TME][3])

If by **“5 类 UTP”** you specifically mean **Cat 5**, rather than “five categories of UTP,” then the 0.85 cm number is almost certainly the **twist length** you're looking at. ([WashU CSE][2])

References:

* [Washington University UTP lecture notes](https://www.cse.wustl.edu/~jain/cse473-22/ftp/i_1cni.pdf?utm_source=chatgpt.com)
* [NSRC Layer 1 Cabling Standards](https://nsrc.org/activities/agendas/en/cndo/networking/cndo/en/presentations/Layer1-Cabling-Standards.pdf?utm_source=chatgpt.com)
* [Eaton Ethernet cable length guide](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/network-connectivity/ethernet-cables-explained.html?utm_source=chatgpt.com)

[1]: https://nsrc.org/activities/agendas/en/cndo/networking/cndo/en/presentations/Layer1-Cabling-Standards.pdf?utm_source=chatgpt.com "Slide 1"
[2]: https://www.cse.wustl.edu/~jain/cse473-22/ftp/i_1cni.pdf?utm_source=chatgpt.com "Student Questions"
[3]: https://www.tme.com/us/en-us/news/library-articles/page/78420/how-to-choose-the-length-and-type-of-network-cable-cat5e-cat6-cat6a-cat7-differences-and-applications/?utm_source=chatgpt.com "How to choose the length and type of network cable? CAT5e, CAT6, CAT6A, CAT7 – differences and applications | TME US"
