---
audio: false
generated: true
image: false
lang: en
layout: post
title: Networking Ports Explained
translated: false
type: note
---

Question: What does "port" mean in networking?

Answer:

A **port** is a logical endpoint used to identify a specific process or service on a networked device. Think of it as an extension number on a phone system — the IP address gets you to the right building (the device), and the port number routes you to the right room (the application).

**Key points:**

- Ports are represented as numbers ranging from **0 to 65535**
- They work alongside IP addresses in the format `IP:PORT` (e.g., `192.168.1.1:80`)
- Both **TCP** and **UDP** protocols use ports
- The operating system uses the port number to hand incoming data to the correct application

**Port categories:**

| Range | Name | Description |
|---|---|---|
| 0 – 1023 | Well-known ports | Reserved for standard services (HTTP, FTP, SSH…) |
| 1024 – 49151 | Registered ports | Used by applications (databases, game servers…) |
| 49152 – 65535 | Dynamic/ephemeral | Temporarily assigned by the OS for outgoing connections |

**Common examples:**

| Port | Protocol | Service |
|---|---|---|
| 22 | TCP | SSH (remote login) |
| 80 | TCP | HTTP (web) |
| 443 | TCP | HTTPS (secure web) |
| 53 | UDP/TCP | DNS |
| 3306 | TCP | MySQL |

**How it works in practice:**

When you visit `https://example.com`, your browser connects to that server on **port 443**. Your OS also assigns your browser a random ephemeral port (e.g., 52341) on your side, so the server knows where to send the response back. The full connection is identified by the 4-tuple: `(your IP, your port, server IP, server port)`.

References:
- [What is a Port? - Cloudflare](https://www.cloudflare.com/learning/network-layer/what-is-a-computer-port/)
- [Port (computer networking) - Wikipedia](https://en.wikipedia.org/wiki/Port_(computer_networking))
