---
audio: false
generated: true
image: false
lang: en
layout: post
title: Presentation, Data Link, and Network Layers
translated: false
type: note
---

**Question:** What is an introduction to the OSI model, with a focus on the Presentation Layer, Data Link Layer, and Network Layer?

**Answer:**

The **OSI (Open Systems Interconnection) model** is a conceptual framework that standardizes how different computer systems communicate over a network. It divides communication into **7 ordered layers**, each with a distinct role — from the physical transmission of bits up to user-facing applications.

Here's an overview diagram followed by a deep dive into those three layers:Now let's break down each of your three target layers in detail.

---

### Layer 6 — Presentation Layer

Think of this as the **translator and formatter** of the OSI model. It sits just below the Application layer and is responsible for ensuring that the data from one system can be understood by another, regardless of internal differences in encoding.

Its three key jobs:

**Translation** — converts data between formats (e.g., EBCDIC ↔ ASCII, or different character encodings). If two machines use different internal representations, the Presentation layer resolves it.

**Encryption/Decryption** — handles securing data for transit (e.g., SSL/TLS operates here). Before data leaves, it can be encrypted; upon arrival, it's decrypted.

**Compression** — reduces data size for efficiency. Formats like JPEG, MP3, and ZIP compression operate at this layer.

> In practice, many modern protocols (like HTTP/2 or TLS) blur the lines — but conceptually, encoding, encryption, and compression all belong to Layer 6.

---

### Layer 3 — Network Layer

This is the **routing layer** — responsible for moving packets from a source host to a destination host, potentially across many intermediate networks.

Its core job: **logical addressing and path selection**.

- Uses **IP addresses** (IPv4/IPv6) to identify source and destination across different networks.
- **Routers** are the primary devices here. They examine packet headers and make forwarding decisions at this layer.
- Key protocols: **IP, ICMP** (ping), **OSPF, BGP** (routing protocols).

A key distinction: Layer 3 handles *end-to-end* delivery between networks. It doesn't care about the physical path — only the logical destination.
