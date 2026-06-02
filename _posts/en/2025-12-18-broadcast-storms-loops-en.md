---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Broadcast Storms from Network Loops
translated: false
type: note
---

Question: 1. In a switched network, what causes a broadcast storm?
A) Too many unicast frames
B) Network loops without STP
C) Misconfigured VLANs
D) High bandwidth usage

2. [The user indicates the answer is B]

Answer:

### Question 1 Explanation

In a switched Ethernet network, a **broadcast storm** occurs when broadcast or multicast frames flood the network uncontrollably, consuming excessive bandwidth and potentially bringing the network down.

The primary cause is **network loops without Spanning Tree Protocol (STP)** (or a similar loop-prevention mechanism).

- When a physical loop exists in the topology (e.g., two switches connected by multiple links without proper configuration), a broadcast frame sent by a device enters the loop.
- Each switch forwards the frame out all ports (except the incoming one), so the frame circulates indefinitely.
- Each circulation generates additional copies of the broadcast frame, leading to exponential growth in traffic — this is the broadcast storm.

**Why the other options are incorrect:**

- **A) Too many unicast frames**: Unicast frames are sent to a specific MAC address and do not flood all ports unless the destination is unknown. Excessive unicasts may cause congestion but not a self-perpetuating storm like broadcasts in a loop.
- **C) Misconfigured VLANs**: VLAN misconfigurations can lead to traffic leaks, security issues, or suboptimal paths, but they do not inherently create the infinite frame multiplication seen in broadcast storms.
- **D) High bandwidth usage**: This is a symptom or result of a broadcast storm, not the cause.

STP prevents this by detecting loops and logically blocking redundant paths, stopping infinite frame circulation.

### Question 2 Feedback

Your selected answer **B) Network loops without STP** is **correct**.

This is a classic networking concept tested in certifications like CCNA.
