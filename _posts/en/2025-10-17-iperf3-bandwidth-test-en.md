---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: iPerf3 Network Bandwidth Testing Tool
translated: false
type: note
---

### What is iPerf3?

iPerf3 is an open-source command-line tool designed for measuring network bandwidth and performance. It's commonly used to test the maximum achievable throughput on IP networks by simulating traffic between two endpoints (one acting as a server and the other as a client). This helps diagnose issues like latency, packet loss, and bottlenecks in local or wide-area networks.

#### Key Features:
- **Protocols Supported**: TCP, UDP, and SCTP for flexible testing scenarios.
- **Customization**: Allows tuning parameters like buffer sizes, test duration, and bidirectional traffic.
- **Output**: Provides detailed statistics on bandwidth, jitter, and datagram loss.

#### Basic Usage Example:
To test bandwidth between two machines:
1. On the server: `iperf3 -s` (starts the server).
2. On the client: `iperf3 -c <server_IP>` (connects and runs a 10-second test by default).

It's lightweight, cross-platform (works on Linux, Windows, macOS), and widely used by network admins, developers, and IT pros for troubleshooting.

#### History:
iPerf3 is a complete rewrite of the original iPerf tool, started in 2009 by ESnet (Energy Sciences Network) and first released in 2014. The redesign aimed for a smaller, more maintainable codebase while improving accuracy.

For more details, check the official site or GitHub repo.

### References
- [iPerf - The TCP, UDP and SCTP network bandwidth measurement tool](https://iperf.fr/)
- [iperf3: A TCP, UDP, and SCTP network bandwidth measurement tool](https://github.com/esnet/iperf)
- [Iperf - Wikipedia](https://en.wikipedia.org/wiki/Iperf)
