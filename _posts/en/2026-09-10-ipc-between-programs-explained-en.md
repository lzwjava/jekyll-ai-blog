---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPC Between Programs Explained
translated: false
type: note
---

**Question:** How can I understand data communication between two running programs?

**Answer:**

When two programs exchange data, they use an **Inter-Process Communication (IPC)** mechanism. Even though each process lives in its own isolated memory space, the OS provides several "channels" through which data can travel. Here's a visual overview of the most common ones:The core idea is that each running program (process) lives in **isolated memory** — it cannot directly read or write another process's variables. To exchange data, they must go through a shared channel managed by the OS. There are three fundamental steps no matter which channel is used:

**① Serialize** — Process A converts its internal data (objects, structs, etc.) into a format that can be transmitted: raw bytes, JSON, Protobuf, etc.

**② Transport** — The OS kernel moves the data through the chosen mechanism (pipe, socket, shared memory, message queue, or file).

**③ Deserialize** — Process B receives the bytes and reconstructs meaning from them.

The five common mechanisms differ mainly in **who manages the buffer** and **how fast** the transfer is:

- **Pipe** — a one-way byte stream the kernel buffers; classic for shell pipelines (`ls | grep`). Simple but unidirectional.
- **Socket** — bidirectional; works across a network (TCP/UDP) or locally (Unix domain socket). What HTTP servers use.
- **Shared Memory** — both processes map the same physical RAM page. Zero-copy means it's the fastest, but requires a mutex/semaphore to avoid race conditions.
- **Message Queue** — processes post and receive structured, discrete messages. The queue buffers them, so sender and receiver don't need to be running at the same moment.
- **File / Signal** — the simplest: write to a file, the other reads it. Signals are tiny asynchronous notifications (just a number, like `SIGTERM`).

The key mental model: **process isolation is the rule, IPC channels are the exceptions**. The OS acts as a trusted middleman ensuring neither process can corrupt the other's memory directly.

---

References:
- [Inter-process communication – Wikipedia](https://en.wikipedia.org/wiki/Inter-process_communication)
- [Linux IPC mechanisms (pipes, sockets, shared memory) – The Linux Documentation Project](https://tldp.org/LDP/lpg/node7.html)
- [Unix Network Programming – Stevens (socket & IPC reference)](https://www.unpbook.com/)
