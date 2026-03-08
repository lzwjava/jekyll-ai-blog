---
audio: false
generated: true
image: false
lang: en
layout: post
title: QUIC Protocol Explained Simply
translated: false
type: note
---

Question: What is a comprehensive introduction to the QUIC protocol in networking?

Answer:

## QUIC Protocol — A Comprehensive Introduction

---

### 1. What is QUIC?

QUIC, as defined by the Internet Engineering Task Force (IETF), is an encrypted connection-oriented protocol that operates at the Transport Layer (Layer 4) in the OSI model. It was initially designed by Jim Roskind at Google, first implemented and deployed in 2012, and publicly announced in 2013. Although its name was initially proposed as an acronym for "Quick UDP Internet Connections," in IETF's usage, QUIC is not an acronym — it is simply the name of the protocol.

QUIC was officially published as RFC 9000 by the IETF in May 2021.

---

### 2. Why Was QUIC Created? The Problem with TCP

TCP aims to provide an interface for sending streams of data between two endpoints. It breaks data into network packets, adds sequence numbers and checksums, and uses Automatic Repeat Request (ARQ) to re-send lost or damaged packets. In most implementations, TCP treats any error as a blocking operation, stopping further transfers until the error is resolved or the connection is considered failed.

This leads to a well-known problem called **Head-of-Line (HoL) Blocking**: a single lost packet can stall all other streams sharing the same TCP connection.

Additionally, because TCP is implemented in operating system kernels and middleboxes, deploying significant changes to TCP is nearly impossible. QUIC, being built on top of UDP, suffers from no such limitations.

---

### 3. QUIC's Architecture: Built on UDP

QUIC operates at the transport layer and is built on top of UDP (User Datagram Protocol). This allows it to avoid some of the overhead and latency associated with TCP.

QUIC provides applications with flow-controlled streams for structured communication, low-latency connection establishment, and network path migration. It includes security measures that ensure confidentiality, integrity, and availability across a range of deployment circumstances.

---

### 4. Key Features of QUIC

#### 4.1 Reduced Latency & Faster Handshake

The initial QUIC handshake combines the typical three-way TCP handshake with the TLS 1.3 handshake, providing endpoint authentication and cryptographic parameter negotiation. The typical QUIC handshake only takes a single round-trip between client and server, compared to the two round-trips required for TCP and TLS 1.3 combined.

#### 4.2 Zero Round-Trip Time (0-RTT)

In some cases, QUIC can send data during the very first connection cycle — known as 0-RTT (zero round-trip time). This is possible when the server has a previously cached connection with the client.

#### 4.3 Multiplexing Without Head-of-Line Blocking

Unlike TCP, where the loss of a single packet can block delivery of subsequent packets, QUIC allows multiple streams to be sent over a single connection without head-of-line blocking. QUIC resolves this issue by enabling each stream ("lane") to keep running independently. The protocol enables retransmission of data in just one stream as opposed to blocking all streams.

#### 4.4 Built-in Security (TLS 1.3)

QUIC is inherently secure as it mandates TLS 1.3 usage. By embedding both authentication and encryption into the protocol itself, QUIC streamlines secure communication while maintaining the lightweight benefits of UDP.

All data sent over QUIC is encrypted by default, and there is no option for cleartext communication. This helps protect against eavesdropping and other forms of attack.

#### 4.5 Connection Migration

QUIC includes a connection identifier to uniquely identify the connection to the server regardless of the client's source IP address. This solves the problem that occurs with TCP when a user moves from a Wi-Fi hotspot to a mobile network — in TCP, every existing connection times out one-by-one and must be re-established.

Connection migration uses connection identifiers to allow connections to transfer to a new network path. This design also allows connections to continue after changes in network topology or address mappings, such as might be caused by NAT rebinding.

#### 4.6 Encrypted Metadata

QUIC also encrypts additional connection metadata that could be abused by middleboxes to interfere with connections. For example, packet numbers could otherwise be used by passive on-path attackers to correlate users' activity over multiple network paths.

---

### 5. QUIC vs TCP+TLS vs UDP — Comparison

