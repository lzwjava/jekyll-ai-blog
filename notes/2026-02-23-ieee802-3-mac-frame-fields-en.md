---
audio: false
generated: true
image: false
lang: en
layout: post
title: IEEE 802.3 MAC Frame Fields Explained
translated: false
type: note
---

Question: What are the names and lengths (in bytes) of each field in the IEEE 802.3 MAC frame format?

Answer:

The IEEE 802.3 MAC (Media Access Control) frame format consists of the following fields, listed in order from the beginning of the frame to the end:

1.  **Preamble**
    *   **Length:** 7 bytes
    *   **Description:** A pattern of alternating 1s and 0s (`10101010...`) used to synchronize the receiver's clock with the sender's clock.

2.  **Start Frame Delimiter (SFD)**
    *   **Length:** 1 byte
    *   **Description:** The sequence `10101011` which indicates the start of the frame. The last two bits (`11`) signal the beginning of the destination address.
    *   *Note:* In many modern contexts, the Preamble and SFD are often grouped together as an 8-byte "Preamble" field, but strictly speaking, they are distinct. They are typically stripped by the physical layer before the MAC layer processes the rest of the frame.

3.  **Destination Address (DA)**
    *   **Length:** 6 bytes
    *   **Description:** Contains the MAC address of the intended recipient. It can be a unicast, multicast, or broadcast address.

4.  **Source Address (SA)**
    *   **Length:** 6 bytes
    *   **Description:** Contains the MAC address of the sending station. This is always a unicast address.

5.  **Length / Type**
    *   **Length:** 2 bytes
    *   **Description:**
        *   If the value is less than or equal to 1500 (0x05DC), it indicates the **Length** of the data field (IEEE 802.3 standard).
        *   If the value is greater than or equal to 1536 (0x0600), it indicates the **Type** of protocol encapsulated in the payload (Ethernet II framing, which is commonly used over IEEE 802.3 physical layers).

6.  **Data (and Padding)**
    *   **Length:** 46 to 1500 bytes
    *   **Description:** Contains the payload from the upper layer (e.g., an IP packet).
        *   **Maximum:** 1500 bytes (Maximum Transmission Unit - MTU).
        *   **Minimum:** 46 bytes. If the actual data is less than 46 bytes, padding bytes are added to reach this minimum. This ensures the total frame size (from Destination Address to FCS) is at least 64 bytes, which is required for collision detection in CSMA/CD networks.

7.  **Frame Check Sequence (FCS)**
    *   **Length:** 4 bytes
    *   **Description:** Contains a 32-bit Cyclic Redundancy Check (CRC) value calculated over the Destination Address, Source Address, Length/Type, and Data fields. It is used for error detection.

**Summary Table:**

| Field Name | Length (Bytes) |
| :--- | :--- |
| Preamble | 7 |
| Start Frame Delimiter (SFD) | 1 |
| Destination Address | 6 |
| Source Address | 6 |
| Length / Type | 2 |
| Data (Payload + Padding) | 46 – 1500 |
| Frame Check Sequence (FCS) | 4 |
| **Total Frame Size** | **64 – 1518** |

*(Note: If VLAN tagging (802.1Q) is used, an additional 4-byte tag is inserted after the Source Address, increasing the maximum frame size to 1522 bytes.)*
