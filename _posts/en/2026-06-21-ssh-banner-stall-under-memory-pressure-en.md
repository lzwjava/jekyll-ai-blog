---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Banner Stall Under Memory Pressure
translated: false
type: note
---

**Question:** Why does sshd accept TCP connections but never send its banner when the machine is under severe memory/CPU pressure?

**Answer:**

## The SSH Banner Problem — Root Cause

SSH handshake has two phases:

```
Client               Server
  |                    |
  |--- TCP SYN ------->|   ← port 22 open, kernel accepts (ring buffer)
  |<-- TCP SYN-ACK ----|   ← this works even on a frozen machine
  |--- TCP ACK ------->|
  |                    |
  |<-- SSH-2.0-OpenSSH-|   ← THIS NEVER ARRIVES
        (banner)
```

The TCP handshake (SYN/SYN-ACK/ACK) is handled by the **kernel's network stack** — it lives in kernel space and runs even when userspace is completely frozen. The kernel has a socket accept queue; it will complete TCP connections autonomously.

But sending the SSH banner requires **sshd to actually run** — it's a userspace process. It needs to:

1. Be scheduled by the CPU scheduler
2. `accept()` the connection from the kernel queue
3. Allocate memory for the session
4. Write `SSH-2.0-OpenSSH-x.x\r\n` to the socket

If the machine is swapping or CPU-starved, sshd never gets scheduled, or tries to allocate memory and blocks waiting for swap pages to come in — so the banner never arrives. Your SSH client just... waits.

---

## Why the Tokenize Job Causes This

### Memory path

```
16 workers × 270MB parquet file = 4.3 GB just for raw reads
+ tokenized output lists in each worker
+ main process memory
+ OS page cache
─────────────────────────────────────────────────────
easily 10–15 GB total on a 16GB or 32GB machine
```

When RAM fills up, the kernel starts swapping. Swap on a spinning disk does ~100 MB/s. The machine needs to swap gigabytes — it becomes essentially frozen. Every process, including sshd, is waiting on I/O to page in its code/stack before it can run.

### CPU path

`mp.Pool` with 16 workers on a machine with (say) 8 cores means the scheduler is juggling 16 CPU-bound Python processes + the main process. sshd is low-priority, gets starved.

### The silent hang in `pool.imap`

```python
for result in pool.imap(worker_fn, files):
    ...  # main process blocks here forever
```

If a worker gets OOM-killed by the kernel (`SIGKILL` from the OOM killer), `pool.imap` doesn't raise an exception — it just never yields that result. The main process sits in the `for` loop waiting. No timeout, no error. This is a well-known Python `multiprocessing` footgun.

---

## Why ping works but SSH doesn't

| Operation | Who handles it | Survives memory starvation? |
|---|---|---|
| `ping` reply (ICMP echo) | kernel network stack | ✅ yes |
| TCP SYN-ACK (port 22) | kernel TCP stack | ✅ yes |
| SSH banner | sshd userspace process | ❌ no |
| Any SSH command | bash + userspace | ❌ no |

The kernel stays partially alive even in extreme conditions — it handles interrupts, network packets, and the OOM killer itself. Userspace dies first.

---

## The Fix (streaming approach)

Instead of loading whole parquet files:

```python
import pyarrow.parquet as pq

def worker_streaming(path):
    pf = pq.ParquetFile(path)
    tokens = []
    for batch in pf.iter_batches(batch_size=1000, columns=["content"]):
        for text in batch.column("content").to_pylist():
            tokens.extend(tokenizer.encode(text))
    return tokens
```

This keeps each worker's memory footprint to ~batch_size rows instead of the entire file. Also drop workers to 2–4 so you don't multiply the pressure.
