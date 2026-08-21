---
audio: false
generated: true
image: false
lang: en
layout: post
title: Synchronous Time Division Multiplexing
translated: false
type: note
---

Question: What is the multiplexing method called when each signal source is assigned a fixed time slot that cannot be transferred between sources?

Answer: This multiplexing method is called **Synchronous Time Division Multiplexing (同步时分多路复用, STDM)**.

In synchronous TDM, the total transmission time is divided into fixed-length **frames**, and each frame is subdivided into a fixed number of **time slots (时隙)**. Each signal source (channel) is permanently assigned one specific slot in every frame — regardless of whether that source actually has data to send. The slot assignment is rigid and non-transferable.

Key characteristics:

- **Fixed slot assignment** — each source always owns the same slot position in every frame
- **Waste possible** — if a source has no data, its slot goes empty (wasted bandwidth)
- **Simple synchronization** — no addressing overhead needed; position alone identifies the source
- **Contrast with Statistical TDM (统计时分多路复用)** — where slots are dynamically allocated only to sources that have data, eliminating waste but requiring address headers

A classic real-world example is **T1/E1 telephone circuits**, where each voice channel gets a fixed 8-bit slot in every 125 µs frame.

References:

- [Time-division multiplexing – Wikipedia](https://en.wikipedia.org/wiki/Time-division_multiplexing)
- [Synchronous vs Statistical TDM – GeeksforGeeks](https://www.geeksforgeeks.org/difference-between-synchronous-tdm-and-asynchronous-tdm/)
