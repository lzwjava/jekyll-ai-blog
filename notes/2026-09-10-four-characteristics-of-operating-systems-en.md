---
audio: false
generated: true
image: false
lang: en
layout: post
title: Four Characteristics of Operating Systems
translated: false
type: note
---

Question: **What are the four classic characteristics of an operating system, such as virtualization and concurrency?**

Answer:

A useful way to remember the **four fundamental characteristics of an OS** is:

1. **Virtualization** — gives each program the illusion that it has its own CPU, memory, and devices.

   * CPU → processes/threads appear to run independently.
   * Memory → virtual address space.
   * Storage → files/directories abstract disks.
   * Example: process `P1` thinks it owns address `0x400000`, even though many processes share physical RAM.

2. **Concurrency** — multiple programs can make progress "at the same time."

   * On one CPU: rapid context switching.
   * On multiple CPUs: actual parallel execution.
   * OS must handle synchronization, races, deadlocks, etc.

3. **Persistence** — data can survive program termination and power cycles.

   * RAM is temporary.
   * OS provides filesystems/storage abstractions over disks/SSDs.
   * Example:

     ```bash
     echo hello > a.txt
     ```

     `a.txt` persists after the process exits.

4. **Protection / Isolation** — one program/user should not arbitrarily interfere with another.

   * User/kernel mode
   * Process address-space isolation
   * File permissions
   * System-call boundary
   * Hardware protection mechanisms

A compact mental model is:

```text
                 Operating System
                       │
       ┌───────────────┼────────────────┐
       │               │                │
 Virtualization    Concurrency     Persistence
       │               │                │
  CPU / Memory      Processes       Files / Disk
  Devices           Threads         Filesystem
       │               │
       └────────── Protection ──────────┘
                   Isolation
```

If you're thinking of the **classic OS textbook formulation**, especially *OSTEP (Operating Systems: Three Easy Pieces)*, the core three are actually **virtualization, concurrency, and persistence**. **Protection** is another fundamental OS concern, but it is not usually counted as one of OSTEP's "three easy pieces."

The key insight is: **an OS is fundamentally an abstraction + resource-management layer**. It turns messy physical hardware into useful abstractions such as processes, virtual memory, files, and permissions.

I can also map these four directly to **Linux system calls and kernel mechanisms** (`fork`, `exec`, `mmap`, `open`, `read`, scheduler, etc.) if you want to connect the theory to actual code.
