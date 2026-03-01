---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ethernet Switch Frame Forwarding Analysis
translated: false
type: note
---

Question: In the given Ethernet topology (as shown in Figure 28) with the current switch forwarding table (as shown in Table 28), host 00-e1-d5-00-23-a1 sends a data frame to host 00-e1-d5-00-23-c1. After receiving the frame, host 00-e1-d5-00-23-c1 sends an acknowledgment frame back to host 00-e1-d5-00-23-a1. Please answer: (1) Which ports does the switch forward the data frame and the acknowledgment frame to, respectively? (2) Based on the process described, draw the updated switch forwarding table.

Answer: 

Since the problem refers to "Figure 28" and "Table 28" which are not provided in the text, I can only give the most common and typical analysis pattern for this type of question. The following answer assumes a very common topology and initial table used in Chinese university network courses (especially in the 408 exam or similar exercises). If your actual figure/table is different, the conclusion may differ.

**Most common topology assumption in such problems:**

- There is one switch (often with 4 ports: 1, 2, 3, 4)
- Port 1 connects to host A (00-e1-d5-00-23-a1)
- Port 2 connects to host B (some intermediate host, often not used in this process)
- Port 3 connects to host C (00-e1-d5-00-23-c1)
- Port 4 connects to another host or uplink (sometimes not involved)

**Most common initial forwarding table assumption:**

| MAC address           | Port |
|-----------------------|------|
| 00-e1-d5-00-23-a1     | 1    |
| 00-e1-d5-00-23-b?     | 2    |  (sometimes exists, sometimes empty)
| (other entries or empty) |      |

**Typical process and answers:**

**(1) Forwarding ports of the switch**

- When host A (…-a1) sends a data frame to host C (…-c1):  
  → Destination MAC = 00-e1-d5-00-23-c1  
  → At this time, the switch forwarding table **does not have an entry for …-c1** (very common in such questions)  
  → The switch performs **flooding** → forwards the frame out of **all ports except the incoming port (port 1)**  
  → So the data frame is forwarded to **ports 2, 3, 4** (commonly port 3 reaches host C)

- When host C (…-c1) sends the ACK frame back to host A (…-a1):  
  → Destination MAC = 00-e1-d5-00-23-a1  
  → The switch already has the entry …-a1 → port 1 (learned when A sent the first frame)  
  → So the switch **unicasts** → forwards only to **port 1**

**Answer to (1):**  
Data frame: forwarded to ports **2, 3, 4** (flooding)  
Acknowledgment frame: forwarded to port **1** (unicast)

**(2) Updated switch forwarding table**

After the above two frames pass through the switch, the switch must have learned the MAC address of host C.

Updated forwarding table (most common final state):

| MAC address           | Port |
|-----------------------|------|
| 00-e1-d5-00-23-a1     | 1    |
| 00-e1-d5-00-23-c1     | 3    |
| (possibly still has …-b? → 2 if it existed before) |      |

**Text representation of the updated table:**

```
MAC address             VLAN    Port    Type    Age
00-e1-d5-00-23-a1              1       dynamic 
00-e1-d5-00-23-c1              3       dynamic 
(possibly other entries remain unchanged)
```

**Core learning rule reminder (key points for this type of question):**

- When a frame arrives, the switch always learns the **source MAC** → associates it with the **incoming port**
- If the **destination MAC** is in the table → unicast to the corresponding port
- If the **destination MAC** is not in the table → flood to all other ports
- The return ACK frame is the most common way to let the switch learn the MAC-port mapping of the destination host

If your actual Figure 28 or Table 28 is significantly different (e.g., multiple switches, hosts on different ports, already has …-c1 entry, etc.), please provide the topology and initial table content, and I can give a more precise answer.

References:  

- None (answer based on standard Ethernet switch self-learning behavior and common patterns in Chinese computer network exam questions)