---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-3-flash-preview
title: UDP Checksum for Data Integrity
translated: false
type: note
---

Question: Which field in the UDP header is used to ensure data integrity, and how does it work?

Answer:

The field used in the User Datagram Protocol (UDP) header to ensure data safety is the **Checksum** (检验和).

While UDP is known for being a "best-effort" and unreliable protocol, the Checksum provides a basic layer of error detection to prevent the delivery of corrupted data.

### How the UDP Checksum Works

The checksum is designed to verify that the bits within the UDP header and the data payload have not been altered during transit.

1. **The Pseudo-Header**: To make the check more robust, UDP creates a "pseudo-header" that includes the Source IP Address, Destination IP Address, and the Protocol number (17 for UDP). This ensures the packet wasn't misrouted.
2. **Calculation**: The sender treats the pseudo-header, UDP header, and data as a series of 16-bit integers. It performs a **one's complement sum** of these integers.
3. **Verification**: The receiver performs the same calculation. If the result is all 1s (in one's complement arithmetic), the data is considered intact.
4. **Action on Failure**: If the checksums do not match, the UDP layer **silently discards** the packet. Unlike TCP, UDP does not request a retransmission.

---

### Key Characteristics of the UDP Checksum

* **Optional in IPv4**: In IPv4, the checksum is technically optional. If not used, the field is filled with zeros.
* **Mandatory in IPv6**: Because IPv6 removed the header checksum at the IP layer, the UDP checksum is **required** to ensure basic integrity.
* **Limitations**: It only detects errors; it cannot fix them. It also doesn't protect against packets being lost or arriving out of order.

---

### Comparison: UDP vs. TCP Checksum

| Feature | UDP Checksum | TCP Checksum |
| --- | --- | --- |
| **Requirement** | Optional (IPv4) / Mandatory (IPv6) | Always Mandatory |
| **Error Handling** | Discards packet silently | Discards and requests retransmission |
| **Focus** | Speed and low overhead | Reliability and data integrity |

Would you like me to show you the step-by-step math for calculating a one's complement checksum?