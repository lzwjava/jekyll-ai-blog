---
audio: false
generated: true
image: false
lang: en
layout: post
title: Batch Processing OS Definition
translated: false
type: note
---

Question: What does "批处理操作系统" mean?

Answer: **批处理操作系统** means **Batch Processing Operating System**.

It refers to an early type of operating system design where jobs (programs/tasks) are collected into a group ("batch") and executed sequentially without user interaction during processing.

Key characteristics:

- Jobs are submitted in advance and queued up
- The OS automatically runs them one after another (or in parallel in more advanced versions)
- No real-time user interaction while jobs run
- Common in early mainframe computing (1950s–60s)

Two main subtypes:

- **单道批处理** (Single-stream batch): one job runs at a time; CPU sits idle during I/O
- **多道批处理** (Multiprogramming batch): multiple jobs loaded in memory; CPU switches to another job while one waits for I/O — much more efficient

A classic example is IBM's early OS/360. Modern equivalents include HPC job schedulers like SLURM or PBS, and cloud batch services like AWS Batch.

References:

- [Batch Processing - Wikipedia](https://en.wikipedia.org/wiki/Batch_processing)
- [History of Operating Systems - Wikipedia](https://en.wikipedia.org/wiki/History_of_operating_systems)
