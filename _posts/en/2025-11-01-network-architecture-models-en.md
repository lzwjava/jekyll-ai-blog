---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Network Architecture and Models Study
translated: false
type: note
---

This chapter lays the foundation for understanding how computer networks are structured and how data is transmitted across them. In the context of the *Computer Networks Technology* course (自考 code 02141 or similar), it emphasizes theoretical models like OSI and TCP/IP, which are core to exam questions on layering, protocols, and data flow. Focus on memorizing layer names, functions, and mappings between models. Expect multiple-choice, short-answer, or diagram-based questions testing comparisons and responsibilities.

## 1. Introduction to Layered Architectures

Networks use **layered architectures** to simplify complex communication by dividing tasks into modular layers. Each layer:

- Handles specific functions (e.g., error checking, routing).
- Interacts only with adjacent layers via standardized interfaces.
- Uses **encapsulation** (adding headers/trailers) when sending data down the stack and **decapsulation** when receiving.

**Benefits**:

- Modularity: Easy to develop, test, and update individual layers.
- Interoperability: Devices from different vendors can communicate.
- Scalability: Layers can evolve independently (e.g., new transport protocols).

**Responsibilities** (general across models):

- **Lower layers**: Focus on hardware and reliable data transfer (physical transmission, error detection).
- **Upper layers**: Handle user-facing tasks (e.g., file transfer, web browsing).
- Data flows **down** the sender's stack (encapsulation) and **up** the receiver's stack (decapsulation).

## 2. OSI Reference Model

The **Open Systems Interconnection (OSI)** model is a conceptual 7-layer framework developed by ISO in 1984. It's theoretical, not implemented directly, but used as a standard for understanding protocols. Mnemonic: **Please Do Not Throw Sausage Pizza Away** (Physical → Application).

| Layer Number | Layer Name | Key Functions and Protocols | PDU (Protocol Data Unit) | Devices/Examples |
| -------------- | ------------------ | ----------------------------- | -------------------------- | ------------------ |
| 7 | Application | Provides network services to user apps (e.g., email, file transfer). Interfaces with software. | Data | HTTP, FTP, SMTP; Web browser |
| 6 | Presentation | Translates data formats (e.g., encryption, compression, ASCII to EBCDIC). Ensures syntax compatibility. | Data | JPEG, SSL/TLS |
| 5 | Session | Manages sessions/connections (e.g., setup, synchronization, dialog control). Handles checkpoints for recovery. | Data | NetBIOS, RPC |
| 4 | Transport | End-to-end reliable delivery (e.g., segmentation, flow control, error recovery). | Segment (TCP) / Datagram (UDP) | TCP, UDP; Ports (e.g., 80 for HTTP) |
| 3 | Network | Logical addressing and routing (e.g., path determination across networks). Handles congestion. | Packet | IP, ICMP, OSPF; Routers |
| 2 | Data Link | Node-to-node delivery on same network (e.g., framing, error detection via CRC, MAC addressing). | Frame | Ethernet, PPP; Switches, NICs |
| 1 | Physical | Bit transmission over physical medium (e.g., signaling, cabling, topology). Deals with hardware specs. | Bit | RJ-45, Fiber optics; Hubs, Cables |

**Key Notes**:

- Layers 1-2: Media-focused (LAN/WAN).
- Layers 3-4: Host-to-host (internetworking).
- Layers 5-7: User-oriented (application support).
- Exam Tip: Draw the stack and label PDUs/headers (e.g., TCP segment has TCP header + data).

## 3. TCP/IP Protocol Suite

The **TCP/IP model** (or Internet Protocol Suite) is a practical 4-layer model developed in the 1970s for the ARPANET (basis of the internet). It's implemented worldwide and maps loosely to OSI. Mnemonic: **LITA** (Link → Application).

| Layer Number | Layer Name | Key Functions and Protocols | PDU | Devices/Examples |
| -------------- | ------------------ | ----------------------------- | ---------------------- | ------------------ |
| 4 | Application | Combines OSI Layers 5-7: User services (e.g., web, email). | Data/Segment | HTTP, FTP, DNS; Apps like browsers |
| 3 | Transport | End-to-end (OSI Layer 4): Reliable/unreliable delivery. | Segment/Datagram | TCP (reliable, connection-oriented), UDP (best-effort) |
| 2 | Internet | Routing and addressing (OSI Layer 3): Logical paths across networks. | Packet | IP (IPv4/IPv6), ICMP; Routers |
| 1 | Link (or Network Access) | Physical + Data Link (OSI Layers 1-2): Hardware delivery on local network. | Frame/Bit | Ethernet, Wi-Fi; Switches, Cables |

