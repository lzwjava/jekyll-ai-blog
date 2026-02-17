---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed Slot Time Division Multiplexing
translated: false
type: note
---

Question: A multiplexing method where time slots assigned to each signal source are fixed and cannot be transferred between sources is called _______ multiplexing.

Answer:

The correct answer is **Synchronous Time Division Multiplexing (STDM)**, often simply referred to as **Synchronous TDM**.

### Understanding Synchronous TDM

In this multiplexing technique, the total bandwidth of the communication channel is divided into specific **time slots**. Each input source is pre-assigned a dedicated slot in every frame, regardless of whether that source has data to send or not.

#### Key Characteristics:

* **Fixed Assignment:** Every device gets a "turn" at a specific, repeating time.
* **No Transferability:** If a signal source (Source A) is idle and has no data to transmit, its time slot remains **empty**. Source B cannot "borrow" or use Source A's slot.
* **Wasted Bandwidth:** Because slots are reserved even when idle, it can lead to inefficiency if some sources are not constantly active.
* **Simplicity:** No complex addressing is needed because the receiver knows which data belongs to which source based solely on *when* it arrives.

---

### Comparison: Synchronous vs. Asynchronous (Statistical) TDM

To better understand why your question specifies "fixed" and "non-transferable," it helps to compare it to its alternative:

| Feature | Synchronous TDM | Asynchronous (Statistical) TDM |
| --- | --- | --- |
| **Slot Allocation** | Fixed and Pre-determined | Dynamic (On-demand) |
| **Idle Sources** | Slot remains empty (wasted) | Slot is given to an active source |
| **Efficiency** | Lower (due to empty slots) | Higher (uses all available capacity) |
| **Complexity** | Simple (no addressing needed) | Complex (requires addressing headers) |

### Why it is called "Synchronous"

It is called "synchronous" because the sender and receiver must be perfectly synchronized in time. The receiver identifies the data stream by counting the slots; for example, it knows that the 1st slot always belongs to Device 1, the 2nd to Device 2, and so on.

Would you like me to explain the mathematical calculation for the bit rate of a Synchronous TDM link?