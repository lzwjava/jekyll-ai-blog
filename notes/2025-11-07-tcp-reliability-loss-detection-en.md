---
audio: false
generated: true
image: false
lang: en
layout: post
model: moonshotai/kimi-k2-thinking
title: TCP Reliability and Loss Detection
translated: false
type: note
---

Let me break down this TCP reliability conversation into clear concepts:

## **1. Detecting Lost Packets**

TCP uses two primary mechanisms to spot missing data:

- **Timeout**: A simple countdown timer starts when a packet is sent. If no acknowledgment (ACK) arrives before the timer expires, the packet is declared lost and retransmitted. This is the "last resort" detection method.

- **Duplicate ACKs (Fast Retransmit)**: This is more sophisticated. When the receiver gets packets *out of order*, it keeps sending ACKs for the *last* successfully received *in-order* packet. For example:
  - If it got packets #1, #2, but #3 is missing, it keeps ACKing #2 even when it later receives #4, #5, etc.
  - **Three duplicate ACKs** for the same sequence number (#2 in our example) signals that packet #3 is likely lost (not just delayed), triggering *immediate* retransmission—much faster than waiting for a timeout.

## **2. High RTT Performance Impact**

You’re absolutely right—high Round-Trip Time makes retransmissions painful:
- If RTT = 200ms (e.g., cross-continent), and a packet is lost, you wait *at least* 200ms to find out via timeout
- During that waiting period, bandwidth sits idle, throughput plummets, and the connection feels "sluggish"
- Fast retransmit helps dramatically here, cutting detection time from seconds to milliseconds

## **3. Adaptive Timeout Intervals**

TCP doesn't use a fixed timeout value—it intelligently tracks network conditions:

- **RTT Estimation**: TCP continuously measures how long acknowledgments take to return
- **Dynamic Timeout**: The retransmission timeout (RTO) is calculated based on measured RTT plus a safety margin (typically RTT + 4×deviation)
- **Self-Tuning**: When RTT increases (network congestion, longer paths), the timeout automatically stretches to avoid *premature* retransmissions
- **Avoiding Unnecessary Retransmits**: Without this, TCP might re-send perfectly fine packets that were just delayed, wasting bandwidth and causing duplicate deliveries

**Bottom line**: TCP's reliability isn't just about retransmitting—it's about *smartly* detecting loss without waiting too long or acting too hastily.
