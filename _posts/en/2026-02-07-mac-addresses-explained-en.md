---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-3-flash-preview
title: Multiple MAC Addresses Explained
translated: false
type: note
---

Question: If a computer has multiple local area network (LAN) adapters installed, which type of addresses will it have multiple of?

Answer: A computer with multiple network adapters will have multiple **MAC (Media Access Control)** addresses.

### Why multiple MAC addresses?

Every network interface card (NIC) or adapter—whether it is a physical Ethernet port, a Wi-Fi chip, or even a virtual adapter—is manufactured with a unique identifier burned into its hardware.

* **1:1 Relationship:** Each individual adapter is assigned exactly one unique MAC address. Therefore, if you have two adapters (e.g., one for Wi-Fi and one for Ethernet), your computer inherently has two MAC addresses.
* **Hardware Layer:** The MAC address operates at the **Data Link Layer (Layer 2)** of the OSI model. It serves as a permanent physical "fingerprint" for that specific piece of hardware.

### What about IP addresses?

While the answer to your specific question is **MAC**, it is important to note that such a computer will also typically have multiple **IP addresses**.

* **Logical vs. Physical:** While the MAC address is physical and permanent, the IP address is logical and assigned by the network (Layer 3).
* **Connectivity:** To communicate on different networks simultaneously through different adapters, each adapter must be assigned its own unique IP address.

---

### Comparison Table

| Feature | MAC Address | IP Address |
| --- | --- | --- |
| **Full Name** | Media Access Control | Internet Protocol |
| **OSI Layer** | Layer 2 (Data Link) | Layer 3 (Network) |
| **Permanence** | Hardcoded/Permanent | Dynamic/Assigned |
| **Function** | Identifies the specific hardware | Identifies the location on the network |

Would you like me to explain how to find all the MAC addresses currently active on your specific operating system?