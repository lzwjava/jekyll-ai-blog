---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: TCP Segment Count for MB vs MiB
translated: false
type: note
---

Ah, now I see exactly what the table means! Thank you for the context.

This table is showing how many **maximum-sized TCP segments** (1460 bytes of application data each) fit into different amounts of data when using standard Ethernet (MTU 1500).

The key point of the table:

| Amount of data | Using decimal MB/GB (1 MB = 1,000,000 bytes) | Using binary MiB/GiB (1 MiB = 1,048,576 bytes) |
|------------------------|---------------------------------------------|------------------------------------------------|
| **1 MB** of application data  | → needs ~685 TCP segments                  |                                                |
| **1 MiB** of application data |                                                | → needs ~719 TCP segments                      |

### Why the difference exists here

- Maximum TCP payload per segment on Ethernet = **1460 bytes**
  (1500 byte MTU − 40 bytes IPv4+TCP headers)

Calculation:

- 1 decimal MB = 1,000,000 bytes
  → 1,000,000 ÷ 1460 ≈ **684.93** → rounded to **~685 segments**

- 1 binary MiB = 1,048,576 bytes
  → 1,048,576 ÷ 1460 ≈ **718.47** → rounded to **~719 segments**

So the table is 100% correct.

### Summary

- **MB** here means the decimal megabyte (1,000,000 bytes) → common in network calculations and bandwidth marketing.
- **MiB** here means the binary mebibyte (1,048,576 bytes) → common in operating systems and RAM.

Because 1 MiB contains 48,576 more bytes than 1 MB, it requires about 33–34 extra TCP segments (48,576 ÷ 1460 ≈ 33.27), which explains the jump from ~685 to ~719.

The table is simply highlighting that tiny but real difference when you’re counting maximum-size packets/segments precisely.
