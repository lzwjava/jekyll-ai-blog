---
audio: false
generated: true
image: false
lang: en
layout: post
title: UDP Header First Word Length
translated: false
type: note
---

Question: Analyze the UDP header structure, and what is the length of the first word (首字长度)?

Answer:

## UDP Header Structure

The UDP (User Datagram Protocol) header is **fixed at 8 bytes (64 bits)** total, with four 16-bit fields:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |  ← 首字 (First Word)
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|            Length             |           Checksum            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Data (variable)                          ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

| Field | Size | Description |
| --- | --- | --- |
| **Source Port** | 16 bits (2 bytes) | Sender's port |
| **Destination Port** | 16 bits (2 bytes) | Receiver's port |
| **Length** | 16 bits (2 bytes) | Total UDP segment length (header + data); minimum = 8 |
| **Checksum** | 16 bits (2 bytes) | Error detection (optional in IPv4, mandatory in IPv6) |

---

## 首字长度 (First Word Length)

> In Chinese networking terminology, **"字" (word) = 16 bits = 2 bytes** in the UDP context.

- **首字 (First Word)** = the first 16-bit unit = **Source Port** field
- **首字长度 = 16 bits (2 bytes)**

The entire first 32-bit row (Source Port + Destination Port) = **4 bytes = 1 "double word"**

The full **UDP header (首部) length = 8 bytes (fixed)** — unlike IP/TCP, UDP has **no variable-length options** and no separate "header length" field.

---

## Key Differences from TCP

| Feature | UDP | TCP |
| --- | --- | --- |
| Header size | Fixed 8 bytes | Variable 20–60 bytes |
| Header length field | ❌ None | ✅ Yes (4 bits, in 32-bit words) |
| Connection | Connectionless | Connection-oriented |
| Reliability | ❌ No | ✅ Yes |

References:

- [RFC 768 – User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768)
- [UDP – Wikipedia](https://en.wikipedia.org/wiki/User_Datagram_Protocol)
- [TCP/IP Guide – UDP](http://www.tcpipguide.com/free/t_UDPMessageFormat.htm)