| Feature | TCP + TLS | UDP | QUIC |
|---|---|---|---|
| Connection Setup | Slow (2+ RTT) | None | Fast (1 RTT / 0-RTT) |
| Encryption | TLS (separate) | None | TLS 1.3 built-in |
| Multiplexing | Limited (HoL blocking) | None | Yes, independent streams |
| Connection Migration | No | No | Yes (Connection ID) |
| HoL Blocking | Yes | N/A | No |
| Packet Loss Handling | Blocks all streams | None | Per-stream only |

---

### 6. QUIC and HTTP/3

HTTP/3 is designed to take advantage of QUIC's features, including the lack of Head-of-Line blocking between streams. The QUIC project started as an alternative to TCP+TLS+HTTP/2, with the goal of improving user experience, particularly page load times.

QUIC was developed with HTTP in mind, and HTTP/3 was its first application. DNS-over-QUIC is another application of QUIC to name resolution, providing security for data transferred between resolvers similar to DNS-over-TLS.

---

### 7. gQUIC vs IETF QUIC

There are in fact two protocols that share the same name: "Google QUIC" (gQUIC), the original protocol designed by Google engineers, which was later adopted by the IETF for standardization; and "IETF QUIC," which has diverged from gQUIC significantly enough to be considered a separate protocol. IETF QUIC uses standard TLS 1.3 for its cryptographic handshake and incorporates a modular packet and connection design intended for broader interoperability.

---

### 8. Use Cases

- **Web browsing:** QUIC is used extensively by Google Chrome (in Chrome, QUIC is used by more than half of all connections to Google's servers).
- **IoT Devices:** QUIC can provide a more reliable and efficient alternative for IoT devices, as it is designed to work well in high-latency and lossy networks.
- **Internet of Vehicles (IoV):** QUIC's low latency, multiplexing capabilities, and resilience to packet loss can ensure reliable and efficient communication between vehicles and infrastructure components.
- **eCommerce & Payments:** QUIC's use of TLS encryption and reliable HTTP/3 streams make it a good choice for secure and reliable data transmission in payment applications.
- **Cloud/Load Balancing:** AWS Network Load Balancer now supports QUIC passthrough, enabling ultra-low latency forwarding with session stickiness using QUIC Connection IDs.

---

### 9. Challenges and Limitations

- QUIC does not support SSL decryption, which is a common method used by enterprise firewalls to inspect and secure network traffic. This creates a significant blind spot in network visibility for IT teams.
- Many middleboxes in Internet infrastructure are tuned for TCP and may rate-limit or even block UDP traffic. Google's solution was to have Chromium start both a QUIC and a TCP connection simultaneously, allowing seamless fallback.
- As a newer protocol, its adoption is still growing and QUIC traffic may even be blocked by some networking components.

---

### 10. Standardization Timeline

| Year | Milestone |
|---|---|
| 2012 | First implementation by Google |
| 2013 | Public announcement; Chrome experiments begin |
| 2017 | IETF begins diverging from gQUIC |
| 2020 | Chrome wide-scale experiments with IETF QUIC |
| May 2021 | IETF officially publishes QUIC as **RFC 9000** |

---

### Summary

QUIC is a modern, secure, and highly efficient transport protocol designed to replace TCP for most internet applications. Its combination of reduced latency (0-RTT/1-RTT), multiplexed independent streams, built-in TLS 1.3 encryption, and connection migration makes it particularly powerful for mobile-first and performance-sensitive applications. As the transport backbone of HTTP/3, QUIC represents the future direction of internet communication at the transport layer.

References:

- [QUIC - Wikipedia](https://en.wikipedia.org/wiki/QUIC)
- [What is QUIC? Everything You Need to Know | Auvik](https://www.auvik.com/franklyit/blog/what-is-quic-protocol/)
- [The Road to QUIC | Cloudflare Blog](https://blog.cloudflare.com/the-road-to-quic/)
- [RFC 9000 - QUIC: A UDP-Based Multiplexed and Secure Transport](https://datatracker.ietf.org/doc/rfc9000/)
- [QUIC Protocol Overview | Chromium](https://www.chromium.org/quic/)
- [QUIC Protocol Features & Use Cases | EMQ](https://www.emqx.com/en/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov)
- [What is QUIC Protocol? | Check Point](https://www.checkpoint.com/cyber-hub/network-security/what-is-quic/)
- [QUIC Support in .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/quic/quic-overview)