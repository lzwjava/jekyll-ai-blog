---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: PAT Maps Multiple IPs to One
translated: false
type: note
---

Question: Which type of NAT maps multiple private IPs to a single public IP?
A) Static NAT
B) Dynamic NAT
C) PAT (Overload)
D) One-to-One NAT

Answer:

The correct answer is **C) PAT (Overload)**.

### Explanation

Network Address Translation (NAT) allows private IP addresses to communicate with external networks using public IP addresses. The different types are:

- **Static NAT**: Provides a one-to-one mapping where a single private IP is always translated to the same single public IP. It does not allow multiple private IPs to share one public IP.

- **Dynamic NAT**: Uses a pool of public IPs to map private IPs dynamically (also one-to-one, but the public IP can change). Multiple private IPs require multiple public IPs from the pool; it does not overload a single public IP.

- **PAT (Port Address Translation), also known as NAT Overload**: Maps **multiple private IPs to a single public IP** by using different port numbers to distinguish sessions. This is the most common form of NAT in home routers and enterprises to conserve public IPv4 addresses.

- **One-to-One NAT**: Refers to static or dynamic NAT with fixed or variable one-to-one mappings (equivalent to A or B); it does not share a single public IP among multiple private IPs.

PAT is specifically designed for many-to-one translation, making **C** the correct choice.
