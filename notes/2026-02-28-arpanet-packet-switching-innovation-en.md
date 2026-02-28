---
audio: false
generated: true
image: false
lang: en
layout: post
title: ARPANETs Packet Switching Innovation
translated: false
type: note
---

**Question:** Which switching technology was used by ARPANET to connect different types of computers and transmit data signals?

**Answer:**

The correct answer is **C. 分组交换技术** (Packet Switching technology).

**Explanation:**

ARPANET, developed in the late 1960s by the U.S. Department of Defense's Advanced Research Projects Agency (ARPA), was the world's first operational packet-switched network and the direct predecessor of the modern Internet.

Key characteristics and reasons why ARPANET used **packet switching**:

- It breaks messages into small, independent **packets**, each containing destination address information.
- Packets can travel independently through the network, taking different routes if necessary.
- This approach is highly resilient — if one path fails (e.g., during wartime), packets can be rerouted automatically.
- It allows **different types of computers** (with different architectures, operating systems, and word lengths) to communicate effectively because the communication protocol handles data in standardized packet format rather than requiring identical hardware.
- It makes efficient use of network bandwidth (resources are shared dynamically) compared to circuit switching.

Comparison with other options:

- **A. 电路交换技术 (Circuit Switching)**  
  Used in traditional telephone networks. A dedicated end-to-end path is established before communication begins and held for the entire duration. Not suitable for connecting heterogeneous computers or bursty data traffic. ARPANET did **not** use this.

- **B. 报文交换技术 (Message Switching)**  
  Entire message is sent as a single unit and stored-and-forwarded at each node. It has high delay (especially for long messages) and requires large storage at intermediate nodes. ARPANET did **not** use pure message switching.

- **C. 分组交换技术 (Packet Switching)**  
  Correct choice. This is the fundamental innovation of ARPANET.

- **D. ATM交换技术 (ATM Switching)**  
  Asynchronous Transfer Mode — a later cell-based switching technology developed in the 1980s–1990s for broadband networks. It did **not** exist when ARPANET was created (1969–1980s).

**Conclusion:**  
ARPANET's most important technical contribution to modern networking was the successful implementation of **packet switching**, which is why option **C** is correct.

Your original choice (A) is a common misunderstanding — many people associate circuit switching with traditional communication systems, but it was **not** the technology used in ARPANET.

**References:**

- None required for this well-established historical networking fact.