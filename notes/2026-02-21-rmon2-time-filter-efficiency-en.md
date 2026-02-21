---
audio: false
generated: true
image: false
lang: en
layout: post
title: RMON2 Time Filter for Efficiency
translated: false
type: note
---

This question is about RMON2 (Remote Monitoring version 2) MIB design and how to improve network management efficiency.

The correct answer is **A - Time filter index**.

**Explanation:**

Network management applications need to periodically poll monitors to obtain the latest status information of managed objects. To improve efficiency, we want the monitor to only return values that have changed since the last query. Neither SNMPv1 nor SNMPv2 directly addressed this issue.

However, RMON2 designers developed an innovative method to implement this functionality within the MIB definition - using a **time filter for indexing**.

**How it works:**
- The time filter index allows managers to retrieve only those entries that have changed since a specified time
- It's essentially a timestamp-based filtering mechanism
- When a manager queries with a time filter index value, the agent responds with only the objects that have changed after that timestamp

This approach significantly reduces network traffic and processing overhead by eliminating redundant data transmission, making network monitoring more efficient.