**Key Notes**:

- No dedicated session/presentation layers; handled within Application.
- TCP/IP is "protocol family" – e.g., IP is core, with TCP/UDP on top.
- Exam Tip: Emphasize real-world use (e.g., TCP ensures reliability via acknowledgments, while UDP is lightweight for video streaming).

## 4. Comparison of OSI and TCP/IP Models

Use this table for quick revision. OSI is theoretical (reference), TCP/IP is practical (implementation).

| Aspect              | OSI Model                          | TCP/IP Model                       |
|---------------------|------------------------------------|------------------------------------|
| **Layers**         | 7 (detailed, conceptual)          | 4 (simplified, practical)         |
| **Development**    | ISO (1984), top-down design       | DoD/Internet (1970s), bottom-up   |
| **Focus**          | General networking standards      | Internet-specific protocols       |
| **Implementation** | Not directly implemented; reference for standards | Widely used (basis of modern internet) |
| **Layer Mapping**  | 1: Physical → Link<br>2: Data Link → Link<br>3: Network → Internet<br>4: Transport → Transport<br>5-6-7: Session/Presentation/Application → Application | Application absorbs OSI 5-7; Link absorbs 1-2 |
| **Protocols**      | Theoretical (e.g., no single IP)  | Specific (e.g., IP, TCP, HTTP)    |
| **PDU Flow**       | Strict per-layer headers          | Flexible (e.g., IP packet includes transport data) |
| **Strengths**      | Comprehensive, easy to teach      | Efficient, scalable, vendor-neutral |
| **Weaknesses**     | Overly complex, not practical     | Less detailed for upper layers    |

**Key Differences**:

- **Granularity**: OSI separates session/presentation; TCP/IP merges them into Application for simplicity.
- **Addressing**: OSI uses service access points (SAPs); TCP/IP uses ports/IP addresses.
- **Reliability**: Both have transport reliability, but TCP/IP's TCP is connection-oriented like OSI's Transport.
- Exam Tip: Questions often ask for mappings (e.g., "Which OSI layer corresponds to TCP?") or advantages (e.g., TCP/IP's adaptability led to the internet's growth).

## 5. Layered Architecture Functions and Responsibilities

**Core Principles**:

- **Abstraction**: Each layer hides lower-layer details (e.g., Transport doesn't care about physical cables).
- **Service Primitives**: Layers provide services like CONNECT, DATA, DISCONNECT to upper layers.
- **Error Handling**: Lower layers detect errors; upper layers recover (e.g., Transport retransmits lost packets).
- **Addressing**: Hierarchical – physical (MAC), logical (IP), service (ports).

**Data Transmission Example**:

1. Application data → Transport adds segment header (ports, seq. no.) → Network adds packet header (IP addresses) → Link adds frame header/trailer (MAC) → Physical sends bits.
2. Reverse at receiver.

**Common Pitfalls**:

- Don't confuse layers: Physical is bits/signals; Data Link is frames/error-free frames.
- TCP/IP Link layer = OSI 1+2 combined.

## Study Tips for 自考 Exam

- **Memorization**: Use mnemonics and draw layered diagrams daily. Focus on 80% exam weight on OSI/TCP/IP descriptions.
- **Practice**:
  - Compare layers in essays (200-300 words).
  - MCQs: "Which layer handles routing? (A) Network".
  - Diagrams: Label a PDU traversal.
- **Resources**: Review textbook figures for encapsulation. Time yourself: 30 mins for comparison table.
- **Common Questions**: Explain why OSI has 7 layers vs. TCP/IP's 4; Describe Transport layer duties.

Master this chapter for a strong start – it's referenced in later topics like protocols (e.g., IP in Chapter 3). Next, tackle physical layer details.

**References**:

- [Computer Networking: A Top-Down Approach by Kurose & Ross](https://www.pearson.com/us/higher-education/program/Kurose-Computer-Networking-A-Top-Down-Approach-8th-Edition/PGM1836378.html) (for TCP/IP depth).
- [OSI Model Explained - GeeksforGeeks](https://www.geeksforgeeks.org/open-systems-interconnection-model-osi/) (visual aids).
