---
audio: false
generated: true
image: false
lang: en
layout: post
title: IBM PC BSC Protocol Overview
translated: false
type: note
---

### Comprehensive Introduction to IBM PC BSC (Binary Synchronous Communication)

**Binary Synchronous Communication (BSC)**, often referred to as **Bisync**, is a character-oriented, synchronous data link layer protocol developed by IBM in 1967 following the introduction of the System/360 family [[8]]. It was designed primarily for **half-duplex** transmission lines, meaning data can travel in both directions but not simultaneously [[9]]. The protocol replaced the older Synchronous Transmit-Receive (STR) protocol and became a standard for early mainframe and personal computer communications [[11]].

#### 1. Core Characteristics of the BSC Protocol
*   **Character-Oriented:** Unlike bit-oriented protocols (like SDLC or HDLC), BSC treats data as a stream of characters. Special control characters (such as SOH, STX, ETX) are used to frame messages and manage the flow of data [[17]].
*   **Synchronous Transmission:** Data is sent in blocks synchronized by a clock signal, eliminating the need for start and stop bits for every individual character, which improves efficiency over asynchronous methods [[16]].
*   **Half-Duplex Operation:** The protocol operates on a "turn-around" basis. One station transmits a block of data, and the line must be turned around (a process involving delay) before the receiving station can send an acknowledgment (ACK) or negative acknowledgment (NAK) [[13]]. This inherent design makes it unsuitable for full-duplex environments without complex workarounds [[28]].
*   **Error Checking:** BSC uses vertical and longitudinal redundancy checks (VRC/LRC) or Cyclic Redundancy Check (CRC) to ensure data integrity [[15]].

#### 2. The IBM PC BSC Communication Adapter
In the early 1980s, as the IBM Personal Computer (PC) and PC AT gained popularity in enterprise environments, there was a critical need to connect these new machines to existing IBM mainframes (like the System/370) and mid-range systems that relied on Bisync terminals.

*   **Hardware Function:** The **IBM Binary Synchronous Communications (BSC) Adapter** was an expansion card (typically for the ISA bus in PC/XT/AT models) that provided an RS-232C-compatible interface specifically configured for synchronous, half-duplex communication [[3]].
*   **Configuration Limits:** On systems like the IBM PC AT, a maximum of two BSC adapters could be installed. However, if an SDLC (Synchronous Data Link Control) adapter was present, only one BSC adapter was allowed due to resource conflicts or architectural limitations [[4]].
*   **Usage Scenario:** This adapter allowed the PC to emulate legacy 3270 or other Bisync terminals, enabling users to run Remote Job Entry (RJE) tasks or access host applications that had not yet migrated to the newer SNA/SDLC protocols [[31]].

#### 3. BSC vs. SDLC
While BSC was widely used, it was eventually superseded by **SDLC (Synchronous Data Link Control)** and later **SNA (Systems Network Architecture)**.
*   **Efficiency:** SDLC is a bit-oriented protocol that supports full-duplex communication, allowing simultaneous sending and receiving, which offers significantly higher throughput than the stop-and-wait nature of BSC [[28]].
*   **Transparency:** BSC struggles with "data transparency" because its control characters might appear within the actual data payload, requiring escape sequences (like DLE). SDLC handles binary data more naturally using bit stuffing [[34]].
*   **Legacy Status:** By the late 1980s and 1990s, IBM shifted focus to 5250 emulation adapters (for AS/400 systems) and 3270 emulation over SDLC/SNA, rendering the dedicated BSC adapter a legacy component for maintaining older connections [[19]].

#### 4. Why "Half-Duplex" is the Defining Feature
The exam question correctly identifies that the adapter is designed for **half-duplex** lines because the BSC protocol itself dictates this mode. The protocol relies on explicit "turnaround" sequences where the transmitting station sends an EOT (End of Transmission) character and waits for the line to settle before the receiver can respond. This mechanical and logical constraint is hardwired into the design of the BSC adapter, distinguishing it from asynchronous adapters (which can be full-duplex) or SDLC adapters (which support full-duplex) [[13]].

### Summary
The **IBM PC BSC Communication Adapter** was a specialized hardware interface that enabled early IBM PCs to communicate with legacy mainframe systems using the **Binary Synchronous Communication (Bisync)** protocol. Its design is fundamentally tied to the **half-duplex**, character-oriented nature of Bisync, requiring strict turn-around procedures for data exchange. While largely obsolete today, it played a crucial role in the transition era of corporate computing, bridging the gap between the PC revolution and the established mainframe infrastructure.

References:
- [Binary Synchronous Communications - Wikipedia](https://en.wikipedia.org/wiki/Binary_Synchronous_Communications)
- [IBM Binary Synchronous Communications Adapter PDF](https://minuszerodegrees.net/oa/OA%20-%20IBM%20Binary%20Synchronous%20Communications%20Adapter.pdf)
- [IBM Personal Computer AT Product Announcement - Lo-tech Wiki](https://www.lo-tech.co.uk/wiki/IBM_Personal_Computer_AT_Product_Annoucement)
- [Binary Synchronous Communication (BISYNC) - GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/binary-synchronous-communication-bisync/)
- [SDLC and BSC on satellite links: a performance comparison](https://dl.acm.org/doi/10.1145/1024894.1024895)
